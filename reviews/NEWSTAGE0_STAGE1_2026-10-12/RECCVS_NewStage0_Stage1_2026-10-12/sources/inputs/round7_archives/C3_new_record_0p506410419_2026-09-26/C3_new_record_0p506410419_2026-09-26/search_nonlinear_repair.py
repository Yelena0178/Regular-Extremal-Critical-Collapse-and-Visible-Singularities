import sys,json,numpy as np
from fractions import Fraction
from scipy.signal import find_peaks
from scipy.optimize import minimize
exec(open('/mnt/data/c3work/local_geom.py').read().split('for w in [')[0])
# args w src scale maxiter
w=float(sys.argv[1]); srcp=sys.argv[2]; scale=float(sys.argv[3]) if len(sys.argv)>3 else 1e-5; maxiter=int(sys.argv[4]) if len(sys.argv)>4 else 300; mtarg=float(sys.argv[5]) if len(sys.argv)>5 else 1e-7; cfloor=float(sys.argv[6]) if len(sys.argv)>6 else 2e-11
D=json.load(open(srcp)); aS=np.array(D['a'],float);bS=np.array(D['b'],float);qbase=np.r_[j*aS,j*bS]  # override global used by setup
B,p0,ev=setup(w)
thdense=np.linspace(0,0.38,12001);*_,rden,Gden=ev(p0,thdense);inds=find_peaks(-rden)[0];inds=inds[np.argsort(rden[inds])[:3]];thmins=np.sort(thdense[inds]);*_,r0,G0=ev(p0,thmins)
A=np.vstack([p0,G0]);U,s,Vt=np.linalg.svd(A,full_matrices=True);rank=(s>1e-10*s[0]).sum();Z=Vt[rank:].T
ths=np.unique(np.r_[np.linspace(0,0.36,145),thmins]); ny=Z.shape[1]
def pj(y):
 v=p0+scale*(Z@y);nr=np.linalg.norm(v);p=np.sqrt(2)*v/nr;J=(np.sqrt(2)/nr)*(np.eye(len(p))-np.outer(p,p)/2)@(scale*Z);return p,J
def fun(y):
 p,J=pj(y);la,m,EL,CL,gl,gm=ev(p);return la,J.T@gl
def cons(y):
 p,J=pj(y);la,m,EL,CL,gl,gm,rr,G=ev(p,ths);vals=np.r_[(m-mtarg)/1e-5,(rr-cfloor)/1e-10];jac=np.vstack([J.T@gm/1e-5,(G@J)/1e-10]);return vals,jac
print('START',w,'src',srcp,'metrics',ev(p0)[:2],'mins',list(zip(thmins,r0)),flush=True)
y0=np.zeros(ny);res=minimize(lambda y:fun(y)[0],y0,jac=lambda y:fun(y)[1],constraints=[{'type':'ineq','fun':lambda y:cons(y)[0],'jac':lambda y:cons(y)[1]}],method='SLSQP',options={'ftol':1e-13,'maxiter':maxiter,'disp':True})
p,J=pj(res.x);la,m,*_=ev(p);*_,rr,_=ev(p,thdense);inds=find_peaks(-rr)[0];order=inds[np.argsort(rr[inds])[:8]]
print('RES',res.success,res.nit,'normy',np.linalg.norm(res.x),'metric',la,m,'mins',[(float(thdense[i]),float(rr[i])) for i in order],flush=True)
q=B@p;a=q[:N]/j;b=q[N:]/j;out={'N':N,'w':w,'a':a.tolist(),'b':b.tolist(),'label':f'endpoint_factored_branch_w{w}'};outp=f'/mnt/data/c3work/branch_{w:.8f}.json';json.dump(out,open(outp,'w'),indent=2);print('OUT',outp)
