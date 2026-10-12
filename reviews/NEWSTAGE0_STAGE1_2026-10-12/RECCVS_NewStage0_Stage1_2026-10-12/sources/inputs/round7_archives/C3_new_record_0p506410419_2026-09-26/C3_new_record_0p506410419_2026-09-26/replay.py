import sys; sys.set_int_max_str_digits(0)
import json
from fractions import Fraction as F
from pathlib import Path
from certificate import prepare,bernstein,kcert
ROOT=Path(__file__).resolve().parent
r=json.load(open(ROOT/'candidate_rational.json'))
d=prepare(r)
assert d['lam'] < F(506411,1000000)
assert d['K0'] > 0 and d['e'][0] > 0 and d['c'][0] > 0
c=bernstein(d['poly'],d['den'])
k=kcert(d)
print('PRIMARY REPLAY PASS')
print('lambda =', float(d['lam']))
print('current lower =', float(F(c['lower'])))
print('K compact lower =', float(F(k['compact_lower'])))
