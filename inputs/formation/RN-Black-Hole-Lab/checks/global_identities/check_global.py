"""Finite identities only; does not certify existence or global causality."""
import json
import pathlib
import sympy as s

checks = []

def zero(name, expression):
    residual = s.simplify(expression)
    assert residual == 0, (name, residual)
    checks.append({"name": name, "status": "PASS"})

r = s.symbols("r", positive=True)
F = (1 - 1/r)**2
rstar = r + 2*s.log(r-1) - 1/(r-1)
zero("tortoise derivative", s.diff(rstar, r) - 1/F)
zero("static tail induced radial metric", -F/F**2 + 2/F - 1/F)

# EF pullback using dv=k dt and dr=r_U dU + k F dt/2.
k, nu, ru = s.symbols("k nu ru", nonzero=True)
zero("EF dt squared cancellation", -F*k**2 + 2*k*(k*F/2))
zero("EF cross coefficient", (2*k*ru + ru/nu).subs(k, -1/(2*nu)))
zero("horizon surface gravity", s.diff(F, r).subs(r, 1)/2)

# Norm of d(U-sigma(t)); Omega squared is exp(ell).
omega, slope = s.symbols("omega slope", positive=True)
g_inv = s.Matrix([[0, -2/omega], [-2/omega, 0]])
dG = s.Matrix([1, slope])  # sigma'=-slope
zero("barrier covector timelike", (dG.T*g_inv*dG)[0] + 4*slope/omega)

def christoffel(metric, coords, a, b, c):
    inv = metric.inv()
    return s.simplify(sum(inv[a,d]*(s.diff(metric[d,c], coords[b])
                           + s.diff(metric[d,b], coords[c])
                           - s.diff(metric[b,c], coords[d]))/2
                          for d in range(len(coords))))

u, x = s.symbols("u x", real=True)
physical = s.Matrix([[-F, -1], [-1, 0]])
for a in range(2):
    zero(f"outgoing radial affine component {a}", christoffel(physical, [u,r], a,1,1))
conformal = s.Matrix([[-x*x*(1-x)**2, 1], [1, 0]])
zero("conformal boundary null", conformal.inv()[1,1].subs(x,0))
for a in range(2):
    zero(f"conformal infinity affine component {a}", christoffel(conformal, [u,x], a,0,0).subs(x,0))

q = s.symbols("q")
a = 1 - 2*q/3
zero("necessity square cross coefficient", 1/(2*a)-s.Rational(1,2)-q + 2*q*(1-q)/(3-2*q))
B, mu, h, D = s.symbols("B mu h D")
S = 1-B
P = 1-mu*B+mu*D
C = 1-h-P**2/S
zero("quantitative threshold defect identity", (2*mu-1)*B
     -(mu**2*B**2+S*(h+C)+2*mu*(1-mu*B)*D+mu**2*D**2))

report = {"scope": "finite algebra only; G-A and G-B remain unresolved",
          "sympy": s.__version__, "checks": checks}
path = pathlib.Path(__file__).with_name("RESULTS_GLOBAL.json")
path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
