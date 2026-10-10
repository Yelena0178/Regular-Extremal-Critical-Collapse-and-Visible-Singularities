from current_check import *
ri=json.loads((ROOT/'data/right_inverse.json').read_text());hz=F(0);hv=F(0);hx=F(0);hb=F(0)
for typ,modes,rows in [('real',ri['real_modes'],ri['real_corrections']),('imag',ri['imag_modes'],ri['imag_corrections'])]:
 for row in rows:
  co=list(map(F,row));zz={0:F(0)};xp=[F(0)];bp=[F(0)]
  for j,vv in zip(modes,co):
   if typ=='real':zz[0]-=vv;zz[j]=vv/2;zz[-j]=vv/2;xp=add(xp,scale(add(cheb[j],[F(-1)]),vv))
   else:zz[j]=vv/2;zz[-j]=-vv/2;bp=add(bp,scale(U[j-1],vv))
  hz+=sum(map(abs,zz.values()));hv+=sum(abs(j*w*v) for j,v in zz.items());hx+=sum(map(abs,xp));hb+=sum(map(abs,bp))
rho=F(1,10**200);Z=sum(map(abs,z.values()));V=sum(map(abs,v.values()));dz=rho*hz;dv=rho*hv
ed=2*V*dv+dv*dv;cd=Z*dv+V*dz+dz*dv
assert cd<C[0]/2 and ed<E[0]/2
ld=2*ed/(C[0]/2)+2*E[0]*cd/(C[0]*(C[0]/2))
assert ld<F(1,1000)
kd=45*ed+(2/w+2)*((abs(lam)+ld)*cd+ld*sum(map(abs,C))+ed)
assert kd<F(1,200000000)
curd=(4*N-1)*(rho*hx*sum(map(abs,B))+rho*hb*sum(map(abs,X))+rho*rho*hx*hb)*comb(2*N+4,4)
assert curd<F(1,200)
# Tail slope and tail value remain positive; compact loses at most 5e-9.
assert 44*E[0]-abs(D)-sum(map(abs,S))-sum(map(abs,T))-kd>F(1,10)
out={'rho_linf':str(rho),'kappa_star':'1/200000000','current_factor_margin':'1/200','bounds':{k:str(x) for k,x in [('delta_energy_l1',ed),('delta_current_l1',cd),('delta_lambda',ld),('delta_K_compact_and_tail_intercept',kd),('delta_current_factor_l1',curd)]}}
(ROOT/'data/correction_stability_certificate.json').write_text(json.dumps(out,indent=2))
print('PASS uniform correction ball ||c||inf<=1e-200: K>=5e-9, current factor>=1/200, positive energy/current means.')
