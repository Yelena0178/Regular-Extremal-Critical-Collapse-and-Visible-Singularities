import sys; sys.set_int_max_str_digits(0)
import json
from fractions import Fraction as F
from pathlib import Path
import high_precision, certificate
ROOT=Path(__file__).resolve().parent
d=json.load(open(ROOT/'floating_candidate.json'))
r=high_precision.rationalize(d)
json.dump(r,open(ROOT/'candidate_rational.json','w'),indent=2)
a=high_precision.audit(r)
json.dump(a,open(ROOT/'audit.json','w'),indent=2)
p=certificate.prepare(r)
c=certificate.bernstein(p['poly'],p['den'])
k=certificate.kcert(p)
out={'input':'candidate_rational.json','objective_exact':str(p['lam']),'objective':float(p['lam']),'linear_conditions':'exact','current':c,'K':k}
json.dump(out,open(ROOT/'certificate.json','w'),indent=2)
print('BUILD PASS')
print('lambda =',float(p['lam']))
print('K0 =',float(p['K0']))
print('current lower =',float(F(c['lower'])))
print('K compact lower =',float(F(k['compact_lower'])))
