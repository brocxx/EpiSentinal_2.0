# EpiSentinel — IEEE Paper

This directory contains the publication-ready LaTeX source for:

> **EpiSentinel: An Explainable Ensemble Framework with Autoregressive
> Epidemiological Signals and SOP-Grounded Advisory for District-Level
> Dengue Outbreak Forecasting in Karnataka, India**
>
> Ekansh Nandan Sharma, GN Disha, Ishan Mahajan, Prof. Saraswathi Govind Datar  
> Department of Computer Science Engineering, RV College of Engineering, Bengaluru

---

## File List

| File | Description |
|------|-------------|
| `episentinel_paper.tex` | Complete IEEE two-column LaTeX source (~1,491 lines, ~8-10 pages compiled) |
| `build.bat` | Windows build script (requires MiKTeX / TeX Live on PATH) |

---

## How to Compile

### Option 1 — Overleaf (Recommended, no installation needed)

1. Go to [https://overleaf.com](https://overleaf.com) and log in
2. Click **New Project → Upload Project**
3. Upload `episentinel_paper.tex` (just the single `.tex` file — all packages are on Overleaf)
4. Set compiler to **pdfLaTeX** (Menu → Compiler → pdfLaTeX)
5. Click **Compile** — the PDF renders immediately

### Option 2 — MiKTeX (Windows)

1. Install MiKTeX from https://miktex.org/download
2. Open **MiKTeX Console** → let it install missing packages
3. Run from this directory:
   ```
   build.bat
   ```
   Or manually:
   ```
   pdflatex -interaction=nonstopmode episentinel_paper.tex
   pdflatex -interaction=nonstopmode episentinel_paper.tex
   pdflatex -interaction=nonstopmode episentinel_paper.tex
   ```
   (Three passes resolve all cross-references)

### Option 3 — TeX Live (Linux/macOS/WSL)

```bash
pdflatex episentinel_paper.tex
pdflatex episentinel_paper.tex
pdflatex episentinel_paper.tex
```

---

## Paper Structure

| Section | Title |
|---------|-------|
| I | Introduction |
| II | Related Work |
| III | Dataset and Feature Engineering |
| IV | Systematic Identification and Removal of Geographic Identity Proxies |
| V | Model Development and Experiments |
| VI | Explainability: SHAP Analysis |
| VII | Uncertainty Quantification via Conformal Prediction |
| VIII | System Architecture and Dashboard |
| IX | Discussion |
| X | Conclusion |
| — | References (13 citations) |

---

## Key Results

| Metric | Value |
|--------|-------|
| ROC-AUC | **0.821** |
| PR-AUC | **0.825** |
| Recall | **0.856** |
| F1 Score | **0.720** |
| Conformal Coverage | 90% |
| Conformal Half-Width ($\hat{q}$) | ±21.7 pp |

---

## Required LaTeX Packages

All standard — available on Overleaf and in any modern TeX distribution:

`IEEEtran`, `amsmath`, `amssymb`, `booktabs`, `tikz`, `hyperref`,
`microtype`, `xcolor`, `lmodern`, `array`, `multirow`, `balance`

---

## Notes

- The SHAP bar chart (Figure 1) and system architecture diagram (Figure 2)
  are rendered entirely in **TikZ** — no external image files required.
- The bibliography uses the inline `\begin{thebibliography}` format —
  no `.bib` file is needed.
- The paper is formatted for `\documentclass[conference]{IEEEtran}`.
  For journal submission use `\documentclass[journal]{IEEEtran}`.
