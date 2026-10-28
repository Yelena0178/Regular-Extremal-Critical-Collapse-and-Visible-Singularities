"""Arbitrary dyadic reference for a uniformly thin smooth onset family.

The endpoint value of theta is set to zero at the vacuum corner. Away from
that corner the reference edge samples the C0 limit. No physical solution or
smooth boundary certificate is inferred from this numerical reference alone.
"""

import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from neutral_onset_input import NeutralOnset
from neutral_transport import TransportConfiguration,evolve,fourth_derivative,geometry
from transport_defect import residual_forecast
from interval_transport_grid import V,propagate


def boundaries():
    p=NeutralOnset.from_first_jet_report(.05).parameters()
    cap,r0=p['v_cap'],p['r_cap'];q=p['field_amplitude']/p['v_onset_width']
    def radius(v):
        t=v-cap
        return r0*np.cos(q*t)+np.sin(q*t)/(2*q),-r0*q*np.sin(q*t)+np.cos(q*t)/2
    def z_rhs(v,z):
        r,lam=radius(v)
        return -q-(1/v-lam/r)*z
    zsol=solve_ivp(z_rhs,(cap,p['v_end']),[0.],method='DOP853',
                   rtol=2e-12,atol=2e-14,max_step=p['v_onset_width']/384,dense_output=True)
    if not zsol.success:raise ArithmeticError(zsol.message)
    def outgoing(v):
        r,lam=radius(v)
        theta=0. if v==cap else r*q
        return np.array([r,r/v,theta,-v/(4*r),float(zsol.sol(v)[0]),(r-v*lam)/2])
    def incoming(u):return np.array([r0-u/2,.5,0.,-.5,0.,0.])
    return outgoing,incoming,p,radius


def main(steps_v=384):
    base=Path(__file__).resolve().parent
    out,inc,p,radius=boundaries();n=steps_v
    cfg=TransportConfiguration(steps_u=384,steps_v=n,final_u=p['v_end']/2,
                               initial_v=p['v_cap'],final_v=31*p['v_end']/32)
    data=evolve(out,inc,cfg);x=data['state'][0]
    h=data['v'][1]-data['v'][0];slope=fourth_derivative(x,0,h)
    boundary=np.zeros((n+1,6));q=p['field_amplitude']/p['v_onset_width']
    t=np.linspace(0,1,129)[:,None]
    for j in range(n):
        a,b,da,db=x[j,:3],x[j+1,:3],slope[j,:3],slope[j+1,:3]
        poly=a+h*da*t+(3*(b-a)-h*(2*da+db))*t*t+(2*(a-b)+h*(da+db))*t*t*t
        v=data['v'][j]+h*t[:,0];r,_=radius(v)
        target=np.array([r,r/v,r*q]).T
        boundary[j+1,:3]=np.max(abs(target-poly),axis=0)+1e-7
    boundary[1,2]=1.
    low,high,delta=residual_forecast(data)
    result=dict(evidence='E0_C0_reference_thin_layer_feasibility',
                steps_u=384,steps_v=steps_v,
                trial_first_cell_theta_error=1.,maximum_trial_boundary=np.max(boundary,axis=0).tolist(),
                actual_thin_layer_transfer=False,original_eta_seed_transfer=False,goal_A_proved=False,
                fixed_point=geometry(data['state'][-1,-1]))
    try:
        radii,report=propagate(low,high,delta,V(data['u'][1]),V(h),boundary)
        M=radii[-1,-1];last=data['state'][-1,-1]
        result.update(completed=True,endpoint_radii=M.tolist(),conditional_report=report,
                      hypothetical_2m_minus_r_lower=float(2*(last[5]-M[5])-(last[0]+M[0])))
    except ArithmeticError as error:result.update(completed=False,failure=str(error))
    suffix='' if steps_v==384 else '_NV'+str(steps_v)
    (base/('THIN_ONSET_REFERENCE_FORECAST_2026-10-17'+suffix+'.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
