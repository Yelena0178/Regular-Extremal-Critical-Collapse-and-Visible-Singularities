from exact_core import *
assert sum((F(j*j)*a[j-1] for j in range(1,N+1)),F(0))==0
assert sum((F(j)*b[j-1] for j in range(1,N+1)),F(0))==0
assert sum((F(j**3)*b[j-1] for j in range(1,N+1)),F(0))==0
for s in (1,2,3):
 assert sum((-a[j-1]*(j*w)**2/(s*(s*s+(j*w)**2)) for j in range(1,N+1)),F(0))==0
 assert sum((b[j-1]*j*w/(s*s+(j*w)**2) for j in range(1,N+1)),F(0))==0
real=[9,20,36,50];imag=[7,16,29,41,50]
A=[[F(j*j) for j in real]]+[[-(j*w)**2/(s*(s*s+(j*w)**2)) for j in real] for s in (1,2,3)]
B=[[F(j) for j in imag],[F(j**3) for j in imag]]+[[j*w/(s*s+(j*w)**2) for j in imag] for s in (1,2,3)]
Ai=inverse(A);Bi=inverse(B)
for m,mi in [(A,Ai),(B,Bi)]:
 assert all(sum(m[i][k]*mi[k][j] for k in range(len(m)))==int(i==j) for i in range(len(m)) for j in range(len(m)))
# Ordering c = Re M1, Im M1, Re M2, Im M2, Re M3, Im M3
out={'real_modes':real,'imag_modes':imag,'real_corrections':[[str(Ai[j][s]) for j in range(4)] for s in (1,2,3)],'imag_corrections':[[str(Bi[j][s]) for j in range(5)] for s in (2,3,4)]}
(ROOT/'data/right_inverse.json').write_text(json.dumps(out,indent=2))
assert F('0.56129762150689')<lam<F('0.56129762150691')
K0=4*E[0]-D+sum(T)
assert F('0.00000010951713352')<K0<F('0.00000010951713353')
# Real determinant = |d1*d2*d3|^2, exact positive expression.
det=(lam**2/F(16))*(lam**2*(9*lam**2+4)/256)*(lam**2*(9*lam**2+4)*(25*lam**2+36)/16384)
assert det>0
print('PASS: rational tangential constraints; six zero moments; exact right inverse; coupling enclosure; positive real Jacobian determinant.')
print('lambda=',float(lam),'K0=',float(K0),'det_real=',float(det))
