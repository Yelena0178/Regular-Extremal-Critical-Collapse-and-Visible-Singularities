"""E0 incoming-null optical diagnostics; interpolation errors are not certified."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from charge_preserving_shell import ChargePreservingShell, ShellParameters
from centered_cauchy_diamond import axis_state, evolve_centered


class IncomingDiagnostics:
    def __init__(self, rays=(12.,14.,16.,20.,24.)):
        self.rays={str(v):[] for v in rays}
        self.minimum_f=None
        self.minimum_lambda=None

    def __call__(self,t,x,state):
        for name,points in self.rays.items():
            at=float(name)-t
            if not x[0] <= at <= x[-1]:
                continue
            y=np.array([np.interp(at,x,state[:,j]) for j in range(12)])
            r,k,nu,m,Q=y[0],y[1],y[4],y[7],y[10]
            if r<1e-4 or k<=0 or nu>=0:
                continue
            z2=y[5]**2+y[6]**2
            f=1-2*m/r
            points.append(dict(t=float(t),r=float(r),kappa=float(k),nu=float(nu),
                               f=float(f),charge_ratio=float(abs(Q)/r),
                               optical_integrand=float(-2*nu*z2/r),
                               mixed_integrand=float(2*k*(-nu)*(1-Q*Q/r**2))))
        valid=state[:,0]>=.25
        if not np.any(valid):
            return
        y=state[valid]; xp=x[valid]
        f=1-2*y[:,7]/y[:,0]; lam=y[:,1]*f
        for key,values in [('minimum_f',f),('minimum_lambda',lam)]:
            j=int(np.argmin(values))
            point=dict(t=float(t),x=float(xp[j]),r=float(y[j,0]),f=float(f[j]),
                       lambda_value=float(lam[j]),kappa=float(y[j,1]),
                       charge_ratio=float(abs(y[j,10])/y[j,0]))
            old=getattr(self,key)
            field='f' if key=='minimum_f' else 'lambda_value'
            if old is None or point[field]<old[field]:
                setattr(self,key,point)

    def report(self):
        rays=[]
        for name,points in self.rays.items():
            if len(points)<2:
                rays.append(dict(v=float(name),covered=False)); continue
            t=np.array([p['t'] for p in points]); r=np.array([p['r'] for p in points])
            k=np.array([p['kappa'] for p in points]); f=np.array([p['f'] for p in points])
            op=np.array([p['optical_integrand'] for p in points])
            mx=np.array([p['mixed_integrand'] for p in points])
            B=np.r_[0.,np.cumsum(np.diff(t)*(op[:-1]+op[1:])/2)]
            J=np.r_[0.,np.cumsum(np.diff(t)*(mx[:-1]+mx[1:])/2)]
            logdef=np.log(k[0]/k)-B
            mixeddef=r[0]*k[0]*f[0]-r*k*f-J
            # A first half-radius layer, if covered; only sampled charge/endpoint checks.
            half=np.flatnonzero(r<=r[0]/2)
            gate=None
            if half.size:
                i=int(half[0]); qmax=max(p['charge_ratio'] for p in points[:i+1])
                theta=(r[0]-r[i])/r[0]
                gate=dict(theta=float(theta),sampled_qmax=float(qmax),B=float(B[i]),
                          outer_f=float(f[0]),inner_f=float(f[i]),
                          lower_bound_if_continuous_premises_hold=float(theta*(1-qmax*qmax)*np.exp(-B[i])),
                          continuous_premises_certified=False)
            for j,p in enumerate(points):
                p.update(cumulative_B=float(B[j]),log_k_defect=float(logdef[j]),
                         mixed_transport_defect=float(mixeddef[j]))
            rays.append(dict(v=float(name),covered=True,radius_strictly_decreasing=bool(np.all(np.diff(r)<0)),
                             maximum_log_k_defect=float(max(abs(logdef))),
                             maximum_mixed_transport_defect=float(max(abs(mixeddef))),
                             first_half_radius_layer=gate,points=points))
        return dict(rays=rays,minimum_f_r_ge_quarter=self.minimum_f,
                    minimum_lambda_r_ge_quarter=self.minimum_lambda,
                    evidence='EXPERIMENTAL',finite_PDE_error_certified=False,
                    notes=['u=t-x, v=t+x; du=2dt on incoming rays',
                           'linear interpolation and trapezoidal integrals; no continuous envelopes'])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--direction',type=float,required=True)
    parser.add_argument('--time',type=float,required=True)
    parser.add_argument('--steps',type=int,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    parameters=ShellParameters(amplitude=.4,frequency=.15,direction=args.direction)
    data=ChargePreservingShell(parameters,exterior_width=max(10.,2*args.time+20))
    observer=IncomingDiagnostics()
    result=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,
                           data.proper_max,args.time,args.steps,observer=observer)
    for key in ['x','state','initial_state']:
        result.pop(key,None)
    result.update(diagnostics=observer.report(),initial_data=data.summary(),
                  requested_time=args.time,requested_steps=args.steps,goal_A_proved=False,
                  evidence='EXPERIMENTAL; finite optical-transport diagnostic')
    root=Path(__file__).resolve().parent
    names=['screen_incoming_optical_depth.py','charge_preserving_shell.py','centered_cauchy_diamond.py',
           'charged_cauchy_diamond.py','charged_lobatto.py']
    result['source_sha256']={n:sha256((root/n).read_bytes()).hexdigest() for n in names}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(output=str(args.output),completed=result['completed'],
                         minimum_f=observer.minimum_f,minimum_lambda=observer.minimum_lambda,
                         rays=[{k:v for k,v in r.items() if k!='points'} for r in result['diagnostics']['rays']]),indent=2))


if __name__ == '__main__':
    main()
