"""Attempt full outward charged error tubes using certified frozen inflow.

FAIL is retained as a failed error budget, never as physical breakdown.
Even PASS concerns only this frozen C0 reference, not a smooth endpoint root.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import time

import numpy as np

from charged_interval_kernel import (NAMES,JACOBIAN,V,coefficients,cell_bounds,jacobian_upper)
from charged_lobatto import rhs
from neutral_transport import fourth_derivative
from graded_transport import v_derivative
from interval_transport_grid import up
from frozen_charged_boundary import proposal


def floating_jacobian(x):
    states={name:x[...,j] for j,name in enumerate(NAMES)};cache={}
    jac=np.empty(x.shape[:-1]+(12,12))
    for i,row in enumerate(JACOBIAN):
        for j,poly in enumerate(row):
            total=np.zeros(x.shape[:-1])
            for monomial,coefficient in poly.terms.items():
                term=float(coefficient)
                for name,power in monomial:
                    if (name,power) not in cache:cache[name,power]=states[name]**power
                    term=term*cache[name,power]
                total=total+term
            jac[...,i,j]=total
    return jac


def derivatives(x,v_exact,hu):
    f=rhs(x);xu=fourth_derivative(x,0,float(hu));xv=v_derivative(x,v_exact)
    xu[...,:4]=f[...,:4];xv[...,4:]=f[...,4:]
    for j,V0 in enumerate(v_exact):xv[0,j,:4]=proposal(float(V0),derivatives.piece)[1]
    jac=floating_jacobian(x);xuv=np.empty_like(x)
    xuv[...,:4]=np.einsum('...ij,...j->...i',jac[...,:4,:],xv)
    xuv[...,4:]=np.einsum('...ij,...j->...i',jac[...,4:,:],xu)
    return xu,xv,xuv


def propagate(low,high,delta,hu,hv,outgoing,incoming,progress):
    nu,nv=delta.shape[:2];radii=np.zeros((nu+1,nv+1,12));least=np.inf
    radii[0,:,:4]=outgoing;radii[:,0,4:]=incoming
    for diagonal in range(nu+nv-1):
        ii=np.arange(max(0,diagonal-nv+1),min(nu-1,diagonal)+1);jj=diagonal-ii
        h=V(np.column_stack([np.full(len(ii),float(hu.lo))]*4+[hv.lo[jj]]*8),
            np.column_stack([np.full(len(ii),float(hu.hi))]*4+[hv.hi[jj]]*8))
        edge=np.concatenate([radii[ii,jj+1,:4],radii[ii+1,jj,4:]],axis=-1)
        M=up(edge+h.hi*delta[ii,jj]+1e-12)
        for attempt in range(40):
            lo=(V(low[ii,jj])-V(M)).lo;hi=(V(high[ii,jj])+V(M)).hi
            if np.any(lo[...,0]<=0) or np.any(lo[...,1]<=0) or np.any(hi[...,4]>=0):
                raise ArithmeticError(f'positive charged tube failed on diagonal {diagonal}')
            L=jacobian_upper(lo,hi);total=V(delta[ii,jj])
            for j in range(12):total=total+V(L[...,j])*V(M[...,j,None])
            margin=V(M)-V(edge)-h*total;passed=np.min(margin.lo,axis=-1)>0
            if passed.all():break
            matrix=np.eye(12)-h.hi[...,None]*L
            estimate=np.linalg.solve(matrix,(edge+h.hi*delta[ii,jj]+1e-12)[...,None])[...,0]
            if not np.isfinite(estimate).all() or np.min(estimate)<0:
                raise ArithmeticError(f'invalid charged radius proposal on diagonal {diagonal}')
            trial=up(edge+1.08*np.maximum(estimate-edge,0))
            M=np.where(passed[:,None],M,np.maximum(M,trial))
        else:raise ArithmeticError(f'charged compression failed on diagonal {diagonal}')
        if not np.isfinite(margin.lo).all():raise ArithmeticError('nonfinite charged margin')
        least=min(least,float(np.min(margin.lo)));radii[ii+1,jj+1]=M
        if diagonal%32==0:progress(diagonal,least)
    return radii,dict(verified_cells=nu*nv,minimum_margin=least)


def verify_sources(folder,report):
    for name,want in report['source_sha256'].items():
        if sha256((folder/name).read_bytes()).hexdigest()!=want:raise ArithmeticError('stale input '+name)


def main(reuse_directory=None):
    start=time.monotonic();folder=Path(__file__).resolve().parent
    reference_name='FROZEN_CHARGED_REFERENCE_N96_2026-10-17.json'
    boundary_name='FROZEN_CHARGED_BOUNDARY_CERTIFICATE_2026-10-17.json'
    ref=json.loads((folder/reference_name).read_text());boundary=json.loads((folder/boundary_name).read_text())
    verify_sources(folder,ref);verify_sources(folder,boundary)
    if boundary['status']!='PASS':raise ArithmeticError('boundary not accepted')
    if sha256((folder/ref['cache']).read_bytes()).hexdigest()!=ref['cache_sha256']:raise ArithmeticError('reference cache changed')
    cache=np.load(folder/ref['cache']);n=ref['n'];hu_exact=Q(ref['exact_U'])/n;hu=V.rational(hu_exact)
    incoming=np.zeros((n+1,8));incoming[:,0]=float(V.rational(Q(boundary['incoming_nu_error'])).hi)
    reused=None;reuse_sources=[]
    if reuse_directory is not None:
        archive=folder/reuse_directory;manifest=json.loads((archive/'manifest.json').read_text())
        for name,want in manifest['files'].items():
            if sha256((archive/name).read_bytes()).hexdigest()!=want:raise ArithmeticError('checkpoint changed '+name)
            reuse_sources.append(str((archive/name).relative_to(folder)))
        old=json.loads((archive/'FROZEN_CHARGED_RECTANGLE_ATTEMPT_2026-10-17.json').read_text())
        for name,want in old['source_sha256'].items():
            source=archive/name if name=='attempt_charged_rectangle.py' else folder/name
            if sha256(source.read_bytes()).hexdigest()!=want:raise ArithmeticError('cached bound dependency changed '+name)
        reused=np.load(archive/old['prepared_cache'])
        reuse_sources.append(str((archive/'manifest.json').relative_to(folder)))
    reports=[];old_x=None;prepared={}
    result=dict(status='FAIL',scope='attempted frozen C0 charged finite rectangle',
                complete_C0_rectangle_certified=False,strict_trapping_certified=False,
                actual_smooth_seed_certified=False,goal_A_proved=False)
    try:
        with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
            for piece in range(3):
                x=cache[f'piece{piece}_state'].copy();v=[Q(z) for z in ref['exact_meshes'][piece]]
                if old_x is not None:x[:,0,4:]=old_x[:,-1,4:]
                for j,V0 in enumerate(v):x[0,j,:4]=proposal(float(V0),piece)[0]
                derivatives.piece=piece
                xu,xv,xuv=derivatives(x,v,hu_exact)
                if piece==0:xu[:,0,4:]=0.
                for name,array in [('nodes',x),('du',xu),('dv',xv),('duv',xuv)]:prepared[f'piece{piece}_{name}']=array
                widths=[V.rational(b-a) for a,b in zip(v,v[1:])]
                hv=V(np.array([float(h.lo) for h in widths]),np.array([float(h.hi) for h in widths]))
                low=np.empty((n,n,12));high=np.empty_like(low);delta=np.empty_like(low)
                if piece==0 and reused is not None:
                    for name,array in [('nodes',x),('du',xu),('dv',xv),('duv',xuv)]:
                        if not np.array_equal(array,reused[f'piece0_{name}']):raise ArithmeticError('cached Hermite input differs '+name)
                    low[:]=reused['piece0_low'];high[:]=reused['piece0_high'];delta[:]=reused['piece0_delta']
                    print(json.dumps(dict(stage='charged_cached_bounds_verified',piece=0,cells=n*n)),flush=True)
                else:
                    for first in range(0,n,4):
                        last=min(first+4,n);sl=slice(first,last+1)
                        c=coefficients(x[sl],xu[sl],xv[sl],xuv[sl],hu,hv[:,None])
                        B,d=cell_bounds(c,hu,hv[:,None,None]);low[first:last]=B.lo;high[first:last]=B.hi;delta[first:last]=d
                        if first%24==0:print(json.dumps(dict(stage='charged_cell_bounds',piece=piece,rows_complete=last)),flush=True)
                for name,array in [('low',low),('high',high),('delta',delta)]:prepared[f'piece{piece}_{name}']=array
                out=np.array([float(V.rational(Q(e)).hi) for e in boundary['pieces'][piece]['errors']])
                print(json.dumps(dict(stage='charged_tube_start',piece=piece,
                    maximum_residuals=np.max(delta,axis=(0,1)).tolist(),boundary_errors=out.tolist())),flush=True)
                radii,report=propagate(low,high,delta,hu,hv,out,incoming,
                    lambda diagonal,margin:print(json.dumps(dict(stage='charged_tube',piece=piece,diagonal=diagonal,margin=margin)),flush=True))
                prepared[f'piece{piece}_radii']=radii;reports.append(dict(piece=piece,**report))
                incoming[1:]=radii[1:,-1,4:];incoming[0]=incoming[1];old_x=x
                if piece==2:
                    endpoint=V((V(x[-1,-1])-V(radii[-1,-1])).lo,(V(x[-1,-1])+V(radii[-1,-1])).hi)
                    lam=endpoint[1]*(1-2*endpoint[7]/endpoint[0])
                    result.update(status='PASS',complete_C0_rectangle_certified=True,
                                  endpoint_lambda_interval=[float(lam.lo),float(lam.hi)],
                                  strict_trapping_certified=bool(lam.hi<0))
    except (ArithmeticError,ValueError,FloatingPointError,np.linalg.LinAlgError) as error:
        result['failure']=str(error)
        print(json.dumps(dict(stage='charged_tube_failure',failure=str(error))),flush=True)
    name='FROZEN_CHARGED_PREPARED_N96_2026-10-17.npz'
    np.savez_compressed(folder/name,**prepared)
    result.update(completed_pieces=reports,prepared_cache=name,
                  prepared_cache_sha256=sha256((folder/name).read_bytes()).hexdigest(),elapsed_seconds=time.monotonic()-start)
    names=['attempt_charged_rectangle.py','charged_interval_kernel.py','interval_transport_grid.py',
           'charged_lobatto.py','graded_transport.py','neutral_transport.py','frozen_charged_boundary.py',reference_name,boundary_name]
    result['source_sha256']={source:sha256((folder/source).read_bytes()).hexdigest() for source in names+reuse_sources}
    (folder/'FROZEN_CHARGED_RECTANGLE_ATTEMPT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2),flush=True)
    return result['status']=='PASS'


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-directory')
    if not main(parser.parse_args().reuse_directory):raise SystemExit(1)
