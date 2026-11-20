# Sense, Correct, or Abstain：研究地圖與執行時程 v1

**版本日期：** 2026-11-20  
**狀態：** 可編輯的研究規劃稿；不是凍結 protocol、不是 preregistration、不是實驗結果，也不構成硬體執行授權。  
**權威範圍：** 本文件取代 `docs/research_program_plan_v0.md` 原 Section 5 的週時程；理論定義、Gate 判準與 endpoint 若有衝突，仍以總計畫及其後續明確修訂為準。  
**規劃假設：** 每週投入 8--10 小時，從 2026-11-23 開始，待使用者確認。若工時或開始日期改變，所有日期等量後移，Part 內容、Gate 順序、主要終點與資料邊界不跟著改變。

## 執行原則

1. **內容固定、日期可移。** 四個 Part 的問題與順序在執行前決定；延誤只往後推，不以結果為理由改題。
2. **唯一感測分岔。** 先跑 Gate 1A（RC labels）；只有 Gate 1A 依事前判準失敗時，才可跑事前完整指定的 Gate 1B（P-amp）。兩者都失敗後不得加入第三種探針。
3. **單一主要終點。** 唯一主要終點是：固定總預算下，可部署 sensor policy 相對於開發期鎖定的最佳 fixed policy，其 paired decision value improvement。所有 parameter recovery、false certification、coverage、flip prediction 與 oracle regret 都是次要或探索性。
4. **證據分層。** 解析、無雜訊模擬、有雜訊模擬、裝置參數模擬（fake backend）與硬體證據分開標示。fake backend 永遠不是硬體證據。
5. **開發與確認分離。** 開發資料可用來決定事前允許決定的 threshold、loss 與 power；holdout 只在 protocol 獨立時間戳後讀一次。
6. **負面結果不換題。** Gate 失敗、policy collapse、無淨收益或不可辨識都是正式結果；不以增加預算、縮小參數格點或替換 sensor 來救結果。
7. **硬體另案。** 第三章不依賴硬體成功。任何硬體工作必須另有 protocol、獨立時間戳與每次使用者授權。

---

## 1. 博論地圖（一頁）

### 1.1 傘狀問題

**主版本**

> 在固定量子執行資源下，執行時證據何時足以支持我們相信、修正或放棄一個量子決策？

**替代措辭 A：可辨識性重點**

> 在有限執行預算下，哪些會改變決策的偏差能由 runtime evidence 識別，哪些在資訊上不可區分？

**替代措辭 B：資源配置重點**

> 面對有偏且會漂移的量子執行結果，有限資源應如何在作答、感測、校正、重跑與拒答之間配置？

主版本最適合作為博論主軸，因為它不預設感測器、校正或硬體一定成功；替代 A 適合理論章，替代 B 適合序列決策與系統章。

### 1.2 五章位置表

| 章 | 暫定章名 | 核心問題 | 狀態 | 從前章繼承 | 主要證據類型 | 事前備案 |
|---|---|---|---|---|---|---|
| Ch. 1 | 估計改善不等於決策改善 | 固定 shot 預算下，較低 estimator error 何時仍使 top-1 selection 變差？ | 已完成：`adaptive-qem-benchmark` | 起點 | 解析、有雜訊模擬 | 若不存在普遍勝出的 QEM selector，保留反例、Proposition 1 與方法邊界；這已是實際章形。 |
| Ch. 2 | 決策偏差的 runtime 可見性 | 哪些 runtime probes 能看見會翻轉決策的 differential bias，警報與拒答付出多少 coverage？ | 已完成：`bias-probe-visibility` | Ch. 1 的 estimator/decision 區分、decision flip 與 differential bias | 解析、有雜訊模擬；硬體 readout addendum 另列為 hardware-derived | 若廣泛 detection 失敗，產出 visibility/blindness 邊界與 abstention cost；這已是實際章形。 |
| Ch. 3 | Sense, Correct, or Abstain | runtime evidence 能否支援 no action、recalibration、abstention 的選擇？RC labels 能否辨識 angle-dependent `epsilon`；不能時何時任何允許的探針都不能可靠選動作？ | 進行中：規劃與文獻／前作稽核完成，尚未執行 Gate 1 模擬 | Ch. 2 的 visibility、blindness、probe cost、false certification 與 coverage tradeoff | 解析、無雜訊模擬、有雜訊模擬；可選裝置參數模擬；硬體不屬主證據 | Gate 1A 失敗只進事前固定 P-amp；兩者失敗轉成 action-selection blindness、finite-pilot lower bound 與負面實例；後續 Gate 失敗則報告 decision relevance、resource boundary 或 fixed-action collapse。 |
| Ch. 4 | 漂移下的重新感測與重新校正 | noise/calibration 隨時間變化時，何時重新 sense、correct、switch 或 stop？ | 規劃中；尚無授權硬體時間序列 | Ch. 3 的 action space、loss、sensor cost、correction uncertainty 與 abstention | 解析、明示生成機制的 simulated drift；若另行登記與逐次授權才有 longitudinal hardware-derived evidence | 若無法取得穩定硬體序列，完成 time-uniform／sequential 方法與 simulated-drift 邊界，不把模擬寫成硬體漂移發現。 |
| Ch. 5 | 極限、轉移與普遍性 | action-selection 的下界與規則能否轉移到不對稱任務、其他 estimand 或更大規模？ | 規劃中 | Ch. 1--4 的 risk、visibility、action、time 與 failure taxonomy | 解析、無雜訊模擬、有雜訊模擬、可能的裝置參數模擬 | 若 transfer 不成立，產出 QAOA-specific 與一般 decision-theoretic 結構的 failure taxonomy；候選備案是不對稱 ranking/readout 任務。 |

### 1.3 章間銜接

- **Ch. 1 → Ch. 2：** 既然 estimator 變準仍可能選錯，就必須問危險的差異偏差能否在 runtime 被看見。
- **Ch. 2 → Ch. 3：** 看見風險後只會拒答會犧牲大量 coverage，因此下一步是證據能否支持校正或其他 action。
- **Ch. 3 → Ch. 4：** 一次性的最佳 action 會隨 calibration 變舊，因此決策還必須包含何時重新感測與切換。
- **Ch. 4 → Ch. 5：** 時序規則只有在跨任務與規模後仍能說清適用與失敗條件時，才具有一般研究價值。

### 1.4 為何維持五章順序

順序遵循「發現決策失敗 → 研究偏差可見性 → 把證據轉成動作 → 加入時間 → 測試轉移」的因果鏈。Ch. 4 不能先於 Ch. 3，因為序列決策需要已定義的一次性 action/loss；Ch. 5 不能先凍結 transfer task，因為要先知道 Ch. 3 哪些理論物件真正成立。

---

## 2. 進度總表

工時是 focused research time，不含等待外部審查、OSF 時間戳、硬體 queue、出版或大檔上傳。

| 章 | 已有產出 | 目前缺口 | 下一個可交付物 | 預估剩餘 focused work | 主要阻擋因素 |
|---|---|---|---|---:|---|
| Ch. 1 | 完整 repo、固定預算模擬、Proposition 1、論文稿 | 穩定引用／出版資訊與外部審查不在本專案控制內 | 1 頁 Ch. 1→2 interface note，固定可繼承定義與不可外推項目 | 4--8 h | 出版與第三方審查 |
| Ch. 2 | 凍結 protocol、一次 holdout、理論、paper、hardware readout addendum、E2 稽核 | release/DOI closure；將 P2/P3/E2 邊界正式交接給 Ch. 3 | 穩定 citation package＋已完成的 predecessor E2 audit/review | 4--8 h | release/DOI 決策由使用者控制 |
| Ch. 3 | 博論定位、四 Part、Gate 1A/1B 路由、前作 E2 稽核、RC assumptions、Vyas oracle audit、P2/CDR/P-amp 比較、novelty draft、文獻庫 | 尚無正式 likelihood、label construction、Gate 1 design lock、程式、開發資料、primary loss、power、holdout protocol | `gate1_math_spec_v1.md`＋`gate1_design_lock_candidate.md` | Part 1 約 45--60 h；全章約 200--250 h（約 24--28 週 × 8--10 h，含 verification） | RC closure、E2 semantics、visibility nuisance、P-amp 規格、abstention loss、算力與 power |
| Ch. 4 | 章問題、每月一次構想、電路 panel、qubit 選擇與欄位草案 | 無獨立時間戳 protocol、無授權、無時間序列、backend 可行性未確認 | longitudinal protocol v0＋authorization template；不送 job | 設計 16--24 h；若獲准，之後每月約 2--4 h 加 queue 等待 | backend 存續、平台規則、physical control 可見性、逐次授權 |
| Ch. 5 | lower-bound transfer、不對稱任務與 scale 的候選方向 | Ch. 3 理論尚未穩定，task/estimand 未選 | Ch. 3 Gate 2 後製作最多三個 transfer task 的 2 頁比較 | task selection 12--18 h；實驗工時待確認 | Ch. 3 定義、可算 ground truth、計算預算與 generalization boundary |

---

## 3. 第三章細部大綱

### 3.1 固定四 Part

| Part | 固定目的 | Gate | 允許證據 | 完成定義 |
|---|---|---|---|---|
| Part 1：Identifiability and label semantics | 凍結 E2 semantics、RC construction、likelihood、資訊分解、blind cases、P-amp fallback 與最小無雜訊核對 | Gate 1A、必要時 Gate 1B | 解析、無雜訊模擬 | Gate 1A/1B report；若通過，指定唯一 sensor；若皆失敗，停止 empirical-policy branch |
| Part 2：Decision relevance and correction | 檢驗 sensor output 是否預測 gap bias／翻號／correction benefit，定義 recalibration 與 uncertainty propagation | Gate 2 | 開發用有雜訊模擬；不得讀 confirmatory holdout | 開發期鎖定的 deployable estimator/correction rule 與 Gate 2 report |
| Part 3：Policy value, non-degeneracy, audit and freeze | 將 sensing、calibration、rerun、failure、abstention 全部入帳；檢驗淨收益與至少兩個 action；完成 power、adversarial audit 與獨立時間戳 | Gate 3、Gate 4 | 開發模擬、split-99 design/power；無 holdout | 唯一 primary rule、loss、threshold、manifest、protocol 與 registration record |
| Part 4：One-time confirmation and synthesis | frozen holdout 只讀一次、固定 endpoint scoring、獨立重算、claim ledger、paper 與 hardware go/no-go | 不新增設計 Gate | 確認性有雜訊模擬；可選 fake backend 另列；硬體另案 | confirmatory report、reproducibility package、章／paper draft |

Part 不因前一 Part 結果改題。若 gate 失敗，取消不再有科學意義的實證工作，改完成同一 Part 已預先寫下的負面／理論交付物，不加入新方法。

### 3.2 四道生死關與路由

| Gate | 通過判準 | 失敗判準 | 失敗後唯一允許路徑 |
|---|---|---|---|
| 1A：RC-label identifiability | 僅使用 label-contrast information `I1` 與將未知 ideal response／visibility 視為 nuisance 後仍可部署的 efficient/profile information `I3`；`(epsilon, phi)` 在至少一個事前凍結設計下 full rank，且無雜訊 recovery 與解析 rank 一致。已知 ideal-response 的 absolute-level `I2` 只能診斷，不能通過。 | 所有允許設計中 `epsilon` admitted information 為 0／rank deficient；或 full rank 只來自 ideal target、true parameter、structure label、simulator derivative 等 oracle。 | 保留 RC-label blindness／negative-identifiability 結果；不得調整 RC 設計；只進執行前完整凍結的 Gate 1B。 |
| 1B：P-amp identifiability | 事前凍結的 amplification repetitions、echo reference、angle/grid、budget、aliasing 與 power 條件全部通過；無 target ideal value；無雜訊 recovery 達事前 tolerance。 | rank、recovery、budget、visibility robustness 或 no-alias 條件任一失敗。 | 停止 empirical-policy branch；完成三動作理論、blindness lemma、finite-pilot lower bound、Gate 1A/1B 負面實例；不新增第三種 sensor。 |
| 2：decision relevance | 在 development-only units 上，事前固定且可部署的規則對 correction-benefit sign 或等價 decision target 優於 frozen no-information baseline，並達事前 uncertainty criterion；不使用 ideal gap／error label。 | 只能估 gate parameter、無法預測 gap/flip/correction benefit；或 improvement 只在 oracle rule 出現。 | 結束 adaptive-correction claim；保留 identifiability 與「parameter estimation 不足以決策」的結果；不進 confirmatory adaptive-policy holdout。 |
| 3：net value | 在固定 total `N`、鎖定 loss 與 cluster uncertainty 下，sensor policy 相對 development-locked best fixed policy 的 improvement lower bound > 0。 | 改善非正、依賴未入帳 calibration/rerun、或在 primary abstention cost 下消失。 | 報告 value-of-information/resource boundary；不放大預算、不換 loss、不進 confirmatory policy test。 |
| 4：policy non-degeneracy | 事前固定 strata 下至少兩個 action 的選擇率均超過由 power 支持的最小頻率，且不是 tie-break artifact。 | always-correct、always-abstain、effectively no-action，或某 action 太少而無法估 loss。 | 報告 fixed-action collapse；不得在看到結果後改 threshold 讓 policy 看起來 adaptive。 |

### 3.3 Gate 1「一頁數學問題」規格

令 `k` 表示 candidate，`ell` 表示 cost layer／rotation，`t` 表示 compiler label：

- `theta_{k ell}`：凍結的 logical cost angle；
- `g_t(theta_{k ell})`：label absorption 後的 compiled representation；
- `epsilon`：乘法 over-/under-rotation；
- `phi`：固定加法相位；
- `b`：可觀測 outcome；
- `s_t`：由 compiler 記錄且與未知參數獨立的 label sign。

必須分開三種 E2 定義：

1. **Logical-angle E2：** 先對 logical `theta` 施加 `(1+epsilon)`，再做 frame/label bookkeeping。前作 `bias-probe-visibility` 在其實作下等價於此模型。
2. **Compiled-angle E2：** 對 label absorption 後實際編譯角度 `g_t(theta)` 施加比例誤差。
3. **Physical-control E2：** 誤差作用於 pulse amplitude/duration 或 composite implementation 的控制參數；virtual `RZ` 不得冒充 physical pulse。

Gate 1A 必須從實際凍結 construction 推導

```text
P(b | t, epsilon, phi, nuisance)
```

而不是從 `X RZ(theta) X = RZ(-theta)` 直接猜 error sign。依目前未定稿的 frame-covariance 推導，logical-frame phase 可能為

```text
alpha_t = (1 + epsilon) theta + s_t phi,
partial_epsilon alpha_t = theta,
partial_phi alpha_t = s_t.
```

若此式成立，balanced label contrast 在 `phi=0` 對 `epsilon` 的一階資訊為 0；absolute outcome 仍可能依 `epsilon` 改變，但若需要 ideal response 才能反推，不能算 Gate 1A 通過。

應分開報告：

- `I1`：label contrasts 本身的 Fisher／identifiability；
- `I2`：假設 ideal response 已知時的 absolute-level Fisher，只作 oracle diagnostic；
- `I3`：將 ideal response、visibility、offset 等視為 nuisance 後，`epsilon` 的 efficient/profile information；
- finite-separation：選兩個對 runtime evidence 近似不可區分、但最佳 action 不同的 latent states，用 total variation、Hellinger、KL 或 Le Cam 路線建立有限 pilot 下界。

角度集合條件：

- 若觀測方程只依 `epsilon theta_k + phi`，只有單一有效角度時 design rank ≤ 1；
- 至少兩個不同、且 measurement score 非零的有效角度是區分 `epsilon` 與 `phi` 的必要候選條件，但不保證 label-only deployability；
- 兩個 candidate 的不同 `gamma` 可提供不同角度，但不能使用 unknown ideal gap 當輸入；
- depth 1＋單一 candidate／單一有效角度列為預期 blind 的 negative control。

### 3.4 Gate 1 最小模擬規格

這是預定規格，執行前仍需在 design lock 中填入 exact grid、seed、shots 與 tolerance。

| 欄位 | 最小規格 |
|---|---|
| Qubit 數 | 2 與 3 qubit 都做；2 qubit 用於完整列舉／解析交叉核對，3 qubit 檢查非平凡 candidate/context。 |
| Cost layer | Primary：1 個 cost layer；只在事前指定的 identifiability extension 中加入 `p=2`，不得因 `p=1` 失敗後臨時加入。 |
| Candidate | 至少一個 single-candidate blind control；一對不同 `gamma` candidate 用於多角度設計；candidate 生成規則在執行前固定。 |
| E2 semantics | logical、compiled、physical-control proxy 分開；Gate 1 primary semantics 必須在執行前選定。physical-control 若無可信實作則標 `not modeled`，不假造。 |
| Additive phase | `phi=0` 為必要 negative control；非零、正負對稱的小格點檢查 label sign sensitivity。格點需在 design lock 中列明。 |
| 要估統計量 | label-outcome contrast、absolute-level response、profile score／efficient Fisher、rank／condition number、`epsilon_hat`／`phi_hat` recovery error；P-amp 另報 aliasing 與 repetition visibility。 |
| Oracle diagnostic | 可計算 ideal response 只用來形成 `I2` 與 simulator sanity check，不得進 deployable estimator／pass criterion。 |
| 事前預測 | logical-angle模型與目前 frame bookkeeping 下，Gate 1A 對 `epsilon` 預期 blind；label 可能看見 `phi`。單一有效角度下 `(epsilon,phi)` 預期不可辨識。P-amp 在 rank/no-alias/visibility 條件滿足時可能識別，但這不是結果。 |
| Pass／fail | 以 Gate table 為準；numerical tolerance、minimum eigenvalue／condition rule 與 recovery grid 必須在任何相關輸出存在前固定。 |

### 3.5 唯一主要終點與可部署政策

對 unit `u` 定義事前鎖定 loss：

```text
L_u = 1{作答且選錯}
    + lambda_A * 1{拒答}
    + lambda_F * 1{校正／重跑失敗}.
```

唯一 primary statistic：

```text
Delta_V = mean_u[L_fixed,u - L_policy,u].
```

其中：

- `policy` 只能讀 Gate 1 通過之 sensor runtime data、已知 circuit metadata、事前宣告可在 runtime 計算的量；
- 禁止讀 target ideal value、true `epsilon`、error-structure label、future calibration 或 holdout outcome；
- `fixed` comparator 從 no action、always recalibrate、always abstain 中只用 development data 選一次並鎖定；
- sensing、reference、calibration、recalibration、rerun、失敗 shots 全部包含於同一 `N`；classical compute 與 circuit count 另報但不藏起來；
- `lambda_A`、`lambda_F`、uncertainty method 與 success threshold 必須在 holdout 前獨立時間戳。

次要：false certification、coverage、parameter calibration、gap/flip prediction、oracle regret、loss sensitivity。探索性：fake backend、`p=2` extension、其他 graph family、一天 CRN variance component。

### 3.6 方法預期失敗條件

| 方法／主張 | 應失敗的條件 |
|---|---|
| Gate 1A labels→`epsilon` | label 不改變 noisy physical quantity；multiplicative term 在 logical frame 對 label 不變；單一有效角度；score 為 0；資訊只來自 ideal response。 |
| Gate 1B P-amp | repetition 造成 visibility collapse；echo/reference 不重現 target-context error；negative angle 誤差不對稱；drift；phase alias；固定預算 power 不足。 |
| P2 comparator | Clifford twin 與 target 對 angle-dependent error 的 response 不可轉移；alarm 與 flip/correction benefit 無關。 |
| parameter→decision | candidate gap 對參數不敏感；其他未量測誤差主導；相同 `epsilon` 在不同 context 引起不同 gap bias。 |
| recalibration | 模型錯置、estimate uncertainty 大於 margin、校正後已漂移、rerun cost 吃掉收益。 |
| abstention | alarm 未校準到 decision error、matched null 也常警報、coverage cost 大於錯答損失。 |
| three-action policy | 某個 action 在所有 unit 都支配；threshold 只製造表面多樣性；需要 oracle 才能分流。 |
| Fisher/local analysis | global alias、boundary/nonregular likelihood、離 local point 太遠。 |
| finite-pilot lower bound | 兩點不在凍結 model class、action 不真的不同、或 bound 在研究預算下過鬆。 |
| CRN 附屬檢查 | between-compilation component 很小、covariance 非正，或 bias 未移除而 CI 變窄。 |

### 3.7 與 QAOA/E2 無關、Gate 1 失敗仍成立的理論骨架

下列物件先以 latent state `eta`、runtime evidence `S`、actions `A={no action, correct, abstain}`、budget `N` 與 loss `L(a,eta)` 表示：

1. 三動作 risk identity／pairwise action-value condition；
2. action-selection blindness lemma：相同 evidence law 對應不同 optimal action；
3. finite-pilot lower bound：有限 sensing budget 下選錯 action 的不可避免機率；
4. value-of-information condition：預期 action-loss reduction 必須大於 sensing／rerun cost；
5. policy non-degeneracy 定義與 fixed-action collapse 的誠實結論。

即使 Gate 1A、1B 都失敗，以上理論仍可構成完整章；QAOA/E2 只作第一個具體不可辨識實例，不把失敗隱藏。

---

## 4. 第四章平行準備：每月漂移研究

### 4.1 授權與登記邊界

- 本節只規劃，不授權任何 job。
- 第一次執行前，完整 protocol、circuit hashes、backend/qubit rule、analysis、stopping rule 與欄位必須取得 OSF 等獨立時間戳，才可稱 registered/preregistered。
- 每一個月仍需使用者另外明確授權；上月授權不延伸到下月。
- 同日執行前重新檢查平台規則、backend availability 與 protocol version；若不符合就記錄 missed month，不臨時換較好的 qubit/backend。

### 4.2 最小電路 panel

| Panel | 電路／準備 | 目的與限制 |
|---|---|---|
| Reference | `|0>`,`|1>`,`|+>`,`|+i>`；依需求做 X/Y/Z basis measurement | 分開 SPAM、phase-sensitive 與 population-sensitive drift。 |
| Mixed preparation | 事前固定的 50:50 classical mixture：`|+>` 與 `|+i>`；每個 circuit 保留 preparation label，不先 pooling | 檢驗結論是否只對單一 preparation 成立。 |
| Phase-sensitive | Ramsey-like `H -- phase operation -- H/S`，兩個固定角度 | 只有 backend representation 具有物理意義時才執行；virtual `RZ` 不當作有 pulse error。 |
| Two-qubit context | 最短可支援 entangling-gate echo／identity-like sequence，加一個固定 idle-depth control | 追蹤 context/crosstalk；不能從單一 pair 推廣全 backend。 |
| Matched null | 邏輯等價但無注入 phase perturbation 的 circuit | 監測 false alarm、SPAM 與 analysis artifact。 |

### 4.3 Backend 與 qubit 選擇規則

1. protocol 登記前選定一個使用者方案可用且支援 panel 的 backend；序列期間固定。
2. primary single qubit：滿足事前功能條件的最小 index operational qubit，不按當日 fidelity 挑最好者。
3. primary pair：支援所需 entangling instruction 的 lexicographically first operational directed edge。
4. fallback 按 lexicographic 順序事前列出，只能因明確 unavailable reason 啟用；同月不得巡迴搜尋好看的 pair。
5. calibration metrics 在 qubit 選定後才記錄，不用當日結果反選 qubit。
6. backend 消失或 instruction 改變時暫停，寫 protocol amendment；不把新 backend 與舊序列無註記拼接。

### 4.4 每次必記欄位

- protocol version、independent-registration identifier、repository commit、circuit manifest hash、analysis version；
- 本次使用者 authorization record；
- backend、service/channel、region（若提供）、backend status；
- UTC submission/start/completion timestamp、provider calibration timestamp；
- job ID、session ID、execution mode、shots、circuit count；
- transpiler version、optimization level、layout、routing、seeds、basis/native instructions；
- physical qubit indices、directed coupling、schedule/duration metadata（若可得）；
- selection 完成後才讀取的 readout metrics、T1、T2、gate error/duration 與各自 timestamp；
- randomized label、preparation label、angle、repetition/depth、circuit hash；
- raw counts、partial/failed jobs、cancellation reason、queue/runtime metadata、provider messages（不得含 credential）；
- Python/Qiskit/runtime/OS versions 與 analysis log；
- evidence label 固定為 `hardware-derived`，並註明單 backend／單時間序列不支持普遍性。

### 4.5 月節奏與分析限制

- 目標：至少 6 個月，每 28--35 天一次；missed month 保留 missing，不用同月雙跑補值。
- 每月可產生 descriptive QC summary，但不得依月結果改 circuit、qubit、threshold 或 final test。
- longitudinal hypothesis 只在事前固定 milestone 評分；若要用 confidence sequence，須在 Month 1 前推導、測試並登記。
- Ch. 4 time series 不作 Ch. 3 confirmatory evidence，也不回頭調整 Ch. 3 holdout rule。

---

## 5. 第三章詳細時程

### 5.1 工時模型與里程碑

- **每週：** 8--10 focused hours（待確認）。
- **開始：** 2026-11-23（待確認）。
- **基準長度：** 26 週，約 208--260 小時；符合全章約 200--250 小時的規劃量級，差額以 scope cut 或日期後移處理，不壓縮 verification。
- **最早停損點：** Week 6（2026-12-28 至 2027-01-03）。Gate 1A 失敗時只跑已凍結 Gate 1B；兩者都失敗時 empirical-policy branch 在 Week 6 結束。
- **確認性資料最早時間：** Week 19，且只在 Gates 1--4 通過、audit 完成、clean commit 與獨立時間戳存在後。

### 5.2 Week 0：已完成的 pre-work（不算正式執行結果）

| 日期 | 已有項目 | 證據狀態 |
|---|---|---|
| 至 2026-11-20 | 前作 E2 audit/review、RC assumption table、Vyas oracle audit、P2/CDR/P-amp comparison、novelty branches、文獻庫 | planning／read-code／literature synthesis；沒有 Gate 1 模擬結果 |

### 5.3 逐週主時程

| 週 | 日期 | Part | 主要工作（固定內容） | 週末可驗收交付物 | 禁止提前做的事 |
|---:|---|---|---|---|---|
| 1 | 2026-11-23--11-29 | P1 | 整合前作 audit、RC/Vyas/P2 文獻；列出 unresolved decisions；凍結 terminology：logical/compiled/control、label、frame、sensor、oracle | model-and-claim ledger；owner decision list（primary E2 semantics、`lambda_A` 決策時點、correction action） | 不執行 Gate 1 grid；不產生 noisy development data |
| 2 | 11-30--12-06 | P1 | 寫 `gate1_math_spec_v1.md`：`P(b|t,epsilon,phi,nuisance)`、angle set、single-angle blindness、multi-angle necessary condition、Vyas model-match | 一頁數學問題＋完整 appendix derivation route | 不用 ideal response 讓 deployable Fisher 看似 full rank |
| 3 | 12-07--12-13 | P1 | 寫 RC construction contract：`C,G,T,T^c`、boundary cycles、label storage、compiled angle；逐 label 無雜訊 logical-equivalence test 設計 | RC closure/semantics checklist；測試規格，不是結果 | 不在 closure 失敗後臨時更換 twirl group |
| 4 | 12-14--12-20 | P1 | 推導與審查 `I1/I2/I3`；建立 finite-separation lower-bound 候選；完成 blind/null/positive controls | information decomposition note；lower-bound candidate pair ledger | 不選擇讓結果漂亮的 parameter pair |
| 5 | 12-21--12-27 | P1 | 完成 P-amp circuit、repetitions、echo、grid、budget、power/no-alias 條件；P2 same-budget comparator；adversarial pre-Gate review | `gate1_design_lock_candidate.md`；Gate 1A/1B/P2 完整 manifest | Gate 1A 結果存在後不得修改 P-amp/P2 |
| 6 | 12-28--2027-01-03 | P1 | 只跑鎖定的解析／無雜訊 Gate 1A；若且僅若失敗，跑鎖定 Gate 1B；P2 只按 comparator contract 執行 | **Gate 1 report；最早 kill point；唯一 sensor 指定或 empirical branch STOP** | 不加入第三種 sensor；不縮 grid／放寬 tolerance |
| 7 | 01-04--01-10 | P1→P2 | 若 1A/1B 通過：完成 Part 1 report、鎖定 development noisy model 與 units；若皆失敗：完成 negative-identifiability chapter route與 general theory workplan | Part 1 report；branch declaration | STOP branch 不得偷偷執行 Gate 2 simulation |
| 8 | 01-11--01-17 | P2 | 定義 `epsilon_hat` uncertainty、candidate gap bias estimand、flip/correction-benefit target、deployable inputs與 oracle diagnostics | Gate 2 method contract | 不用 ideal gap 作 policy feature |
| 9 | 01-18--01-24 | P2 | 建 development-only graph/candidate/noise strata、seeds、nulls、sample-size feasibility；實作前測試規格 | development manifest＋unit/semantic test plan | 不建立 confirmatory holdout outcomes |
| 10 | 01-25--01-31 | P2 | 執行 development noisy simulation；分開 method/model/resource failures；保留 null/negative results | Gate 2 evidence bundle（development） | 不看結果改 Gate 2 target |
| 11 | 02-01--02-07 | P2 | out-of-sample development scoring、uncertainty、P2 comparator；判定 parameter 是否具 decision relevance | **Gate 2 report與 GO/STOP** | 失敗後不換成較容易的 prediction metric |
| 12 | 02-08--02-14 | P2→P3 | Gate 2 通過才凍結 correction operation、uncertainty propagation、failure handling；完成 Part 2 report | correction contract＋Part 2 report | 不允許多種 correction 在 holdout 後挑最好者 |
| 13 | 02-15--02-21 | P3 | 定義完整 budget ledger、actions、fixed baselines、candidate `lambda_A/lambda_F`；使用者決定 primary loss 或 constrained endpoint | policy/loss decision record | 不以探索性 loss 取代 primary loss |
| 14 | 02-22--02-28 | P3 | power analysis：primary paired value、graph clustering、action frequencies；執行一天 CRN variance-component check並依規則停止 | power report＋CRN stop memo | CRN 不得被描述成 bias correction |
| 15 | 03-01--03-07 | P3 | development policy evaluation、threshold calibration、fixed comparator selection一次 | **Gate 3 report與 GO/STOP** | Gate 3 失敗不加 shots／換 comparator |
| 16 | 03-08--03-14 | P3 | action-frequency／tie-break／strata檢查 | **Gate 4 report與 GO/STOP** | 不為製造多 action 改 threshold |
| 17 | 03-15--03-21 | P3 | adversarial pre-data audit：endpoint、oracle leakage、budget、missing/failed units、ties、multiplicity、artifact provenance | adversarial audit＋issue closure ledger | unresolved critical issue 時不得 freeze |
| 18 | 03-22--03-28 | P3 | 最終 protocol、hashes、environment lock、single-run marker、independent timestamp；holdout preflight 不讀 outcome | registration package＋confirmatory GO/NO-GO | 沒有獨立時間戳不得稱 preregistered |
| 19 | 03-29--04-04 | P4 | frozen holdout 執行一次；保留 raw rows、failure、marker與log | immutable raw evidence package | 不重跑失敗 unit，除非 frozen rule 明確允許 |
| 20 | 04-05--04-11 | P4 | 只評分唯一 primary endpoint與 frozen secondary endpoints一次 | confirmatory report v0 | 不增 endpoint／subgroup |
| 21 | 04-12--04-18 | P4 | 獨立重算、seed/hash/provenance、cross-platform deterministic checks | verification report | 內部重算不得稱第三方驗證 |
| 22 | 04-19--04-25 | P4 | failure taxonomy、negative/null/nonevaluable classification、claim ledger | locked claim ledger | hypothesis 不得寫成 observed cause |
| 23 | 04-26--05-02 | P4 | paper：Abstract、Introduction、Methodology、Experiment Setup、Results | first-half paper draft | 結果證據類型不得混寫 |
| 24 | 05-03--05-09 | P4 | paper：Conclusion、Discussion、limitations、References、appendix derivations | full paper/chapter draft | 不擴大存在性結論 |
| 25 | 05-10--05-16 | P4 | figures/tables from manifests、citation audit、reproducibility README、release checklist | release candidate | 不手動修改 generated result numbers |
| 26 | 05-17--05-23 | P4 | 外部閱讀包、回應清單、Ch. 3→4 interface、hardware addendum go/no-go（只決策，不送 job） | chapter package＋next-chapter handoff | 不把硬體列為完成條件 |

### 5.4 Gate failure 後的預定時程

| 觸發 | 取消 | 保留的 2--6 週交付物 |
|---|---|---|
| Gate 1A fail、1B pass | RC-label empirical claim；其餘週次日期原則不變 | RC-label negative result；P-amp 作唯一 sensor；P2 comparator；新穎性限於 decision layer |
| Gate 1A、1B 都 fail | Weeks 8--20 empirical policy work與 holdout | 三動作 risk、blindness lemma、finite-pilot lower bound、RC/P-amp negative examples、negative chapter draft；不新增 sensor |
| Gate 2 fail | Weeks 13--20 adaptive policy與 holdout | identifiability report、parameter≠decision theorem/empirical boundary、correction-insufficiency analysis |
| Gate 3 fail | Gate 4與confirmatory policy holdout | value-of-information/resource boundary、cost sensitivity（仍以 frozen primary 為主）、negative paper |
| Gate 4 fail | confirmatory adaptive-policy holdout | fixed-action collapse、non-degeneracy theory、development-only comparison，清楚標 evidence level |
| pre-data audit critical issue | freeze與holdout延後 | 修正 implementation/protocol bug；科學內容不改；重新 clean lock與獨立時間戳 |

### 5.5 第四章平行日程（不自動執行）

| 時段 | 工作 | 授權狀態 |
|---|---|---|
| Weeks 1--4 | protocol draft、backend capability check、circuit/hash schema、authorization template | 只讀／規劃；不得送 job |
| Weeks 5--8 | 外部審查、修訂、可行性與成本確認 | 仍不得送 job |
| Week 9 以後 | 若使用者決定啟動，取得獨立時間戳 | 登記不是執行授權 |
| Month 1 | 登記完成後，另行請求第一次明確授權 | 無授權即不執行 |
| Months 2--6 | 每 28--35 天重新請求一次授權並按固定 rule 執行 | 不預設延續授權 |
| Frozen milestone | longitudinal scoring／confidence sequence update | 不依單月好壞改 protocol |

### 5.6 每週固定工作流

每週只維持必要研究基礎設施：

1. 週初：確認本週 input commit、允許資料層、驗收條件與禁止事項。
2. 執行前：tests／semantic checks；記錄 environment 與 seed manifest。
3. 產出時：raw→derived→report provenance 分開；證據標籤不可省略。
4. 週末：交付物 review、decision ledger、unresolved issue；未通過則同一週內容延後，不偷跑下一 Gate。
5. Commit：一個科學決策或可驗收交付物一組 commit；不混入無關 refactor。
6. 外部 AI review：提供 commit link、指定 review 問題與 evidence boundary；AI 意見是 review，不是獨立驗證。

### 5.7 使用者仍需確認的項目

1. 是否確認每週 8--10 小時與 2026-11-23 起算；否則提供新工時／日期。
2. Gate 1 primary E2 semantics：logical、compiled 或 control model 中哪一個作主要存在性問題；其他作 secondary/diagnostic。
3. `correct` 的唯一操作：estimated angle recalibration＋second execution，或另一個具體 compiled correction。
4. `lambda_A` 與 `lambda_F` 的實務意義；若無法合理 scalarize，是否改用事前固定 constrained endpoint。
5. 是否現在只完成 Ch. 4 protocol draft，還是未來另行啟動每月硬體序列；任何選項都不等於授權實際 job。

---

## 驗收清單

- [ ] 每週工時與開始日期經使用者確認或修訂。
- [ ] 四 Part、Gate 1A→1B 路由與唯一 primary endpoint 未被結果導向修改。
- [ ] Gate 1 math specification 經審查。
- [ ] P-amp、P2 comparator、grid、budget與 pass/fail 在 Gate 1A 前完整鎖定。
- [ ] 無 noisy development data 在 Part 1 lock 前產生。
- [ ] 無 holdout outcome 在 audit、clean lock 與獨立時間戳前產生。
- [ ] 所有 evidence 明標 analytic／noiseless simulation／noisy simulation／device-parameter simulation／hardware-derived。
- [ ] 無硬體 job 在另行 protocol、獨立時間戳與當次使用者授權前送出。
- [ ] negative、null、failed、nonevaluable 結果皆保留。
- [ ] 結論限定於凍結 model/task/resource 下的存在性或邊界，不宣稱普遍規律。

