# 🛡️ LAB v1.0 – Runtime AI Safety Verification Framework

> **A runtime verification system that checks every AI decision before it is allowed to execute.**

This project demonstrates how an AI system can be continuously monitored at runtime to prevent unsafe, malicious, or unauthorized actions.

Instead of trusting an AI model blindly, this framework places a **verification layer** between the AI and the final action.

If the request is considered safe, it is **approved**.

If any security rule is violated, the system immediately blocks the request and moves into a **SAFE_STATE**.

---

# 🎯 Why was this project built?

Modern AI systems can make mistakes or even be manipulated through attacks such as:

- Prompt Injection
- Fake Authorization
- Expired Access Tokens
- Context Manipulation
- Replay Attacks
- Privilege Escalation

This project demonstrates how those attacks can be detected **before** the AI performs a sensitive action.

Think of it as:

> **An airport security checkpoint for AI systems.**

Every request is inspected before being allowed to continue.

---

# 🚀 Project Workflow

```text
Incoming Request
        │
        ▼
 Runtime Verification Engine
        │
        ├──────────────┐
        │              │
     SAFE             UNSAFE
        │              │
        ▼              ▼
 PERMIT ACTION     SAFE_STATE
```

---

# 📂 Project Structure

```text
.
├── maincode.py                ← Main program (Run this file)
├── maincodedashboard.html     ← Interactive dashboard generated after execution
├── testdata.csv               ← Sample dataset used for testing
├── lab_benchmark.py           ← Benchmark engine
├── dashboard.html             ← Benchmark dashboard
├── ertuple_audit_manifest.json
├── test_baseline_metrics.py
├── test_corpus_enforcement.py
└── README.md
```

---

# 📌 Main Files

## ✅ maincode.py

This is the **main entry point** of the project.

Running this file performs the complete verification process.

It:

- Loads the test dataset
- Runs Runtime Enforcement
- Executes attack simulations
- Calculates security metrics
- Generates reports
- Creates the HTML dashboard

> **If you only want to run the project, this is the only file you need to execute.**

---

## 📊 maincodedashboard.html

This dashboard is automatically generated after running `maincode.py`.

It provides a visual representation of:

- Runtime verification results
- Security metrics
- Attack simulations
- Interactive graphs
- Performance analysis

Instead of reading logs in the terminal, simply open this HTML file in any web browser.

---

## 📁 testdata.csv

This is the sample dataset used to test the framework.

It contains example requests representing both:

- Legitimate actions
- Malicious or unsafe actions

The verification engine processes every row and decides whether it should be:

- **PERMIT**
- **SAFE_STATE**

You can replace this dataset with your own CSV to evaluate different scenarios.

---

# ⚙️ How the System Works

For every incoming request, the system verifies:

- ✅ Authorization
- ✅ Token Validity
- ✅ Security Rules
- ✅ Runtime Conditions
- ✅ Risk Thresholds

If every rule passes:

```text
PERMIT
```

Otherwise:

```text
SAFE_STATE
```

---

# 🛠️ Requirements

Before running the project, make sure you have:

- Python 3.9 or later

No external Python packages are required.

Everything runs using Python's built-in standard library.

---

# ▶️ How to Run

## Step 1 — Clone the Repository

```bash
git clone <repository-url>
```

---

## Step 2 — Open the Project Folder

```bash
cd LAB-v1
```

---

## Step 3 — Run the Main Program

On Windows:

```bash
python maincode.py
```

On macOS/Linux:

```bash
python3 maincode.py
```

---

## Step 4 — Wait for Execution

The program will automatically:

- Load the test dataset
- Run Runtime Enforcement
- Execute attack simulations
- Calculate security metrics
- Generate reports
- Create the dashboard

---

## Step 5 — Open the Dashboard

After execution completes, open:

```text
maincodedashboard.html
```

using your favorite web browser.

The dashboard contains:

- Runtime verification results
- Interactive charts
- Security metrics
- Attack analysis
- Overall verification summary

---

# 📊 Dashboard Features

The generated dashboard includes:

- Runtime Enforcement Results
- Attack Detection Summary
- Security Metrics
- Performance Statistics
- Benchmark Comparison
- Verification Outcome
- Interactive Graphs
- Audit Summary

---

# 🔬 Technical Features

- Runtime Reference Monitor
- Non-Compensatory Decision Logic
- Permit-to-Act Verification
- SAFE_STATE Enforcement
- HMAC Token Validation
- Replay Attack Detection
- TOCTOU Protection
- Class-Level Security Veto
- Tamper-Evident Audit Ledger
- Benchmark Verification

---

# 📈 Execution Flow

```text
Incoming Request
        │
        ▼
Runtime Verification
        │
        ▼
Checks Passed?
        │
   ┌────┴────┐
   │         │
 YES        NO
   │         │
   ▼         ▼
PERMIT   SAFE_STATE
        │
        ▼
Dashboard Generated
```

---

# 🎯 Expected Output

After running the project, you will obtain:

- ✅ Terminal Verification Report
- ✅ Interactive HTML Dashboard
- ✅ Security Metrics
- ✅ Verification Summary
- ✅ Audit Logs

---

# 👥 Who Can Use This Project?

This project is designed for:

- AI Security Researchers
- Software Engineers
- Cybersecurity Professionals
- Students
- Academic Researchers
- Anyone interested in AI Safety

No prior know

ledge of AI security is required to understand the overall workflow.

---

# 💡 Project Goal

The goal of this project is to demonstrate how a runtime verification framework can improve the safety and trustworthiness of AI systems by validating every action before execution.

Rather than assuming an AI model is always correct, the framework continuously evaluates every request, verifies its authenticity, and blocks unsafe operations before they occur.

This approach helps create AI systems that are **more secure, reliable, transparent, and accountable**.

---

# 📄 License

This project is provided for **research, educational, and demonstration purposes**.

---

# 📊 Dashboard Preview

The Runtime Verification Dashboard provides a complete overview of the system's security evaluation, attack detection, performance metrics, and benchmark verification. Each section highlights a different aspect of the runtime enforcement process.

---

## 🛡️ Section 1 – Runtime Enforcement Overview

This section summarizes the overall verification results, including the total number of evaluated requests, adversarial samples, unauthorized permits, replay determinism, and baseline comparisons. It also visualizes how the runtime enforcement engine successfully blocks malicious requests while maintaining deterministic execution.

![Section 1]<img width="1464" height="605" alt="Screenshot 2026-06-28 at 1 17 43 PM" src="https://github.com/user-attachments/assets/c5978b89-a441-4389-ba4b-e061ebb89392" />

---

## ⚠️ Section 2 – Stress Test Scenarios

This section reproduces multiple real-world attack scenarios such as deepfake financial fraud, sanctions drift, multi-agent liquidity attacks, and compound failure cases. Each scenario is evaluated by the runtime enforcement engine and classified as **PERMIT**, **SAFE_STATE**, or **Documented Scope Limitation**.

![Section 2]
<img width="1470" height="635" alt="Screenshot 2026-06-28 at 1 18 48 PM" src="https://github.com/user-attachments/assets/2e8993a1-ea43-45e7-9dd7-ed8a9bd51ad5" />

---

## ⚡ Section 3 – Performance & Security Metrics

This section presents runtime performance measurements, including latency, throughput, replay determinism, and security ablation studies. It demonstrates the efficiency of the enforcement engine while highlighting the contribution of each security control to the overall protection mechanism.

![Section 3]

<img width="1470" height="655" alt="Screenshot 2026-06-28 at 1 19 07 PM" src="https://github.com/user-attachments/assets/9dcd6382-47f6-49d0-828c-32fe4216bcb9" />

---

## 📈 Section 4 – Benchmark Reproduction

This section compares the implementation results with the benchmark claims defined in the LAB v1.0 reference framework. It verifies security invariants, replay consistency, adaptive attack resistance, and overall compliance status through reproducible benchmark evaluation.

![Section 4](<img width="1470" height="372" alt="Screenshot 2026-06-28 at 1 19 30 PM" src="https://github.com/user-attachments/assets/b756c2c9-13f2-4f6b-a620-fee9309a6613" />

---

## 📄 Final Runtime Report

The dashboard concludes with a comprehensive execution report that combines all verification stages into a single summary. It provides detailed logs, benchmark outcomes, performance statistics, security decisions, and the final audit verdict generated during execution.

![Final Report]

<img width="1470" height="737" alt="Screenshot 2026-06-28 at 1 20 01 PM" src="https://github.com/user-attachments/assets/83935dc2-78fc-4206-8816-c67694d7a433" />


## ⭐ If you find this project useful, consider giving it a star on GitHub!
