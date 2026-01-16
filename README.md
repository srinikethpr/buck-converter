# Voltage-Mode Buck Converter Calculations

This repository contains a Python script that reproduces key analytical calculations for a high‑frequency voltage‑mode buck converter, including power‑stage metrics, PWM modulator gain, and Type‑III compensator design for two different phase‑margin targets.[file:1][file:2]

---

## Project Overview

- Input voltage \(V_{in} = 3.3\) V and output voltage \(V_{out} = 1.5\) V.[file:1]  
- Switching frequency \(F_{sw} = 1.5\) MHz with an inductor current ripple target of approximately 20% of maximum load current.[file:1][file:2]  
- Two Type‑III compensation cases are evaluated: a low phase‑margin design (~5°) and a high phase‑margin design (~60°), both targeting a closed‑loop crossover frequency near \(F_{sw}/10 \approx 150\) kHz.[file:1][file:2]

The Python script is intended as a calculation and documentation aid alongside circuit‑level simulations or hardware prototypes.[file:2]

---

## Power Stage and PWM Relations

These values are computed from the design specifications and component choices.[file:2]

- Duty cycle:  
  \[
  D = \frac{V_{out}}{V_{in}} = 0.454545
  \]
- Load resistance at maximum load:  
  \[
  R_{load} = \frac{V_{out}}{I_{out,\max}} = 1.5000\ \Omega
  \]

Ripple targets (typical design rule):

- Target inductor ripple current:  
  \[
  \Delta I_L^{target} \approx 0.2 \cdot I_{out,\max} = 0.200\ \text{A}
  \]
- Computed inductor ripple:  
  \[
  \Delta I_L = 202\ \text{mA}
  \]
- Computed output ripple due to capacitor only:  
  \[
  \Delta V_{out,\text{cap}} = 1.684\ \text{mV}
  \]

Resonant frequency of LC filter:

- Ideal LC resonance:
  \[
  f_0^{ideal} = 30.63\ \text{kHz}
  \]
- Corrected resonance including ESR term:
  \[
  f_0^{corr} = 30.53\ \text{kHz}
  \]

Quality factor:

- \(Q = 2.6067\)  
- \(Q_{max} = 25.9808\)

PWM scaling:

- PWM gain:
  \[
  G_{pwm} = \frac{1}{V_{ramp}} = 1.000\ \frac{1}{\text{V}}
  \]
- Overall small‑signal relation:
  \[
  \frac{V_{out}}{V_{ctrl}} = \frac{V_{in}}{V_{ramp}} \cdot H(s) = 3.300 \cdot H(s)
  \]

All expressions above are directly printed by the script from the chosen values of \(L\), \(C\), \(R_{loss}\), \(R_{ESR}\), \(V_{in}\), \(V_{out}\), \(V_{ramp}\), and \(I_{out,\max}\).[file:2]

---

## Type‑III Compensation: Low Phase Margin (~5°)

This case corresponds to a **marginally** stable design with low phase margin, primarily used for comparison and educational purposes.[file:1][file:2]

- Target crossover frequency:
  \[
  f_c = 150\ \text{kHz} \quad (F_{sw}/10)
  \]
- Zeros:
  \[
  \omega_{z1} = \frac{\omega_c}{k_1} = 82.46\ \text{krad/s}
  \quad\Rightarrow\quad f_{z1} = 13.12\ \text{kHz}
  \]
  \[
  \omega_{z2} = \frac{\omega_c}{k_2} = 864.7\ \text{krad/s}
  \quad\Rightarrow\quad f_{z2} = 137.6\ \text{kHz}
  \]
- Poles:
  \[
  \omega_{p1} = k_1^2 \omega_{z1} = 10.77\ \text{Mrad/s}
  \quad\Rightarrow\quad f_{p1} = 1.714\ \text{MHz}
  \]
  \[
  \omega_{p2} = k_2^2 \omega_{z2} = 1.027\ \text{Mrad/s}
  \quad\Rightarrow\quad f_{p2} = 163.5\ \text{kHz}
  \]

Component values:

- \(R_1 = 25\ \text{k}\Omega\)  
- \(R_2 = 100\ \text{k}\Omega\)  (enforcing \(R_2 = 4R_1\))  
- \(C_2 = 1\ \text{pF}\)  
- \(C_i = (k_1^2 - 1) C_2 = 129.6\ \text{pF}\)  
- \(R_p = \dfrac{k_1}{C_i \omega_c} = 93.54\ \text{k}\Omega\)  
- \(R_d = \dfrac{5 - 4k_2^2}{5(k_2^2 - 1)} R_1 = 6.582\ \text{k}\Omega\)  
- \(C_d = \dfrac{1}{(4R_d + R_2)\omega_{p2}} = 7.706\ \text{pF}\)  
- Transconductance:
  \[
  g_m = \frac{7 \omega_c k_1 V_{out} C_2}{k_2 V_{ref}} = 86.48\ \mu\text{S}
  \]

The resulting closed‑loop system shows unity gain at 150 kHz and a phase margin close to 5–6°, as confirmed by AC simulations in the associated design report.[file:1][file:2]

---

## Type‑III Compensation: High Phase Margin (~60°)

This case corresponds to a **robust** design with significantly higher phase margin and better damping of output transients.[file:1][file:2]

- Target crossover frequency:
  \[
  f_c = 150\ \text{kHz} \quad (F_{sw}/10)
  \]
- Zeros:
  \[
  \omega_{z1} = \frac{\omega_c}{k_1} = 82.46\ \text{krad/s}
  \quad\Rightarrow\quad f_{z1} = 13.12\ \text{kHz}
  \]
  \[
  \omega_{z2} = \frac{\omega_c}{k_2} = 252.7\ \text{krad/s}
  \quad\Rightarrow\quad f_{z2} = 40.21\ \text{kHz}
  \]
- Poles:
  \[
  \omega_{p1} = k_1^2 \omega_{z1} = 10.77\ \text{Mrad/s}
  \quad\Rightarrow\quad f_{p1} = 1.714\ \text{MHz}
  \]
  \[
  \omega_{p2} = k_2^2 \omega_{z2} = 3.515\ \text{Mrad/s}
  \quad\Rightarrow\quad f_{p2} = 559.5\ \text{kHz}
  \]

Component values (from the computed design):

- \(R_1 = 25\ \text{k}\Omega\)  
- \(R_2 = 100\ \text{k}\Omega\)  (maintaining \(R_2 = 4R_1\))  
- \(C_2 = 0.3957\ \text{pF}\)  
- \(C_i = 51.3\ \text{pF}\)  
- \(R_p = 236.4\ \text{k}\Omega\)  
- \(C_d = 10\ \text{pF}\)  
- \(R_d = 28.45\ \text{k}\Omega\)  
- First gain stage:
  \[
  g_{m1} = 10\ \mu\text{S}
  \]
- Second gain stage (derived from \(k_2\)):
  \[
  g_{m2} = \frac{4}{5}(k_2^2 - 1)g_{m1} = 103.3\ \mu\text{S}
  \]

The complete system with this compensation achieves a unity‑gain bandwidth of 150 kHz and a phase margin essentially equal to the 60° target, yielding a well‑damped transient response.[file:1][file:2]

---

## Repository Structure

A minimal suggested structure for this project:

- `VoltageModeBuckConverter.py`  
  - Contains all computations for:
    - Power‑stage metrics (duty cycle, inductor ripple, output ripple, LC resonance, quality factor).[file:2]  
    - PWM gain relation \(V_{out}/V_{ctrl} = (V_{in}/V_{ramp})H(s)\).[file:2]  
    - Type‑III compensation for low and high phase margin, including all derived component values.[file:2]
- `README.md`  
  - This Markdown file, summarizing the design context and presenting example numerical results from the script.[file:1][file:2]

To reproduce the sample numbers shown above, clone the repository, ensure Python 3 is installed, and run:

```bash
python VoltageModeBuckConverter.py
