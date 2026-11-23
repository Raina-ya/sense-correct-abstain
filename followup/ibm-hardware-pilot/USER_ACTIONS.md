# HW-P1 actions requiring the owner

Everything before real-backend access is prepared. No hardware job has been
submitted. Complete these steps in order.

## 1. Use a Linux environment

The local Windows machine blocks unsigned native Python extensions through
Smart App Control. Do not disable that protection. Use an IBM Quantum cloud
notebook, another Linux environment, or a Linux virtual machine.

Clone the repository at the commit reported by the assistant, then install:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r followup/ibm-hardware-pilot/requirements.txt
```

## 2. Configure the IBM account privately

Save the API key inside that Linux environment. Never commit it and never paste
it into an issue, log, or chat transcript.

```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(token="YOUR_PRIVATE_API_KEY", overwrite=True)
```

## 3. Record plan, remaining allocation, and backend

In the IBM Quantum dashboard, record:

- plan type and instance;
- remaining resource units/minutes;
- exact Heron backend name;
- whether the backend is operational.

Approve a maximum of **3 QPU minutes** for Stage A. The local quick estimate is
1.052 minutes; the cap leaves contingency without authorising Stage B.

## 4. Run the non-executing cloud preflight

```bash
cd followup/ibm-hardware-pilot
python cloud_preflight.py --backend EXACT_BACKEND_NAME
```

This contacts IBM for backend metadata and transpiles locally. It does not
submit a QPU job. Return `cloud_preflight_report.json` to the repository owner
for review.

## 5. Stop for the final lock

Do not submit circuits yet. The cloud preflight fixes the backend name,
physical qubits, actual ISA circuits, durations, and environment. Those values
must be inserted into the protocol lock v2 and independently timestamped if the
study is to be called preregistered.

The remaining owner decisions are:

1. confirm Stage A only;
2. approve the exact backend and selected qubit pair;
3. approve the 3-minute cap;
4. keep unmitigated counts as primary (recommended);
5. choose whether the locked protocol is deposited to Zenodo before execution;
6. sign the lock review note.

Only after those six decisions and a passing v2 pre-lock check should the
hardware submission runner be enabled.
