# Define some useful functions for calculating intermediate results and parameters
from config import *
from math import pi
import cmath
import numpy as np

def capillary(S, mode = 0):
    # Evaluate the capillary pressure and its first derivative
    # Mode indicates capillary expression to use:
    # 0 - van Genuchten
    # 1 - Santos
    # Return [capillary pressure], [first derivative w.r.t. water saturation]

    if mode == 0:
        # Relation based on van Genuchten equation
        # mvG, nvG and alphavG are material dependent fitting parameters
        mvG = 0.5
        nvG = 2
        alphavG = 0.00005

        p = 1/alphavG*(S**(-1/mvG) - 1)**(1/nvG) # capillary pressure
        dpdS = -(1/alphavG*nvG*mvG) * (alphavG*p)**(nvG/(nvG - 1)) * S**((-1/mvG) - 1)
        return p, dpdS
    elif mode == 1:
        # Relation based on Santos' expression
        # Fitting parameters A, Sor, pcr
        A = 6.029158
        Sor = 0.519
        pcr = 0.0000026509E10

        So = 1-S
        p = pcr*np.exp(-A*Sor)*(np.exp(-A*So) - 1)
        dpdS = A*pcr*np.exp(-A*Sor)*np.exp(-A*So)
        return p, dpdS
    else:
        return 0

def permeability(S):
    # Evaluate relative permeability as a function of saturation
    # Measurement by Wyckoff and Botset and relation from van Genuchten
    # Return kf, kg

    # Matrix dependent permeability parameter
    # Values chosen to fit permeability curve with experiment
    m = 0.85

    kf = S**(1/2) * (1 - (1 - S**(1/m))**m)**2
    kg = (1 - S)**(1/3) * (1 - S**(1/m))**(2*m)
    return kf, kg

def partial_density(S, material_mode = 0):
    # Evaluate saturation dependent partial densities for fluids
    # Partial density defined as mass / bulk volume
    # Return [rho_matrix], [rho_water], [rho_air]

    rhoGR0 = material_param(material_mode)[1]
    # Bulk density is microscopic density weighted by 1 - porosity
    rhoS0 = rhoSR0*(1-n0)
    # Water is incompressible so rhoFR0 constant
    rhoF0 = rhoFR0*S*n0
    rhoG0 = rhoGR0*(1-S)*n0

    return rhoS0, rhoF0, rhoG0

def santos_param(S0, pc, dpcdS, material_mode = 0, compare_mode = 0):
    # Evaluate material parameters according to Santos et. al
    # Input parameters:
    # Saturation, capillary pressure, derivative w.r.t. saturation
    # Return Kc, B1, B2. M1, M2, M3

    # Match variables with those used by Albers
    # In Santos et. al, oil and water were considered instead of gas and water
    # Therefore o, w subscripts represent oil and water respectively
    # Theory is valid for any two phase (non-wetting and wetting) fluid
    SoBar = 1-S0
    SwBar = S0

    if compare_mode == 0:
        Kg, rhoGR0, piG = material_param(material_mode)
        phiBar = n0
        K_s = Ks
        K_w = Kf
        K_o = Kg
        K_m = K_s/(1+g*n0)

    # Override parameters for oil-water-sandstone
    # For comparing with Santos' table
    # In CGS units
    if compare_mode == 1:
        phiBar = 0.19
        K_s = 37.9E10
        K_w = 2.25E10
        K_o = 5.7E9
        # Adjust drained modulus to match Santos' examples
        # adjust = 4.27594
        adjust = 5.49764
        K_m = K_s/(1+g*n0)*adjust

    # Derivative w.r.t. oil saturation is negative that of water saturation
    dpcdSo = -dpcdS

    # Intermediate variables
    beta = pc/dpcdSo
    gamma = (1 + dpcdSo*SoBar*SwBar/K_w) / (1 + dpcdSo*SoBar*SwBar/K_o)
    alpha = (gamma - 1)*(SoBar + beta) + 1

    # First material parameter Kc*
    KfStar = (1/alpha)*((gamma*SoBar/K_o)+(SwBar/K_w))
    KfStar = 1/KfStar
    QStar = KfStar*(K_m - K_s)/(phiBar*(KfStar - K_s))
    KcStar = K_s*(K_m + QStar)/(K_s + QStar)

    # B parameters
    Theta = (1/K_s - 1/K_m + phiBar*(1/K_m - 1/KcStar))
    Theta = Theta/(alpha*(1/K_s - 1/K_m + phiBar*(1/K_m - 1/KfStar)))
    B1 = KcStar*Theta*((SoBar + beta)*gamma - beta)
    B2 = KcStar*SwBar*Theta

    # M parameters
    delta = 1/K_s - 1/K_m
    q = phiBar*(1/K_o + 1/(dpcdSo*SoBar*SwBar))
    chi = (K_m/(KcStar - K_m))*(B2*q + (SoBar + beta)*(1 - KcStar/K_s))
    r = (SoBar + beta)/K_s + chi/K_m
    M3 = -B2*(1/(K_m*delta) + r/q)
    M2 = B2*(r/q)
    M1 = -B1/(K_m*delta) - M3
    return KcStar, B1, B2, M1, M2, M3

def albers_param(S0, pc, dpcdS, material_mode=0):
    # Evaluate material parameters according to Albers' Three Component Model
    # Define bulk modulus bulkMod = lambda + 2/3mu from classical dynamics
    # Material parameters in Albers are related to the Santos parameters
    KcStar, B1, B2, M1, M2, M3 = santos_param(S0, pc, dpcdS, material_mode, 0)
    bulkMod = KcStar - 2*n0*(B1 + B2) + n0**2*(M1 + M2 + 2*M3)
    rhoF0kappaF = M2*n0**2
    rhoG0kappaG = M1*n0**2
    Qf = n0*(B2 - n0*(M2 + M3))
    Qg = n0*(B1 - n0*(M1 + M3))
    Qfg = M3*n0**2
    return bulkMod, rhoF0kappaF, rhoG0kappaG, Qf, Qg, Qfg

def derived_param(S0, material_mode=0):
    # Derive remaining parameters for wave analysis
    # Return [Lame constant], [partial densities], [compressibility], [resistance]
    piG = material_param(material_mode)[2]
    pc, dpcdS = capillary(S0, 1)
    bulkMod, rhoF0kappaF, rhoG0kappaG = albers_param(S0, pc, dpcdS, material_mode)[0:3]
    kf, kg = permeability(S0)
    rhoS0, rhoF0, rhoG0 = partial_density(S0, material_mode)
    # First Lame constant
    lambS = bulkMod - (2/3)*muS
    # Compressibility factor
    kappaF = rhoF0kappaF/rhoF0
    kappaG = rhoG0kappaG/rhoG0
    # Resistance parameters
    piFS = piF/kf
    piGS = piG/kg
    return lambS, rhoS0, rhoF0, rhoG0, kappaF, kappaG, piFS, piGS

def material_param(material_mode = 0):
    # Return material parameters for the non-wetting phase which can be substituted
    if material_mode == 0:
        # Non-wetting phase: air
        Kg = 1.01E5
        rhoGR0 = 1.2
        piG = 1.82E5
    if material_mode == 1:
        # Non-wetting phase: oil
        Kg = 5.7E8
        rhoGR0 = 700
        piG = 1E8
    if material_mode == 2:
        # Non-wetting phase: "gas"
        Kg = 2.2E7
        rhoGR0 = 100
        piG = 1.5E5
    return Kg, rhoGR0, piG