# Erratum E007 — Owner review of Lemma S1′ and Lemma B (2026-11-21)

**Append-only.** E001–E006 and every file in the v1 and v2 errata manifests
remain byte-identical. Where this erratum differs from E006 §2–§3, **this
erratum governs**. No frozen verdict changes.

**Reviewed material:** E006 §2–§3, typeset as the review draft
`Lemma_S1prime_and_Lemma_B_review_draft.pdf`.

**Review supplied by the owner:**
[`../theory/S1prime_B_rigorous.tex`](../theory/S1prime_B_rigorous.tex) and
[`../theory/S1prime_B_rigorous.pdf`](../theory/S1prime_B_rigorous.pdf) (7
pages). Both are byte-identical to the files the owner supplied on 2026-11-21.

**Owner verdict:** accept with corrections. No correction changes a conclusion.

## 1. Status after review

| Result | Status before | Status now |
|---|---|---|
| Frame covariance (assumption A1 made explicit) | proved at M2 | proved; exact, no global phase (owner note, Lemma 2) |
| Lemma S1′ (1): local non-identification under N-q and N-loc | draft | **proved, owner-reviewed** |
| Prop. 4 (new): sharp identified set under N-q is a bounded open interval, so global non-identification fails there | — | **proved, owner-reviewed** |
| Lemma S1′ (2): `I = R` under N-loc | draft | **proved, owner-reviewed** |
| Lemma S1′ (3): `I = R` under per-candidate N-free (translation construction) | draft | **proved, owner-reviewed, with correction** |
| Lemma S1′ (4): the `epsilon` score lies in the nuisance tangent **set** | draft | **proved, owner-reviewed, with correction** (explicit in-class nuisance paths) |
| Gate 1A corollary: profile maximizers attaining the maximum = identified set (Gibbs); flat even under misspecification | draft | **proved, owner-reviewed, with correction** (non-nesting) |
| Extension to the per-context and visibility/offset readings of §5.3 (§3 below) | — | proved (draft, Claude); owner review pending |
| Lemma B (assumptions A2 single occurrence, A3 error model; constant 1/2 sharp; `theta > 0` not needed) | draft | **proved, owner-reviewed** |
| What is not proved about `B_hat` (E006 §3) | — | unchanged; accepted as stated |

## 2. Corrections adopted from the owner note

1. **Non-nesting (Corollary, Step 4).** N-q is contained in N-loc, but N-q is
   **not** contained in N-free. An affine response with some
   `D_{c,ell} != 0` leaves the open simplex for large angles, so it is not a
   map from `R^{L_c}` to the open simplex. N-loc and N-free are not nested.
   The N-free case is covered by item (3) directly, not by item (1).
2. **Item (3).** The condition `1 + epsilon' != 0` is unnecessary in the
   per-candidate parameterization. The pointwise construction is valid only
   for classes containing arbitrary maps. The translation
   `R'_c(u) = R_c(u + (epsilon_0 - epsilon') theta_c)` preserves regularity
   and works for every real `epsilon'` in any class closed under translation.
   This removes a tension with item (4), which assumes differentiability.
3. **Item (4).** Explicit nuisance submodels:
   - N-q and N-loc: `q_c + tau v_c`;
   - N-free: `R_c + tau psi_c w_c`, where `psi_c` is a smooth bump that
     preserves positivity.

   The score lies in the tangent **set** itself, not only in its closed span.
4. **Corollary.** By Gibbs' inequality, at exact probabilities the profile
   maximizers that attain `Lambda*` are exactly the identified set. The
   profile is flat on an interval even if N-q is misspecified, so
   well-specification is not needed.
5. **Sharp identified set under N-q (Prop. 4).**
   `I = (epsilon_0 - alpha, epsilon_0 + beta)`, both endpoints finite when some
   `v_c != 0`. This proves that E006's "only local non-identification is
   guaranteed under N-q" is tight.
6. **Lemma B.** Single-occurrence assumption made explicit (each occurrence of
   a QAOA angle is its own coordinate). Smoothness (Step 0) justifies the
   fundamental theorem of calculus. The constant 1/2 is sharp (single-qubit
   example `E = cos^2(x/2)`). The condition `theta > 0` is not needed. A
   companion bound `min(||delta_A||_1/2, 1) + min(||delta_B||_1/2, 1)` holds
   for large perturbations.

## 3. The two specification points the owner flagged

### 3.1 Wording of §7 and §9 (checked against the repository)

Source: `docs/theory/gate1_math_spec_v1.md`, M3-hashed, unchanged.

- §7: "The exact-probability recovery check uses the full grid", "Bounds are
  `[-0.05,0.05]^2`", "All starts must reach the same identified solution",
  "A flat profile, nonunique solution, boundary solution for an interior
  truth, or optimizer disagreement is a failure, not averaged away."
- §9: "Gate 1A passes only if, in at least one frozen primary `p=1`
  deployable design, ... exact-probability recovery meets the frozen
  tolerance at every required grid point".
- §4: the grid is `{-0.04, ..., 0.04}^2`, so each design has nine grid points
  with `phi = 0`.

**One detail absent from the draft's paraphrase:** the box
`[-0.05,0.05]^2`. Every grid truth has `|epsilon_0| <= 0.04`, an interior
point of the box, so the open non-identification interval intersected with
the box is still a non-degenerate interval. The box does not restore
uniqueness.

**Conclusion:** the specification step "nonunique profile maximizer at the
nine `phi = 0` points of every design ⇒ FAIL" matches the repository text. It
remains a specification inference, as the owner note says, not a
mathematical theorem.

### 3.2 Do N-q, N-loc, and N-free cover §5.3?

§5.3: "treats **each target context's** ideal outcome distribution and its
local response directions as unknown, subject only to normalization,
positivity, and the shared frozen circuit/label design. Visibility and
label-independent offset are also nuisance quantities."

**Not literally.** Two readings fall outside the per-candidate
parameterizations. Both are covered by the short results below.

**(a) Per-context shared response (affects only the `distinct` design).**
Here the two candidates (angle vectors `theta_1 != theta_2`, both tagged
blocks at the same angle within a candidate) share one map
`R: R^L -> open simplex`, so at `phi = 0`,
`P_k = R((1 + epsilon) theta_k)` for `k = 1, 2`.

- The translation construction fails, because the two candidates would need
  different shifts.

*Claim S1″ (proved, draft; owner review pending).* If the class is closed
under linear rescaling of the argument (true for arbitrary, continuous, and
`C^k` maps), then `I ⊇ R \ {-1}`.

*Proof.* For `epsilon' != -1`, set
`R'(u) := R(((1 + epsilon_0)/(1 + epsilon')) u)`. Then
`R'((1 + epsilon') theta_k) = R((1 + epsilon_0) theta_k) = P_k` for both `k`,
and `R'` has the regularity of `R`. ∎

- At `epsilon' = -1` both candidates would be evaluated at `u = 0`, which is
  impossible when `P_1 != P_2`. So in this reading `1 + epsilon' != 0` **is**
  needed, and `I = R` holds only when `P_1 = P_2`.
- First-order shared version (one `q`, shared directions `D`, unknown): the
  item (2) construction (`D' = (epsilon_0/epsilon') D`, `q' = q`) does not
  depend on sharing, so `I ⊇ R \ {0}`.
- If the shared directions `D` were **known**, `epsilon` could be identified
  in the `distinct` design from `P_1 - P_2`. That is not a reading of §5.3,
  which declares the response directions unknown.

**(b) Visibility and label-independent offset.** Laws of the form
`v P + (1 - v) o`, with `v in (0, 1]` and `o` a label-independent
distribution, contain each original class (`v = 1`). Enlarging the class can
only enlarge every equivalence class, so every non-identification statement
above still holds.

**Consequence.** In all six primary designs (G2 and G3 × single, same,
distinct), and under every reading of §5.3 considered here, the identified set
at each `phi = 0` grid point contains an open interval around `epsilon_0`.
The profile maximizer is therefore nonunique, and Gate 1A fails by §7 and §9.
**The frozen verdict and its corrected basis stand.**

## 4. Effect on other documents

- `docs/claim_ledger.md` A3, A7, and B1 updated to the statuses in §1. The
  ledger is a living MT7 draft and is not hashed.
- `paper/technical_report_v1.md`, `docs/results/project_status.md`, `README.md`,
  and `docs/literature/novelty_claim_draft.md`: status lines updated. The
  sentences "Owner review of Lemma S1′ and Lemma B is deferred", added in
  commit `d6814a9` (MT7.4), are superseded by this review. All other
  `d6814a9` content is unchanged.
- E006 is not edited. Its "proved (draft, owner review pending)" labels for
  Lemma S1′ and Lemma B are superseded by §1 above.
- The three-action theory note results (A4–A6) were not part of this review
  and remain drafts.
