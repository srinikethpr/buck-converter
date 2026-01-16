# Voltage-Mode Buck Converter Calculations

This repository contains a Python script that reproduces key analytical calculations for a high-frequency voltage-mode buck converter, including power-stage metrics, PWM modulator gain, and Type-III compensator design for two different phase-margin targets. [file:1][file:2]

---

## Project Overview

- Input voltage: $V_{in} = 3.3\ \text{V}$  
- Output voltage: $V_{out} = 1.5\ \text{V}$ [file:1]  
- Switching frequency: $F_{sw} = 1.5\ \text{MHz}$ with an inductor current ripple target of approximately 20% of the maximum load current [file:1][file:2]  
- Two Type-III compensation cases are evaluated:
  - **Low phase-margin design** (~5°)
  - **High phase-margin design** (~60°)  
  Both target a closed-loop crossover frequency near  
  $$
  F_{sw}/10 \approx 150\ \text{kHz}
  $$
  [file:1][file:2]

The Python script is intended as a calculation and documentation aid alongside circuit-level simulations or hardware prototypes. [file:2]

---

## Power Stage and PWM Relations

These values are computed from the design specifications and component choices. [file:2]

### Duty Cycle
$$
D = \frac{V_{out}}{V_{in}} = 0.454545
$$

### Load Resistance at Maximum Load
$$
R_{load} = \frac{V_{out}}{I_{out,\max}} = 1.5000\ \Omega
$$

---

### Ripple Targets (Typical Design Rule)

- Target inductor ripple current:
  $$
  \Delta I_L^{target} \approx 0.2 \cdot I_{out,\max} = 0.200\ \text{A}
  $$

- Computed inductor ripple:
  $$
  \Delta I_L = 202\ \text{mA}
  $$

- Computed output ripple (capacitive component only):
  $$
  \Delta V_{out,\text{cap}} = 1.684\ \text{mV}
  $$

---

### Resonant Frequency of the LC Filter

- Ideal LC resonance:
  $$
  f_0^{ideal} = 30.63\ \text{kHz}
  $$

- Corrected resonance including ESR effects:
  $$
  f_0^{corr} = 30.53\ \text{kHz}
  $$

---

### Quality Factor

- $$
  Q = 2.6067
  $$
- $$
  Q_{max} = 25.9808
  $$

---

### PWM Scaling

- PWM gain:
  $$
  G_{pwm} = \frac{1}{V_{ramp}} = 1.000\ \text{V}^{-1}
  $$

- Overall small-signal relation:
  $$
  \frac{V_{out}}{V_{ctrl}} = \frac{V_{in}}{V_{ramp}} \cdot H(s) = 3.300 \cdot H(s)
  $$

All expressions above are directly printed by the Python script using the selected values of  
$L$, $C$, $R_{loss}$, $R_{ESR}$, $V_{in}$, $V_{out}$, $V_{ramp}$, and $I_{out,\max}$. [file:2]

---

## Type-III Compensation — Low Phase Margin (~5°)

This case corresponds to a **marginally stable** design with low phase margin, primarily used for comparison and educational purposes. [file:1][file:2]

### Target Crossover Frequency
$$
f_c = 150\ \text{kHz} \quad (F_{sw}/10)
$$

---

### Zero Locations
$$
\omega_{z1} = \frac{\omega_c}{k_1} = 82.46\ \text{krad/s}
\quad\Rightarrow\quad
f_{z1} = 13.12\ \text{kHz}
$$

$$
\omega_{z2} = \frac{\omega_c}{k_2} = 864.7\ \text{krad/s}
\quad\Rightarrow\quad
f_{z2} = 137.6\ \text{kHz}
$$

---

### Pole Locations
$$
\omega_{p1} = k_1^2 \omega_{z1} = 10.77\ \text{Mrad/s}
\quad\Rightarrow\quad
f_{p1} = 1.714\ \text{MHz}
$$

$$
\omega_{p2} = k_2^2 \omega_{z2} = 1.027\ \text{Mrad/s}
\quad\Rightarrow\quad
f_{p2} = 163.5\ \text{kHz}
$$

---

### Component Values

$$
R_1 = 25\ \text{k}\Omega
$$

$$
R_2 = 100\ \text{k}\Omega \quad (R_2 = 4R_1)
$$

$$
C_2 = 1\ \text{pF}
$$

$$
C_i = (k_1^2 - 1) C_2 = 129.6\ \text{pF}
$$

$$
R_p = \frac{k_1}{C_i \omega_c} = 93.54\ \text{k}\Omega
$$

$$
R_d = \frac{5 - 4k_2^2}{5(k_2^2 - 1)} R_1 = 6.582\ \text{k}\Omega
$$

$$
C_d = \frac{1}{(4R_d + R_2)\omega_{p2}} = 7.706\ \text{pF}
$$

### Transconductance
$$
g_m = \frac{7 \omega_c k_1 V_{out} C_2}{k_2 V_{ref}} = 86.48\ \mu\text{S}
$$

The resulting closed-loop system shows unity gain at 150 kHz and a phase margin close to 5–6°, as confirmed by AC simulations in the associated design report. [file:1][file:2]

---

## Type-III Compensation — High Phase Margin (~60°)

This case corresponds to a **robust** design with significantly higher phase margin and well-damped transient behavior. [file:1][file:2]

### Target Crossover Frequency
$$
f_c = 150\ \text{kHz} \quad (F_{sw}/10)
$$

---

### Zero Locations
$$
\omega_{z1} = \frac{\omega_c}{k_1} = 82.46\ \text{krad/s}
\Rightarrow
f_{z1} = 13.12\ \text{kHz}
$$

$$
\omega_{z2} = \frac{\omega_c}{k_2} = 252.7\ \text{krad/s}
\Rightarrow
f_{z2} = 40.21\ \text{kHz}
$$

---

### Pole Locations
$$
\omega_{p1} = k_1^2 \omega_{z1} = 10.77\ \text{Mrad/s}
\Rightarrow
f_{p1} = 1.714\ \text{MHz}
$$

$$
\omega_{p2} = k_2^2 \omega_{z2} = 3.515\ \text{Mrad/s}
\Rightarrow
f_{p2} = 559.5\ \text{kHz}
$$

---

### Component Values

$$
R_1 = 25\ \text{k}\Omega
$$

$$
R_2 = 100\ \text{k}\Omega \quad (R_2 = 4R_1)
$$

$$
C_2 = 0.3957\ \text{pF}
$$

$$
C_i = 51.3\ \text{pF}
$$

$$
R_p = 236.4\ \text{k}\Omega
$$

$$
C_d = 10\ \text{pF}
$$

$$
R_d = 28.45\ \text{k}\Omega
$$

### Gain Stages
$$
g_{m1} = 10\ \mu\text{S}
$$

$$
g_{m2} = \frac{4}{5}(k_2^2 - 1) g_{m1} = 103.3\ \mu\text{S}
$$

This compensation achieves a unity-gain bandwidth of 150 kHz and a phase margin essentially equal to the 60° target, yielding a well-damped transient response. [file:1][file:2]

---

## Repository Structure

- `VoltageModeBuckConverter.py`  
  - Power-stage metrics (duty cycle, ripple, LC resonance, quality factor) [file:2]  
  - PWM gain relation $V_{out}/V_{ctrl} = (V_{in}/V_{ramp})H(s)$ [file:2]  
  - Type-III compensation for both low-PM and high-PM cases [file:2]

- `README.md`  
  - This document, summarizing the design methodology and sample numerical results [file:1][file:2]

---

## How to Run

```bash
python VoltageModeBuckConverter.py
