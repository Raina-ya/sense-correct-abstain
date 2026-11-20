# 前作 E2 稽核：bias-probe-visibility

狀態：稽核報告（2026-11-20）。只讀前作的程式、文件與已提交的結果，沒有改動前作，也沒有產生新的研究資料。

**稽核對象：** `Raina-ya/bias-probe-visibility`，commit `cd5e5764eabff6f51c406048be393bfd109130d5`（2026-11-19，"Paper v4.2 …"）。下文的檔案路徑都相對於該 repo，行號以這個 commit 為準。

**證據標示：**
- **〔讀碼〕** 直接讀程式或文件得到的事實。
- **〔前作結果〕** 前作已提交的結果檔，證據類型為有雜訊模擬（holdout 只讀一次）。
- **〔稽核核對〕** 本次稽核用前作程式做的無雜訊精確計算，只用來確認讀碼結論，不是新的研究結果。
- **〔解釋〕** 本稽核的推論，沒有被檢驗過。

## 摘要

1. 前作的 E2 作用在**轉譯後、被標記的 cost `RZ`（`rzc`）的參數**上，執行時才乘上 (1+ε)。轉譯不改動角度，frame 也從不併入這個 `RZ`，所以它**等價於邏輯角度模型**：目標電路在 E2 下與「γ 改成 (1+ε)γ 的理想電路」逐位相同，前作有測試鎖定這一點。不是實體控制參數模型。
2. 前作的「frame」是在每個 CX 前後插入**獨立的 X 閘**，16 個固定版本，從不穿過或併入 cost `RZ`，而且 X 閘無雜訊。所以前作**沒有任何 label 吸收進 cost 旋轉的機制**，第三章的 RC-label 建構必須新寫。
3. P3 對 E2 是**看不見的**（invariant, blind）。分析初稿曾標成 visible，後來被語意測試推翻並更正，凍結版是 blind。前作 E2 的改善來自 **P2（Clifford twin）**，不是 P3。
4. 前作的主要規則 R1 依「結構→指定探針」選探針，**用到了結構標籤**，在第三章的定義下不可部署；只有「每個結構都用 P2」的次要規則與結構無關。
5. E2 的 false certification 最嚴重是已觀察的事實（holdout FC(R0) = 0.0609，195 次、集中在 7 張圖）。「為什麼」目前只有解釋，沒有檢驗。

## 1. E2 實際作用在哪裡？

**結論：** 作用在轉譯後被標記的 cost `RZ`（`rzc`）的參數上。這個參數等於邏輯角度 γ（不 wrap），frame 也不改它，所以對第三章而言等價於**邏輯角度模型**；不是實體控制參數。

| 證據 | 位置 | 類型 |
|---|---|---|
| 邏輯電路：每條邊 `qc.rzz(gamma, i, j)` | `src/circuits.py` 65–76 | 〔讀碼〕 |
| 用 Qiskit 轉譯（basis `rz,sx,x,cx`、identity layout、routing `none`、optimization level 0），再把每個 `CX(c,t) RZ(t) CX(c,t)` 中間的 `RZ` 改名為 `rzc` | `src/circuits.py` 94–122（標記：33–47）；說明 13–15 | 〔讀碼〕 |
| 凍結協定：轉譯後標記 cost rotation；E2 在執行時作用於每個被標記的 cost rotation | `docs/freeze/frozen_protocol_v4.md` 132–135 | 〔讀碼〕 |
| E2 定義表：每個被標記的 `RZ(theta)` 執行成 `RZ((1+epsilon)*theta)`，目標與探針電路皆然，包含 folding 的反閘與 twin；格點 ε ∈ {±0.005, ±0.01, ±0.02, ±0.04} | `docs/freeze/frozen_protocol_v4.md` 148 | 〔讀碼〕 |
| 測試 `test_e2_target_equals_scaled_logical_rzz`：E2 ε = 0.04 的目標分布等於把 γ 改成 1.04γ 的無雜訊目標分布（atol 1e-12） | `tests/test_v4.py` 168– | 〔讀碼〕 |
| `rzz(0.37)` 與 `rzz(5.9)` 轉譯後的 `rz` 參數分別就是 0.37 與 5.9，沒有 wrap（Qiskit 2.6.2；前作 run log 記錄 Qiskit 2.2.3，未用該版本重跑） | 稽核當場核對 | 〔稽核核對〕 |
| 模擬器沒有任何脈衝或控制參數模型 | `src/simulate.py` 全檔（1–169） | 〔讀碼〕 |

**對第三章的含意：** 第三章計畫的「compiled-angle model」與「control model」在前作中都不存在。前作只提供邏輯角度模型的實作與測試。

## 2. E2 怎麼寫進程式？

**結論：** 是 θ → (1+ε)θ，但時機是**轉譯並標記之後、在模擬器執行時**才乘。電路本身的參數不修改。

| 證據 | 位置 | 類型 |
|---|---|---|
| `GateNoise.over_rotation`（E2 的 ε） | `src/simulate.py` 41–45 | 〔讀碼〕 |
| 執行迴圈：遇到 `rzc` 時執行 `_rz((1.0 + noise.over_rotation) * params[0])`；其他單量子位元閘照原矩陣、無雜訊；CX 之後才有 E1／E3 的掛鉤 | `src/simulate.py` 132–151（E2：147–148） | 〔讀碼〕 |
| 結構設定：`parse_condition("E2", value)` 產生 `GateNoise(over_rotation=value)`，並把 ε 記在 `Condition.epsilon` | `src/channels.py` 30–38、49–58 | 〔讀碼〕 |
| folding 的反閘是 `rzc(-theta)`，也被乘上 (1+ε)，所以 G G† G = G，折疊後的錯誤與原電路完全相同（第一篇「folding 看不到 over-rotation」的機制） | `src/circuits.py` 160–184；測試 `tests/test_v4.py` 143–153 | 〔讀碼〕 |
| Clifford twin 把 `rz`／`rzc` 角度四捨五入到 π/2 的倍數，E2 再乘在這個四捨五入後的角度上；角度為 0 的不受影響 | `src/circuits.py` 187–204；`docs/theory/06_matrix_v4.csv`（P2,E2 列） | 〔讀碼〕 |

**γ 的範圍：** 每個 cost angle 從 [0, 2π) 均勻抽取（`docs/freeze/frozen_protocol_v4.md` 90–97）。由於不 wrap，εγ 的大小取決於 γ 在 [0, 2π) 中的代表值：γ 接近 2π 的旋轉在邏輯上接近恆等，卻承受最大的 over-rotation。〔讀碼〕＋〔解釋〕

## 3. Pauli／frame／RC label 如何保存或合併？

**結論：** 前作沒有 RC label 吸收。它使用 16 個固定的 X-only frame 版本，以獨立的 `x` 運算插在每個 CX 前後，不合併進任何旋轉，也不穿過 cost `RZ`；X 閘在模擬器中無雜訊。label 以版本編號保存在電路標籤與帳本中。

| 證據 | 位置 | 類型 |
|---|---|---|
| `frame_rows(width)`：16 列強度 2 正交陣列（Sylvester–Hadamard 欄 1..w），每列每個 qubit 一個 0/1 | `src/circuits.py` 207–228；平衡性測試 `tests/test_execution.py`（`test_frame_rows_are_strength_two_balanced`） | 〔讀碼〕 |
| `framed(compiled, row)`：每個 CX(c,t) 前插 `X^a_c X^a_t`，後插共軛後的 `X^a_c X^(a_c xor a_t)_t`，使邏輯 unitary 不變；其他運算（含 `rzc`）原樣保留 | `src/circuits.py` 231–255 | 〔讀碼〕 |
| 只有 X，沒有 Y／Z；不是逐 shot 隨機，而是 16 個固定版本 | 同上 | 〔讀碼〕 |
| label 保存：版本以 `frame{c}_{h}` 命名，c 為候選、h 為列號 | `src/execution.py` 156–161 | 〔讀碼〕 |
| 每個電路的 shots、counts、`circuit_sha256` 寫進每列資料的帳本 | `src/execution.py` 328–356（`ledger.append` 在 350 行） | 〔讀碼〕 |
| P3 統計量 = \|plain gap − 16 個 framed gap 的平均\| | `src/probes.py` 73–83 | 〔讀碼〕 |
| 單量子位元閘（含 frame 的 `x`）在模擬器中沒有雜訊掛鉤 | `src/simulate.py` 136–150 | 〔讀碼〕 |
| 凍結矩陣：P3/E2 invariant, blind，理由是「X frame 只作用在每個 CX 周圍；CX 之間的非 Clifford cost rotation 沒有被 twirl」 | `docs/theory/06_matrix_v4.csv`（P3,E2 列） | 〔讀碼〕 |
| 分析初稿 `06_matrix.md` 曾把 P3/E2 標成 visible (medium)；第一輪語意測試推翻，凍結前更正為 blind | `docs/theory/06_matrix.md` 222–224；`docs/freeze/frozen_protocol_v4.md` 215–233（表中 227 行） | 〔讀碼〕 |
| 語意測試：P3/E2 在最強設定與 matched null 之間的最大差值 3.9e-16（invariant） | `experiments/semantic/semantic_tests_v4.csv` 第 17 行 | 〔前作結果〕（精確期望值計算） |
| 稽核核對：4 qubit、depth 2 的例子，E2 ε = −0.04 下 16 個 framed 版本與 plain 的分布最大差值 0.0；對照組 E3 ζ = 0.04 的差值 0.033 | 用前作 `src/circuits.py`、`src/simulate.py` 計算 | 〔稽核核對〕 |

**對第三章的含意：**
- 前作完全沒有「label 改變 cost `RZ` 實體角度」的情況，所以它**既不支持也不否定** frame-covariance 草稿；兩者描述的是不同的建構。
- 前作的 E3 可見性（X frame 讓 ZZ 誤差變號）與草稿中 φ 型誤差隨 label 翻號是同一類機制。〔解釋〕
- 第三章需要新的 label 建構：frame 必須穿過 cost `RZ` 並被吸收，且吸收規則（sign flip、Z 是否 virtual、是否 wrap）要明確凍結。這與 GitHub 主計畫 §3.4 的寫法一致（"not inherited from predecessor P3"）。

## 4. 前作是否記錄了理想值、oracle 標籤或不可部署資訊？

**結論：** 有，但與探針隔離。理想 gap 只在 `reference.py` 中計算，用於設計時的強度選擇與事後計分；探針函式的簽名被測試禁止接受理想值。不過原始資料列記錄了真實的結構與 ε，而主要規則 R1 依結構選探針，在第三章的定義下不可部署。

| 項目 | 位置 | 可部署嗎（第三章定義） |
|---|---|---|
| 理想 gap 與有雜訊母體 gap（`ReferenceGap.ideal_gap`、`noisy_population_gap`、`harmful_ratio`、`flipped`），只用於強度圖（開發）與事後計分（holdout） | `src/reference.py` 1–7、22–51、85–96 | 否，只能計分 |
| 探針函式不得接受理想值，以參數名稱檢查（禁止 `ideal`、`truth`、`true_gap`、`target_reference`） | `tests/test_execution.py` 114–124；`src/probes.py` 1–5 | — |
| 原始資料列不得含目標理想值 | `tests/test_execution.py` 141–153 | — |
| 原始資料列記錄 `structure`、`setting`（即真實 ε）、`parameter_index` | `src/execution.py` 66–95、362–382（`structure`、`setting` 在 370–371 行） | 否：這是 oracle 標籤，只能用於分組與計分 |
| P2 使用 twin 自身的無雜訊參考 gap（古典計算，宣告為執行時可算） | `src/execution.py` 404–414 | 是（已知參考，不讀目標理想值） |
| R1 的指定探針：E1→P1、E2→P2、E3→P3、E4–E6→P4a | `src/cells_v4.py` 37–46；`docs/freeze/frozen_protocol_v4.md` 404–420 | **否**：需要知道誤差結構 |
| 結構無關的次要規則：每個結構都用 P2 | `docs/results/primary_endpoint_v4.md` 35–37 | 是（就結構而言） |
| 主操作點的正負號選擇：同一強度下，取開發集 β/Δ 中位數較小（較有害）的那一側；E2 主點因此是 ε = −0.04 | `src/strength_map.py` 3–8、116–135；`results/development_v4/strength_map_v4.csv` 第 4–5 行 | 設計時使用理想值（前作允許），不是執行時資訊 |

## 5. 哪些可以重用，哪些不能？

### 可以重用（附條件）

| 項目 | 位置 | 條件 |
|---|---|---|
| QAOA 目標編譯與 `rzc` 標記 | `src/circuits.py` 33–47、65–122 | 第三章若改用 2–4 qubit、自訂候選，需另寫候選產生；標記邏輯可直接用 |
| 精確模擬引擎（state vector／density matrix） | `src/simulate.py` 52–151 | 需新增：label 吸收後的 compiled-angle E2、加法相位 φ、（若需要）單量子位元閘雜訊。現有 `GateNoise.over_rotation` 只等於邏輯角度模型 |
| 理想／母體 gap 計算 | `src/reference.py` | 只能用於計分與 oracle 上限，不能進政策 |
| gap、mean score、Hoeffding CI-only 下界（P0） | `src/probes.py` 26–58 | 可直接作為 Base-CI 基準 |
| 固定預算帳本與「每列總 shots 必須等於 N」的檢查 | `src/execution.py` 328–383（檢查在 383 行） | 模式可重用；entries 與 allocation 需改寫 |
| SeedSequence 種子鍵結構 | `docs/freeze/frozen_protocol_v4.md` 第 9 節；`src/protocol_contract.py` | 欄位需改成第三章的 artifact／action 編碼 |
| 強度 2 正交陣列 `frame_rows` | `src/circuits.py` 207–228 | 只作為平衡的 label 設計工具；`framed()` 本身不能當 RC label |
| Clifford twin（P2） | `src/circuits.py` 187–204；`src/probes.py` 67–70 | 可作為第三章的結構無關比較對象（見第 6 節最後一點） |
| 測試 | `tests/test_v4.py` 143–153、155–166、168–（E2 語意）；`tests/test_execution.py` 114–124、141–153（禁止理想值） | E2 語意測試可作為「邏輯角度模型」的回歸測試；禁止理想值的測試模式應沿用到第三章的政策函式 |
| 語意測試的做法（精確期望值比較 invariant／sensitive） | `experiments/semantic/semantic_tests_v4.py` | 適合 Gate 1A/1B 的無雜訊核對 |

### 不能重用

| 項目 | 原因 |
|---|---|
| `framed()` 作為 RC label | 只有 X、不穿過 cost `RZ`、不吸收、X 閘無雜訊；對 E2 恆等不變 |
| `GateNoise.over_rotation` 作為 compiled-angle 模型 | 它等價於邏輯角度模型（第 1 節） |
| 指定探針對照表 `DESIGNATED` | 依賴結構標籤，不可部署 |
| `results/development_v4/thresholds_v4.csv` | 為第二篇的探針、預算（N = 16,384，`src/protocol_contract.py`）與 f = 0.10 校準，不適用第三章的感測器與動作 |
| 前作 holdout 資料（`results/holdout_v4/`）作為第三章的確認性證據 | 已讀過一次、設計不同；最多作為背景描述 |
| 前作開發資料作為第三章的開發集 | 誤差模型、規模（寬度 4–8、深度 1–5）、候選設計都不同；最多作探索性參考 |
| `docs/theory/06_matrix.md` 中 P3/E2 的 visible 判斷 | 已被更正，凍結版為 blind；引用時要用 `06_matrix_v4.csv` |

## 6. E2 的 false certification 為何特別嚴重？

### 已觀察的結果（前作已提交，有雜訊模擬，holdout 只讀一次）

| 觀察 | 數值 | 位置 |
|---|---|---|
| E2 主操作點 | ε = −0.04（依第 4 節的較有害一側規則選出） | `results/development_v4/strength_map_v4.csv` 第 4 行 |
| CI-only 規則 R0 的 false certification | E2 0.0609（195 次，集中在 7 張圖）；E3 0.0113（36 次，2 張圖）；其餘五個結構 0 | `docs/results/primary_endpoint_v4.md` 27–29 |
| R1（P2 警報就拒答）後 | FC 0.0159；R0 的 false certification 有 0.744 被攔下；coverage 從 0.6025 降到 0.300 | 同上第 28 行；`docs/results/secondary_endpoints_v4.md` 第 14 行 |
| 翻號的圖數（holdout 參考，精確機率） | E2 主點 20 張（各結構中最多）；中位 β/Δ = −0.2286。E1 主點 13 張，中位 −0.6879 | `docs/results/boundary_synthesis_v4.md` 99–104 |
| E1 的對照 | 雖有 13 張翻號，R0 的 false certification 為 0，R0 coverage 只有 0.2978（E2 為 0.6025） | `docs/results/primary_endpoint_v4.md` 27–28 |
| P2 的警報幾乎分不出翻號與否 | 翻號圖警報率 0.4719（n = 20）；未翻號 0.4289（n = 80） | `docs/results/secondary_endpoints_v4.md` 第 28 行；論文 `paper/main_v4.tex` 482–485 |
| P2 對 E2 的靈敏度集中在少數圖 | 語意測試最大差值 0.208，中位數 0.0019 | `experiments/semantic/semantic_tests_v4.csv` 第 10 行 |
| 設計檢查（split 99） | 最強 gate 設定下，β/Δ ≤ −1 的比例最大是 0.12，出現在 E2 | `paper/main_v4.tex` 709–715 |

### 只是解釋（未檢驗）

1. **coherent shift 不衰減訊號。** E1（去極化）把 gap 往 0 壓，CI 變得不易認證，所以翻號也很少被錯誤認證；E2 只移動旋轉角，gap 的大小保留，CI 就會更有信心地認證錯誤的一方。這與「E1 coverage 低、FC 為 0；E2 coverage 高、FC 高」一致，但前作沒有直接檢驗這個機制。
2. **主操作點刻意選在較有害的一側。** ε = −0.04 是依開發集 β/Δ 選出的較有害符號（這是事實），所以 E2 的嚴重程度有一部分是設計選擇。
3. **γ 的代表值放大了誤差。** γ 在 [0, 2π) 均勻抽取且不 wrap，εγ 最大約 0.25 rad；γ 接近 2π 的邏輯近恆等旋轉承受最大的誤差。這可能讓 E2 的翻號集中在特定的圖與候選上（觀察到的「195 次集中在 7 張圖」與此相容，但沒有檢驗）。第三章若採用 wrap 或不 wrap 的慣例，E2 的嚴重度可能不同。
4. **兩個候選的 γ 不同，所以偏差是差異性的。** 乘法誤差和角度成正比，兩個候選的偏差自然不同，不會像 E0 那樣抵消。
5. **P2 能攔截，但不是因為它看見了翻號。** P2 透過 twin 中四捨五入後的 Clifford 角度（kπ/2 乘上 ε）感測 E2，與目標的翻號沒有直接對應；它的警報率在翻號與否之間幾乎相同。所以攔截主要是「警報就拒答」換來的（coverage 減半），不是選擇性的偵測。

### 對第三章的提醒

- 第二篇「改善來自 E2」的結論，實際上是 **P2 在邏輯角度模型下**得到的，與 RC label 無關。第三章不能把它當作 RC label 能感測 ε 的前例。
- P2 本身就是一個「已知參考、與結構無關、角度非零才有訊號」的 ε 感測器，性質接近 Gate 1B 的 P-amp。第三章應在 Part 1 決定是否把 P2 列為比較對象，並在新穎性說明中提到它。這是建議，不改動已凍結的 Gate 1A/1B 流程。
- 上面的解釋 1、3 可以在第三章 Part 1 用無雜訊精確計算檢驗（例如比較 wrap 與不 wrap 下的 β/Δ 分布）。是否納入，由使用者決定。
