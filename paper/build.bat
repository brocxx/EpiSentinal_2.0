@echo off
REM ============================================================
REM  EpiSentinel Paper Build Script (Windows)
REM  Requires: MiKTeX or TeX Live installed and on PATH
REM  Run from the paper\ directory
REM ============================================================

echo [1/3] First pass: pdflatex...
pdflatex -interaction=nonstopmode episentinel_paper.tex
if %errorlevel% neq 0 (
    echo ERROR: First pdflatex pass failed. Check episentinel_paper.log
    exit /b 1
)

echo [2/3] Second pass (resolve cross-refs)...
pdflatex -interaction=nonstopmode episentinel_paper.tex
if %errorlevel% neq 0 (
    echo ERROR: Second pdflatex pass failed.
    exit /b 1
)

echo [3/3] Third pass (finalise)...
pdflatex -interaction=nonstopmode episentinel_paper.tex
if %errorlevel% neq 0 (
    echo ERROR: Third pdflatex pass failed.
    exit /b 1
)

echo.
echo ============================================================
echo  Build complete: episentinel_paper.pdf
echo ============================================================
