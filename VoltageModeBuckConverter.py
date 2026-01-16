"""
Buck Converter Calculations (from handwritten notes)

This script reproduces:
1) Power-stage (plant) key metrics: D, ΔIL, ΔVout(capacitive), f0, ω0, Q, Qmax
2) PWM modulator gain relationship: Vout/Vctrl = (Vin/Vramp) * H(s)
3) Type-III compensation component calculations for:
   - Low phase margin design (~5°)
   - High phase margin design (~60°)

Units:
- L in H, C in F, R in ohms, f in Hz, ω in rad/s
"""

import math

# -----------------------------
# Helpers
# -----------------------------
def rad(f_hz: float) -> float:
    """Hz -> rad/s"""
    return 2 * math.pi * f_hz

def hz(w_rad: float) -> float:
    """rad/s -> Hz"""
    return w_rad / (2 * math.pi)

def pretty_eng(x: float, unit: str = "") -> str:
    """Simple engineering format (no external libs)."""
    prefixes = [
        (1e-12, "p"), (1e-9, "n"), (1e-6, "u"), (1e-3, "m"),
        (1, ""), (1e3, "k"), (1e6, "M"), (1e9, "G")
    ]
    ax = abs(x)
    if ax == 0:
        return f"0 {unit}".strip()
    # choose closest prefix
    best = None
    for scale, p in prefixes:
        if ax >= scale:
            best = (scale, p)
    scale, p = best if best else (1e-12, "p")
    return f"{x/scale:.4g} {p}{unit}".strip()

# -----------------------------
# 1) GIVEN DESIGN SPECS (from notes)
# -----------------------------
Vin   = 3.3
Vout  = 1.5
Vref  = 1.2
Vramp = 1.0
Fsw   = 1.5e6

L     = 2.7e-6
C     = 10e-6
Rloss = 10e-3
Resr  = 10e-3

Iout_max = 1.0
Rload = Vout / Iout_max  # from notes

# -----------------------------
# 2) POWER STAGE CALCULATIONS (from notes)
# -----------------------------
D = Vout / Vin
Tsw = 1 / Fsw

# Inductor ripple (from your report/notes):
# ΔIL = Vin * (1 - D) * D / L * Tsw
dIL = Vin * (1 - D) * D / L * Tsw

# Capacitive ripple approximation (ignores ESR ripple component):
# ΔVout(cap) = ΔIL / (8 * C * Fsw)
dVout_cap = dIL / (8 * C * Fsw)

# LC resonant frequency (ideal):
f0_ideal = 1 / (2 * math.pi * math.sqrt(L * C))
w0_ideal = rad(f0_ideal)

# In your handwritten notes you used an ESR/Rload correction in ω0:
# ω0 ≈ 1 / sqrt(L*C*(1 + Resr/Rload))
w0_corr = 1 / math.sqrt(L * C * (1 + Resr / Rload))
f0_corr = hz(w0_corr)

# Q (from your handwritten derivation):
# Q = sqrt(Rload * L * C * (Rload + Resr)) / ( L + C*Rload*(Rloss + Resr) )
Q = math.sqrt(Rload * L * C * (Rload + Resr)) / (L + C * Rload * (Rloss + Resr))

# Qmax (from your handwritten notes):
# Qmax = sqrt(L/C) / (Rloss + Resr)
Qmax = math.sqrt(L / C) / (Rloss + Resr)

# Plant + PWM modulator gain relation (from your notes):
# Vctrl = d * Vramp  =>  Vout/Vctrl = (Vin/Vramp) * H(s)
Gpwm = 1 / Vramp
gain_scale_vout_over_vctrl = Vin / Vramp  # multiplies H(s)

print("\n" + "=" * 72)
print("POWER STAGE (PLANT) + PWM RELATIONS")
print("=" * 72)
print(f"D = Vout/Vin = {D:.6f}")
print(f"Rload = Vout/Iout_max = {Rload:.4f} ohm\n")

print("Ripple targets (typical design rule):")
print(f"  Target ΔIL ≈ 0.2 * Iout_max = {0.2*Iout_max:.3f} A")
print(f"  Computed ΔIL = {pretty_eng(dIL, 'A')}")
print(f"  Computed ΔVout(cap) = {pretty_eng(dVout_cap, 'V')} (capacitive-only)\n")

print("Resonant frequency:")
print(f"  f0 ideal = {pretty_eng(f0_ideal, 'Hz')}  (1/(2π√(LC)))")
print(f"  f0 corrected = {pretty_eng(f0_corr, 'Hz')}  (includes 1+Resr/Rload term)\n")

print("Quality factor:")
print(f"  Q (notes formula) = {Q:.4f}")
print(f"  Qmax (notes formula) = {Qmax:.4f}\n")

print("PWM scaling:")
print(f"  PWM gain Gpwm = 1/Vramp = {Gpwm:.3f} 1/V")
print(f"  Vout/Vctrl = (Vin/Vramp)*H(s) = {gain_scale_vout_over_vctrl:.3f} * H(s)")

# -----------------------------
# 3) TYPE-III COMPENSATION (LOW PM ~ 5°)
# -----------------------------
def type3_low_pm(Fsw: float, target_fc: float, Vout: float, Vref: float,
                 k1: float, k2: float, R1: float, C2: float):
    """
    Implements the same relationships you used in the notes for the LOW-PM case:
      wz1 = wc/k1
      wz2 = wc/k2
      wp1 = k1^2 * wz1
      wp2 = k2^2 * wz2
      R2 = 4 R1   (from Vout/Vref = 1 + R1/R2 => R1/R2 = 0.25)
      Ci = (k1^2 - 1) C2
      Rp = k1 / (Ci * wc)
      Rd = ((5 - 4k2^2)/(5(k2^2 - 1))) * R1     (from your derivation)
      Cd = 1 / ((4*Rd + R2) * wp2)              (matches your expression)
      gm = 7 * wc * k1 * Vout * C2 / (k2 * Vref)  (matches your computed 86.47 uS)
    """
    wc = rad(target_fc)
    wz1 = wc / k1
    wz2 = wc / k2
    wp1 = (k1**2) * wz1
    wp2 = (k2**2) * wz2

    R2 = 4 * R1
    Ci = (k1**2 - 1) * C2
    Rp = k1 / (Ci * wc)

    Rd = ((5 - 4*(k2**2)) / (5*(k2**2 - 1))) * R1
    Cd = 1 / ((4*Rd + R2) * wp2)

    gm = 7 * wc * k1 * Vout * C2 / (k2 * Vref)

    return {
        "fc": target_fc, "wc": wc,
        "wz1": wz1, "wz2": wz2, "wp1": wp1, "wp2": wp2,
        "R1": R1, "R2": R2, "C2": C2, "Ci": Ci, "Rp": Rp, "Rd": Rd, "Cd": Cd, "gm": gm
    }

# Low-PM numbers from your notes/report
fc_target = Fsw / 10
low = type3_low_pm(
    Fsw=Fsw, target_fc=fc_target, Vout=Vout, Vref=Vref,
    k1=11.43, k2=1.09,
    R1=25e3,
    C2=1e-12
)

print("\n" + "=" * 72)
print("TYPE-III COMPENSATION (LOW PHASE MARGIN ~ 5°)")
print("=" * 72)
print(f"Target fc = {pretty_eng(low['fc'], 'Hz')}  (Fsw/10)")
print(f"wz1 = wc/k1 = {pretty_eng(low['wz1'], 'rad/s')}  -> fz1 = {pretty_eng(hz(low['wz1']), 'Hz')}")
print(f"wz2 = wc/k2 = {pretty_eng(low['wz2'], 'rad/s')}  -> fz2 = {pretty_eng(hz(low['wz2']), 'Hz')}")
print(f"wp1 = k1^2*wz1 = {pretty_eng(low['wp1'], 'rad/s')} -> fp1 = {pretty_eng(hz(low['wp1']), 'Hz')}")
print(f"wp2 = k2^2*wz2 = {pretty_eng(low['wp2'], 'rad/s')} -> fp2 = {pretty_eng(hz(low['wp2']), 'Hz')}\n")

print("Component values:")
print(f"R1 = {pretty_eng(low['R1'], 'ohm')}")
print(f"R2 = {pretty_eng(low['R2'], 'ohm')}  (R2 = 4*R1)")
print(f"C2 = {pretty_eng(low['C2'], 'F')}")
print(f"Ci = (k1^2-1)*C2 = {pretty_eng(low['Ci'], 'F')}")
print(f"Rp = k1/(Ci*wc) = {pretty_eng(low['Rp'], 'ohm')}")
print(f"Rd = ((5-4k2^2)/(5(k2^2-1)))*R1 = {pretty_eng(low['Rd'], 'ohm')}")
print(f"Cd = 1/((4Rd+R2)*wp2) = {pretty_eng(low['Cd'], 'F')}")
print(f"gm = 7*wc*k1*Vout*C2/(k2*Vref) = {pretty_eng(low['gm'], 'S')}")

# -----------------------------
# 4) TYPE-III COMPENSATION (HIGH PM ~ 60°) - follows your handwritten flow
# -----------------------------
def type3_high_pm(target_fc: float, k1: float, k2: float, R1: float,
                  C2: float, Ci: float, Rp: float, Cd: float, Rd: float,
                  gm1: float):
    """
    High-PM sheet uses:
      wz1 = wc/k1, wz2 = wc/k2
      wp1 = k1^2*wz1, wp2 = k2^2*wz2
      Ci = (k1^2-1)*C2, Rp = k1/(Ci*wc)
      Rd = 1/(k2*wc*Cd)
      k2^2 = 1 + gm2/gm1 + gm2*R1/(gm1*R2), with R2=4R1
        => gm2 = (4/5)*(k2^2 - 1)*gm1
    """
    wc = rad(target_fc)
    R2 = 4 * R1

    wz1 = wc / k1
    wz2 = wc / k2
    wp1 = (k1**2) * wz1
    wp2 = (k2**2) * wz2

    gm2 = (4/5) * (k2**2 - 1) * gm1

    return {
        "fc": target_fc, "wc": wc,
        "wz1": wz1, "wz2": wz2, "wp1": wp1, "wp2": wp2,
        "R1": R1, "R2": R2, "C2": C2, "Ci": Ci, "Rp": Rp, "Cd": Cd, "Rd": Rd,
        "gm1": gm1, "gm2": gm2
    }

# Use the numeric values you computed in the high-PM sheet/report
high = type3_high_pm(
    target_fc=fc_target,
    k1=11.43, k2=3.73,
    R1=25e3,
    C2=395.7e-15,
    Ci=51.3e-12,
    Rp=236.39e3,
    Cd=10e-12,
    Rd=28.45e3,
    gm1=10e-6
)

print("\n" + "=" * 72)
print("TYPE-III COMPENSATION (HIGH PHASE MARGIN ~ 60°)")
print("=" * 72)
print(f"Target fc = {pretty_eng(high['fc'], 'Hz')}  (Fsw/10)")
print(f"wz1 = wc/k1 = {pretty_eng(high['wz1'], 'rad/s')}  -> fz1 = {pretty_eng(hz(high['wz1']), 'Hz')}")
print(f"wz2 = wc/k2 = {pretty_eng(high['wz2'], 'rad/s')}  -> fz2 = {pretty_eng(hz(high['wz2']), 'Hz')}")
print(f"wp1 = k1^2*wz1 = {pretty_eng(high['wp1'], 'rad/s')} -> fp1 = {pretty_eng(hz(high['wp1']), 'Hz')}")
print(f"wp2 = k2^2*wz2 = {pretty_eng(high['wp2'], 'rad/s')} -> fp2 = {pretty_eng(hz(high['wp2']), 'Hz')}\n")

print("Component values (from your computed design):")
print(f"R1 = {pretty_eng(high['R1'], 'ohm')}")
print(f"R2 = {pretty_eng(high['R2'], 'ohm')}  (R2 = 4*R1)")
print(f"C2 = {pretty_eng(high['C2'], 'F')}")
print(f"Ci = {pretty_eng(high['Ci'], 'F')}")
print(f"Rp = {pretty_eng(high['Rp'], 'ohm')}")
print(f"Cd = {pretty_eng(high['Cd'], 'F')}")
print(f"Rd = {pretty_eng(high['Rd'], 'ohm')}")
print(f"gm1 = {pretty_eng(high['gm1'], 'S')}")
print(f"gm2 = (4/5)*(k2^2-1)*gm1 = {pretty_eng(high['gm2'], 'S')}")

print("\nDone.")
