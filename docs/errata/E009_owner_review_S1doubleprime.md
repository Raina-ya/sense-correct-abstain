# Erratum E009 — Owner review of extension S1″ (2026-11-21)

**Append-only.** E001–E008 and every file in the v1–v4 errata manifests remain
byte-identical. For S1″, **this erratum governs** E007 §3.2 and the review
sheet `docs/theory/S1doubleprime_review_draft.pdf`. No frozen verdict changes.

**Reviewed material:**

- E007 §3.2 (commit `630ef91`); and
- `docs/theory/S1doubleprime_review_draft.pdf` (commit `cc8ef21`).

**Review supplied by the owner:**
[`../theory/S1doubleprime_rigorous.tex`](../theory/S1doubleprime_rigorous.tex) and
[`../theory/S1doubleprime_rigorous.pdf`](../theory/S1doubleprime_rigorous.pdf)
(3 pages). Both are byte-identical to the files the owner supplied on
2026-11-21. The `.tex` file compiles cleanly and its text matches the PDF
exactly.

**Owner verdict:** accept with corrections. No correction changes a conclusion.

## 1. Status after review

| Result | Status before | Status now |
|---|---|---|
| S1″(a) shared nonlinear class: `I ⊇ R \ {-1}` by rescaling | draft | **proved, owner-reviewed**; holds for arbitrary angle vectors and any number of candidates |
| S1″(b) exceptional point `epsilon' = -1`: in `I` iff all `P_k` coincide (constants in the class) | draft | **proved, owner-reviewed, with correction** (§2) |
| S1″(c) shared first-order class: `I ⊇ R \ {0}`; `0 ∈ I` iff all `P_k` coincide | draft | **proved, owner-reviewed, with correction** (§2) |
| S1″(d) visibility/offset enlargement | draft | **proved, owner-reviewed**; restated as a general monotonicity lemma (a larger model has a larger identified set), which also covers a per-candidate offset |
| Corollary: open interval around `epsilon_0` at every `phi_0 = 0` point of all six designs | draft | **proved, owner-reviewed**; every construction uses `phi' = 0`, so it is feasible in the spec box `[-0.05,0.05]^2` (both coordinates) |
| Whether readings (a)–(b) fairly represent spec §5.3 | — | remains a **specification question**, not a mathematical claim |

## 2. Corrections

1. **`phi' != 0` at the exceptional points.**
   - The draft proves the forward direction of S1″(b) by "both candidates are
     evaluated at `u = 0`", and of S1″(c) by "`P'_1 = q' = P'_2`". Both
     arguments assume the equivalent point has `phi' = 0`.
   - For a general equivalent point, the evaluation point at `epsilon' = -1` is
     `R'(s(t) phi')`, and at `epsilon' = 0` the law is
     `q' + phi' sum_ell s_ell(t) D'_ell`.
   - Neither depends on the candidate `k`. Fixing one label pattern `t`
     therefore still forces all `P_k` to coincide, and the conclusions are
     unchanged.
   - The same patch applies to E007 §3.2(a) ("both candidates would be
     evaluated at `u = 0`"), which is superseded by this erratum.
2. **Generality.** Claims (a)–(c) do not use `Theta_k = theta_k 1_L`,
   `theta_1 != theta_2`, or `K = 2`. The conclusion does not depend on how the
   distinct design assigns angles within a candidate.
3. **Box feasibility.** The draft's corollary checked only `epsilon'` against
   the box. The spec box constrains `(epsilon', phi')`. All constructions use
   `phi' = 0`, so `I ∩ [-0.05, 0.05]` contains a non-degenerate interval: for
   example `(0, 0.05]` when `epsilon_0 ∈ (0, 0.04]` in the first-order shared
   reading.

## 3. Independent check (Claude)

Each correction was re-derived:

- At `epsilon' = -1`, `(1 + epsilon') Theta_k + s(t) phi' = s(t) phi'` is
  independent of `k`.
- At `epsilon' = 0`, every `Theta_{k,ell}` term vanishes.
- The rescaling `R'(u) = R(c u)` with `c = (1 + epsilon_0)/(1 + epsilon')`
  works for any finite set of angle vectors.
- `v_0 P' + (1 - v_0) o_0` lies in the open simplex whenever `P'` does and
  `v_0 > 0`.

Agreed.

## 4. Review status of all project mathematics

| Result | Status |
|---|---|
| Lemma S1′, Prop. 4, Gate 1A corollary, Lemma B | proved, owner-reviewed (E007) |
| A4–A6: T1, C1, C2, L1, wrong-action form, T2, D1, P2 | proved, owner-reviewed (E008) |
| S1″ (a)–(d) and corollary | proved, owner-reviewed (E009) |
| Example E1 | corrected (E008 §2) |
| Example E2 | first condition discharged conditionally; second condition open (E008 §3) |
| Nonuniqueness ⇒ Gate 1A FAIL | specification inference, checked against spec §7 and §9 (E007 §3.1) |
| Readings of spec §5.3 | specification question |
| Chow (1970) rule form; Tsybakov lemma locations | attribution **unverified** (full texts unavailable). C2 and T2 are self-contained and do not depend on them. |

No draft proof remains open in the project.
