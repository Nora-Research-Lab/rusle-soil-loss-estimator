![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# RUSLE Soil Loss Estimator
 
*For environmental geoscientists and land managers: enter rainfall erosivity, soil erodibility, slope, cover, and support practice factors to compute annual soil loss and erosion risk classification using the Revised Universal Soil Loss Equation.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Environmental Geoscience
 
The tool computes annual soil loss using RUSLE: A = R × K × LS × C × P, where A is annual soil loss (t ha⁻¹ yr⁻¹). Inputs: (1) R factor (MJ mm ha⁻¹ h⁻¹ yr⁻¹) numeric input with range 0–1000; (2) K factor (t ha h ha⁻¹ MJ⁻¹ mm⁻¹) numeric input with range 0–1; (3) LS factor (dimensionless) numeric input, with an optional sub-section where user can compute LS by entering slope length (m) and slope steepness (%) using the formula LS = (λ/22.13)^m * (65.41 sin²θ + 4.56 sinθ + 0.065) where m = 0.5 for slopes ≥5%, 0.4 for 3–5%, 0.3 for 1–3%, else 0.2; (4) C factor: dropdown with typical values (Bare soil 1.0, Row crops 0.5, Cereal crops 0.2, Pasture 0.02, Forest 0.01, Custom) plus a numeric input if Custom selected; (5) P factor: dropdown (Straight row 1.0, Contour tillage 0.5, Strip cropping 0.3, Terracing 0.2, Custom) plus numeric input if Custom. UI: Title at top. Two-column layout: left column for R, K, LS inputs (with a small 'Compute LS from slope' expandable section); right column for C and P dropdowns with custom numeric fields, and a 'Calculate' button. Output: numeric A value prominently displayed with unit, color-coded erosion risk bar (green <5 low, yellow 5–10 moderate, orange 10–20 high, red >20 severe), and a text summary showing the RUSLE equation with substituted values. Optionally, a simple horizontal bar chart comparing the five factor contributions. No AI component. All calculations are deterministic.
 
## Run it
 
```bash
docker build -t rusle-soil-loss-estimator .
docker run -p 7860:7860 rusle-soil-loss-estimator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-25.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
