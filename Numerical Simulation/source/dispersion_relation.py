# Define dispersion relations for the transverse and longitudinal wave cases
from config import muS
from soil_acoustic import derived_param, albers_param, capillary
from sympy import Symbol, I
from sympy.solvers import solveset
from sympy import im, nroots
import math

def transverse_disp(S0, w, material_mode):
    # Evaluate LHS of disp(k, w, S0) = 0
    # Output can be solved for k

    # Material modes:
    # 0 - Air
    # 1 - Oil
    # 2 - Gas

    param = derived_param(S0, material_mode)
    rhoS0, rhoF0, rhoG0 = param[1:4]
    piFS, piGS = param[6:8]

    k = Symbol('k')

    sum_rho = rhoS0 + rhoF0 + rhoG0
    prod_rho = rhoS0*rhoF0*rhoG0

    A = piFS*piGS*(sum_rho)/prod_rho
    B = (piFS + piGS)/rhoS0
    C = piFS/rhoF0 + piGS/rhoG0

    dispersion = w**2*(1 - (muS/rhoS0)*(k/w)**2) \
                 - A*(1 - (muS/sum_rho)*(k/w)**2) \
                 + I*w*(B + C)*(1 - C/(B + C)*(muS/rhoS0)*(k/w)**2)
    return dispersion

def longitudinal_disp(S0, w, material_mode):
    # Evaluate LHS of disp(k, w, S0) = 0
    # Output can be solved for k

    # Material modes:
    # 0 - Air
    # 1 - Oil
    # 2 - Gas

    k = Symbol('k')

    pc, dpcdS = capillary(S0, 1)
    bulkMod, rhoF0kappaF, rhoG0kappaG, Qf, Qg, Qfg = albers_param(S0, pc, dpcdS, material_mode)
    lambS, rhoS0, rhoF0, rhoG0, kappaF, kappaG, piFS, piGS = derived_param(S0, material_mode)

    sum_rho = rhoS0 + rhoF0 + rhoG0
    prod_rho = rhoS0*rhoF0*rhoG0

    A = (lambS + 2*muS)/rhoS0

    R1 = -(A + kappaF + kappaG)
    R2 = A*(kappaF + kappaG) + kappaF*kappaG \
         - (rhoS0*Qfg**2 + rhoF0*Qg**2 + rhoG0*Qf**2)/prod_rho
    R3 = A*(Qfg**2/(rhoF0*rhoG0) - kappaF*kappaG) + Qf**2*kappaG/(rhoS0*rhoF0) \
         + Qg**2*kappaF/(rhoS0*rhoG0) - 2*Qf*Qg*Qfg/prod_rho
    C0 = -piFS*piGS*sum_rho/prod_rho
    C1 = A*piFS*piGS/(rhoF0*rhoG0) \
         + (piFS*piGS/prod_rho)*(rhoF0kappaF + rhoG0kappaG + 2*(Qf + Qg + Qfg))

    I0 = (piFS + piGS)/rhoS0 + piFS/rhoF0 + piGS/rhoG0
    I1 = -(A*(kappaG/rhoG0 + kappaF/rhoF0) \
         + (piFS + piGS)*(kappaF + kappaG)/rhoS0 \
         + (piFS*kappaG + piGS*kappaF)/rhoF0 \
         + 2*piFS*Qf/(rhoS0*rhoF0) + 2*piGS*Qg/(rhoS0*rhoG0))
    I2 = A*(piFS*kappaG/rhoF0 + piGS*kappaF/rhoG0) \
         + (piFS + piGS)*kappaF*kappaG/rhoS0 - (piFS/prod_rho)*(Qg + Qfg)**2 \
         - (piGS/prod_rho)*(Qf + Qfg)**2 + 2*piGS*kappaF*Qg/(rhoS0*rhoG0) \
         + 2*piFS*kappaG*Qf/(rhoS0*rhoF0)

    dispersion = w**2*(1 + R1*(k/w)**2 + R2*(k/w)**4 + R3*(k/w)**6) \
                 + I*w*(I0 + I1*(k/w)**2 + I2*(k/w)**4) \
                 + C0 + C1*(k/w)**2
    return dispersion

def atten_coeff(disp, solve_mode = 0):
    k = Symbol('k')
    if solve_mode == 0:
        # Solve mode for transverse dispersion relation
        ksol = list(solveset(disp, k))[0]
    else:
        # Solve mode for longitudinal dispersion relation
        ksol = list(nroots(disp, maxsteps = 100))[2]
    alpha = abs(im(ksol))
    return alpha

def detect_range(atten_coeff, psource, pnoise):
    detectrange = -(1/(2*atten_coeff))*math.log(pnoise/psource)
    return detectrange