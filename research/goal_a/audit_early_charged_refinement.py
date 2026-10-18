"""Independent constraints and shared-node E0 refinement diagnostics."""

from hashlib import sha256
import json
from pathlib import Path
import numpy as np

from neutral_transport import fourth_derivative


def diagnostics(data):
    x=data['state'];u,v=data['u'],data['v'];r,k,tr,ti,nu,zr,zi,m,pr,pi,Q,A=np.moveaxis(x,-1,0)
    z,phi=zr+1j*zi,pr+1j*pi;f=1-2*m/r;lam=k*f
    xu=fourth_derivative(x,0,float(u[1]-u[0]));xv=fourth_derivative(x,1,float(v[1]-v[0]))
    defects=dict(radius_v=xv[...,0]-lam,
        scalar_u=xu[...,8]+1j*xu[...,9]-nu*z/r+1j*.6*A*phi,
        charge_u=xu[...,10]+.6*r*nu*(phi*z.conjugate()).imag,
        mass_u=xu[...,7]-Q*Q*nu/(2*r*r)-f*nu*abs(z)**2/2)
    sl=(slice(2,-2),slice(2,-2))
    terminal=x[0,-1];rr,kk,nn=terminal[0],terminal[1],terminal[4]
    coeff=kk*nn*nn/(rr*rr)
    return dict(independent_constraint_max={name:float(abs(a[sl]).max()) for name,a in defects.items()},
        first_interior_terminal_lambda=float(lam[1,-1]),
        first_interior_lambda_over_du_squared=float(lam[1,-1]/(u[1]-u[0])**2),
        analytic_terminal_quadratic_coefficient_proposal=float(coeff)),lam


def main():
    folder=Path(__file__).resolve().parent
    sources=['EARLY_CHARGED_REFINEMENT_48_96_2026-10-17.json','EARLY_CHARGED_REFINEMENT_192_2026-10-17.json']
    records=[]
    for source in sources:
        report=json.loads((folder/source).read_text())
        for name,want in report['source_sha256'].items():
            if sha256((folder/name).read_bytes()).hexdigest()!=want:raise ArithmeticError('stale experiment '+name)
        records+=report['runs']
    comparisons=[];hashes={}
    for label in ((.2,8.),(.3,4.)):
        selected=sorted([r for r in records if (r['configuration']['amplitude'],r['configuration']['frequency'])==label],key=lambda r:r['n'])
        old=None;oldlam=None;entry=dict(amplitude=label[0],frequency=label[1],resolutions=[])
        for record in selected:
            name=record['cache'];want=record['cache_sha256']
            if sha256((folder/name).read_bytes()).hexdigest()!=want:raise ArithmeticError('stale reference '+name)
            hashes[name]=want;data=np.load(folder/name);diagnostic,lam=diagnostics(data)
            diagnostic['n']=record['n']
            if old is not None:
                diagnostic['shared_node_state_difference']=np.max(abs(old-data['state'][::2,::2]),axis=(0,1)).tolist()
                diagnostic['shared_node_lambda_difference']=float(np.max(abs(oldlam-lam[::2,::2])))
            old=data['state'];oldlam=lam;entry['resolutions'].append(diagnostic)
        comparisons.append(entry)
    result=dict(status='E0_DIAGNOSTICS_ONLY',comparisons=comparisons,cache_sha256=hashes,
        complete_PDE_error_certified=False,actual_no_trapping_proved=False,goal_A_proved=False)
    names=['audit_early_charged_refinement.py','neutral_transport.py']+sources
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'EARLY_CHARGED_REFINEMENT_AUDIT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','cache_sha256')},indent=2))


if __name__=='__main__':main()
