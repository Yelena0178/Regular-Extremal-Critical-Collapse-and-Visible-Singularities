"""Exact initial identities, finite evaluator controls, and archived evidence audit."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
import sympy as sp
from charge_preserving_shell import ShellParameters, ChargePreservingShell
from split_direction_shell import SplitDirectionShell

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def exact_checks():
    a, ap, r, w, da, dq = sp.symbols('a ap r w da dq', real=True)
    B = ap+a/r
    chi, grad = -da*B-sp.I*w*a, ap+sp.I*dq*w*a
    norm = lambda z: sp.expand(z*sp.conjugate(z))
    dv = (r*(chi+grad)+a)/2
    du = (r*(chi-grad)-a)/2
    physical_dv = (chi+grad)/2  # D_v phi / sqrt(f), not D_v(r phi)
    current = sp.im(a*sp.conjugate(physical_dv))
    phase_cost = (1-dq)**2*w*w*a*a/4
    S = ap**2+da**2*B**2+(1+dq**2)*w**2*a**2
    expressions = {
        'Gauss_current': sp.im(a*sp.conjugate(chi))-w*a*a,
        'constraint_energy': norm(chi)+norm(grad)-S,
        'momentum_source': sp.re(chi*sp.conjugate(grad))+da*B*ap+dq*w*w*a*a,
        'outgoing_decomposition': dv-((1-da)*(a+r*ap)+sp.I*(dq-1)*r*w*a)/2,
        'incoming_decomposition': du+((1+da)*(a+r*ap)+sp.I*(1+dq)*r*w*a)/2,
        'flux_difference': norm(du)-norm(dv)-da*(a+r*ap)**2-dq*(r*w*a)**2,
        'positive_energy_difference': S.subs({da:1,dq:1})-S-((1-da**2)*B**2+(1-dq**2)*w*w*a*a),
        'physical_charge_current': current-(1-dq)*w*a*a/2,
        'physical_focusing_cost': norm(physical_dv)-((ap-da*B)**2/4+phase_cost),
        'phase_flip_current_factor': current.subs(dq,-sp.Rational(4,5))-9*current.subs(dq,sp.Rational(4,5)),
        'phase_flip_focusing_factor': phase_cost.subs(dq,-sp.Rational(4,5))-81*phase_cost.subs(dq,sp.Rational(4,5)),
    }
    for name, expression in expressions.items():
        require(sp.simplify(expression) == 0, name)
    require(sp.simplify(sp.im(a*sp.conjugate(-da*B))-w*a*a) != 0,
            'omitted charge term negative control was not detected')
    require(sp.simplify(dv.subs(dq,da)-dv) != 0,
            'relocking the phase direction negative control was not detected')
    return {'identities':list(expressions), 'negative_controls':2,
            'scope':'finite exact algebra; positivity comparison is analytic, not inferred from samples'}


def evaluator_checks():
    radii = np.linspace(6.05,13.95,37)
    baseline = ChargePreservingShell(ShellParameters(amplitude=.4, frequency=.15, direction=1.))
    base_f = baseline.sol.sol(radii)[1]
    records=[]
    for da in (-.8,0.,.8):
        p=ShellParameters(amplitude=.4, frequency=.15, direction=da)
        old=ChargePreservingShell(p)
        for dq in (-.8,0.,.8):
            new=SplitDirectionShell(p,dq)
            q,f,_=new.sol.sol(radii)
            require(float(np.min(f-base_f)) > -2e-8, 'finite comparison control failed')
            require(abs(new.ADM_charge-old.ADM_charge)<2e-8, 'charge changed')
            for radius in radii:
                phi,grad,chi=new.free(float(radius))
                yy=new.sol.sol(radius)
                rhs=new.constraint_rhs(radius,yy)
                require(abs(rhs[0]-.6*radius**2*np.imag(phi*np.conjugate(chi)))<1e-10,
                        'evaluator Gauss mismatch')
                independently=(1-yy[1])/radius-yy[0]**2/radius**3-radius*yy[1]*(abs(grad)**2+abs(chi)**2)
                require(abs(rhs[1]-independently)<1e-10, 'evaluator Hamiltonian mismatch')
                if da==dq:
                    require(float(np.max(np.abs(np.asarray(new.free(radius))-old.free(radius))))<1e-12,
                            'diagonal does not recover the old family')
            if da==dq:
                require(float(np.max(abs(new.sol.sol(radii)-old.sol.sol(radii))))<2e-8,
                        'diagonal constraint solve changed')
            records.append({'envelope_direction':da,'phase_direction':dq,
                            'ADM_mass':new.ADM_mass,'ADM_charge':new.ADM_charge,
                            'minimum_sampled_f':float(np.min(f))})
    return records


def archived_evidence():
    names=['BIASED_SHELL_BM2_D05_T30_N1024_2026-10-22.json',
           'BIASED_SHELL_BP2_D05_T30_N1024_2026-10-22.json',
           'BIASED_SHELL_BM2_D08_T30_N1024_2026-10-22.json',
           'BIASED_SHELL_BP2_D08_T30_N1024_2026-10-22.json',
           'BIASED_SHELL_BP2_D08_T60_N3072_2026-10-22.json']
    rows=[]
    for name in names:
        path=ROOT/name
        obj=json.loads(path.read_text(encoding='utf-8'))
        require(bool(obj.get('source_sha256')), 'missing source receipt')
        for source,digest in obj['source_sha256'].items():
            require(sha256((ROOT/source).read_bytes()).hexdigest()==digest, f'stale source: {source}')
        sample=obj['diagnostics']['fixed_radius_samples'][-1]
        require(sample['areal_radius_monotone'], 'radius interpolation not monotone')
        gate=next(g for g in sample['gates'] if g['radius']==14.)
        require(gate['covered'], 'r=14 not covered')
        require(obj['initial_data']['ADM_mass']>0 and obj['initial_data']['ADM_charge']!=0,
                'invalid diagnostic denominators')
        negative=obj.get('first_negative_sample')
        rows.append({'report':name,'report_sha256':sha256(path.read_bytes()).hexdigest(),
                     'sources_match_current':True,'completed':obj['completed'],
                     'last_diagnostic_time':sample['time'],
                     'axis_proper_time':sample['axis_proper_time'],
                     'm14':gate['renormalized_mass'],'Q14':gate['charge'],
                     'm14_over_ADM':gate['renormalized_mass']/obj['initial_data']['ADM_mass'],
                     'abs_Q14_over_ADM':abs(gate['charge']/obj['initial_data']['ADM_charge']),
                     'first_negative_abs_Q_over_r':abs(negative['Q']/negative['radius']) if negative else None})
    return rows


def probe_evidence():
    rows=[]
    for direction in ('08','M08'):
        for steps in (256,512):
            name=f'SPLIT_DA08_DQ{direction}_T15_N{steps}_2026-11-01.json'
            path=ROOT/name
            obj=json.loads(path.read_text(encoding='utf-8'))
            require(obj['completed'] and obj['final_time']==15., 'probe did not reach the comparison time')
            for source,digest in obj['source_sha256'].items():
                require(sha256((ROOT/source).read_bytes()).hexdigest()==digest, f'stale probe: {source}')
            sample=obj['diagnostics']['fixed_radius_samples'][-1]
            require(sample['areal_radius_monotone'] and sample['time']==15., 'invalid endpoint diagnostic')
            gate=next(g for g in sample['gates'] if g['radius']==14.)
            require(gate['covered'], 'probe does not cover r=14')
            negative=obj['first_negative_sample']
            rows.append({'report':name,'report_sha256':sha256(path.read_bytes()).hexdigest(),
                         'sources_match_current':True,'phase_direction':obj['initial_data']['phase_direction'],
                         'steps':steps,'ADM_mass':obj['initial_data']['ADM_mass'],
                         'ADM_charge':obj['initial_data']['ADM_charge'],
                         'minimum_sampled_lambda':obj['worst']['lambda_value'],
                         'first_negative_sample':negative,
                         'first_negative_abs_Q_over_r':abs(negative['Q']/negative['radius']) if negative else None,
                         'm14':gate['renormalized_mass'],'Q14':gate['charge'],
                         'axis_proper_time':sample['axis_proper_time'],
                         'final_maximum_residuals':obj['final_row_constraints']['maximum_absolute']})
    require(max(x['ADM_mass'] for x in rows)-min(x['ADM_mass'] for x in rows)<1e-12,
            'controlled pair has different initial mass')
    require(max(x['ADM_charge'] for x in rows)-min(x['ADM_charge'] for x in rows)<1e-12,
            'controlled pair has different initial charge')
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    receipt={'created_utc':datetime.now(timezone.utc).isoformat(),
             'claim':'SPLIT01.1 initial family only',
             'exact_checks':exact_checks(),'finite_evaluator_controls':evaluator_checks(),
             'archived_candidate_diagnostics':archived_evidence(),
             'controlled_finite_probes':probe_evidence(),
             'finite_PDE_error_certified':False,'full_future_classified':False,'goal_A_proved':False}
    names=['verify_split_direction_shell.py','split_direction_shell.py','charge_preserving_shell.py',
           'CHARGE_SHELL_INITIAL_CERTIFICATE_2026-10-22.json','CHARGE_PRESERVING_DIRECTION_FAMILY.md']
    receipt['source_sha256']={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('PASS: 11 exact identities, 2 negative controls, 9 finite initial controls, 5 archived receipts, 4 finite probes')
    print('LIMIT: no new future PDE certificate, retained core, or Goal A proof')
