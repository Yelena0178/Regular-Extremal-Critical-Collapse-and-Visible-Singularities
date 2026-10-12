from exact_core import *
cheb=[[F(1)],[F(0),F(1)]];U=[[F(1)],[F(0),F(2)]]
for j in range(2,N+1):cheb.append(add(mul([F(0),F(2)],cheb[-1]),scale(cheb[-2],-1)))
for j in range(2,N):U.append(add(mul([F(0),F(2)],U[-1]),scale(U[-2],-1)))
X=[F(0)];B=[F(0)]
for j in range(1,N+1):X=add(X,scale(add(cheb[j],[F(-1)]),a[j-1]));B=add(B,scale(U[j-1],b[j-1]))
cur=add(mul(X,add(mul([F(0),F(1)],B),scale(mul([F(1),0,F(-1)],diff(B)),-1))),mul([F(1),0,F(-1)],mul(B,diff(X))))
fac=div(cur,[F(1),F(-4),F(6),F(-4),F(1)])
leaves=[]
def check(bb,l,h,depth=0):
 if min(bb)>F(1,100):leaves.append((str(l),str(h),str(min(bb)),depth));return
 assert depth<24,'unresolved positivity'
 a,b=split(bb);m=(l+h)/2;check(a,l,m,depth+1);check(b,m,h,depth+1)
check(bern(fac),F(-1),F(1))
(ROOT/'data/current_certificate.json').write_text(json.dumps({'factor':'C_theta/(1-cos(theta))^4','lower_bound':'1/100','degree':len(fac)-1,'leaves':leaves},indent=2))
print('PASS current factor >=1/100; degree',len(fac)-1,'leaves',len(leaves),'maxdepth',max(x[3] for x in leaves))
