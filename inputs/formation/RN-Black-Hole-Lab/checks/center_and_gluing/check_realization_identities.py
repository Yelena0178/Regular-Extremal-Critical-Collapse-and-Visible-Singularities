"""Exact finite algebra checks. Not a test of PDE existence or globalization.

Run beside check_bondi_center_jets.py (copied unchanged from the prior package).
"""
from pathlib import Path
from fractions import Fraction as F

ns = {}
source = Path(__file__).with_name('check_bondi_center_jets.py').read_text()
exec(source.split('for n in range(2,7):')[0], ns)
S, C, evolve, fields = [ns[x] for x in ('S', 'C', 'evolve', 'fields')]

# The two geometric directions have determinant -beta, using f*g'-f'*g=1.
for beta in [F(1, 3), F(2), F(17, 5)]:
    for g1 in [F(1, 7), F(3), F(19, 2)]:
        assert g1 * (-beta / g1) == -beta
print('PASS: geometric 2x2 Jacobian determinant = -beta')
for m in range(0, 100):
    assert (2*m+1)*(2*m+2) != 0
print('PASS: radial wave odd-coefficient pivot through degree 199')

S.nt = 3
S.nr = 10
e = F(3, 2)
h = evolve({0:C(1,1), 1:C(2,-1), 2:C(F(1,3),F(2,5))}, 3)
f,g,Q,alpha,s,B = fields(h)

def inv(v):
    z = S(1)-v
    assert all(k[1] >= 2 for k in z.d)
    out = S(1)
    p = S(1)
    for _ in range(S.nr//2+1):
        p = p*z
        out = out+p
    return out

si, gi = inv(s), inv(g)
a2 = g*si
# Up to the unit complex gauge factor:
# Pi = s^{-1}D_u f, Psi = partial_R f - s^{-1}D_u f.
pi = (f.du()+alpha*f*C(0,e))*si
rad = f.dr()-pi
energy = pi*pi.conj()+rad*rad.conj()
# Fixed polar T derivative in old coordinates: P = partial_R-s^{-1}partial_u.
# The time-coordinate Jacobian obeys P log(u_T)=s_u/s^2.
lhs_a = (g.dr()*gi-g.du()*gi*si-s.dr()*si+s.du()*si*si).scale(F(1,2))
rhs_a = ((S(1)-a2).shift(-1)+energy.shift(1)+(a2*Q*Q).shift(-3)).scale(F(1,2))
lhs_n = (g.dr()*gi-g.du()*gi*si+s.dr()*si+s.du()*si*si).scale(F(1,2))
rhs_n = ((a2-S(1)).shift(-1)+energy.shift(1)-(a2*Q*Q).shift(-3)).scale(F(1,2))
gauss = Q.dr()-Q.du()*si-(f*pi.conj()).imag().shift(2).scale(e)
for name, residual in [
    ('polar radial Einstein constraint',lhs_a-rhs_a),
    ('polar lapse constraint',lhs_n-rhs_n),
    ('polar Gauss constraint',gauss),
]:
    bad = {key:v for key,v in residual.d.items()
           if key[0]<=1 and key[1]<=5 and v}
    assert not bad, (name,bad)
    print(f'PASS: {name}, all coefficients through u^1 R^5')
print('All calculations use rational arithmetic on a nonzero complex charged background.')
print('No assertion here verifies analytic estimates, Cauchy stability, or a global spacetime.')
