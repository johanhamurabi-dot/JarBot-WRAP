import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Jar Test Robot | G-Value to RPM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLES
# ============================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef7ff 0%, #f7fbff 45%, #ffffff 100%);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111F 0%, #102A43 100%);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: white !important;
}

/* Inputs negros, fondo blanco */
[data-testid="stSidebar"] input {
    color: #111111 !important;
    background-color: white !important;
}

/* Selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #111111 !important;
}

/* Cards */
.hero {
    background:
    linear-gradient(135deg, rgba(0, 150, 255, 0.90), rgba(0, 220, 180, 0.82)),
    url("https://images.unsplash.com/photo-1581093458791-9d15482442f6?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    padding: 38px;
    border-radius: 28px;
    color: white;
    box-shadow: 0 14px 34px rgba(0,0,0,0.18);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 18px;
    font-weight: 500;
}

.status-pill {
    display: inline-block;
    background: rgba(255,255,255,0.22);
    padding: 8px 16px;
    border-radius: 999px;
    font-weight: 700;
    margin-top: 14px;
    backdrop-filter: blur(8px);
}

.card {
    background: white;
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 8px 24px rgba(20, 40, 80, 0.10);
    border: 1px solid #E6EAF0;
}

.metric-big {
    font-size: 48px;
    font-weight: 900;
    color: #07111F;
}

.metric-label {
    font-size: 15px;
    color: #64748B;
    font-weight: 700;
}

.metric-sub {
    font-size: 13px;
    color: #94A3B8;
}

.blue-card {
    border-left: 8px solid #0096FF;
}

.green-card {
    border-left: 8px solid #00D4A6;
}

.yellow-card {
    border-left: 8px solid #FFC857;
}

.purple-card {
    border-left: 8px solid #7C3AED;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 16px;
    padding: 12px 18px;
    font-weight: 800;
    border: 1px solid #E6EAF0;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0096FF, #00D4A6) !important;
    color: white !important;
}

/* Buttons */
.stDownloadButton button {
    border-radius: 14px;
    background: linear-gradient(135deg, #0096FF, #00D4A6);
    color: white;
    border: none;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CORE CALCULATIONS
# ============================================================
def water_viscosity(T_c):
    """Dynamic viscosity of water in Pa*s."""
    return 2.414e-5 * 10 ** (247.8 / (T_c + 133.15))

def calculate_rpm(G, T, V, A, Cd, rho, Cr, Lrev):
    mu = water_viscosity(T)
    v = ((2 * (G**2) * mu * V) / (Cd * rho * A)) ** (1/3)
    rpm = (60 * v) / (Cr * Lrev)
    return rpm, mu, v

def rpm_curve(G_range, T, V, A, Cd, rho, Cr, Lrev):
    return np.array([
        calculate_rpm(g, T, V, A, Cd, rho, Cr, Lrev)[0]
        for g in G_range
    ])

def rpm_map(G_grid, T_grid, V, A, Cd, rho, Cr, Lrev):
    Z = np.zeros((len(T_grid), len(G_grid)))
    for i, temp in enumerate(T_grid):
        for j, g_val in enumerate(G_grid):
            Z[i, j] = calculate_rpm(g_val, temp, V, A, Cd, rho, Cr, Lrev)[0]
    return Z

# ============================================================
# SIDEBAR INPUTS
# ============================================================
st.sidebar.title("⚙️ Robot Inputs")

G = st.sidebar.number_input(
    "Target G-Value (s⁻¹)",
    min_value=1.0,
    max_value=600.0,
    value=100.0,
    step=1.0
)

T = st.sidebar.slider(
    "Water temperature (°C)",
    min_value=0,
    max_value=35,
    value=20,
    step=1
)

volume_option = st.sidebar.selectbox(
    "Jar volume",
    ["1 L", "2 L"],
    index=0
)

if volume_option == "1 L":
    V = 0.001
    jar_height = "145 mm"
else:
    V = 0.002
    jar_height = "8.2 in / 208.28 mm"

st.sidebar.divider()
st.sidebar.subheader("Fixed system constants")

A = st.sidebar.number_input("Paddle area A (m²)", value=0.00164, format="%.6f")
Cd = st.sidebar.number_input("Drag coefficient Cd", value=1.9, format="%.3f")
rho = st.sidebar.number_input("Water density ρ (kg/m³)", value=998.0, format="%.1f")
Cr = st.sidebar.number_input("Relative velocity constant Cr", value=0.75, format="%.3f")
Lrev = st.sidebar.number_input("Tip distance Lrev (m/rev)", value=0.235619449, format="%.9f")

RPM, mu, v = calculate_rpm(G, T, V, A, Cd, rho, Cr, Lrev)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">🤖 Jar Test Robot Automation</div>
    <div class="hero-subtitle">G-Value + temperature → required motor RPM</div>
    <div class="status-pill">● Robot calibration mode online</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TOP METRICS
# ============================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card blue-card">
        <div class="metric-label">Required RPM</div>
        <div class="metric-big">{RPM:.2f}</div>
        <div class="metric-sub">Motor setpoint</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card green-card">
        <div class="metric-label">Water viscosity μ</div>
        <div class="metric-big">{mu:.5f}</div>
        <div class="metric-sub">Pa·s</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card yellow-card">
        <div class="metric-label">Paddle velocity</div>
        <div class="metric-big">{v:.3f}</div>
        <div class="metric-sub">m/s</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card purple-card">
        <div class="metric-label">Jar setup</div>
        <div class="metric-big">{volume_option}</div>
        <div class="metric-sub">Height: {jar_height}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 RPM vs G",
    "🌡️ Heatmap",
    "🧊 3D Surface",
    "📊 G-Curves",
    "🤖 Robot Protocol"
])

# ============================================================
# TAB 1: RPM VS G
# ============================================================
with tab1:
    G_range = np.linspace(10, 300, 200)
    rpm_values = rpm_curve(G_range, T, V, A, Cd, rho, Cr, Lrev)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=G_range,
        y=rpm_values,
        mode="lines",
        name=f"T = {T} °C",
        line=dict(width=5, color="#0096FF")
    ))

    fig.add_trace(go.Scatter(
        x=[G],
        y=[RPM],
        mode="markers+text",
        name="Current point",
        text=[f"{RPM:.1f} RPM"],
        textposition="top center",
        marker=dict(
            size=16,
            color="#00D4A6",
            line=dict(color="#07111F", width=3)
        )
    ))

    fig.update_layout(
        title="Required RPM as a Function of Target G-Value",
        xaxis_title="G-Value, G (s⁻¹)",
        yaxis_title="Required RPM",
        template="plotly_white",
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: HEATMAP
# ============================================================
with tab2:
    G_grid = np.linspace(10, 300, 140)
    T_grid = np.linspace(0, 35, 90)
    Z = rpm_map(G_grid, T_grid, V, A, Cd, rho, Cr, Lrev)

    fig = go.Figure(data=go.Heatmap(
        x=G_grid,
        y=T_grid,
        z=Z,
        colorscale="Turbo",
        colorbar=dict(title="RPM")
    ))

    fig.add_trace(go.Scatter(
        x=[G],
        y=[T],
        mode="markers+text",
        marker=dict(
            size=15,
            color="white",
            line=dict(color="black", width=3)
        ),
        text=[f"{RPM:.1f} RPM"],
        textposition="top center",
        name="Current input"
    ))

    fig.update_layout(
        title="RPM Heatmap",
        xaxis_title="G-Value, G (s⁻¹)",
        yaxis_title="Temperature (°C)",
        template="plotly_white",
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 3: 3D SURFACE
# ============================================================
with tab3:
    G_grid_3d = np.linspace(10, 300, 80)
    T_grid_3d = np.linspace(0, 35, 55)
    Z3 = rpm_map(G_grid_3d, T_grid_3d, V, A, Cd, rho, Cr, Lrev)

    fig = go.Figure(data=[go.Surface(
        x=G_grid_3d,
        y=T_grid_3d,
        z=Z3,
        colorscale="Viridis",
        colorbar=dict(title="RPM")
    )])

    fig.add_trace(go.Scatter3d(
        x=[G],
        y=[T],
        z=[RPM],
        mode="markers",
        marker=dict(size=7, color="red"),
        name="Current input"
    ))

    fig.update_layout(
        title="3D Calibration Surface: RPM = f(G, Temperature)",
        scene=dict(
            xaxis_title="G-Value (s⁻¹)",
            yaxis_title="Temperature (°C)",
            zaxis_title="RPM"
        ),
        height=720,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 4: DIGITAL G-CURVES
# ============================================================
with tab4:
    rpm_axis = np.logspace(np.log10(10), np.log10(320), 250)
    temps = [4, 10, 16, 22, 30]

    fig = go.Figure()

    colors = ["#0096FF", "#00D4A6", "#FFC857", "#7C3AED", "#EF4444"]

    for Tc, color in zip(temps, colors):
        mu_c = water_viscosity(Tc)
        v_axis = Cr * ((Lrev * rpm_axis) / 60)
        P_axis = 0.5 * Cd * rho * A * (v_axis ** 3)
        G_axis = np.sqrt(P_axis / (mu_c * V))

        fig.add_trace(go.Scatter(
            x=rpm_axis,
            y=G_axis,
            mode="lines",
            name=f"{Tc} °C",
            line=dict(width=4, color=color)
        ))

    rpm_ref = np.array([18, 26, 37, 200])
    G_ref = np.array([12, 18, 28, 300])

    fig.add_trace(go.Scatter(
        x=rpm_ref,
        y=G_ref,
        mode="markers+text",
        name="Lab notebook points",
        marker=dict(size=11, color="black"),
        text=["18→12", "26→18", "37→28", "200→300"],
        textposition="top center"
    ))

    fig.update_xaxes(type="log", title="Agitator paddle speed (RPM)")
    fig.update_yaxes(type="log", title="Velocity gradient, G (s⁻¹)")

    fig.update_layout(
        title="Digital G-Value Calibration Curves",
        template="plotly_white",
        height=700,
        legend_title="Water temperature"
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 5: ROBOT PROTOCOL
# ============================================================
with tab5:
    st.subheader("🤖 Custom Robot Protocol")

    st.write("Adjust each stage and generate the RPM setpoints for the robot.")

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
        "Time (min)": [rapid_time, floc1_time, floc2_time, floc3_time]
    })

    protocol["Calculated RPM"] = [
        calculate_rpm(g, T, V, A, Cd, rho, Cr, Lrev)[0]
        for g in protocol["Target G (s⁻¹)"]
    ]

    protocol["Command"] = protocol.apply(
        lambda row: f"SET RPM {row['Calculated RPM']:.1f} FOR {row['Time (min)']} MIN",
        axis=1
    )

    st.write("")
    st.dataframe(protocol, use_container_width=True, hide_index=True)

    fig = px.bar(
        protocol,
        x="Stage",
        y="Calculated RPM",
        text=protocol["Calculated RPM"].round(1),
        color="Stage",
        title="Robot RPM Setpoints by Stage",
        template="plotly_white",
        color_discrete_sequence=["#0096FF", "#00D4A6", "#FFC857", "#7C3AED"]
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=550, yaxis_title="RPM", showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    csv = protocol.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download protocol as CSV",
        data=csv,
        file_name="jar_test_robot_protocol.csv",
        mime="text/csv"
    )