"""Builds the full portfolio page (site/index.html) in the approved poster style (hero = hero/h18).
Usage: python build.py"""
import re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
_src = HERE.parent / "assets" / "portrait_sq.jpg"   # only present on the author's machine
if _src.exists(): shutil.copy(_src, HERE / "portrait_sq.jpg")

# ---- settings you may change -------------------------------------------------
SITE_URL = "https://bhavanmehta.github.io"   # where the page is published (used for the link preview image)
GOATCOUNTER_CODE = "bhavanmehta"                      # visitor counter: your code from goatcounter.com, or "" for none
# ------------------------------------------------------------------------------
ROLE = "Senior Data Engineer, Finance Data Engineering, Tesla"
COUNTER = (f'<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>' if GOATCOUNTER_CODE else "")
X = lambda cls="x", st="": f'<svg class="{cls}"{st} viewBox="0 0 12 15" aria-hidden="true"><use href="#xl"/></svg>'
SHEETS = "".join(X("x", f' style="--i:{i}"') for i in range(25))
PIPES = "<i></i>" * 50
PEOPLE = "<i></i>" * 200

# ------------------------------------------------------------------ data flow
STAGES = [
 ("Sources", "Raw", "Where the numbers start", [
   ("Treasury", "Data from a treasury system."),
   ("Procurement and invoicing", "Data from the procurement and invoicing system."),
   ("Databases", "Finance and operational data in several databases.")]),
 ("Pipelines", "50+", "Airflow and SSIS", [
   ("50+ pipelines", "I build and run the Airflow and SSIS pipelines that bring these sources together for FP&amp;A, Accounting and Investor Relations."),
   ("90 to 10 minutes", "Tuned the daily inventory extracts from 90 minutes to 10."),
   ("Lakehouse <i>supporting</i>", "Supporting the migration of finance ETL from SSIS to a new lakehouse built on S3, PySpark, Airflow, Apache Iceberg (bronze/silver/gold) and Trino.")]),
 ("Checks", "Audit", "Controls before anything is reported", [
   ("Audited reports", "Financial reports for Accounting that are audited."),
   ("Access control", "Row-level security and AD groups on sensitive finance data."),
   ("Reconciliation agents <i>building</i>", "Building AI agents that run daily reconciliations across finance sources and flag mismatches.")]),
 ("Models", "25 &rarr; 1", "The financial model and the forecast cube", [
   ("Corporate financial model", "Led the data engineering side of re-engineering it: 25 Excel workbooks and a 7-10 day consolidation replaced by one refresh of the P&amp;L, balance sheet and cash flow."),
   ("Forecast cube", "Architected and scaled a global SSAS cube that combines the Energy, Automotive and Manufacturing forecasts.")]),
 ("Reporting", "40+", "Close, forecast, CAPEX, earnings prep", [
   ("40+ dashboards", "SSRS and Power BI dashboards for finance and operations, including work-order and cycle-count reporting."),
   ("3 hours to 30 minutes", "Month-end variance analysis, after rewriting the stored procedures behind the Day-1 close.")]),
 ("People", "200+", "Who reads the numbers", [
   ("200+ stakeholders", "Use the forecast cube for freeze reporting and prior-vs-actual analysis."),
   ("Finance leadership", "Uses the corporate model refresh."),
   ("Teams", "FP&amp;A, Accounting and Investor Relations.")]),
]
def stage(i, s):
    name, fig, sub, items = s
    its = "".join(f"<div><h4>{a}</h4><p>{b}</p></div>" for a, b in items)
    return (f'<li><button class="st" type="button" id="st{i}" aria-controls="pn{i}" aria-expanded="false" data-i="{i}"><span class="sn">0{i+1}</span>'
            f'<b class="d">{name}</b><em class="d">{fig}</em><small>{sub}</small></button>'
            f'<div class="pn" id="pn{i}" role="region" aria-labelledby="st{i}"><div class="pn-h"><span class="d">{fig}</span><p>{name}: {sub.lower()}</p></div><div class="pn-b">{its}</div></div></li>')
FLOW = "".join(stage(i, s) for i, s in enumerate(STAGES))

# ------------------------------------------------------------------ experience
def cards(rows):
    out = []
    for lead, txt, *tag in rows:
        t = f'<span class="tag">{tag[0]}</span>' if tag else ""
        out.append(f'<div class="a"><b class="d">{lead}</b>{t}<p>{txt}</p></div>')
    return "".join(out)
SR = cards([
 ("25 &rarr; 1", "Led the data engineering side of re-engineering Tesla's corporate financial model, replacing 25 Excel workbooks and a 7-10 day consolidation with one refresh of the P&amp;L, balance sheet and cash flow, used by finance leadership."),
 ("3 h &rarr; 30 min", "Cut month-end variance analysis from 3 hours to 30 minutes by rewriting the stored procedures behind the Day-1 close, and tuned daily inventory extracts from 90 minutes to 10."),
 ("200+", "Architected and scaled a global SSAS forecast cube that combines the Energy, Automotive and Manufacturing forecasts, used by 200+ stakeholders for freeze reporting and prior-vs-actual analysis."),
 ("50+", "Build and run 50+ Airflow and SSIS pipelines integrating finance and operational data from a treasury system, a procurement and invoicing system and several databases for FP&amp;A, Accounting and Investor Relations."),
 ("40+", "Delivered 40+ SSRS and Power BI dashboards for finance and operations, including work-order and cycle-count reporting."),
 ("Audit", "Build audited financial reports for Accounting, and control access to sensitive finance data with row-level security and AD groups."),
 ("AI agents", "Building AI agents that run daily reconciliations across finance sources and flag mismatches.", "In progress"),
 ("Lakehouse", "Supporting the migration of finance ETL from SSIS to a new lakehouse built on S3, PySpark, Airflow, Apache Iceberg (bronze/silver/gold) and Trino.", "Supporting"),
 ("6 interns", "Review teammates' code in Git and built an AI agent that helps with code reviews. Mentored 6 interns and several new hires, and trained 20+ business users in DAX and Power Query."),
])
BI = cards([
 ("$1B+", "Built the data model and 30+ executive dashboards tracking budget, spend and risk on $1B+ of CAPEX projects for global finance."),
 ("1,200+", "Built Power Platform solutions (Power Apps, Power BI, Power Automate) that automated workflows and opened up data access for 1,200+ users in manufacturing and supply chain."),
 ("4 apps", "Developed 4 Power Apps for forecasting and tracking, including a construction progress app used by field crews at 10+ regional sites."),
 ("15+ flows", "Built 15+ Power Automate flows that check financial and construction data and alert users when something doesn't match."),
 ("30+", "Ran 30+ technical interviews covering SQL, DAX and data modeling as the team grew."),
])
ONTO = cards([
 ("60%", "Wrote Python scripts and SQL Server stored procedures that pulled ERP data into one place, cutting manual reporting by 60%."),
 ("ERP", "Built executive dashboards in Power BI and Report Builder on ERP data for sales and business reporting."),
])
TOTAL = 108  # months, Jan 2018 .. Dec 2026
def bar(cls, a, b, href, label):
    return f'<a class="tb {cls}" href="{href}" style="left:{a/TOTAL*100:.2f}%;width:{(b-a)/TOTAL*100:.2f}%"><span>{label}</span></a>'
TIMELINE = (bar("t1", 0, 31, "#r4", "Earlier roles") + bar("t2", 31, 42, "#r3", "Onto") + bar("t3", 42, 65, "#r2", "Tesla, BI Developer")
            + bar("t4", 65, 107, "#r1", "Tesla, Senior Data Engineer"))
YEARS = "".join(f"<span>{y}</span>" for y in range(2018, 2027))

def role(i, when, org, title, where, body):
    return (f'<article class="role" id="r{i}"><div class="role-h"><p class="when">{when}</p><h3 class="d">{org}</h3><p class="title">{title}</p><p class="where">{where}</p></div>'
            f'<div class="ach">{body}</div></article>')
ROLES = (role(1, "Jun 2023 to present", "Tesla", "Senior Data Engineer, Finance Data Engineering", "Fremont, CA", SR)
         + role(2, "Jul 2021 to Jun 2023", "Tesla", "Business Intelligence Developer", "Fremont, CA", BI)
         + role(3, "Aug 2020 to Jul 2021", "Onto Innovation", "Business Intelligence Intern", "Milpitas, CA", ONTO)
         + '<article class="role" id="r4"><div class="role-h"><p class="when">2018 to 2020</p><h3 class="d">Earlier</h3></div><div class="ach solo">'
           '<div class="a"><p><b>BI Intern, Pegasus Knowledge Solutions.</b> KPIs and Tableau dashboards.</p></div>'
           '<div class="a"><p><b>Data Analyst, The Dezine, India.</b></p></div></div></article>')

# ------------------------------------------------------------------ how I work, skills
HOW = [
 ("Reconcile before you report.", "Every number I publish has a second source it must tie to.", ["Reconciliation agents", "Mismatch alerts", "Audited reports"]),
 ("Fail loudly, keep serving.", "A broken run should stop and leave yesterday's good data live, not publish quietly.", ["BreakoutAI guards"]),
 ("Replace the spreadsheet, keep the logic auditable.", "Automation that finance can trace line by line.", ["25 workbooks to one refresh"]),
 ("Make it faster where people wait.", "Tune the step someone sits and watches.", ["3 h to 30 min", "90 to 10 min"]),
 ("Leave the team stronger.", "Review the code, train the people who use the numbers, and help hire the next engineers.", ["Code review", "Mentoring", "Interviews"]),
]
HOWH = "".join(f'<li><span class="hn d">0{i+1}</span><div><h3 class="d">{a}</h3><p>{b}</p></div><ul class="chips">{"".join(f"<li>{c}</li>" for c in cs)}</ul></li>' for i, (a, b, cs) in enumerate(HOW))
SKILLS = [
 ("Data engineering", "Apache Airflow, SSIS, ETL/ELT, PySpark, Apache Iceberg, Trino, S3 Lakehouse (Medallion)"),
 ("Languages and databases", "SQL (SQL Server, MySQL, Vertica), Python (pandas, NumPy), PowerShell, PostgreSQL, DuckDB, Redis"),
 ("Data quality and access", "Automated Reconciliations, Data Validation, Row-Level Security, Active Directory Access Groups"),
 ("Engineering practice", "Git, Code Review, Query and Index Tuning, Linux, CI/CD (GitHub Actions), REST APIs, Automated Testing"),
 ("AI and LLM", "LLM Agents (Claude Code, Cursor), Tool Calling, Natural-Language-to-SQL"),
 ("Finance and BI", "Close, Forecasting, CAPEX, Procurement, Earnings Prep, 3-Statement Models, SSAS, Power BI, Tableau"),
]
SKH = "".join(f'<div class="sk"><h3>{a}</h3><ul class="chips">{"".join(f"<li>{c.strip()}</li>" for c in re.split(r", (?![^(]*\))", b))}</ul></div>' for a, b in SKILLS)

LINKS = ('<a class="l l1" href="resume.pdf">Resume</a><a class="l" href="https://github.com/Bhavanmehta">GitHub</a>'
         '<a class="l" href="https://www.linkedin.com/in/bhavan-mehta">LinkedIn</a><a class="l" href="mailto:bhavanmehtap@gmail.com">Email</a>')

CSS = (HERE / "style.css").read_text(encoding="utf-8")
JS = (HERE / "app.js").read_text(encoding="utf-8")

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bhavan Mehta - Senior Data Engineer</title>
<meta name="description" content="Senior Data Engineer on Tesla's Finance Data Engineering team. Six years of making sure the number in the meeting is the right one.">
<meta property="og:title" content="Bhavan Mehta - Senior Data Engineer">
<meta property="og:description" content="I turn month-end spreadsheets into pipelines finance can trust.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE_URL}/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%231f3fff'/%3E%3Ctext x='16' y='23' font-family='Arial' font-weight='700' font-size='18' text-anchor='middle' fill='%23fff'%3EBM%3C/text%3E%3C/svg%3E">
<meta name="theme-color" content="#f3f1eb">
<script>(function(){{try{{var t=localStorage.getItem('theme')}}catch(e){{}}if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);document.documentElement.className='js'}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="xl" viewBox="0 0 12 15">
<path d="M1 .5h6.6L11 3.9V14a.5.5 0 0 1-.5.5h-9A.5.5 0 0 1 1 14z" fill="currentColor"/><path d="M7.6.5V3.9H11" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".8"/>
<path d="M3 6.2h6M3 8.6h6M3 11h6M5.1 6.2v6.6M7.2 6.2v6.6M3 6.2v6.6h6V6.2" fill="none" stroke="#fff" stroke-width=".7"/></symbol></svg>
<a class="skip" href="#main">Skip to content</a>

<header class="top" id="topbar">
  <a class="brand" href="#top">BHAVAN MEHTA</a>
  <nav class="nav" aria-label="Sections">
    <a href="#flow">Data flow</a><a href="#results">Results</a><a href="#experience">Experience</a><a href="#personal">Off the clock</a><a href="#how">How I work</a><a href="#contact">Contact</a>
  </nav>
  <div class="tools">
    <button class="tool" id="kbtn" type="button" aria-haspopup="dialog" aria-label="Open the command menu"><span class="kl">Menu</span><kbd>Ctrl K</kbd></button>
    <button class="tool" id="theme" type="button" aria-label="Switch colour theme"><span id="theme-t">Dark</span></button>
  </div>
</header>

<main id="main">
<section class="hero" id="top">
  <h1 class="d">Six years of making sure the number in the meeting is <span>the right one.</span></h1>
  <div class="id">
    <div class="who"><img class="ph" src="portrait_sq.jpg" width="240" height="240" alt="Bhavan Mehta"><div><b>Bhavan Mehta</b><span>{ROLE}</span></div></div>
    <p class="sub">I turn month-end spreadsheets into pipelines finance can trust.</p>
    <div class="links">{LINKS}</div>
  </div>
  <div class="po"><p>bhavanmehtap@gmail.com | linkedin.com/in/bhavan-mehta | github.com/Bhavanmehta | San Francisco Bay Area</p>
    <p>Senior Data Engineer with 6+ years building data pipelines, semantic models and reporting for finance teams. At Tesla I support FP&amp;A, Accounting and Investor Relations through the close, forecasting, CAPEX, earnings prep and financial controls, with models used by 200+ stakeholders. A lot of my work replaces manual Excel processes with automated ones.</p></div>
  <div class="tiles">
    <a class="t" href="#case-model"><b class="d"><s>25</s> <small>to</small> <em>1</em></b><div class="viz" role="img" aria-label="25 spreadsheet files became 1 model refresh"><div class="sheets">{SHEETS}</div><span class="arr">&rarr;</span>{X("one")}</div><p>Excel workbooks replaced by one model refresh</p></a>
    <a class="t" href="#case-close"><b class="d"><s>3 h</s> <small>to</small> <em>30 min</em></b><div class="viz" role="img" aria-label="Two bars drawn to scale: 3 hours and 30 minutes"><div class="bars"><span></span><span></span></div></div><p>Month-end variance analysis</p></a>
    <a class="t" href="#flow"><b class="d">50+</b><div class="viz" role="img" aria-label="50 marks, one per pipeline"><div class="dots p50">{PIPES}</div><span class="plus">+</span></div><p>Airflow and SSIS pipelines feeding the close</p></a>
    <a class="t" href="#flow"><b class="d">200+</b><div class="viz" role="img" aria-label="200 dots, one per stakeholder"><div class="dots p200">{PEOPLE}</div><span class="plus">+</span></div><p>Stakeholders on one forecast cube</p></a>
  </div>
</section>

<section class="band" aria-label="What the work is for">
  <p class="d">Finance data that holds up in a <span>close</span>, a <span>forecast</span> and an <span>audit</span>.</p>
</section>

<section class="sec" id="flow" aria-labelledby="h-flow">
  <header class="sh"><span class="no">01</span><h2 class="d" id="h-flow">The data flow</h2>
    <p>The finance data flow I work on at Tesla, simplified. Pick a stage to see what I did there.</p>
    <button class="btn js-only" id="run" type="button"><span aria-hidden="true">&#9654;</span> Run it</button></header>
  <ol class="stages" id="stages">{FLOW}</ol>
  <p class="note">Work examples are described at resume level. System names and figures beyond what is public are left out on purpose.</p>
</section>

<section class="sec" id="results" aria-labelledby="h-res">
  <header class="sh"><span class="no">02</span><h2 class="d" id="h-res">Before and after</h2><p>Two changes, drawn to scale.</p></header>

  <article class="case" id="case-model">
    <div class="ex">
      <div class="ex-h"><h3 class="d">25 workbooks became one refresh</h3><button class="btn js-only" id="replay" type="button">Replay</button></div>
      <div class="fold" id="fold">
        <div><div class="grid25" id="grid25">{SHEETS}</div><p class="cap"><b class="d">25</b> Excel workbooks</p></div>
        <span class="arr big" aria-hidden="true">&rarr;</span>
        <div class="model"><p class="mh">{X("one")}<span>Corporate financial model</span></p><b class="d">One refresh</b>
          <ul class="chips st3"><li>P&amp;L</li><li>Balance sheet</li><li>Cash flow</li></ul></div>
      </div>
      <div class="days" role="img" aria-label="Consolidation took 7 to 10 days before. Now it is one refresh.">
        <div class="dr"><span>Before</span><div class="track"><i class="solid"></i><i class="range"></i></div><b>7 to 10 days</b></div>
        <div class="dr"><span>After</span><div class="track"><i class="tick"></i></div><b class="acc">One refresh</b></div>
        <p class="axis"><span>0</span><span>5</span><span>10 days</span></p>
      </div>
    </div>
    <div class="story"><p class="k">Case 1, Tesla</p>
      <dl><div><dt>Context</dt><dd>Tesla's corporate financial model ran on 25 Excel workbooks and a 7-10 day consolidation.</dd></div>
      <div><dt>What I did</dt><dd>Led the data engineering side of re-engineering the model.</dd></div>
      <div><dt>Result</dt><dd>One refresh of the P&amp;L, balance sheet and cash flow, used by finance leadership.</dd></div></dl></div>
  </article>

  <article class="case" id="case-close">
    <div class="ex">
      <div class="ex-h"><h3 class="d">The close, faster</h3><p class="lg"><i class="sw old"></i>Before <i class="sw new"></i>After</p></div>
      <div class="speed" id="speed" role="img" aria-label="Month-end variance analysis: 3 hours before, 30 minutes after. Daily inventory extracts: 90 minutes before, 10 minutes after.">
        <p class="sl">Month-end variance analysis</p>
        <div class="sb"><i class="old" style="--w:100%"></i><b>3 h</b></div><div class="sb"><i class="new" style="--w:16.667%"></i><b class="acc">30 min</b></div>
        <p class="sl">Daily inventory extracts</p>
        <div class="sb"><i class="old" style="--w:50%"></i><b>90 min</b></div><div class="sb"><i class="new" style="--w:5.556%"></i><b class="acc">10 min</b></div>
        <p class="axis ax7"><span>0</span><span>30</span><span>60</span><span>90</span><span>120</span><span>150</span><span>180 min</span></p>
      </div>
    </div>
    <div class="story"><p class="k">Case 2, Tesla</p>
      <dl><div><dt>Context</dt><dd>Month-end variance analysis took 3 hours. The daily inventory extracts took 90 minutes.</dd></div>
      <div><dt>What I did</dt><dd>Rewrote the stored procedures behind the Day-1 close. Separately, tuned the daily inventory extracts.</dd></div>
      <div><dt>Result</dt><dd>Variance analysis now takes 30 minutes, and the inventory extracts run in 10.</dd></div></dl></div>
  </article>
</section>

<section class="sec" id="experience" aria-labelledby="h-exp">
  <header class="sh"><span class="no">03</span><h2 class="d" id="h-exp">Experience</h2><p>Six years, drawn to scale. Pick a bar to jump to that role.</p></header>
  <div class="tl" aria-label="Timeline of roles, 2018 to now"><div class="tl-bars">{TIMELINE}</div><div class="tl-y" aria-hidden="true">{YEARS}</div><ul class="tl-k" aria-hidden="true"><li><i class="t1"></i>Earlier roles</li><li><i class="t2"></i>Onto Innovation</li><li><i class="t3"></i>Tesla, BI Developer</li><li><i class="t4"></i>Tesla, Senior Data Engineer</li></ul></div>
  {ROLES}
</section>

<section class="inv" id="personal" aria-labelledby="h-per">
  <header class="sh"><span class="no">04</span><h2 class="d" id="h-per"><span class="scr">Off the clock</span><span class="po-i">Personal projects</span></h2>
    <p>Two systems I built and run on my own time. Personal projects, 2026. Not Tesla work.</p></header>

  <article class="proj" id="breakoutai">
    <div class="proj-h"><div><p class="k">Personal project</p><h3 class="d">BreakoutAI</h3>
      <p class="lede">A daily stock market data platform for the US and India.</p>
      <ul class="pl"><li>Two scheduled jobs pull data for ~6,700 stocks every trading day from 10+ sources (market data APIs, SEC EDGAR filings, PDFs, FINRA) and publish it to a CDN.</li>
      <li>Checks stop a run and keep the previous day's data live if bad data shows up.</li>
      <li>Serverless Python REST APIs on Redis for a watchlist and live quotes, and an LLM assistant that writes read-only SQL.</li></ul>
      <ul class="chips"><li>Python</li><li>DuckDB</li><li>GitHub Actions</li><li>Vercel</li><li>Redis</li><li>LLMs</li></ul></div>
      <div class="pstats"><div><b class="d">~6,700</b><p>stocks every trading day</p></div><div><b class="d">10+</b><p>data sources</p></div>
        <div><b class="d">2</b><p>scheduled jobs, US and India</p></div><div><b class="d">4</b><p>guards against bad data</p></div></div></div>

    <div class="night" id="night" data-s="then">
      <div class="night-h"><h4 class="d">A bad run fails red and yesterday's data keeps serving</h4>
        <div class="tog js-only" role="group" aria-label="Show the run"><button type="button" data-s="then" aria-pressed="true">The night it broke</button><button type="button" data-s="now" aria-pressed="false">Now, with four guards</button></div></div>
      <ol class="runsteps">
        <li><span class="rs">fetch</span><p class="then bad"><b>Login failed.</b> Most prices came back blank.</p>
          <p class="now ok"><b>Guard 1.</b> Retry the login once.<br><b>Guard 2.</b> Date each record to the bar it actually priced.</p></li>
        <li><span class="rs">checks</span><p class="then bad"><b>Blanks got through.</b> NaN passes a "&lt;= 0" check.</p>
          <p class="now ok"><b>Guard 3.</b> Reject any price that is not a finite number.</p></li>
        <li><span class="rs">publish</span><p class="then bad"><b>Published anyway.</b></p>
          <p class="now ok"><b>Guard 4.</b> Abort the publish if the stock count falls below 67% of yesterday's.</p></li>
        <li><span class="rs">site</span><p class="then bad"><b>64% of India stocks had no price.</b> The site went down.</p>
          <p class="now ok"><b>The run fails red.</b> Yesterday's good data keeps serving.</p></li>
      </ol>
      <p class="trade"><b>What I'd tell you about it.</b> The login retry was not the real fix. The failure was intermittent, so the downstream guards are what keep bad data off the site.</p>
    </div>

    <div class="two">
      <div class="live" id="live"><div class="live-h"><h4 class="d">Last nightly run</h4><span class="pill" id="live-s">Last known run</span></div>
        <div class="lv"><div><b class="d" id="lv-us">4,047</b><p>US stocks published<br><span id="lv-us-d">as of 2026-11-12</span></p></div>
          <div><b class="d" id="lv-in">2,008</b><p>India stocks published<br><span id="lv-in-d">as of 2026-11-13</span></p></div></div>
        <p class="fine" id="lv-g">Generated 2026-11-13 02:22 UTC. This card reads the first 400 bytes of the public output file.</p></div>
      <article class="ledger" id="ledger"><p class="k">Personal project</p><h3 class="d">Ledger</h3><p class="lede">A self-hosted personal finance tracker.</p>
        <ul class="pl"><li>Pulls bank, card and brokerage accounts into one place via the Plaid and SnapTrade APIs, without double-counting pending charges.</li>
        <li>Sends Telegram alerts for large or duplicate charges, new subscriptions and low balances, plus spending digests and return tracking.</li>
        <li>Runs on a private VPS reachable only over Tailscale, with two-factor login, encrypted bank tokens and nightly encrypted backups.</li></ul>
        <ul class="chips"><li>Python</li><li>FastAPI</li><li>SQLite</li><li>Plaid</li><li>SnapTrade</li><li>Telegram</li><li>Linux</li></ul></article>
    </div>
  </article>
</section>

<section class="sec" id="how" aria-labelledby="h-how">
  <header class="sh"><span class="no">05</span><h2 class="d" id="h-how">How I work</h2><p>I find out why two numbers don't match, then build the pipeline so they always do.</p></header>
  <ol class="how">{HOWH}</ol>
  <div class="tiles beyond"><div class="t"><b class="d">6</b><p>Interns mentored, plus several new hires</p></div><div class="t"><b class="d">30+</b><p>Technical interviews run on SQL, DAX and data modeling</p></div>
    <div class="t"><b class="d">20+</b><p>Business users trained in DAX and Power Query</p></div><div class="t"><b class="d">1</b><p>AI agent built to help with code reviews</p></div></div>
</section>

<section class="sec" id="skills" aria-labelledby="h-sk">
  <header class="sh"><span class="no">06</span><h2 class="d" id="h-sk"><span class="scr">Toolkit</span><span class="po-i">Skills</span></h2><p>Work-used first.</p></header>
  <div class="sks">{SKH}</div>
  <div class="edu"><div><h3>Education</h3><p><b>M.S., Management Information Systems</b><br>UT Dallas, 2021. GPA 3.7.</p><p><b>B.E., Information Technology</b><br>GTU, India, 2018. GPA 3.7.</p></div>
    <div><h3>Certifications</h3><p><b>Microsoft Certified: Power BI Data Analyst Associate</b><br>PL-300</p><p><b>Tableau Certified Desktop Specialist</b></p></div></div>
</section>

<section class="contact" id="contact" aria-labelledby="h-con">
  <h2 class="d" id="h-con">Get in touch</h2>
  <p>Based in the San Francisco Bay Area. Email is the best way to reach me.</p>
  <a class="mail d" href="mailto:bhavanmehtap@gmail.com">bhavanmehtap@gmail.com</a>
  <div class="links"><button class="btn js-only" id="copy" type="button">Copy email</button><a class="l l1" href="resume.pdf">Resume</a><a class="l" href="https://www.linkedin.com/in/bhavan-mehta">LinkedIn</a><a class="l" href="https://github.com/Bhavanmehta">GitHub</a><button class="btn js-only" id="print" type="button">Print or save as PDF</button></div>
</section>
</main>

<footer class="foot"><span>Bhavan Mehta, Senior Data Engineer</span><span>Last updated 2026-11-16. Built by a Python script and checked by automated tests in three browsers.</span><a href="#top">Back to top</a></footer>

<div class="pal" id="pal" hidden><div class="pal-box" role="dialog" aria-modal="true" aria-label="Command menu">
  <input id="pal-q" type="text" placeholder="Jump to a section or run a command" autocomplete="off" aria-label="Search commands"><ul id="pal-l" role="listbox"></ul>
  <p class="fine">Up and down to move, Enter to run, Esc to close</p></div></div>
<p class="sr" id="say" aria-live="polite"></p>
<script>{JS}</script>
{COUNTER}
</body>
</html>
"""
(HERE / "index.html").write_text(HTML, encoding="utf-8")
print("index.html", round(len(HTML.encode("utf-8")) / 1024, 1), "KB")
