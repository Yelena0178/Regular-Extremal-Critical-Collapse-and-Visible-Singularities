# Audit certificate and limitations

[C] Original rational N=50 coefficients are byte-for-byte preserved; hashes appear in data/provenance.json. No Fourier optimization was performed.

[C] Analytic audit: files 01–09 contain the derivations and the proof-level checks. The most consequential additions are the exact product boundary terms, a parameter-uniform Banach algebra envelope, the explicit compact H expansion, and the gauge-normalized pure/mixed endpoint tables. The KU source used for precise numbering is arXiv:2211.15742v2.

[C] Executable certificate audit: all scripts use Python's standard library only. Run `python proof_checks/run_checks.py`. The checks below were run successfully on the delivered source. Their role and limitations are separate from the analytic proof:

|Check|Arithmetic|What it establishes|
|---|---|---|
|jacobian_check.py|exact Fraction|endpoint constraints, moments, right inverse, λ enclosure, determinant|
|current_check.py|exact Fraction/Bernstein|factored current ≥1/100 over a continuum|
|interval_checks.py|directed Decimal intervals, Taylor remainders, Bernstein, exact tail|K≥10^-8 on the entire half-line|
|stability_check.py|exact Fraction coefficient bounds|fixed correction cube; K≥5×10^-9; positive current|
|symbolic_checks.py|exact Laurent-polynomial differentiation|quotient/lapse/Maxwell derivatives and throat coefficients|
|endpoint_jet_check.py|exact rational substitution|nonzero normalized RN mixed jets, representative Minkowski identities|

The profile positivity verification is independently implemented here from the earlier numerical validator and the inherited certificate summary. It covers intervals, not mesh points. The Decimal certificate uses outward rounding for every arithmetic operation and explicit analytic remainders for its transcendental quantities. The script's complete coverage list and lower bounds are saved in data/K_certificate.json.

[O] These scripts do not prove F_{δ*,L*}(c*)=0 for printed numerical parameters. The exact finite root in the theorem is obtained analytically by C1 zero stability. No interval-Newton certificate of a finite member is claimed.

[O] This is not a Lean/Coq proof or a claim of external peer review. The executable certificates verify the stated finite algebraic/interval portions; the analytic limiting and global PDE argument is the mathematical proof in the accompanying manuscript.

## Actual check log

```text
jacobian_check.py
PASS: rational tangential constraints; six zero moments; exact right inverse; coupling enclosure; positive real Jacobian determinant.
lambda= 0.5612976215068984 K0= 1.0951713352112002e-07 det_real= 9.55322554849204e-07

symbolic_checks.py
PASS exact symbolic quotient, lapse, and second Maxwell derivatives.
PASS third throat kernel coefficients by exact polynomial identity checks.

endpoint_jet_check.py
PASS exact symbolic quotient, lapse, and second Maxwell derivatives.
PASS third throat kernel coefficients by exact polynomial identity checks.
PASS nonzero RN mixed jets, and Minkowski zero mixed jets.

stability_check.py
PASS current factor >=1/100; degree 95 leaves 7 maxdepth 5
PASS uniform correction ball ||c||inf<=1e-200: K>=5e-9, current factor>=1/200, positive energy/current means.

interval_checks.py
PASS K>=1e-8 on all x>=0; compact leaves 40 min certified 1.095171335136733405130448983557148927253455189183261976028561565396633765272621337178668121258387813E-7 tail lower 0.17966134138645043
```
