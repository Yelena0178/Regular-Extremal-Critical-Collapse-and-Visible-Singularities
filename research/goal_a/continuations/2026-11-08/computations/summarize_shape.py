from pathlib import Path
import json, math, hashlib
ROOT=Path.cwd(); SRC=ROOT/'source/goal-a/research/goal_a'
paths={f'{s}_{n}':ROOT/f'results/SHAPE_{s}_TRACE_N{n}.json' for s in ['M','P'] for n in [512,1024]}
paths.update({f'BASE_{n}':SRC/f'AMP_S150_TRACE_T15_N{n}_2026-11-01.json' for n in [512,1024]})
reports={k:json.loads(v.read_text()) for k,v in paths.items()}
metrics={}
for key,p in reports.items():
 u=p['ray_selection']['primary_u']; trace=next(t for t in p['diagnostics']['target_ray_traces'] if t['u']==u); ray=next(t for t in p['diagnostics']['null_ray_budgets'] if t['u']==u)
 q0=ray['initial_Q']; row=trace['first_negative']; assert row is not None
 r=row['radius']; B=row['entry_expansion']-row['amplitude_cost']; H=row['capacity']; assert B>0
 metrics[key]=dict(u=u,time=row['time'],r=r,Q=row['Q'],Q_over_r=abs(row['Q'])/r,B=B,H=H,HB=H*B,HB_over_r2=H*B/r**2,capacity=(abs(q0)+.6*math.sqrt(H*B))/r,amplitude_fraction=row['amplitude_cost']/row['focusing'],phase_efficiency=row['minimum_charge_cost']/row['phase_cost'],ray_defect=trace['max_raychaudhuri_defect'],completed=p['completed'],constraints=p.get('final_row_constraints'))
common=[]
for t in sorted(set.intersection(*[{s['time'] for s in p['diagnostics']['fixed_radius_samples']} for p in reports.values()])):
 for radius in [5.,10.,14.,28.]:
  vals={}
  for key,p in reports.items():
   row=next(s for s in p['diagnostics']['fixed_radius_samples'] if s['time']==t)
   gate=next((g for g in row['gates'] if g['radius']==radius and g['covered']),None)
   if gate is None: break
   vals[key]={k:gate[k] for k in ['renormalized_mass','charge']}
  if len(vals)==len(reports):common.append(dict(time=t,radius=radius,values=vals))
assert all(p['completed'] for p in reports.values())
assert all(reports[f'{s}_512']['observer_regression_passed'] for s in ['M','P'])
decisions={}
for s in ['M','P']:
 fine=metrics[f'{s}_1024']; coarse=metrics[f'{s}_512']; base=metrics['BASE_1024']; basec=metrics['BASE_512']
 dcap=abs(fine['capacity']-coarse['capacity'])+abs(base['capacity']-basec['capacity'])
 dr=abs(fine['r']-coarse['r'])+abs(base['r']-basec['r'])
 decisions[s]=dict(capacity_gain=fine['capacity']-base['capacity'],combined_grid_capacity_difference=dcap,radius_change=fine['r']-base['r'],combined_grid_radius_difference=dr,capacity_gain_exceeds_grid_difference=fine['capacity']-base['capacity']>dcap,radius_not_smaller=fine['r']>=base['r']-dr)
 decisions[s]['passes_prespecified_joint_gate']=decisions[s]['capacity_gain_exceeds_grid_difference'] and decisions[s]['radius_not_smaller']
summary=dict(metrics=metrics,common_fixed_radius=common,decisions=decisions,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()},finite_PDE_error_certified=False,goal_A_proved=False,decision=('retain outward shape as finite mechanism lead; audit phase transport realizability, no new scan yet' if any(d['passes_prespecified_joint_gate'] for d in decisions.values()) else 'stop same-kind single-shell tweaking; audit staged loading or purely asymptotic mechanism'),comparison_scope='own first-negative ray samples are different events; common coordinate time fixed areal radii are compared separately, not common proper time')
(ROOT/'results/SHAPE_COMPARISON.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(dict(metrics={k:{j:v for j,v in m.items() if j!='constraints'} for k,m in metrics.items()},decisions=decisions,common_T15_r14=next(c for c in common if c['time']==15 and c['radius']==14)),indent=2))
