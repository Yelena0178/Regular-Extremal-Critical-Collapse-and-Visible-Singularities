"""Exact conservative arithmetic for the sufficient bounds in L023.

These checks validate the analytical implication, not the presence of an
actual finite-amplitude root or the choice of its incoming cone.
"""
from fractions import Fraction as F
import json


def require(condition, message):
    if not condition: raise ValueError(message+'; NOT CERTIFIED')


omega=F(1,2); eps=F(1,2**10); d_power=F(1,2**15); e_width=F(1,16)
# g_{1/2}(d) < 9 d^(3/4); d<=2^-20.
first=26*eps+9*d_power
second=14*d_power
width1=9*e_width**2/(4*(1-eps)**2)
width2=45*e_width**2/(1-eps)**2
require(first<F(1,16),'first mass threshold failed')
require(second<F(1,16),'second mass threshold failed')
require(width1<omega/4,'first physical-width constraint failed')
require(width2<4*omega,'second physical-width constraint failed')
require(omega/4+2*eps<1,'strict trapping upgrade charge bound failed')
# exp(z)-1<=2z for z<=1/2, with z<=2^-22.
require(2*F(1,2**22)<F(1,2**20),'radius width bound failed')
T=2**20+2; m_exponent=2*T+7000
require(m_exponent>3246,'explicit geometry length: radius margin failed')
require(F(1,2**(m_exponent-6427))<F(1,100),'explicit radius Gronwall error failed')
require(F(48,2**m_exponent)<F(1,32),'explicit geometry length: charge margin failed')
require(m_exponent-(3204+2*T)==3796,'explicit physical-width exponent failed')
require(F(101,80)+F(1,100)<F(4,3),'left-radius integral bound failed')
require(F(11,4)**4<4**3,'left-radius exponential comparison failed')
print(json.dumps(dict(scope='L023_SUFFICIENT_IMPLICATION_NOT_A_FROZEN_SEED',
                      first_mass_threshold_upper=str(first),
                      second_mass_threshold_upper=str(second),
                      first_width_LHS_upper=str(width1),
                      second_width_LHS_upper=str(width2),
                      lower_actual_mass_ratio='1/2',
                      worst_mass_margin_lower=str(F(1,2)-max(first,second)),
                      fixed_period=T,
                      geometric_minimum_m_expression='2^'+str(m_exponent),
                      worst_physical_width_upper='2^-3796',
                      geometric_left_radius_lower='1/4',
                      finite_amplitude_root_certified=False,
                      strict_upgrade_Q_squared_over_r_squared_upper=str(omega/4+2*eps)),indent=2))
