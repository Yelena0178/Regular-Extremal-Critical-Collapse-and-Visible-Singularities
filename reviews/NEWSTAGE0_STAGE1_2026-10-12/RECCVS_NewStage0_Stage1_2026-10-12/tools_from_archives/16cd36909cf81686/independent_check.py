"""Independent Frobenius reconstruction and exact certificate re-computation.

No finite 17-dimensional root is certified by this script.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import json
import math
import tempfile
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r01_exact as ref

Z=(F(0),F(0));O=(F(1),F(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
    d=b[0]*b[0]+b[1]*b[1];assert d
    return mul(a,(b[0]/d,-b[1]/d))
def scale(a,t):return (a[0]*t,a[1]*t)

def frobenius(j,p,mu):
    nu=(F(0),mu);coeff=[O]
    for ell in range(j):
        factor=add((F(ell*(ell+1)),F(0)),scale(nu,F(-(2*ell+1))))
        coeff.append(scale(mul(coeff[-1],factor),F(1,(ell+1)*(p+ell+1))))
    total=Z
    for ell in range(1,j+1):
        total=add(total,scale(coeff[ell],F((-1)**(j-ell)*math.comb(j-1,ell-1))))
    return scale(total,F(math.factorial(j),4**j))

def reconstruct_row(j,mu):
    a=[[(F(1,p+s),F(0)) for s in range(1,j+1)]+[frobenius(j,p,mu)] for p in range(1,j+1)]
    for col in range(j):
        pivot=next(i for i in range(col,j) if a[i][col]!=Z)
        a[col],a[pivot]=a[pivot],a[col]
        v=a[col][col];a[col]=[div(x,v) for x in a[col]]
        for i in range(j):
            if i==col:continue
            factor=a[i][col]
            a[i]=[add(x,neg(mul(factor,y))) for x,y in zip(a[i],a[col])]
    row=[a[i][-1] for i in range(j)]+[Z]*(8-j)
    for p in range(j+1,j+6):
        result=Z
        for s in range(1,j+1):result=add(result,scale(row[s-1],F(1,p+s)))
        assert result==frobenius(j,p,mu)
    return row

def decoded_matrix(value):return [[(F(v[0]),F(v[1])) for v in row] for row in value]
def read_interval(value):return (F(int(value['lo_hex'],16),2**value['binary_scale']),F(int(value['hi_hex'],16),2**value['binary_scale']))

def main(source,certificates,result_path):
    rows=[reconstruct_row(j,F(3,5)) for j in range(1,9)]
    summary=[]
    with tempfile.TemporaryDirectory() as t:
        for index,path in enumerate(certificates):
            saved=json.loads(path.read_text());mexp=saved['parameters']['m']['exponent']
            assert decoded_matrix(saved['leading_matrix']['T_mu'])==rows
            dst=Path(t)/f'check{index}.json'
            ref.calculate(source,dst,mexp)
            assert json.loads(dst.read_text())==saved
            for part in ['leading_17d','finite_scalar','finite_coupling_family']:
                item=saved[part]
                Y=F(item['scaled_Y']);q=F(item['scaled_q'])
                assert Y+q<F(1,4)
                assert q<F(1,8)
                assert Y<F(2)**(-44 if part=='finite_coupling_family' else -400)
            for part,key,power in [('finite_scalar','residual_at_center',-4302),('finite_coupling_family','uniform_residual_at_common_kappa_center',-3946)]:
                a,b=read_interval(saved[part][key])
                assert max(abs(a),abs(b))<=F(2)**power
            a,b=read_interval(saved['finite_coupling_family']['uniform_kappa_derivative'])
            assert F(-23,100)<=a<=b<=F(-11,50)
            assert F(saved['leading_matrix']['inverse_real_infinity_norm'])<64
            assert F(saved['leading_matrix']['derivative_real_norm_upper'])<128
            full=saved['full_finite_17d']
            assert full['finite_transverse_residuals'] is None
            assert full['finite_transverse_jacobian'] is None
            summary.append(dict(m_exponent=mexp,limit_inclusion_passes=True,finite_coupling_family_inclusion_passes=True,full_finite_root_certified=False,full_check_status='INSUFFICIENT_FINITE_TRANSVERSE_ENCLOSURES'))
        # Separate 12288-bit recomputation: enclosed intervals must refine the 8192-bit certificate.
        saved=json.loads(certificates[0].read_text())
        ref.P=12288;ref.S=1<<ref.P
        dst=Path(t)/'higher_precision.json'
        ref.calculate(source,dst,saved['parameters']['m']['exponent'])
        finer=json.loads(dst.read_text())
        assert finer['parameter_box']['kappa_center']==saved['parameter_box']['kappa_center']
        for part,key in [('finite_scalar','residual_at_center'),('finite_scalar','derivative_on_scalar_box'),('finite_coupling_family','uniform_residual_at_common_kappa_center'),('finite_coupling_family','uniform_kappa_derivative')]:
            old=read_interval(saved[part][key]);new=read_interval(finer[part][key])
            assert old[0]<=new[0]<=new[1]<=old[1]
    result=dict(status='PARTIAL_CHECKS_PASS_FULL_R01_NOT_CERTIFIED',
        independent_frobenius_rows_match=True,exact_recomputation_matches=True,
        higher_precision_intervals_refine_original=True,certificates=summary,
        no_assumption_that_missing_finite_residuals_are_zero=True)
    result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    if len(sys.argv)!=5:raise SystemExit('usage: independent_check.py profile.json cert_m12000.json cert_mgeom.json check_results.json')
    main(Path(sys.argv[1]),[Path(sys.argv[2]),Path(sys.argv[3])],Path(sys.argv[4]))
