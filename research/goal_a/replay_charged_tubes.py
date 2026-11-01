"""Replay stored charged tubes and the recorded failure, without recomputing bounds."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from attempt_charged_rectangle import propagate,verify_sources
from charged_interval_kernel import V,NAMES
from verify_interval_transport_grid import arithmetic_checks


def main():
    folder=Path(__file__).resolve().parent
    report_name='FROZEN_CHARGED_RECTANGLE_ATTEMPT_2026-10-17.json'
    report=json.loads((folder/report_name).read_text());verify_sources(folder,report)
    reference='FROZEN_CHARGED_REFERENCE_N96_2026-10-17.json'
    boundary='FROZEN_CHARGED_BOUNDARY_CERTIFICATE_2026-10-17.json'
    ref=json.loads((folder/reference).read_text());b=json.loads((folder/boundary).read_text())
    file=folder/report['prepared_cache']
    if sha256(file.read_bytes()).hexdigest()!=report['prepared_cache_sha256']:raise ArithmeticError('prepared cache changed')
    cache=np.load(file);n=ref['n'];hu=V.rational(Q(ref['exact_U'])/n)
    incoming=np.zeros((n+1,8));incoming[:,0]=float(V.rational(Q(b['incoming_nu_error'])).hi)
    successes=[];failure=None
    for piece in range(3):
        low,high,delta=[cache[f'piece{piece}_{name}'] for name in ['low','high','delta']]
        exact=list(map(Q,ref['exact_meshes'][piece]));widths=[V.rational(c-a) for a,c in zip(exact,exact[1:])]
        hv=V(np.array([float(h.lo) for h in widths]),np.array([float(h.hi) for h in widths]))
        out=np.array([float(V.rational(Q(x)).hi) for x in b['pieces'][piece]['errors']])
        try:
            radii,result=propagate(low,high,delta,hu,hv,out,incoming,lambda *args:None)
            if not np.array_equal(radii,cache[f'piece{piece}_radii']):raise ArithmeticError('replayed tube changed')
            successes.append(dict(piece=piece,**result))
            incoming[1:]=radii[1:,-1,4:];incoming[0]=incoming[1]
        except ArithmeticError as error:
            if str(error)!=report.get('failure'):raise
            failure=dict(piece=piece,message=str(error))
            tb=error.__traceback__;loc=None
            while tb is not None:
                if tb.tb_frame.f_code.co_name=='propagate':loc=tb.tb_frame.f_locals
                tb=tb.tb_next
            if loc is not None and 'estimate' in loc:
                row,column=np.unravel_index(np.argmin(loc['estimate']),loc['estimate'].shape)
                Lh=loc['h'].hi[row,:,None]*loc['L'][row]
                failure.update(cell=[int(loc['ii'][row]),int(loc['jj'][row])],
                    negative_proposed_component=NAMES[column],
                    diagnostic_minimum_proposal=float(loc['estimate'][row,column]),
                    diagnostic_spectral_radius=float(max(abs(np.linalg.eigvals(Lh)))),
                    diagnostic_values_are_not_interval_proofs=True)
            break
    if successes!=report['completed_pieces']:raise ArithmeticError('piece completion changed')
    result=dict(status='PASS_REPLAY',arithmetic_checks=arithmetic_checks(),
                independently_replayed_pieces=successes,reproduced_failure=failure,
                complete_rectangle_certified=False,strict_trapping_certified=False,
                actual_smooth_seed_certified=False,goal_A_proved=False)
    names=['replay_charged_tubes.py','attempt_charged_rectangle.py','charged_interval_kernel.py',
           'verify_interval_transport_grid.py',report_name,report['prepared_cache'],reference,boundary]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'FROZEN_CHARGED_TUBE_REPLAY_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
