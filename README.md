# Voltage-Mode Buck Converter Calculations

This repository contains a Python script that reproduces analytical calculations for a high-frequency voltage-mode buck converter, including power-stage metrics, PWM gain, and Type-III compensation for two phase-margin targets.

---

## Project Overview

- Input voltage: Vin = 3.3 V  
- Output voltage: Vout = 1.5 V  
- Switching frequency: Fsw = 1.5 MHz  
- Inductor ripple target: ≈ 20% of maximum load current  
- Two compensation cases:
  - Low phase margin (~5°)
  - High phase margin (~60°)
- Target crossover frequency: Fsw / 10 ≈ 150 kHz  

The Python script serves as a calculation and documentation aid alongside circuit simulations or hardware prototypes.

---

## Power Stage and PWM Relations

- Duty cycle:  
  D = Vout / Vin = 0.454545

- Load resistance at maximum load:  
  Rload = Vout / Iout_max = 1.5000 ohm

### Ripple Targets

- Target inductor ripple:  
  ΔIL_target ≈ 0.2 × Iout_max = 0.200 A

- Computed inductor ripple:  
  ΔIL = 202 mA

- Output ripple (capacitor only):  
  ΔVout_cap = 1.684 mV

### LC Resonant Frequency

- Ideal resonance:  
  f0_ideal = 30.63 kHz

- Corrected resonance (including ESR):  
  f0_corr = 30.53 kHz

### Quality Factor

- Q = 2.6067  
- Qmax = 25.9808  

### PWM Scaling

- PWM gain:  
  Gpwm = 1 / Vramp = 1.000 1/V

- Small-signal relation:  
  Vout / Vctrl = (Vin / Vramp) × H(s) = 3.300 × H(s)

---

## Type-III Compensation — Low Phase Margin (~5°)

This configuration is marginally stable and mainly used for comparison.

### Component Values

- R1 = 25 kΩ  
- R2 = 100 kΩ  
- C2 = 1 pF  
- Ci = 129.6 pF  
- Rp = 93.54 kΩ  
- Rd = 6.582 kΩ  
- Cd = 7.706 pF  
- gm = 86.48 µS  

Unity gain occurs near 150 kHz with a phase margin of approximately 5–6°.

---

## Type-III Compensation — High Phase Margin (~60°)

This configuration provides robust stability and well-damped transient response.

### Component Values

- R1 = 25 kΩ  
- R2 = 100 kΩ  
- C2 = 0.3957 pF  
- Ci = 51.3 pF  
- Rp = 236.4 kΩ  
- Rd = 28.45 kΩ  
- Cd = 10 pF  
- gm1 = 10 µS  
- gm2 = 103.3 µS  

Unity-gain bandwidth is 150 kHz with a phase margin close to 60°.

---

## Repository Structure

- `VoltageModeBuckConverter.py`  
  Python script implementing all calculations.

- `README.md`  
  Project overview and computed results.

---

## How to Run

```bash
python VoltageModeBuckConverter.py
