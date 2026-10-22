"""Independent E0 checks of the general-angular-curvature implementation."""
import cmath
from pathlib import Path
from hashlib import sha256
import json
import numpy as np
import mpmath as mp
from incoming_family import Parameters,bump,integrate as polar_integrate
from constraint_contraction import Profile,integrate,tail_or_cap,scalar_mass_source,reconstruct


def require(value,label):
    if not value:
        raise ArithmeticError(label)


def make_profile(p,tilt,scalar=True):
    def free(r):
        psi,dp=bump(r,p)
        ell=tilt*psi/r
        ellp=tilt*(dp/r-psi/r**2)
        if not scalar:
            return 0j,0j,0j,ell,ellp
        phase=cmath.exp(-1j*p.frequency*r)
        phi=p.amplitude*psi*phase/r
        gradient=p.amplitude*(dp-psi/r-1j*p.frequency*psi)*phase/r
        chi=p.amplitude*(dp-1j*p.frequency*psi)*phase/r
        return phi,gradient,chi,ell,ellp
    return Profile(p.inner,p.outer,free)


def residuals(result,omit_matter_momentum=False):
    rows=result['rows']
    r=np.array([x['r'] for x in rows])
    h=r[1]-r[0]
    def diff(a):
        return (a[:-4]-8*a[1:-3]+8*a[3:-1]-a[4:])/(12*h)
    get=lambda key:np.array([x[key] for x in rows])
    D,Q,ell,kr=get('D'),get('Q'),get('ell'),get('kr')
    if omit_matter_momentum:
        kr=np.array([result['s']*(result['profile'].free(v)[3]
                                  +v*result['profile'].free(v)[4]) for v in r])
    rr=r[2:-2]
    Rh=2*(1-D[2:-2]-rr*diff(D))/rr**2
    Ham=Rh+4*kr[2:-2]*ell[2:-2]+2*ell[2:-2]**2-4*get('rho')[2:-2]
    Mom=2*((kr[2:-2]-ell[2:-2])/rr-diff(ell))-2*get('jr')[2:-2]
    Gauss=np.sqrt(D[2:-2])*diff(Q)/rr**2-.6*np.imag(
        get('phi')[2:-2]*np.conj(get('Pi')[2:-2]))
    return dict(hamiltonian=float(max(abs(Ham))),momentum=float(max(abs(Mom))),
                gauss=float(max(abs(Gauss))))


def main():
    p=Parameters(amplitude=.7,frequency=.2)
    # The original signed source loses the entire answer in binary64 here.
    mp.mp.dps=90
    for sign in (-1,1):
        ff=mp.mpf('1e-18')
        ell=sign*mp.mpf('1e8')
        DD=ff+ell**2
        chi=-sign
        reference=DD+ell*mp.sqrt(DD)*chi
        computed=scalar_mass_source(1.,float(ff),1.,float(chi),float(ell))
        require(abs(mp.mpf(computed)/reference-1)<mp.mpf('3e-15'),
                'near-null scalar source cancellation')
        probe=Profile(.5,2.,lambda r:(0j,1.+0j,complex(chi),float(ell),0.))
        x=reconstruct(1.,float(ff),0.,probe,1.)
        require(x['expansion_out']>0>x['expansion_in'],
                'near-null expansion rounded to zero')
        require(abs(x['expansion_out']*x['expansion_in']/(-4*float(ff))-1)<3e-15,
                'near-null expansion product')
    # Nonzero K, exactly flat spacetime: arbitrary compactly tilted Minkowski slice.
    vacuum=integrate(make_profile(p,.6,scalar=False),1.,512)
    require(abs(vacuum['ADM_mass'])<1e-13 and abs(vacuum['ADM_charge'])<1e-13,
            'tilted Minkowski acquired mass or charge')
    require(max(abs(x['f']-1) for x in vacuum['rows'])<1e-13,
            'tilted Minkowski lost f=1')
    # A distinct m-based solver checks the ell=0 reduction.
    reduced=integrate(make_profile(p,0.),1.,1024)
    old=polar_integrate(p,1024)
    mismatch=max(max(abs(x['Q']-q),abs(x['f']-(1-2*m/r)))
                 for x,(r,m,q) in zip(reduced['rows'],old))
    require(mismatch<2e-9,'independent polar solver mismatch')
    profile=make_profile(p,.2)
    coarse=integrate(profile,1.,512)
    fine=integrate(profile,1.,1024)
    cr,fr=residuals(coarse),residuals(fine)
    for key in cr:
        require(fr[key]<cr[key]*.15+2e-12,'constraint residual did not converge: '+key)
    wrong=residuals(fine,omit_matter_momentum=True)
    require(wrong['momentum']>max(100*fr['momentum'],1e-7),
            'omitted momentum term negative control not detected')
    curves=[integrate(profile,s,512) for s in (0.,.25,.5,.75,1.)]
    for left,right in zip(curves,curves[1:]):
        require(min(a['f']-b['f'] for a,b in zip(left['rows'],right['rows']))>-1e-12,
                'sampled parameter ordering failure')
    Q1=curves[-1]['ADM_charge']
    for result in curves[1:]:
        require(abs(result['ADM_charge']-result['s']**2*Q1)<1e-12,
                'charge scaling failure')
    for result in curves:
        for x in result['rows']:
            require(x['expansion_out']>0 and x['expansion_in']<0,
                    'sampled expansion sign')
        require(tail_or_cap(result,0.)['D']==1.,'regular flat cap')
        tail=tail_or_cap(result,1000.)
        require(abs(tail['f']-(1-2*result['ADM_mass']/1000+result['ADM_charge']**2/1e6))<1e-14,
                'RN tail reconstruction')
    folder=Path(__file__).resolve().parent
    report=dict(status='PASS',evidence='E0 implementation checks, not candidate evolution',
                near_null_reference_precision_digits=90,
                near_null_signed_tilt_cases_checked=2,
                polar_maximum_difference=mismatch,
                geometric_residuals_512=cr,geometric_residuals_1024=fr,
                omitted_momentum_residual=wrong['momentum'],
                sample_ADM=[dict(s=x['s'],mass=x['ADM_mass'],charge=x['ADM_charge'],
                                minimum_sampled_f=x['minimum_sampled_f']) for x in curves],
                original_AF03_candidate_implemented=False,
                boundary_parameter_located=False,three_branch_goal_proved=False,
                source_sha256={name:sha256((folder/name).read_bytes()).hexdigest()
                    for name in ['constraint_contraction.py','verify_contraction_implementation.py',
                                 'incoming_family.py']})
    (folder/'CONTRACTION_IMPLEMENTATION_CHECKS_2026-10-20.json').write_text(
        json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['status','polar_maximum_difference',
        'geometric_residuals_512','geometric_residuals_1024','omitted_momentum_residual']}))
    print('Scope: implementation benchmark only; the AF03 seed and critical parameter remain unimplemented/unlocated.')


if __name__=='__main__':
    main()
