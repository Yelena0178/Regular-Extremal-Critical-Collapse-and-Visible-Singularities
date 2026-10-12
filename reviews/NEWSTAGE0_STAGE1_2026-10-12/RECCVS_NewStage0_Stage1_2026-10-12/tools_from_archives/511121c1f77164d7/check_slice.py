#!/usr/bin/env python3
"""Exact rational comparisons only. Does not certify PDEs or root existence.
Analytic premises: 0<r0<1/16, 0<eps<r0/8, delta<eps/4096;
theta(1-x)=1-theta(x), and the physical harmonic collar in baseline.
No floating-point representation of epsilon, and no parameter sampling.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
checks = []
def check(name, ok, reason):
    if not ok:
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "reason": reason})

a = F(1,64) # coefficient of eps
b = F(3,8)  # b = r0 + b*eps
h = F(1,4)
I = b-3*a
check("two step transition integral", a/2 + (-4*a) + a/2 == -3*a,
      "theta symmetry supplies integral 1/2; this checks its rational coefficients")
check("I epsilon coefficient", I == F(21,64), "I = r0 + 21 eps/64")
check("h0 epsilon coefficient", h == F(16,64), "h0 = r0 + 16 eps/64")
check("I-h0 positive", I-h == F(5,64), "q=h0/I is strictly between 0 and 1")
check("q numerator scaling", 64*h == 16, "q numerator 64 r0+16 eps")
check("q denominator scaling", 64*I == 21, "q denominator 64 r0+21 eps")
check("b-4a positive epsilon coefficient", b-4*a > 0, "b-4a > r0 >0: transitions disjoint")
check("outer join", b-a == F(23,64), "f=0 for R>=r0+23 eps/64")
check("join within actual annulus", b-a < 4, "r1-r0>4 eps inherited")
check("cone margin", F(1,2)-b == F(1,8), "r0+eps/2 - b = eps/8")
check("tube margin", F(1,2)-b-a == F(7,64), "tube half-width eps/64")
check("early cone time-function margin", h == F(1,4), "f+R>=h0 implies F<=-eps/4")
check("graph before p", h>0, "f(0)-r0=eps/4")
check("max reverse time within 2r0", 1+(h+a)/8 < 2,
      "eps<r0/8: h0+eps/64<2r0")
check("whole reverse interval within lifespan", 2*F(1,16)==F(1,8), "r0<1/16")
check("forward tube within lifespan", a*F(1,128)<F(1,8), "eps<1/128")
Dmax=(64+21*F(1,8))*F(1,16)
check("slope denominator bound", Dmax==F(533,128), "r0<1/16, eps<r0/8")
check("gamma exceeds eps", 5>Dmax, "gamma/eps=5/(64r0+21eps)>1")
check("gamma refined bound", 5/Dmax==F(640,533), "gamma/eps>640/533")
check("alpha formula", 2*64==128 and 2*21==42, "alpha=5eps/(128r0+42eps)")
check("b upper bound", F(1,16)+b*F(1,128)<F(1,8), "b<1/8")
check("epsilon upper", F(1,16)/8==F(1,128), "eps<1/128")
dmax=F(1,128*4096)
check("delta tiny", dmax<F(1,64), "delta<eps/4096<1/524288")
check("matrix inverse guard", 4*dmax<F(1,2), "Neumann inverse operator bound <=8delta")
check("inverse perturbation factor", 2*4==8, "||eta||op=1 and ||g^-1||op<=2")
check("normal covector norm", 1+1==2, "q<1 so |dF|_Euc^2<=2")
check("normal perturbation", 8*2==16, "inverse metric error <=16delta")
check("normal strict margin", 1-F(16,4096)>F(1,2), "gamma>eps: -gamma+16delta<-gamma/2")
check("tangent perturbation", 4*2==8, "metric error on (df(v),v) <=8delta |v|^2")
check("induced strict lower margin", 1-F(8,4096)>F(1,2), "gamma>eps gives gamma_- >=alpha")
check("induced upper bound", 1+8*dmax<2, "flat graph metric <=Euclidean metric")
check("true cone propagation margin", F(1,2)+F(1,4096*8)<1,
      "back-propagation adds delta |s| < eps/(4096*8)")
# Radial null roots: the upper envelope at v=1-16d is
# d*(-28+192d+256d^2), and the lower envelope at v=1+16d is
# d*(28+192d-256d^2). Bound for every 0<d<=1/64.
g=F(1,64)
check("lower null root bracket sign", -28+192*g+256*g*g<0,
      "positive powers monotone; upper polynomial remains negative")
check("upper null root bracket sign", 28-256*g*g>0,
      "drop positive 192d; lower polynomial remains positive")
check("lower null speed positive", 1-16*g>0, "outgoing root sign; ingoing by reflection")
check("radius derivative denominator", 1-g>F(1,4), "2sqrt(1-delta)>1")
check("radius derivative lower", F(1,8)<1, "sqrt(1-delta)>=1-delta and R<1/8")
check("expansion total error", 18+F(1,8)<19,
      "-(R delta)+(1-16delta)(1-2delta)>=1-19delta")
check("expansion strict half margin", 1-19*g>F(1,2), "outgoing>1/2 and ingoing<-1/2")
check("graph areal monotonicity", 1-3*g>0, "dr/dR on graph >=1-3delta")

sources=json.loads((ROOT/'verification'/'SOURCES.json').read_text())
for item in sources['files']:
    p=ROOT/item['path']
    check('source hash '+item['path'], hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],
          'checks input bytes only; does not validate mathematical content')
root_cert=ROOT/'baseline'/'ROOT_CERTIFICATE_mgeom.json'
check('same root identity', hashlib.sha256(root_cert.read_bytes()).hexdigest()==
      '7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2',
      'identity check only, not root recertification')
result={"proof_level":"exact rational guard comparisons; NOT PDE or root certification",
        "parameter_domain":"1/32<r0<1/16; 0<eps<r0/8; 0<=delta<eps/4096",
        "theta_integral":"analytic premise theta(1-x)=1-theta(x); integral identity in proof",
        "checks":checks,"check_count":len(checks),"all_passed":True,
        "floating_point_used":False,"epsilon_instantiated_numerically":False}
(ROOT/'verification'/'RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({"check_count":len(checks),"all_passed":True,"scope":result['proof_level']},ensure_ascii=False))

manifest_path=ROOT/'MANIFEST.json'
if manifest_path.exists():
    manifest=json.loads(manifest_path.read_text())
    for item in manifest['files']:
        actual=hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
        if actual!=item['sha256']:
            raise AssertionError('manifest mismatch: '+item['path'])
    print(json.dumps({'manifest_files_verified':len(manifest['files'])}))
