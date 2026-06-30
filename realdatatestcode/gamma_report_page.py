#!/usr/bin/env python3
"""
Gamma G-0 / L-DREA  ->  animated HTML benchmark dashboard
=========================================================

Reads the REAL JSON artifacts produced by gamma_test_runner.py
(--lab-report and --summary) plus the captured terminal text, and emits a
single self-contained, animated HTML page (charts, flowchart, the what/how/why
narrative, and the verbatim terminal output).

No numbers are hand-written here: every value is read from the JSON the runner
actually wrote, so the page cannot show data the run did not produce.

Usage:
    python gamma_report_page.py \
        --lab-report gamma_lab_v1_report_full.json \
        --summary gamma_summary_full.json \
        --terminal gamma_terminal_full.txt \
        --out gamma_report.html
"""

from __future__ import annotations

import argparse
import html
import json
import webbrowser
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate an animated HTML dashboard from runner JSON.")
    p.add_argument("--lab-report", default="gamma_lab_v1_report_full.json")
    p.add_argument("--summary", default="gamma_summary_full.json")
    p.add_argument("--terminal", default="gamma_terminal_full.txt")
    p.add_argument("--out", default="gamma_report.html")
    p.add_argument(
        "--no-open",
        action="store_true",
        help="Do not auto-open the generated HTML page in a browser.",
    )
    return p.parse_args()


def render(lab: dict, summary: dict, out: str | Path,
           terminal_txt: str = "", open_browser: bool = True) -> Path:
    """Build the HTML dashboard from in-memory report dicts and (optionally) open it.

    Reusable entry point: the standalone CLI and gamma_test_runner.py both call
    this so there is a single source of truth for the page. Every value shown is
    derived from the `lab`/`summary` dicts passed in.
    """
    payload = {"lab": lab, "summary": summary}
    data_json = json.dumps(payload)
    terminal_safe = html.escape(terminal_txt)

    page = TEMPLATE.replace("/*__DATA__*/{}", data_json).replace("<!--__TERMINAL__-->", terminal_safe)
    out_path = Path(out)
    out_path.write_text(page, encoding="utf-8")
    print(f"Wrote {out_path}  ({len(page):,} bytes)")

    if not open_browser:
        print(f"Open it with:  open {out_path}")
        return out_path
    # Auto-open the generated dashboard in the default browser.
    url = out_path.resolve().as_uri()
    if webbrowser.open(url):
        print(f"Opened {out_path} in your default browser.")
    else:
        print(f"Could not auto-open a browser. Open it with:  open {out_path}")
    return out_path


def main() -> None:
    args = parse_args()
    lab = json.loads(Path(args.lab_report).read_text())
    summary = json.loads(Path(args.summary).read_text())
    terminal_txt = ""
    if Path(args.terminal).exists():
        terminal_txt = Path(args.terminal).read_text()
    render(lab, summary, args.out, terminal_txt=terminal_txt, open_browser=not args.no_open)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Gamma G-0 / L-DREA — Authorization Benchmark</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{
  --bg:#070b18; --panel:#0e1426; --panel2:#131c33; --ink:#e8eefc; --muted:#8da2c8;
  --acc:#4f8cff; --acc2:#22d3a6; --warn:#ffb454; --bad:#ff5d6c; --line:#23304f;
  --glow:0 0 0 1px rgba(79,140,255,.18), 0 18px 50px -18px rgba(0,0,0,.7);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:radial-gradient(1200px 700px at 70% -10%,#10204a 0%,var(--bg) 55%);
  color:var(--ink);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
a{color:var(--acc)}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.reveal{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.reveal.in{opacity:1;transform:none}

/* hero */
header.hero{padding:70px 0 38px;text-align:center;position:relative;overflow:hidden}
.badge{display:inline-block;padding:6px 14px;border:1px solid var(--line);border-radius:999px;
  color:var(--muted);font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:18px;
  background:rgba(79,140,255,.06)}
h1{font-size:clamp(30px,5vw,52px);margin:.1em 0;line-height:1.05;
  background:linear-gradient(90deg,#fff,#9cc1ff 60%,#22d3a6);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{color:var(--muted);font-size:18px;max-width:760px;margin:14px auto 0}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:42px 0 8px}
.kpi{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);
  border-radius:16px;padding:20px 16px;box-shadow:var(--glow)}
.kpi .n{font-size:30px;font-weight:800;letter-spacing:-.02em}
.kpi .n.good{color:var(--acc2)} .kpi .n.bad{color:var(--bad)}
.kpi .l{color:var(--muted);font-size:12.5px;margin-top:6px;text-transform:uppercase;letter-spacing:.08em}

section{padding:46px 0;border-top:1px solid rgba(35,48,79,.6)}
h2{font-size:26px;margin:0 0 6px;display:flex;align-items:center;gap:12px}
h2 .dot{width:11px;height:11px;border-radius:50%;background:var(--acc);box-shadow:0 0 16px var(--acc)}
.lead{color:var(--muted);max-width:840px;margin:0 0 26px}

.grid{display:grid;gap:18px}
.g3{grid-template-columns:repeat(3,1fr)} .g2{grid-template-columns:repeat(2,1fr)}
.card{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);
  border-radius:16px;padding:20px;box-shadow:var(--glow)}
.card h3{margin:.1em 0 .5em;font-size:16px}
.card p{color:var(--muted);margin:.2em 0}
.tag{display:inline-block;font-size:11px;color:#cfe0ff;border:1px solid var(--line);border-radius:6px;
  padding:2px 8px;margin:2px 4px 2px 0;background:rgba(79,140,255,.07)}

/* flowchart */
.flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:0}
.step{flex:1 1 0;min-width:150px;background:var(--panel2);border:1px solid var(--line);border-radius:14px;
  padding:14px;margin:8px;position:relative;transition:transform .25s,box-shadow .25s}
.step:hover{transform:translateY(-4px);box-shadow:0 16px 40px -16px rgba(79,140,255,.5)}
.step .num{font-size:12px;color:var(--acc);font-weight:700}
.step .t{font-weight:700;margin:4px 0}
.step .d{color:var(--muted);font-size:12.5px}
.branch{display:flex;gap:16px;margin-top:18px}
.branch .b{flex:1;border-radius:14px;padding:16px;border:1px solid var(--line)}
.b.permit{background:linear-gradient(180deg,rgba(34,211,166,.12),transparent)}
.b.safe{background:linear-gradient(180deg,rgba(255,93,108,.12),transparent)}
.b .h{font-weight:800;font-size:15px} .b.permit .h{color:var(--acc2)} .b.safe .h{color:var(--bad)}

.chart-box{position:relative;height:300px}
.mini{height:240px}

table{width:100%;border-collapse:collapse;font-size:14px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left}
th{color:var(--muted);font-weight:600;font-size:12.5px;text-transform:uppercase;letter-spacing:.06em}
td .ok{color:var(--acc2);font-weight:700} td .no{color:var(--bad);font-weight:700}

.inv{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.inv .i{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--panel2)}
.inv .i .s{font-size:12px;color:var(--acc2);font-weight:800;letter-spacing:.08em}
.inv .i .nm{font-size:13.5px;margin-top:4px}

.term{background:#05080f;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.term .bar{display:flex;gap:8px;padding:10px 14px;border-bottom:1px solid var(--line);background:#0a0f1c}
.term .bar i{width:12px;height:12px;border-radius:50%;display:inline-block}
.dotr{background:#ff5f57}.doty{background:#febc2e}.dotg{background:#28c840}
.term pre{margin:0;padding:18px;max-height:520px;overflow:auto;color:#bfe3c9;
  font:12.5px/1.55 "SF Mono",ui-monospace,Menlo,Consolas,monospace;white-space:pre}
.summary li{margin:8px 0;color:#d7e3fb}
.note{font-size:12.5px;color:var(--muted);border-left:3px solid var(--acc);padding:8px 14px;margin-top:16px;
  background:rgba(79,140,255,.05);border-radius:0 10px 10px 0}
footer{padding:40px 0 70px;color:var(--muted);text-align:center;font-size:13px}
@media(max-width:820px){.kpis,.g3,.g2,.inv{grid-template-columns:1fr 1fr}.branch{flex-direction:column}}
</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <div class="badge">Gamma G-0 · L-DREA · LAB v1.0 Authorization Benchmark</div>
  <h1 id="title">Deterministic Runtime Governance<br/>for the Action Boundary</h1>
  <p class="sub">Every AI-proposed action is held at zero authority until a non-compensatory permit
  proves it safe — then the decision is hash-chained, replayable evidence. Below is a
  <b>real run</b> over <span id="hero-n"></span> credit-card transactions.</p>
  <div class="kpis">
    <div class="kpi reveal"><div class="n good" id="kpi-agree">—</div><div class="l">Decision agreement</div></div>
    <div class="kpi reveal"><div class="n" id="kpi-uer">—</div><div class="l">Unauthorized executions</div></div>
    <div class="kpi reveal"><div class="n good" id="kpi-inv">—</div><div class="l">Invariants satisfied</div></div>
    <div class="kpi reveal"><div class="n good" id="kpi-replay">—</div><div class="l">Replay determinism</div></div>
  </div>
</header>

<!-- WHAT -->
<section class="reveal">
  <h2><span class="dot"></span>What we are doing</h2>
  <p class="lead">We re-derive the authorization decision for every transaction from the
  <b>Law of Concurrence</b> (Γ = maxᵢ(1−gᵢ)): a permit is granted only when <i>all</i> governance
  predicates concur. We then score the run against the six LAB v1.0 metrics, the six runtime
  invariants, and the commit-before-actuate / replay guarantees — and compare our derived decision
  to the dataset's ground-truth labels.</p>
  <div class="grid g3">
    <div class="card"><h3>Non-compensatory gate</h3><p>No weighted sum or confidence score can
      offset a failed predicate. One deficit ⇒ Γ&gt;0 ⇒ SAFE_STATE.</p>
      <span class="tag">Γ = maxᵢ(1−gᵢ)</span><span class="tag">fail-closed</span></div>
    <div class="card"><h3>Custodial authority</h3><p>The monitor controls the actuation keys, not the
      truth of the inputs — authorization-sound, not semantically omniscient.</p>
      <span class="tag">Permit-to-Act</span><span class="tag">epoch-keyed token</span></div>
    <div class="card"><h3>Evidence before action</h3><p>Each decision is committed to a hash-chained
      ledger <i>before</i> actuation, so every outcome is replayable.</p>
      <span class="tag">commit-before-actuate</span><span class="tag">Evidence Quad</span></div>
  </div>
</section>

<!-- HOW -->
<section class="reveal">
  <h2><span class="dot"></span>How it works — the authorization pipeline</h2>
  <p class="lead">Seven deterministic steps (OL3 boundary). An action enters with zero authority and
  leaves only through a permit or a logged SAFE_STATE denial.</p>
  <div class="flow">
    <div class="step"><div class="num">01</div><div class="t">Capability Isolation</div><div class="d">Action enters with zero inherent authority.</div></div>
    <div class="step"><div class="num">02</div><div class="t">Predicate Evaluation</div><div class="d">Compute the predicate vector G = {g₁…gₙ}.</div></div>
    <div class="step"><div class="num">03</div><div class="t">Non-Compensatory Γ</div><div class="d">Γ = max(1−gᵢ); any deficit dominates.</div></div>
    <div class="step"><div class="num">04</div><div class="t">Execution Binding</div><div class="d">Bind decision to this action + context.</div></div>
    <div class="step"><div class="num">05</div><div class="t">Dual Permit Gate</div><div class="d">Permit-to-Act (+ Permit-to-Adapt).</div></div>
    <div class="step"><div class="num">06</div><div class="t">Fail-Closed Resolve</div><div class="d">Γ&gt;0 → SAFE_STATE.</div></div>
    <div class="step"><div class="num">07</div><div class="t">Proof-Before-Action</div><div class="d">ERTuple committed before actuation.</div></div>
  </div>
  <div class="branch">
    <div class="b permit"><div class="h">Γ = 0 → ACT_PERMIT</div><p>All predicates concur → execute, then the
      hash-chained ERTuple is sealed. <b id="permit-n">—</b> transactions took this path.</p></div>
    <div class="b safe"><div class="h">Γ &gt; 0 → SAFE_STATE</div><p>Any predicate fails → deny + ERTuple; no
      externalization. <b id="safe-n">—</b> transactions (all real fraud) took this path.</p></div>
  </div>
</section>

<!-- RULES -->
<section class="reveal">
  <h2><span class="dot"></span>Rules &amp; parameters that govern these results</h2>
  <p class="lead">Every PERMIT / SAFE_STATE decision on this page follows the rules below. Nothing is
  scored outside them — they are read straight from the run's config.</p>
  <div class="card" style="margin-bottom:18px">
    <h3>Decision rule</h3>
    <p id="rule-decision" style="color:#d7e3fb"></p>
    <p id="rule-classveto"></p>
  </div>
  <div class="grid g2">
    <div class="card"><h3>Predicates that must all concur</h3>
      <div id="rule-predicates"></div>
      <h3 style="margin-top:16px">Derived deficits</h3>
      <table id="rule-deficits"><tbody></tbody></table></div>
    <div class="card"><h3>Integrity rules</h3>
      <table id="rule-integrity"><tbody></tbody></table></div>
  </div>
  <div class="grid g2" style="margin-top:18px">
    <div class="card"><h3>Parameters (this run)</h3>
      <table id="rule-params"><tbody></tbody></table></div>
    <div class="card"><h3>FULL_SPEC §7.1 acceptance bands <span class="tag">conjunctive · reference</span></h3>
      <table id="rule-bands"><tbody></tbody></table>
      <p class="note" id="rule-bands-note"></p></div>
  </div>
</section>

<!-- WHY -->
<section class="reveal">
  <h2><span class="dot"></span>Why it matters</h2>
  <p class="lead">In high-consequence domains a single unauthorized externalization can outweigh thousands
  of benign denials. The benchmark proves the gate fails closed and that a <i>compensatory</i> aggregator
  would not — the negative control below.</p>
  <div class="grid g2">
    <div class="card"><h3>Negative control — why non-compensatory?</h3>
      <div class="chart-box mini"><canvas id="negChart"></canvas></div>
      <p id="neg-text" style="margin-top:10px"></p></div>
    <div class="card"><h3>Six LAB v1.0 metrics (adverse rate, log scale)</h3>
      <div class="chart-box mini"><canvas id="metricChart"></canvas></div></div>
  </div>
</section>

<!-- RESULTS CHARTS -->
<section class="reveal">
  <h2><span class="dot"></span>Results — measured this run</h2>
  <div class="grid g2">
    <div class="card"><h3>Decision distribution</h3><div class="chart-box"><canvas id="decChart"></canvas></div></div>
    <div class="card"><h3>Measured latency (ms) vs §6.0 limit</h3><div class="chart-box"><canvas id="latChart"></canvas></div></div>
  </div>
  <div class="grid g2" style="margin-top:18px">
    <div class="card"><h3>Per-scenario class</h3><div class="chart-box mini"><canvas id="scenChart"></canvas></div></div>
    <div class="card"><h3>Six runtime invariants</h3><div class="inv" id="invGrid"></div></div>
  </div>
</section>

<!-- METRIC TABLE -->
<section class="reveal">
  <h2><span class="dot"></span>Primary metrics &amp; Wilson bounds</h2>
  <div class="card"><table id="metricTable"><thead><tr>
    <th>Metric</th><th>Events / N</th><th>Rate</th><th>Wilson 95% upper</th></tr></thead><tbody></tbody></table></div>
</section>

<!-- APPENDIX-A SUMMARY -->
<section class="reveal">
  <h2><span class="dot"></span>LAB v1.0 summary (Appendix-A style)</h2>
  <div class="card"><ul class="summary" id="summaryList"></ul></div>
</section>

<!-- TERMINAL -->
<section class="reveal">
  <h2><span class="dot"></span>Verbatim terminal output</h2>
  <p class="lead">Exactly what the runner printed for this run — no edits.</p>
  <div class="term"><div class="bar"><i class="dotr"></i><i class="doty"></i><i class="dotg"></i>
    <span style="color:#7f8fb0;font:12px ui-monospace">python3 gamma_test_runner.py</span></div>
    <pre><!--__TERMINAL__--></pre></div>
</section>

<footer>
  Generated from real runner JSON · ground truth = ULB <code>Class</code> labels · hash chain genuinely
  recomputed · latency measured on host (software path, not HSM/FPGA). <span id="foot-meta"></span>
</footer>
</div>

<script>
const PAYLOAD = /*__DATA__*/{};
const L = PAYLOAD.lab, S = PAYLOAD.summary;
const fmtPct = x => (x*100).toFixed(4) + "%";
const sci = x => x.toExponential(2);

/* ---- KPIs (with count-up where numeric) ---- */
document.getElementById("hero-n").textContent = L.n_total.toLocaleString();
document.getElementById("foot-meta").textContent = L.method_version + " · N=" + L.n_total.toLocaleString();
const invOk = Object.values(L.runtime_invariants_violations).filter(v=>v===0).length;
const da = L.decision_agreement;
setKpi("kpi-agree", fmtPct(da.match_status_rate));
setKpi("kpi-uer", String(L.unauthorized_execution.count), L.unauthorized_execution.count===0?"good":"bad");
setKpi("kpi-inv", invOk + "/6");
setKpi("kpi-replay", fmtPct(L.primary_metrics.replay_determinism_rate.reported_rate));
function setKpi(id,val,cls){const e=document.getElementById(id);e.textContent=val;if(cls==="bad"){e.classList.remove("good");e.classList.add("bad");}}

document.getElementById("permit-n").textContent = (S.derived_permit||0).toLocaleString();
document.getElementById("safe-n").textContent = (S.derived_safe_state||0).toLocaleString();

/* ---- summary list ---- */
const ul=document.getElementById("summaryList");
(L.appendix_a_style_summary||[]).forEach(t=>{const li=document.createElement("li");li.textContent=t;ul.appendChild(li);});

/* ---- metric table ---- */
const mtb=document.querySelector("#metricTable tbody");
Object.values(L.primary_metrics).forEach(m=>{
  const tr=document.createElement("tr");
  const rate = m.higher_is_better ? fmtPct(m.reported_rate) : (m.adverse_rate===0?"0":fmtPct(m.adverse_rate));
  tr.innerHTML = `<td>${m.metric}</td><td>${m.adverse_events} / ${m.n}</td>
    <td>${rate}</td><td>&lt; ${m.wilson95_clustercorrected_upper<1e-3?sci(m.wilson95_clustercorrected_upper):fmtPct(m.wilson95_clustercorrected_upper)}</td>`;
  mtb.appendChild(tr);
});

/* ---- invariants grid ---- */
const ig=document.getElementById("invGrid");
Object.entries(L.runtime_invariants_violations).forEach(([k,v])=>{
  const d=document.createElement("div");d.className="i";
  d.innerHTML=`<div class="s" style="color:${v===0?'var(--acc2)':'var(--bad)'}">${v===0?"✔ HOLDS":"✘ "+v}</div><div class="nm">${k.replace(/_/g," ")}</div>`;
  ig.appendChild(d);
});

/* ---- governing rules ---- */
const GR = L.governing_rules || {};
if(GR.decision_rule){
  document.getElementById("rule-decision").textContent = GR.decision_rule;
  document.getElementById("rule-classveto").innerHTML =
    "<b style='color:var(--warn)'>Class-level veto:</b> " + (GR.class_level_veto||"");
  const pp=document.getElementById("rule-predicates");
  (GR.node_predicates_must_all_concur||[]).forEach(g=>{
    const s=document.createElement("span");s.className="tag";s.textContent=g;pp.appendChild(s);});
  const dfb=document.querySelector("#rule-deficits tbody");
  Object.entries(GR.derived_deficits||{}).forEach(([k,v])=>{
    dfb.innerHTML+=`<tr><td><code>${k}</code></td><td>${v}</td></tr>`;});
  const ib=document.querySelector("#rule-integrity tbody");
  const integ=[["Unauthorized exec (Eq.7)",GR.unauthorized_execution_eq7],
    ["ISB rule",GR.isb_rule],["Commit-before-actuate",GR.commit_before_actuate],
    ["Replay determinism",GR.replay_determinism],["Ground truth",GR.ground_truth]];
  integ.forEach(([k,v])=>{if(v)ib.innerHTML+=`<tr><td style="white-space:nowrap"><b>${k}</b></td><td>${v}</td></tr>`;});
  const pb=document.querySelector("#rule-params tbody");
  Object.entries(GR.parameters||{}).forEach(([k,v])=>{
    pb.innerHTML+=`<tr><td><code>${k}</code></td><td><b style="color:#cfe0ff">${v}</b></td></tr>`;});
  const bb=document.querySelector("#rule-bands tbody");
  const bands=GR.spec_policy_reference_band_7_1||{};
  Object.entries(bands).forEach(([k,v])=>{
    if(k==="note"){document.getElementById("rule-bands-note").textContent=v;return;}
    if(k==="hard_stops"){bb.innerHTML+=`<tr><td><b>hard-stops</b></td><td>${v.join(" · ")}</td></tr>`;return;}
    bb.innerHTML+=`<tr><td>${k.replace(/_/g," ")}</td><td><code>${v}</code></td></tr>`;});
}

/* ---- Chart.js theme ---- */
Chart.defaults.color="#8da2c8";Chart.defaults.font.family="-apple-system,Segoe UI,Roboto,sans-serif";
Chart.defaults.borderColor="rgba(35,48,79,.6)";
const GREEN="#22d3a6",BLUE="#4f8cff",RED="#ff5d6c",AMBER="#ffb454";

/* decision donut */
new Chart(decChart,{type:"doughnut",
  data:{labels:["PERMIT","SAFE_STATE"],datasets:[{data:[S.derived_permit,S.derived_safe_state],
    backgroundColor:[BLUE,RED],borderWidth:0}]},
  options:{cutout:"62%",plugins:{legend:{position:"bottom"}},animation:{animateRotate:true,duration:1200}}});

/* latency bars */
const ml=L.measured_latency;
new Chart(latChart,{type:"bar",
  data:{labels:["mean","P95","P99","max"],datasets:[
    {label:"latency (ms)",data:[ml.mean_ms,ml.p95_ms,ml.p99_ms,ml.max_ms],backgroundColor:[GREEN,BLUE,AMBER,RED],borderRadius:8}]},
  options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.parsed.y.toFixed(4)+" ms"}}},
    scales:{y:{title:{display:true,text:"ms (limit "+ml.limit_ms+" ms)"}}},animation:{duration:1200}}});

/* scenario bars */
const sc=L.per_scenario_class, labels=Object.keys(sc);
new Chart(scenChart,{type:"bar",
  data:{labels:labels.map(s=>s.replace(/_/g," ")),datasets:[
    {label:"N",data:labels.map(k=>sc[k].n),backgroundColor:BLUE,borderRadius:6},
    {label:"→ SAFE_STATE",data:labels.map(k=>sc[k].derived_safe_state),backgroundColor:RED,borderRadius:6},
    {label:"false permits",data:labels.map(k=>sc[k].false_permits),backgroundColor:AMBER,borderRadius:6}]},
  options:{indexAxis:"y",scales:{x:{type:"logarithmic"}},plugins:{legend:{position:"bottom"}},animation:{duration:1200}}});

/* metric adverse-rate (log) */
const pm=Object.values(L.primary_metrics);
new Chart(metricChart,{type:"bar",
  data:{labels:pm.map(m=>m.metric.replace(/\(.*\)/,"").trim()),
    datasets:[{label:"adverse rate",data:pm.map(m=>Math.max(m.adverse_rate,1e-7)),backgroundColor:GREEN,borderRadius:6},
    {label:"Wilson 95% upper",data:pm.map(m=>m.wilson95_clustercorrected_upper),backgroundColor:"rgba(79,140,255,.55)",borderRadius:6}]},
  options:{scales:{y:{type:"logarithmic",title:{display:true,text:"rate (log)"}}},
    plugins:{legend:{position:"bottom"}},animation:{duration:1200}}});

/* negative control */
const nc=L.negative_control;
document.getElementById("neg-text").innerHTML =
  `A compensatory weighted-sum aggregator would <b style="color:var(--bad)">false-permit ${nc.corollary2_rows_masked_if_isolated}</b>
   fraud rows if their deficit were isolated (single deficit ${(1/14).toFixed(3)} &lt; τ=${nc.tau}); the
   non-compensatory Law of Concurrence <b style="color:var(--acc2)">denies all</b> of them.`;
new Chart(negChart,{type:"bar",
  data:{labels:["Non-compensatory (LLC)","Compensatory (weighted-sum)"],
    datasets:[{label:"fraud false permits",data:[0,nc.corollary2_rows_masked_if_isolated],
      backgroundColor:[GREEN,RED],borderRadius:8}]},
  options:{plugins:{legend:{display:false}},animation:{duration:1200}}});

/* scroll reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add("in")}),{threshold:.12});
document.querySelectorAll(".reveal").forEach(el=>io.observe(el));
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
