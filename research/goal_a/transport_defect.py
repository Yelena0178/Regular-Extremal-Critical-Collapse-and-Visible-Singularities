"""Floating-point Bernstein residual and tube-cost forecast, strictly E0.

Polynomial cancellation is retained before taking coefficient bounds. None of
these NumPy operations rounds outwards; the outputs are not interval bounds.
"""

from fractions import Fraction
from math import comb
import numpy as np
from neutral_transport import hermite_coefficients


def add(a, b):
    n, m = max(a.shape[-2], b.shape[-2]), max(a.shape[-1], b.shape[-1])
    out = np.zeros(np.broadcast_shapes(a.shape[:-2], b.shape[:-2])+(n,m))
    out[..., :a.shape[-2], :a.shape[-1]] += a
    out[..., :b.shape[-2], :b.shape[-1]] += b
    return out


def multiply(a, b):
    out = np.zeros(np.broadcast_shapes(a.shape[:-2], b.shape[:-2])
                   +(a.shape[-2]+b.shape[-2]-1, a.shape[-1]+b.shape[-1]-1))
    for i in range(b.shape[-2]):
        for j in range(b.shape[-1]):
            out[..., i:i+a.shape[-2], j:j+a.shape[-1]] += a*b[..., i,j,None,None]
    return out


def derivative(a, axis, spacing):
    if axis == 0:
        return a[..., 1:,:]*np.arange(1,a.shape[-2])[:,None]/spacing
    return a[..., :,1:]*np.arange(1,a.shape[-1])/spacing


def bernstein_range(a):
    n, m = a.shape[-2]-1, a.shape[-1]-1
    T = np.array([[comb(i,j)/comb(n,j) if j <= i else 0 for j in range(n+1)]
                  for i in range(n+1)])
    U = np.array([[comb(i,j)/comb(m,j) if j <= i else 0 for j in range(m+1)]
                  for i in range(m+1)])
    b = np.einsum("ab,...bc,dc->...ad", T, a, U)
    return np.min(b, axis=(-2,-1)), np.max(b, axis=(-2,-1))


def residual_forecast(data, block_rows=8):
    coeff = hermite_coefficients(data)
    du, dv = data["u"][1], data["v"][1]-data["v"][0]
    low, high = bernstein_range(coeff)
    delta = np.empty(coeff.shape[:3])
    for first in range(0, len(coeff), block_rows):
        sl = slice(first, first+block_rows)
        c = coeff[sl]
        r,k,t,n,z,m = [c[...,j,:,:] for j in range(6)]
        ru,ku,tu = [derivative(x,0,du) for x in (r,k,t)]
        nv,zv,mv = [derivative(x,1,dv) for x in (n,z,m)]
        r2 = multiply(r,r)
        kn = multiply(k,n)
        knz = multiply(kn,z)
        numerators = [add(ru,-n),
                      add(multiply(r,ku),-multiply(knz,z)),
                      add(multiply(r2,tu),multiply(knz,add(r,-2*m))),
                      add(multiply(r2,nv),-2*multiply(kn,m)),
                      add(add(multiply(r2,zv),multiply(t,r)),2*multiply(multiply(k,m),z)),
                      add(2*multiply(k,mv),-multiply(t,t))]
        rmin, kmin = low[sl,...,0], low[sl,...,1]
        if np.min(rmin) <= 0 or np.min(kmin) <= 0:
            raise ArithmeticError("interpolant denominator forecast not positive")
        denominators = (1., rmin, rmin*rmin, rmin*rmin, rmin*rmin, 2*kmin)
        for j, (p, denominator) in enumerate(zip(numerators, denominators)):
            lo, hi = bernstein_range(p)
            delta[sl,...,j] = np.maximum(abs(lo),abs(hi))/denominator
    return low, high, delta


def absolute_jacobian_forecast(low, high):
    """Termwise analytic formula, evaluated in ordinary floats, not certified."""
    r, kmin = low[0], low[1]
    _, k,t,n,z,m = np.maximum(abs(low),abs(high))
    L = np.zeros((6,6))
    L[0,3] = 1
    L[1] = (k*n*z*z/r**2,n*z*z/r,0,k*z*z/r,2*k*n*z/r,0)
    L[2] = (k*n*z/r**2+4*k*m*n*z/r**3,n*z/r+2*m*n*z/r**2,
            0,k*z/r+2*k*m*z/r**2,k*n/r+2*k*m*n/r**2,2*k*n*z/r**2)
    L[3] = (4*k*m*n/r**3,2*m*n/r**2,0,2*k*m/r**2,0,2*k*n/r**2)
    L[4] = (t/r**2+4*k*m*z/r**3,2*m*z/r**2,1/r,0,2*k*m/r**2,2*k*z/r**2)
    L[5] = (0,t*t/(2*kmin*kmin),t/kmin,0,0,0)
    return L


def tube_forecast(data, low, high, delta, boundary_error=1e-10, enlargement=1.08,
                  absolute_slack=1e-10):
    """Heuristic cell majorants, with *assumed* boundary error; E0 only.

    Stop on loss of a positive tube or failure of the local super-solution.
    Passing would still require exact boundary, residual and Jacobian checks.
    """
    nu,nv = delta.shape[:2]
    du, dv = data["u"][1], data["v"][1]-data["v"][0]
    lengths = np.array((du,)*3+(dv,)*3)
    radii = np.broadcast_to(np.asarray(boundary_error),(nu+1,nv+1,6)).copy()
    boundary_record = np.asarray(boundary_error).tolist()
    minimum_margin = float("inf")
    for i in range(nu):
        for j in range(nv):
            edge = np.concatenate((radii[i,j+1,:3],radii[i+1,j,3:]))
            M = edge+lengths*delta[i,j]+absolute_slack
            accepted = False
            for iteration in range(24):
                lo, hi = low[i,j]-M,high[i,j]+M
                if lo[0] <= 0 or lo[1] <= 0 or hi[3] >= 0:
                    break
                L = absolute_jacobian_forecast(lo,hi)
                matrix = np.eye(6)-lengths[:,None]*L
                try:
                    proposal = np.linalg.solve(matrix,edge+lengths*delta[i,j])
                except np.linalg.LinAlgError:
                    break
                if np.min(proposal) < 0:
                    break
                margin = M-edge-lengths*(delta[i,j]+L@M)
                if np.min(margin) > 0:
                    minimum_margin = min(minimum_margin,float(np.min(margin)))
                    accepted = True
                    break
                # Pad only the *new cell increment*. Multiplying the incoming
                # edge error by enlargement would create a spurious factor
                # enlargement**N under mesh refinement.
                M = np.maximum(M,edge+enlargement*np.maximum(proposal-edge,0)+absolute_slack)
            if not accepted:
                return {"completed": False,"first_failed_cell": [i,j],
                        "failed_u":float(data['u'][i+1]),"failed_v":float(data['v'][j+1]),
                        "failed_radii":M.tolist(),"assumed_boundary_error":boundary_record,
                        "rigorous_PDE_error":False}
            radii[i+1,j+1] = M
    return {"completed":True,"endpoint_radii":radii[-1,-1].tolist(),
            "maximum_radii":np.max(radii,axis=(0,1)).tolist(),
            "minimum_float_tube_margin":minimum_margin,
            "assumed_boundary_error":boundary_record,"absolute_slack":absolute_slack,
            "rigorous_PDE_error":False}


def exact_cell_margins(radius, edge, lengths, residual, lipschitz):
    """Finite rational inequality kernel; does NOT verify supplied bounds.

    A complete PDE certificate must separately establish polynomial residual,
    Jacobian, boundary, matching-edge, positivity and approximation bounds.
    """
    M,e,h,d = [[Fraction(v) for v in seq] for seq in (radius,edge,lengths,residual)]
    L = [[Fraction(v) for v in row] for row in lipschitz]
    if (not all(len(s)==6 for s in (M,e,h,d,L)) or any(len(row)!=6 for row in L)
            or min(M) <= 0 or min(h) <= 0 or min(e+d) < 0
            or min(v for row in L for v in row) < 0):
        raise ValueError("invalid cell majorant data")
    margin = [M[i]-e[i]-h[i]*(d[i]+sum(L[i][j]*M[j] for j in range(6)))
              for i in range(6)]
    if min(margin) <= 0:
        raise ArithmeticError("strict cell tube inequality failed")
    return margin
