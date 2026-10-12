"""Exact preparatory checks for R01; never certifies the missing finite jets.

Only Python integer/Fraction arithmetic is used. All transcendental bounds
come from explicit positive-term series with a remainder interval.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import sys

P = 8192
S = 1 << P

def ceildiv(a,b): return -((-a)//b)

class I:
    """Closed dyadic interval [lo,hi]/2**P with exact outward rounding."""
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=int(lo);self.hi=int(lo if hi is None else hi)
        assert self.lo<=self.hi
    @classmethod
    def of(cls,v):
        if isinstance(v,I):return v
        v=F(v)
        return cls((v.numerator*S)//v.denominator,ceildiv(v.numerator*S,v.denominator))
    def __add__(self,v):
        v=I.of(v);return I(self.lo+v.lo,self.hi+v.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,v):return self+-I.of(v)
    def __rsub__(self,v):return I.of(v)+-self
    def __mul__(self,v):
        v=I.of(v);w=[a*b for a in (self.lo,self.hi) for b in (v.lo,v.hi)]
        return I(min(w)//S,ceildiv(max(w),S))
    __rmul__=__mul__
    def reciprocal(self):
        assert not self.lo<=0<=self.hi
        return I((S*S)//self.hi,ceildiv(S*S,self.lo))
    def __truediv__(self,v):return self*I.of(v).reciprocal()
    def __rtruediv__(self,v):return I.of(v)/self
    def abs_upper(self):return F(max(abs(self.lo),abs(self.hi)),S)
    def encoded(self):return dict(lo_hex=hex(self.lo),hi_hex=hex(self.hi),binary_scale=P)
    def display(self):return [float(F(self.lo,S)),float(F(self.hi,S))]

def pow2_interval(exponent):
    if exponent+P>=0:return I(1<<(exponent+P))
    return I(0,1)

def log_atanh(z):
    """2*sum z^(2k+1)/(2k+1), N=P, tail bounded geometrically."""
    assert 0<=z.lo<=z.hi<S
    zz=z*z;power=z;total=I(0)
    for k in range(P):
        total+=power/F(2*k+1)
        power*=zz
    tail=2*power/(F(2*P+1)*(1-zz))
    return 2*total+I(0,tail.hi)

def log_interval_y_1_2(y):
    assert S<=y.lo<=y.hi<=2*S
    return log_atanh((y-1)/(y+1))

def exp_positive(x):
    assert 0<=x.lo<=x.hi<4*S
    term=I.of(1);total=term
    for n in range(1,P+1):
        term=term*x/F(n);total+=term
    nxt=term*x/F(P+1)
    tail=nxt/(1-x/F(P+2))
    return total+I(0,tail.hi)

def exp_negative(x):
    assert x.hi<=0
    return exp_positive(-x).reciprocal()

def ca(a,b):return (a[0]+b[0],a[1]+b[1])
def cn(a):return (-a[0],-a[1])
def cm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def ci(a):
    d=a[0]*a[0]+a[1]*a[1];assert d
    return (a[0]/d,-a[1]/d)
def cs(a,s):return (a[0]*s,a[1]*s)
ZERO=(F(0),F(0))
ONE=(F(1),F(0))

def addpoly(a,b):
    out=a.copy()
    for k,v in b.items():out[k]=ca(out.get(k,ZERO),v)
    return {k:v for k,v in out.items() if v!=ZERO}

def scalepoly(a,v,shift=(0,0,0)):
    return {tuple(k[j]+shift[j] for j in range(3)):cm(c,v) for k,c in a.items() if cm(c,v)!=ZERO}

def integral(a):
    """Integrate first argument from s to t; keys (t power,s power,e power)."""
    out={}
    for (t,s,e),c in a.items():
        v=cs(c,F(1,t+1))
        out=addpoly(out,{(t+1,s,e):v,(0,s+t+1,e):cn(v)})
    return out

def kernels(kmax):
    ks=[{}, {(0,0,1):(F(0),F(-1,4))}]
    for n in range(1,kmax):
        kn=ks[n];prev=ks[n-1]
        val=scalepoly(kn,(F(-n,2),F(0)),(1,0,0))
        val=addpoly(val,scalepoly(prev,(F(-n*(n-1),16),F(0)),(2,0,0)))
        integ=integral(kn)
        val=addpoly(val,scalepoly(integ,(F(n,2),F(0))))
        val=addpoly(val,scalepoly(integ,(F(0),F(-(2*n+1),4)),(0,0,1)))
        integprev=integral(scalepoly(prev,ONE,(1,0,0)))
        val=addpoly(val,scalepoly(integprev,(F(n*(n-1),8),F(0))))
        val=addpoly(val,scalepoly(integprev,(F(0),F(-n*(n-1),8)),(0,0,1)))
        ks.append(val)
    return ks

def matrix_and_inverse(mu):
    ks=kernels(8);mat=[];derivative_rows=[]
    for j in range(1,9):
        row=[ZERO for _ in range(8)];drow=[F(0) for _ in range(8)]
        for (_,sp,ep),v in ks[j].items():
            row[sp]=ca(row[sp],cs(v,mu**ep))
            if ep:drow[sp]+=(abs(v[0])+abs(v[1]))*ep*F(3,4)**(ep-1)
        mat.append(row);derivative_rows.append(sum(drow))
    inv=[[ZERO for _ in range(8)] for _ in range(8)]
    for col in range(8):
        for row in range(8):
            numerator=ONE if row==col else ZERO
            for j in range(row):numerator=ca(numerator,cn(cm(mat[row][j],inv[j][col])))
            inv[row][col]=cm(numerator,ci(mat[row][row]))
    for row in range(8):
        for col in range(8):
            val=ZERO
            for j in range(8):val=ca(val,cm(mat[row][j],inv[j][col]))
            assert val==(ONE if row==col else ZERO)
    for j in range(1,9):
        d=(F(0),-mu/F(4**j*math.factorial(j-1)))
        for ell in range(1,j):d=cm(d,(F(-ell*(ell+1)),(2*ell+1)*mu))
        assert mat[j-1][j-1]==d
    norm=max(sum(abs(z[0])+abs(z[1]) for z in r) for r in inv)
    derivative=max(derivative_rows)
    return mat,inv,norm,derivative

def ceil_log2_fraction(v):
    assert v>0
    n=v.numerator.bit_length()-v.denominator.bit_length()
    if v>F(2)**n:n+=1
    return n

def serialize_complex_matrix(mat):
    return [[[str(v[0]),str(v[1])] for v in row] for row in mat]

def calculate(source, output, m_exponent=12000):
    data=json.loads(source.read_text());mu=F(3,5)
    lam=F(data['lambda_exact'])
    assert lam==2*F(data['E_total'])/F(data['C_total'])
    assert F(1,2)<lam<F(51,100)
    assert data['moments_exact']==[['0','0']]*8
    T=2**20+2;MEXP=m_exponent
    mat,inv,M,Dt=matrix_and_inverse(mu)
    Mpow=ceil_log2_fraction(M)
    # kappa_w=-log(1-lambda_w/mu)/2; reduce 8*(1-lambda_w/mu) to [1,2].
    a=1-lam/mu
    assert 1<=8*a<=2
    ln2=log_interval_y_1_2(I.of(2))
    ln8a=log_interval_y_1_2(I.of(8*a))
    kappa_raw=(3*ln2-ln8a)/2
    CENTER_BITS=4300
    center_integer=((kappa_raw.lo+kappa_raw.hi)//2)>>(P-CENTER_BITS)
    center=F(center_integer,1<<CENTER_BITS)
    hc=F(1,1<<4097);hk=F(1,1<<3900)
    point=I.of(center);box=I.of(center-hk)+I(0,I.of(2*hk).hi)
    assert F(box.lo,S)>F(7,8) and F(box.hi,S)<1
    def profile_range(eta_exp):
        eta=pow2_interval(eta_exp)
        eb=I.of(1)+I(-3*eta.hi,3*eta.hi)
        lb=I.of(lam)+I(-10*eta.hi,10*eta.hi)
        return eb,lb
    def coupling(eb,lb,k):
        exponential=exp_negative(-2*eb*k)
        denominator=1-exponential
        value=lb/denominator
        deriv=-2*eb*lb*exponential/(denominator*denominator)
        return value,deriv
    # Base profile and full prescribed L021 complex parameter ball.
    eb0,lb0=profile_range(-19000)
    eb,lb=profile_range(-3950)
    gpoint,_=coupling(eb0,lb0,point)
    gbox,dbox=coupling(eb,lb,box)
    assert F(gbox.lo,S)>F(1,2) and F(gbox.hi,S)<F(3,4)
    assert dbox.abs_upper()<1
    center_res=gpoint-mu
    dev=(gbox-mu).abs_upper()
    coupling_c_bound=F(1<<150)
    top_q=M*Dt*(dev+16*coupling_c_bound*hc+hk)
    scalar_q=(1+4*dbox).abs_upper()+16*4*coupling_c_bound*hc/hk
    q=max(top_q,scalar_q)
    leading_y=4*center_res.abs_upper()/hk
    assert leading_y+q<F(1,4)
    # Effective finite scalar estimates: e error <=2^6440/m; kappa derivative <=2^6460/m.
    b=1<<3201
    assert T<2**21 and MEXP>6470
    assert b+ b*b*T <2**6424
    assert b+2*b*b*T <2**6425
    assert 40*2**6424+5 <2**6440
    assert 100*2**6424+20*2**6425+65 <2**6450
    assert 2**6450+30*2**6440 <2**6460
    assert 2**149*2**6424+20*2**6425+2**150 <2**6600
    assert 2**6600+2**157*2**6440 <2**6620
    finite_value_error=pow2_interval(6440-MEXP)
    finite_deriv_error=pow2_interval(6460-MEXP)
    finite_res=center_res+I(-finite_value_error.hi,finite_value_error.hi)
    _,scalar_d=coupling(eb0,lb0,box)
    finite_d=scalar_d+I(-finite_deriv_error.hi,finite_deriv_error.hi)
    scalar_y=4*finite_res.abs_upper()/hk
    scalar_z=(1+4*finite_d).abs_upper()
    assert scalar_y+scalar_z<F(1,4)
    all_c_point,_=coupling(eb,lb,point)
    all_c_res=all_c_point-mu+I(-finite_value_error.hi,finite_value_error.hi)
    all_c_deriv=dbox+I(-finite_deriv_error.hi,finite_deriv_error.hi)
    assert all_c_deriv.hi<-(S//5)-1
    all_c_y=4*all_c_res.abs_upper()/hk
    all_c_z=(1+4*all_c_deriv).abs_upper()
    assert all_c_y+all_c_z<F(1,4)
    certificate=dict(
        status='PARTIAL_CERTIFICATES_ONLY_FULL_FINITE_17D_ROOT_NOT_CERTIFIED',
        model='D001; D=d+ieA; Av=0; original U gauge',
        precision=dict(binary_scale=P,log_series_terms=P,exp_series_terms=P),
        parameters=dict(K=8,T=T,mu='3/5',m=dict(kind='power_of_two',exponent=MEXP),delta='kappa/m',tau='T*kappa'),
        parameter_box=dict(
            c_order='Re c1, Im c1, ..., Re c8, Im c8',
            c_center='0',c_component_radius=dict(kind='power_of_two',exponent=-4097),
            kappa_center=dict(numerator_hex=hex(center_integer),denominator_power=CENTER_BITS),
            kappa_radius=dict(kind='power_of_two',exponent=-3900),
            raw_kappa_enclosure=kappa_raw.encoded(),
            kappa_center_display_only=float(center)),
        leading_matrix=dict(T_mu=serialize_complex_matrix(mat),T_mu_inverse=serialize_complex_matrix(inv),inverse_real_infinity_norm=str(M),inverse_norm_power_upper=Mpow,derivative_real_norm_upper=str(Dt)),
        leading_17d=dict(status='CERTIFIED_LIMIT_MAP_ONLY',preconditioner='diag(realify(T_mu_inverse), -4)',residual_at_center_scalar=center_res.encoded(),coupling_range=gbox.encoded(),coupling_derivative_kappa_range=dbox.encoded(),coupling_derivative_c_abs_upper='2^150',scaled_top_jacobian_radius=str(top_q),scaled_scalar_jacobian_radius=str(scalar_q),scaled_Y=str(leading_y),scaled_q=str(q),inclusion_Y_plus_q_upper='1/4'),
        finite_scalar=dict(status='CERTIFIED_SINGLE_COUPLING_EQUATION_AT_c_EQUALS_0',
            hypothesis='Explicit L021 profile bounds and scalar Riccati/charge definitions; full proof in REPORT.md',
            uniform_value_error=dict(kind='power_of_two',exponent=6440-MEXP),
            uniform_kappa_derivative_error=dict(kind='power_of_two',exponent=6460-MEXP),
            residual_at_center=finite_res.encoded(),
            derivative_on_scalar_box=finite_d.encoded(),
            scaled_Y=str(scalar_y),scaled_q=str(scalar_z),inclusion_Y_plus_q_upper='1/4',
            does_not_set_transverse_residuals_to_zero=True),
        finite_coupling_family=dict(status='CERTIFIED_SCALAR_COUPLING_ROOT_FOR_EACH_FIXED_c_IN_BOX',
            uniform_c_derivative_error=dict(kind='power_of_two',exponent=6620-MEXP),
            uniform_kappa_derivative_error=dict(kind='power_of_two',exponent=6460-MEXP),
            uniform_residual_at_common_kappa_center=all_c_res.encoded(),
            uniform_kappa_derivative=all_c_deriv.encoded(),
            derivative_kappa_negative_abs_lower='1/5',
            finite_c_derivative_abs_upper='2^151',
            eliminated_kappa_c_derivative_abs_upper='2^154',
            scaled_Y=str(all_c_y),scaled_q=str(all_c_z),inclusion_Y_plus_q_upper='1/4',
            warning='This gives kappa(c), NOT a root of the 16 transverse equations.'),
        full_finite_17d=dict(status='NOT_CERTIFIED_MISSING_FINITE_JET_ENCLOSURES',
            finite_transverse_residuals=None,finite_transverse_jacobian=None,
            sufficient_residual_C0_abs_upper=dict(kind='power_of_two',exponent=-(4100+Mpow)),
            sufficient_jacobian_difference_real_infinity_upper=dict(kind='power_of_two',exponent=-(200+Mpow)),
            warning='Targets are NOT computed enclosures. No finite 17-dimensional Newton/Krawczyk inclusion has passed.'),
    )
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(certificate,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=certificate['status'],kappa_display=float(center),inverse_norm_display=float(M),inverse_norm_power_upper=Mpow,T_derivative_norm_display=float(Dt),leading_y_display=float(leading_y),leading_q_display=float(q),scalar_y_display=float(scalar_y),scalar_q_display=float(scalar_z),finite_scalar_error_exponents=[6440-MEXP,6460-MEXP]),indent=2))

if __name__=='__main__':
    if len(sys.argv) not in (3,4):raise SystemExit('usage: r01_exact.py frozen_profile.json certificate.json [m_exponent]')
    calculate(Path(sys.argv[1]),Path(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)==4 else 12000)
