import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="PLACEMUX // ANALYTICS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# GLOBAL STYLES — Industrial Terminal Aesthetic
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow+Condensed:wght@300;400;600;700;900&family=Barlow:wght@300;400&display=swap');

/* ---- ROOT VARIABLES ---- */
:root {
    --bg:        #0a0c0e;
    --bg2:       #0f1215;
    --bg3:       #141820;
    --border:    #1e2530;
    --amber:     #e8a020;
    --amber-dim: #7a5010;
    --green:     #2ecc71;
    --green-dim: #145e35;
    --red:       #e84040;
    --text:      #c8cdd5;
    --text-dim:  #555f6e;
    --mono:      'Share Tech Mono', monospace;
    --cond:      'Barlow Condensed', sans-serif;
    --body:      'Barlow', sans-serif;
}

/* ---- GLOBAL RESET ---- */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body);
}

.stApp {
    background: var(--bg) !important;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 39px,
            rgba(30,37,48,0.35) 39px,
            rgba(30,37,48,0.35) 40px
        ) !important;
}

/* ---- SCANLINE OVERLAY ---- */
.stApp::before {
    content: "";
    pointer-events: none;
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 2px,
        rgba(0,0,0,0.08) 2px,
        rgba(0,0,0,0.08) 4px
    );
    z-index: 9999;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 2px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
}

[data-testid="stSidebarContent"] {
    padding-top: 2rem !important;
}

/* ---- SELECTBOX / DATE INPUT ---- */
.stSelectbox > div > div,
.stDateInput > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    color: var(--amber) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
}

/* ---- HEADER BAND ---- */
.pmx-header {
    display: flex;
    align-items: baseline;
    gap: 1.4rem;
    padding: 1.8rem 0 0.4rem 0;
    border-bottom: 2px solid var(--amber);
    margin-bottom: 2rem;
}

.pmx-logo {
    font-family: var(--cond);
    font-weight: 900;
    font-size: 2.8rem;
    letter-spacing: -0.02em;
    color: var(--amber);
    text-transform: uppercase;
    line-height: 1;
}

.pmx-logo span {
    color: var(--text-dim);
    font-weight: 300;
}

.pmx-tag {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-dim);
    border: 1px solid var(--border);
    padding: 0.2rem 0.6rem;
    letter-spacing: 0.12em;
}

.pmx-sub {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--green);
    letter-spacing: 0.06em;
    margin-left: auto;
}

/* ---- SECTION LABEL ---- */
.pmx-section {
    font-family: var(--cond);
    font-weight: 700;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--amber);
    border-left: 3px solid var(--amber);
    padding-left: 0.6rem;
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.pmx-section::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ---- KPI CARDS ---- */
.pmx-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 2rem;
}

.pmx-kpi {
    background: var(--bg2);
    padding: 1.4rem 1.6rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.pmx-kpi-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--text-dim);
    text-transform: uppercase;
}

.pmx-kpi-value {
    font-family: var(--cond);
    font-weight: 900;
    font-size: 3rem;
    line-height: 1;
    color: var(--amber);
}

.pmx-kpi-unit {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--green);
}

/* ---- CHART PANELS ---- */
.pmx-panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-top: 2px solid var(--amber-dim);
    padding: 1.2rem 1.4rem 0.8rem 1.4rem;
    margin-bottom: 1.2rem;
}

.pmx-panel-title {
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pmx-panel-title::before {
    content: "▸";
    color: var(--amber);
}

/* ---- INSIGHT BLOCK ---- */
.pmx-insight {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 4px solid var(--green);
    padding: 1.2rem 1.6rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    line-height: 2;
    color: var(--text);
    margin-top: 1.5rem;
}

.pmx-insight b {
    color: var(--amber);
}

/* ---- DATAFRAME ---- */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
}

.stDataFrame * {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    background: var(--bg2) !important;
    color: var(--text) !important;
}

/* ---- DIVIDER ---- */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ---- SIDEBAR HEADER TEXT ---- */
.pmx-sidebar-head {
    font-family: var(--cond);
    font-weight: 900;
    font-size: 1.1rem;
    letter-spacing: 0.1em;
    color: var(--amber);
    text-transform: uppercase;
    border-bottom: 1px solid var(--amber-dim);
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem;
}

/* ---- PLOTLY CHART BACKGROUND FIX ---- */
.js-plotly-plot, .plot-container {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# PLOTLY DARK TEMPLATE
# =====================================================
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(15,18,21,0)",
    plot_bgcolor="rgba(15,18,21,0)",
    font=dict(
        family="Share Tech Mono, monospace",
        size=11,
        color="#555f6e"
    ),
    title_font=dict(
        family="Barlow Condensed, sans-serif",
        size=13,
        color="#c8cdd5"
    ),
    xaxis=dict(
        gridcolor="#1e2530",
        linecolor="#1e2530",
        tickcolor="#1e2530",
        zerolinecolor="#1e2530"
    ),
    yaxis=dict(
        gridcolor="#1e2530",
        linecolor="#1e2530",
        tickcolor="#1e2530",
        zerolinecolor="#1e2530"
    ),
    margin=dict(l=30, r=20, t=40, b=30),
    colorway=["#e8a020", "#2ecc71", "#e84040", "#3498db", "#9b59b6"],
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="#1e2530",
        borderwidth=1
    )
)


def apply_layout(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    students  = pd.read_csv("Data/Student.csv")
    skills    = pd.read_csv("Data/Skills.csv")
    colleges  = pd.read_csv("Data/College.csv")
    activity  = pd.read_csv("Data/Activity.csv")

    try:
        placements = pd.read_csv("Data/Placement.csv")
    except Exception:
        placements = pd.read_excel("Data/Placement.xlsx")

    for df in [students, skills, colleges, activity, placements]:
        df.columns = df.columns.str.strip().str.lower()

    if "date" in activity.columns:
        activity["date"] = pd.to_datetime(activity["date"], errors="coerce")
        activity = activity.dropna(subset=["date"])

    try:
        if all(c in students.columns for c in ["college_id"]) and \
           all(c in colleges.columns for c in ["college_id", "college_name"]):
            for df in [students, colleges]:
                df["college_id"] = (
                    df["college_id"].fillna("").astype(str).str.strip()
                     .str.replace(".0", "", regex=False)
                )
            students = pd.merge(
                students,
                colleges[["college_id", "college_name"]],
                on="college_id", how="left"
            )
    except Exception as e:
        st.error(f"Merge Error: {e}")

    if "placed" in students.columns:
        students["placed"] = students["placed"].fillna(0)

    return students, skills, placements, colleges, activity


students, skills, placements, colleges, activity = load_data()

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="pmx-header">
    <div class="pmx-logo">Place<span>mux</span></div>
    <div class="pmx-tag">ANALYTICS ENGINE</div>
    <div class="pmx-tag">v2.0</div>
    <div class="pmx-sub">● SYSTEM LIVE</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown('<div class="pmx-sidebar-head">// FILTERS</div>', unsafe_allow_html=True)

college_choice = "All"
if "college_name" in students.columns:
    opts = sorted(students["college_name"].dropna().astype(str).unique())
    college_choice = st.sidebar.selectbox("COLLEGE", ["All"] + list(opts))

skill_choice = "All"
if "skill_id" in activity.columns:
    s_opts = sorted(activity["skill_id"].dropna().astype(str).unique())
    skill_choice = st.sidebar.selectbox("SKILL ID", ["All"] + list(s_opts))

date_range = None
if "date" in activity.columns:
    min_d = activity["date"].min().date()
    max_d = activity["date"].max().date()
    date_range = st.sidebar.date_input("DATE RANGE", [min_d, max_d])

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<span style="font-family:\'Share Tech Mono\',monospace;font-size:0.62rem;'
    'color:#555f6e;letter-spacing:0.1em;">PLACEMUX ANALYTICS PLATFORM<br>'
    'STUDENT INTELLIGENCE SYSTEM</span>',
    unsafe_allow_html=True
)

# =====================================================
# APPLY FILTERS
# =====================================================
df_students = students.copy()
df_activity = activity.copy()

if college_choice != "All" and "college_name" in df_students.columns:
    df_students = df_students[df_students["college_name"] == college_choice]

if skill_choice != "All" and "skill_id" in df_activity.columns:
    df_activity = df_activity[df_activity["skill_id"].astype(str) == skill_choice]

if date_range and len(date_range) == 2 and "date" in df_activity.columns:
    df_activity = df_activity[
        (df_activity["date"].dt.date >= date_range[0]) &
        (df_activity["date"].dt.date <= date_range[1])
    ]

# =====================================================
# KPI SECTION
# =====================================================
st.markdown('<div class="pmx-section">01 — SYSTEM OVERVIEW</div>', unsafe_allow_html=True)

total_students   = len(df_students)
avg_score        = round(df_students["avg_score"].mean(), 1)       if "avg_score"       in df_students.columns else "—"
avg_level        = round(df_students["current_level"].mean(), 1)   if "current_level"   in df_students.columns else "—"
placement_pct    = round(df_students["placed"].mean() * 100, 1)    if "placed"          in df_students.columns else "—"

st.markdown(f"""
<div class="pmx-kpi-grid">
    <div class="pmx-kpi">
        <div class="pmx-kpi-label">Total Students</div>
        <div class="pmx-kpi-value">{total_students:,}</div>
        <div class="pmx-kpi-unit">ENROLLED</div>
    </div>
    <div class="pmx-kpi">
        <div class="pmx-kpi-label">Average Score</div>
        <div class="pmx-kpi-value">{avg_score}</div>
        <div class="pmx-kpi-unit">OUT OF 100</div>
    </div>
    <div class="pmx-kpi">
        <div class="pmx-kpi-label">Average Level</div>
        <div class="pmx-kpi-value">{avg_level}</div>
        <div class="pmx-kpi-unit">CURRENT</div>
    </div>
    <div class="pmx-kpi">
        <div class="pmx-kpi-label">Placement Rate</div>
        <div class="pmx-kpi-value">{placement_pct}</div>
        <div class="pmx-kpi-unit">PERCENT</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# ACTIVITY TRENDS
# =====================================================
st.markdown('<div class="pmx-section">02 — ACTIVITY TRENDS</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")

with col1:
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">DAILY ACTIVE USERS</div>', unsafe_allow_html=True)
    if "date" in df_activity.columns and "student_id" in df_activity.columns:
        dau = df_activity.groupby("date")["student_id"].nunique().reset_index()
        dau.columns = ["date", "DAU"]
        fig1 = px.area(dau, x="date", y="DAU")
        fig1.update_traces(
            line_color="#e8a020", fillcolor="rgba(232,160,32,0.08)",
            line_width=1.5
        )
        fig1.update_layout(**PLOTLY_LAYOUT, title=None)
        st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">WEEKLY ACTIVITY VOLUME</div>', unsafe_allow_html=True)
    if "date" in df_activity.columns:
        weekly = df_activity.copy()
        weekly["week"] = weekly["date"].dt.to_period("W").astype(str)
        weekly = weekly.groupby("week").size().reset_index(name="activity")
        fig2 = px.bar(weekly, x="week", y="activity")
        fig2.update_traces(marker_color="#2ecc71", marker_line_width=0)
        fig2.update_layout(**PLOTLY_LAYOUT, title=None)
        fig2.update_xaxes(tickangle=-45, tickfont=dict(size=8))
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PLACEMENT FUNNEL
# =====================================================
st.markdown('<div class="pmx-section">03 — PLACEMENT FUNNEL</div>', unsafe_allow_html=True)

interview_count = 0
placed_count    = 0

if "interview_status" in df_students.columns:
    interview_count = len(df_students[df_students["interview_status"] == "Yes"])
if "placed" in df_students.columns:
    placed_count = len(df_students[df_students["placed"] == 1])

funnel_df = pd.DataFrame({
    "Stage": ["Total Students", "Level 50+", "Interviewed", "Placed"],
    "Count": [
        len(df_students),
        len(df_students[df_students["current_level"] >= 50]) if "current_level" in df_students.columns else 0,
        interview_count,
        placed_count
    ]
})

st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">CONVERSION PIPELINE</div>', unsafe_allow_html=True)
fig3 = px.funnel(funnel_df, x="Count", y="Stage")
fig3.update_traces(
    marker_color=["#e8a020", "#c07818", "#906010", "#604008"],
    textfont=dict(family="Share Tech Mono, monospace", size=11, color="#c8cdd5")
)
fig3.update_layout(**PLOTLY_LAYOUT, title=None)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# SKILL ANALYSIS
# =====================================================
st.markdown('<div class="pmx-section">04 — SKILL INTELLIGENCE</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")
skill_avg = None

with col1:
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">AVG SCORE BY SKILL</div>', unsafe_allow_html=True)
    if "skill_id" in df_activity.columns and "score" in df_activity.columns:
        skill_avg = df_activity.groupby("skill_id")["score"].mean().reset_index()
        fig4 = px.bar(skill_avg, x="skill_id", y="score")
        fig4.update_traces(
            marker_color="#e8a020",
            marker_line_width=0
        )
        fig4.update_layout(**PLOTLY_LAYOUT, title=None)
        st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">PASS RATE BY SKILL</div>', unsafe_allow_html=True)
    if "skill" in skills.columns and "pass_rate" in skills.columns:
        color_col = "difficulty_level" if "difficulty_level" in skills.columns else None
        fig5 = px.bar(skills, x="skill", y="pass_rate", color=color_col,
                      color_discrete_sequence=["#2ecc71","#e8a020","#e84040"])
        fig5.update_traces(marker_line_width=0)
        fig5.update_layout(**PLOTLY_LAYOUT, title=None)
        fig5.update_xaxes(tickangle=-30)
        st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# COLLEGE PERFORMANCE
# =====================================================
st.markdown('<div class="pmx-section">05 — COLLEGE PERFORMANCE</div>', unsafe_allow_html=True)

if "college_name" in colleges.columns and "placement_rate" in colleges.columns:
    sorted_colleges = colleges.sort_values("placement_rate", ascending=True)
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">PLACEMENT RATE BY INSTITUTION</div>', unsafe_allow_html=True)
    fig6 = px.bar(
        sorted_colleges,
        x="placement_rate",
        y="college_name",
        orientation="h"
    )
    fig6.update_traces(
        marker_color="#e8a020",
        marker_line_width=0
    )
    fig6.update_layout(**PLOTLY_LAYOUT, title=None, height=max(300, len(sorted_colleges)*30))
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STUDENT DISTRIBUTION
# =====================================================
st.markdown('<div class="pmx-section">06 — STUDENT DISTRIBUTION</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")

with col1:
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">SCORE FREQUENCY</div>', unsafe_allow_html=True)
    if "avg_score" in df_students.columns:
        fig7 = px.histogram(df_students, x="avg_score", nbins=20)
        fig7.update_traces(
            marker_color="#2ecc71",
            marker_line_color="#0a0c0e",
            marker_line_width=1
        )
        fig7.update_layout(**PLOTLY_LAYOUT, title=None)
        st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">LEVEL vs SCORE MATRIX</div>', unsafe_allow_html=True)
    if "current_level" in df_students.columns and "avg_score" in df_students.columns:
        color_col = "placed" if "placed" in df_students.columns else None
        fig8 = px.scatter(
            df_students, x="current_level", y="avg_score", color=color_col,
            color_continuous_scale=["#1e2530", "#e8a020"]
        )
        fig8.update_traces(marker=dict(size=5, opacity=0.7, line=dict(width=0)))
        fig8.update_layout(**PLOTLY_LAYOUT, title=None)
        st.plotly_chart(fig8, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# HEATMAP
# =====================================================
st.markdown('<div class="pmx-section">07 — SKILL × ACTIVITY HEATMAP</div>', unsafe_allow_html=True)

if all(c in df_activity.columns for c in ["skill_id", "activity_type", "score"]):
    heatmap = df_activity.pivot_table(
        index="skill_id", columns="activity_type", values="score", aggfunc="mean"
    ).fillna(0)
    st.markdown('<div class="pmx-panel"><div class="pmx-panel-title">PERFORMANCE MATRIX</div>', unsafe_allow_html=True)
    fig9 = px.imshow(
        heatmap, aspect="auto",
        color_continuous_scale=[
            [0,   "#0a0c0e"],
            [0.5, "#7a5010"],
            [1,   "#e8a020"]
        ]
    )
    fig9.update_layout(**PLOTLY_LAYOUT, title=None)
    st.plotly_chart(fig9, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# ANOMALY / RISK ANALYSIS
# =====================================================
st.markdown('<div class="pmx-section">08 — RISK FLAGGING</div>', unsafe_allow_html=True)

if "current_level" in df_students.columns and "avg_score" in df_students.columns:
    risk_df = df_students.dropna(subset=["current_level", "avg_score"]).copy()

    if len(risk_df) > 10:
        model = IsolationForest(contamination=0.1, random_state=42)
        risk_df["level_norm"] = risk_df["current_level"] / 100
        risk_df["score_norm"] = risk_df["avg_score"] / 100
        risk_df["flag"] = model.fit_predict(risk_df[["level_norm", "score_norm"]])

        anomalies = risk_df[risk_df["flag"] == -1]
        display_cols = [c for c in ["avg_score", "current_level", "college_name"] if c in anomalies.columns]

        st.markdown(
            f'<div class="pmx-panel"><div class="pmx-panel-title">'
            f'ANOMALOUS RECORDS — {len(anomalies)} FLAGGED</div>',
            unsafe_allow_html=True
        )
        st.dataframe(anomalies[display_cols], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# QUICK INSIGHTS
# =====================================================
st.markdown('<div class="pmx-section">09 — INTELLIGENCE SUMMARY</div>', unsafe_allow_html=True)

try:
    low_skill = skill_avg.sort_values("score").iloc[0]["skill_id"] if skill_avg is not None else "N/A"
except Exception:
    low_skill = "N/A"

try:
    top_college = colleges.sort_values("placement_rate", ascending=False).iloc[0]["college_name"]
except Exception:
    top_college = "N/A"

st.markdown(f"""
<div class="pmx-insight">
    <b>▸ SKILL GAP DETECTED</b> — Students underperform in skill: <b>{low_skill}</b><br>
    <b>▸ TOP INSTITUTION</b> — Best placement rate recorded at: <b>{top_college}</b><br>
    <b>▸ PATTERN</b> — Higher-level students consistently achieve better placement outcomes.<br>
    <b>▸ RECOMMENDATION</b> — Prioritise intervention for low-performing cohorts to lift aggregate outcomes.
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)