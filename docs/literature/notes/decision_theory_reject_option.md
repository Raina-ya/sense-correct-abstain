# Decision theory for the three-action rule

**Status:** reading note, 2026-11-20 (Claude). New sources (`chow1970`,
`herbei2006`, `howard1966voi`) were checked at metadata and abstract level only.
Sources marked "inherited" were verified bibliographically in the predecessor
project; their use here is a routing note, not a content check. Keys refer to
`../library.csv`.

## The project's decision problem

Two candidates, one top-1 decision, one fixed shot budget. After sensing, the
policy chooses no action (N), correct and rerun (C), or abstain (A), with loss
1 for a wrong deployed answer and `lambda_A` for abstaining (research plan §3.5
and the risk identity in Part 1).

## How the literature maps onto it

| Key | What it provides (as far as checked) | Maps to | What it does not provide |
|---|---|---|---|
| `chow1970` | An optimum rejection rule and a general relation between error and reject probabilities in a recognition system (abstract). | The N/A part of the switching rule. With C removed, the three-action rule should reduce to a Chow-type threshold rule; Part 1 should show this as a sanity check. | No correction action; assumes known posteriors. |
| `herbei2006` | Binary classification with a reject option, used where conditional class probabilities are close; plug-in rules and empirical risk minimizers (abstract). The cost of rejection is a constant `d`. | The `lambda_A` loss form; "reject when the two classes are close" is the analogue of "abstain when the candidate gap is within its uncertainty". | No budget, no correction. The ML estimators in the paper are not used. |
| `howard1966voi` | Value of information from the joint probabilistic and economic factors of a decision (abstract). | Gate 3: sensing has value only if it can change the action and the expected loss reduction exceeds its cost. | Bibliographic page range unconfirmed. |
| `bechhofer1954` (inherited) | Ranking and selection of normal means. | Top-1 framing. | No abstention or correction. |
| `kimnelson2006` (inherited) | Selecting the best system under a budget. | Fixed-budget selection. | No correction. |
| `chen2000ocba` (inherited) | Allocating a simulation budget to improve selection. | Splitting the budget between sensing and execution. | Unbiased outputs assumed. |
| `garivier2016`, `kaufmann2016` (inherited) | Lower bounds for best-arm identification. | Template for the finite-pilot lower bound. | Unbiased rewards. |
| `ghosh2017` (inherited) | Bandits with misspecified linear rewards. | The closest decision-theory analogue to biased observations under E2. | Regret setting, no abstention. |
| `scavino2026` (inherited, preprint) | Decision kernels for QEM: accuracy gains need decision relevance. | Closest QEM work at the decision level; must be compared before any novelty wording. | Scope relative to action selection to be checked. |

## A gap worth stating carefully

Among the sources listed here, none combines (i) a costly corrective action
that consumes part of the same budget, (ii) an abstention option with explicit
cost, and (iii) observations whose bias is unknown and only partly sensed. This
is a statement about this list, not a literature-wide claim; the search for
fixed-budget calibrate-or-abstain policies in `../novelty_claim_draft.md` is
still open.

## Concrete tasks for Part 1

1. Show that the three-action rule reduces to a Chow-type rule when C is
   removed and `lambda_A` is fixed (sanity check of the risk identity).
2. State Gate 3 explicitly as a value-of-information inequality in the sense of
   `howard1966voi`, with the sensing cost in shots.
3. Use the best-arm-identification lower bounds only as a template; the biased
   setting needs its own two-point construction (`lecam1973`, `tsybakov2009`).
