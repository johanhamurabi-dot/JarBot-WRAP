import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Jar Test Robot | G-Value to RPM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* GLOBAL */
.stApp {
    background: linear-gradient(135deg, #eef7ff 0%, #f7fbff 45%, #ffffff 100%) !important;
    color: #0f172a !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111F 0%, #102A43 100%) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: white !important;
}

/* INPUTS: white box + black text, even in dark mode */
.stNumberInput input,
.stTextInput input,
.stTextArea textarea,
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
    background-color: white !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

/* Number input buttons */
.stNumberInput button,
[data-testid="stSidebar"] button {
    background-color: #f8fafc !important;
    color: #111111 !important;
    border-color: #CBD5E1 !important;
}

/* SELECTBOX - FORCE LIGHT STYLE */

.stSelectbox,
.stSelectbox * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: white !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: white !important;
    color: #111111 !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #111111 !important;
}

.stSelectbox div[data-baseweb="select"] input {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stSelectbox * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

[data-testid="stSidebar"] .stSelectbox div {
    background: white !important;
}

div[data-baseweb="popover"] {
    background: white !important;
}

div[data-baseweb="popover"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

li[role="option"] {
    background: white !important;
    color: #111111 !important;
}

li[role="option"]:hover {
    background: #E2E8F0 !important;
}

/* Dropdown menu */
div[data-baseweb="popover"] div,
div[data-baseweb="menu"] div,
ul[role="listbox"] li,
li[role="option"] {
    background-color: white !important;
    color: #111111 !important;
}

/* Sidebar slider text */
[data-testid="stSidebar"] .stSlider * {
    color: white !important;
}

/* HERO */
.hero {
    background:
    linear-gradient(135deg, rgba(0,150,255,.90), rgba(0,220,180,.82)),
    url("https://images.unsplash.com/photo-1581093458791-9d15482442f6?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    padding: 38px;
    border-radius: 28px;
    color: white !important;
    box-shadow: 0 14px 34px rgba(0,0,0,.18);
    margin-bottom: 25px;
}

.hero * {
    color: white !important;
}

.hero-title {
    font-size: 46px;
    font-weight: 900;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 18px;
    font-weight: 500;
}

.status-pill {
    display: inline-block;
    background: rgba(255,255,255,.22);
    padding: 8px 16px;
    border-radius: 999px;
    font-weight: 700;
    margin-top: 14px;
    backdrop-filter: blur(8px);
}

/* CARDS */
.card {
    background: white !important;
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 8px 24px rgba(20,40,80,.10);
    border: 1px solid #E6EAF0;
}

.card * {
    color: #0f172a !important;
}

.metric-big {
    font-size: 44px;
    font-weight: 900;
    color: #07111F !important;
}

.metric-label {
    font-size: 15px;
    color: #64748B !important;
    font-weight: 700;
}

.metric-sub {
    font-size: 13px;
    color: #94A3B8 !important;
}

.blue-card { border-left: 8px solid #0096FF; }
.green-card { border-left: 8px solid #00D4A6; }
.yellow-card { border-left: 8px solid #FFC857; }
.purple-card { border-left: 8px solid #7C3AED; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: white !important;
    border-radius: 16px;
    padding: 12px 18px;
    font-weight: 800;
    border: 1px solid #E6EAF0;
    color: #111111 !important;
}

.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {
    color: #111111 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0096FF, #00D4A6) !important;
}

.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span {
    color: white !important;
}

/* DATAFRAME / BUTTON */
.stDataFrame {
    background: white !important;
    color: #111111 !important;
}

.stDownloadButton button {
    border-radius: 14px;
    background: linear-gradient(135deg, #0096FF, #00D4A6) !important;
    color: white !important;
    border: none;
    font-weight: 800;
}

.stDownloadButton button * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CALCULATIONS
# ============================================================
def water_viscosity(T_c):
    return 2.414e-5 * 10 ** (247.8 / (T_c + 133.15))

def calculate_robot_1l_rpm(G, T, V, A, Cd, rho, Cr, Lrev):
    mu = water_viscosity(T)
    v = ((2 * (G**2) * mu * V) / (Cd * rho * A)) ** (1/3)
    rpm = (60 * v) / (Cr * Lrev)
    return rpm, mu, v

# Traditional 2 L chart data digitized visually from the Phipps & Bird graph.
G_POINTS = np.array([12, 18, 28, 50, 80, 100, 200, 300], dtype=float)

RPM_TABLE = {
    4:  np.array([16, 22, 31, 52, 74, 87, 160, 215], dtype=float),
    10: np.array([17, 24, 34, 56, 79, 92, 170, 225], dtype=float),
    16: np.array([17.5, 24.5, 35, 58, 82, 96, 175, 232], dtype=float),
    22: np.array([18, 26, 37, 60, 85, 100, 180, 240], dtype=float)
}

TEMP_POINTS = np.array([4, 10, 16, 22], dtype=float)

def traditional_2l_rpm_from_graph(G, T):
    """
    Traditional 2 L method based on the Phipps & Bird chart.
    Uses interpolation over digitized chart points.
    """
    G_clamped = np.clip(float(G), G_POINTS.min(), G_POINTS.max())
    T_clamped = np.clip(float(T), TEMP_POINTS.min(), TEMP_POINTS.max())

    rpm_at_each_temp = np.array([
        np.interp(G_clamped, G_POINTS, RPM_TABLE[temp])
        for temp in TEMP_POINTS
    ], dtype=float)

    rpm = np.interp(T_clamped, TEMP_POINTS, rpm_at_each_temp)

    return rpm, water_viscosity(T), np.nan

def calculate_required_rpm(G, T, method, A, Cd, rho, Cr, Lrev):
    if method == "Robot method - 1 L":
        return calculate_robot_1l_rpm(G, T, 0.001, A, Cd, rho, Cr, Lrev)
    return traditional_2l_rpm_from_graph(G, T)

def rpm_curve(G_range, T, method, A, Cd, rho, Cr, Lrev):
    return np.array([calculate_required_rpm(g, T, method, A, Cd, rho, Cr, Lrev)[0] for g in G_range])

def rpm_map(G_grid, T_grid, method, A, Cd, rho, Cr, Lrev):
    Z = np.zeros((len(T_grid), len(G_grid)))
    for i, temp in enumerate(T_grid):
        for j, g_val in enumerate(G_grid):
            Z[i, j] = calculate_required_rpm(g_val, temp, method, A, Cd, rho, Cr, Lrev)[0]
    return Z

def g_from_rpm_traditional_2l(rpm, T):
    """
    Inverse interpolation for the traditional 2 L chart.
    Works with scalar RPM and array RPM.
    """
    rpm_arr = np.asarray(rpm, dtype=float)
    T_clamped = np.clip(float(T), TEMP_POINTS.min(), TEMP_POINTS.max())

    g_at_each_temp = []
    for temp in TEMP_POINTS:
        rpm_curve = RPM_TABLE[temp]
        rpm_clamped = np.clip(rpm_arr, rpm_curve.min(), rpm_curve.max())
        g_at_each_temp.append(np.interp(rpm_clamped, rpm_curve, G_POINTS))

    g_at_each_temp = np.array(g_at_each_temp, dtype=float)

    if T_clamped <= TEMP_POINTS[0]:
        result = g_at_each_temp[0]
    elif T_clamped >= TEMP_POINTS[-1]:
        result = g_at_each_temp[-1]
    else:
        upper_idx = np.searchsorted(TEMP_POINTS, T_clamped)
        lower_idx = upper_idx - 1
        t0 = TEMP_POINTS[lower_idx]
        t1 = TEMP_POINTS[upper_idx]
        weight = (T_clamped - t0) / (t1 - t0)
        result = g_at_each_temp[lower_idx] * (1 - weight) + g_at_each_temp[upper_idx] * weight

    if np.isscalar(rpm):
        return float(result)

    return result



def apply_clean_plot_style(fig):
    """Force Plotly charts to stay readable in Streamlit light/dark mode."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#111111", size=14),
        title_font=dict(color="#111111", size=20),
        legend=dict(
            font=dict(color="#111111"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1
        )
    )

    fig.update_xaxes(
        color="#111111",
        title_font=dict(color="#111111"),
        tickfont=dict(color="#111111"),
        gridcolor="#D8DEE9",
        zerolinecolor="#CBD5E1",
        linecolor="#94A3B8"
    )

    fig.update_yaxes(
        color="#111111",
        title_font=dict(color="#111111"),
        tickfont=dict(color="#111111"),
        gridcolor="#D8DEE9",
        zerolinecolor="#CBD5E1",
        linecolor="#94A3B8"
    )

    return fig

# ============================================================
# SIDEBAR INPUTS
# ============================================================
st.sidebar.title("⚙️ Inputs")

G = st.sidebar.number_input("Target G-Value (s⁻¹)", min_value=1.0, max_value=600.0, value=100.0, step=1.0)
T = st.sidebar.slider("Water temperature (°C)", min_value=0, max_value=35, value=20, step=1)

method = st.sidebar.selectbox(
    "Jar test method",
    ["Robot method - 1 L", "Traditional method - 2 L"],
    index=0
)

if method == "Robot method - 1 L":
    jar_setup = "1 L Robot"
    jar_height = "145 mm"
    method_note = "Physical robot model"
else:
    jar_setup = "2 L Traditional"
    jar_height = "8.2 in / 208.28 mm"
    method_note = "Empirical chart model"

st.sidebar.divider()
st.sidebar.subheader("Robot constants")
A = st.sidebar.number_input("Paddle area A (m²)", value=0.00164, format="%.6f")
Cd = st.sidebar.number_input("Drag coefficient Cd", value=1.9, format="%.3f")
rho = st.sidebar.number_input("Water density ρ (kg/m³)", value=998.0, format="%.1f")
Cr = st.sidebar.number_input("Relative velocity constant Cr", value=0.75, format="%.3f")
Lrev = st.sidebar.number_input("Tip distance Lrev (m/rev)", value=0.235619449, format="%.9f")

if method == "Traditional method - 2 L":
    st.sidebar.caption("For 2 L traditional mode, RPM is estimated from the chart. Robot constants are not used.")

RPM, mu, v = calculate_required_rpm(G, T, method, A, Cd, rho, Cr, Lrev)

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="hero">
    <div class="hero-title">🤖 Jar Test RPM Calculator</div>
    <div class="hero-subtitle">Choose the method, enter G-Value, and get the required RPM.</div>
    <div class="status-pill">● {method_note}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TOP METRICS
# ============================================================
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="card blue-card"><div class="metric-label">Required RPM</div><div class="metric-big">{RPM:.2f}</div><div class="metric-sub">Motor setpoint</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card green-card"><div class="metric-label">Target G</div><div class="metric-big">{G:.0f}</div><div class="metric-sub">s⁻¹</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card yellow-card"><div class="metric-label">Temperature</div><div class="metric-big">{T}°C</div><div class="metric-sub">Water sample</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="card purple-card"><div class="metric-label">Method</div><div class="metric-big">{jar_setup}</div><div class="metric-sub">Height: {jar_height}</div></div>', unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 RPM vs G", "🌡️ Heatmap", "🧊 3D Surface", "📊 G-Curves", "🤖 Protocol"])

# ============================================================
# TAB 1
# ============================================================
with tab1:
    G_range = np.linspace(10, 300, 200)
    rpm_values = rpm_curve(G_range, T, method, A, Cd, rho, Cr, Lrev)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=G_range, y=rpm_values, mode="lines", name=f"T = {T} °C", line=dict(width=5, color="#0096FF")))
    fig.add_trace(go.Scatter(x=[G], y=[RPM], mode="markers+text", name="Current point", text=[f"{RPM:.1f} RPM"], textposition="top center", marker=dict(size=16, color="#00D4A6", line=dict(color="#07111F", width=3))))
    fig.update_layout(title=f"Required RPM vs Target G — {method}", xaxis_title="G-Value, G (s⁻¹)", yaxis_title="Required RPM", template="plotly_white", height=600, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white")
    fig = apply_clean_plot_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2
# ============================================================
with tab2:
    G_grid = np.linspace(10, 300, 140)
    T_grid = np.linspace(4, 22, 90) if method == "Traditional method - 2 L" else np.linspace(0, 35, 90)
    Z = rpm_map(G_grid, T_grid, method, A, Cd, rho, Cr, Lrev)
    fig = go.Figure(data=go.Heatmap(x=G_grid, y=T_grid, z=Z, colorscale="Turbo", colorbar=dict(title="RPM")))
    fig.add_trace(go.Scatter(x=[G], y=[np.clip(T, T_grid.min(), T_grid.max())], mode="markers+text", marker=dict(size=15, color="white", line=dict(color="black", width=3)), text=[f"{RPM:.1f} RPM"], textposition="top center", name="Current input"))
    fig.update_layout(title=f"RPM Heatmap — {method}", xaxis_title="G-Value, G (s⁻¹)", yaxis_title="Temperature (°C)", template="plotly_white", height=650)
    fig = apply_clean_plot_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 3
# ============================================================
with tab3:
    G_grid_3d = np.linspace(10, 300, 80)
    T_grid_3d = np.linspace(4, 22, 55) if method == "Traditional method - 2 L" else np.linspace(0, 35, 55)
    Z3 = rpm_map(G_grid_3d, T_grid_3d, method, A, Cd, rho, Cr, Lrev)
    fig = go.Figure(data=[go.Surface(x=G_grid_3d, y=T_grid_3d, z=Z3, colorscale="Viridis", colorbar=dict(title="RPM"))])
    fig.add_trace(go.Scatter3d(x=[G], y=[np.clip(T, T_grid_3d.min(), T_grid_3d.max())], z=[RPM], mode="markers", marker=dict(size=7, color="red"), name="Current input"))
    fig.update_layout(
        title=f"3D Calibration Surface — {method}",
        scene=dict(
            xaxis_title="G-Value (s⁻¹)",
            yaxis_title="Temperature (°C)",
            zaxis_title="RPM",
            xaxis=dict(color="#111111", gridcolor="#CBD5E1", backgroundcolor="white"),
            yaxis=dict(color="#111111", gridcolor="#CBD5E1", backgroundcolor="white"),
            zaxis=dict(color="#111111", gridcolor="#CBD5E1", backgroundcolor="white")
        ),
        height=720,
        template="plotly_white"
    )
    fig = apply_clean_plot_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 4
# ============================================================
with tab4:
    rpm_axis = np.logspace(np.log10(10), np.log10(320), 250)
    temps = [4, 10, 16, 22]
    colors = ["#0096FF", "#00D4A6", "#FFC857", "#7C3AED"]
    fig = go.Figure()
    if method == "Traditional method - 2 L":
        for Tc, color in zip(temps, colors):
            G_axis = g_from_rpm_traditional_2l(rpm_axis, Tc)
            fig.add_trace(go.Scatter(x=rpm_axis, y=G_axis, mode="lines", name=f"{Tc} °C", line=dict(width=4, color=color)))
        rpm_ref = np.array([18, 26, 37, 200, 240])
        G_ref = np.array([12, 18, 28, 250, 300])
        fig.add_trace(go.Scatter(x=rpm_ref, y=G_ref, mode="markers+text", name="Chart reference", marker=dict(size=11, color="black"), text=["18→12", "26→18", "37→28", "200→250", "240→300"], textposition="top center"))
        chart_title = "Traditional 2 L G-Curves Based on Chart"
    else:
        for Tc, color in zip(temps, colors):
            mu_c = water_viscosity(Tc)
            v_axis = Cr * ((Lrev * rpm_axis) / 60)
            P_axis = 0.5 * Cd * rho * A * (v_axis ** 3)
            G_axis = np.sqrt(P_axis / (mu_c * 0.001))
            fig.add_trace(go.Scatter(x=rpm_axis, y=G_axis, mode="lines", name=f"{Tc} °C", line=dict(width=4, color=color)))
        chart_title = "Robot 1 L Digital G-Value Calibration Curves"
    fig.update_xaxes(type="log", title="Agitator paddle speed (RPM)")
    fig.update_yaxes(type="log", title="Velocity gradient, G (s⁻¹)")
    fig.update_layout(title=chart_title, template="plotly_white", height=700, legend_title="Water temperature")
    fig = apply_clean_plot_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 5
# ============================================================
with tab5:
    st.subheader("🤖 Custom Protocol")
    st.write("Adjust each stage and generate the RPM setpoints.")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("#### Rapid Mix")
        rapid_g = st.number_input("Rapid Mix G", min_value=1.0, max_value=600.0, value=300.0, step=1.0)
        rapid_time = st.number_input("Rapid Mix time (min)", min_value=0.1, max_value=60.0, value=1.0, step=0.5)
    with p2:
        st.markdown("#### Flocculation 1")
        floc1_g = st.number_input("Floc 1 G", min_value=1.0, max_value=600.0, value=28.0, step=1.0)
        floc1_time = st.number_input("Floc 1 time (min)", min_value=0.1, max_value=60.0, value=12.5, step=0.5)
    with p3:
        st.markdown("#### Flocculation 2")
        floc2_g = st.number_input("Floc 2 G", min_value=1.0, max_value=600.0, value=18.0, step=1.0)
        floc2_time = st.number_input("Floc 2 time (min)", min_value=0.1, max_value=60.0, value=12.5, step=0.5)
    with p4:
        st.markdown("#### Flocculation 3")
        floc3_g = st.number_input("Floc 3 G", min_value=1.0, max_value=600.0, value=12.0, step=1.0)
        floc3_time = st.number_input("Floc 3 time (min)", min_value=0.1, max_value=60.0, value=12.5, step=0.5)

    protocol = pd.DataFrame({
        "Stage": ["Rapid Mix", "Flocculation 1", "Flocculation 2", "Flocculation 3"],
        "Target G (s⁻¹)": [rapid_g, floc1_g, floc2_g, floc3_g],
        "Time (min)": [rapid_time, floc1_time, floc2_time, floc3_time],
        "Method": [method, method, method, method]
    })
    protocol["Calculated RPM"] = [calculate_required_rpm(g, T, method, A, Cd, rho, Cr, Lrev)[0] for g in protocol["Target G (s⁻¹)"]]
    protocol["Command"] = protocol.apply(lambda row: f"SET RPM {row['Calculated RPM']:.1f} FOR {row['Time (min)']} MIN", axis=1)
    st.dataframe(protocol, use_container_width=True, hide_index=True)

    fig = px.bar(protocol, x="Stage", y="Calculated RPM", text=protocol["Calculated RPM"].round(1), color="Stage", title=f"RPM Setpoints by Stage — {method}", template="plotly_white", color_discrete_sequence=["#0096FF", "#00D4A6", "#FFC857", "#7C3AED"])
    fig.update_traces(textposition="outside")
    fig.update_layout(height=550, yaxis_title="RPM", showlegend=False)
    fig = apply_clean_plot_style(fig)
    st.plotly_chart(fig, use_container_width=True)

    csv = protocol.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download protocol as CSV", data=csv, file_name="jar_test_protocol.csv", mime="text/csv")
