import streamlit as st
import geopandas as gpd
import osmnx as ox
import leafmap.foliumap as leafmap
from shapely.geometry import box
import numpy as np
import folium
from streamlit_folium import st_folium


# 1. Page Configuration
st.set_page_config(layout="wide", page_title="EV Infrastructure Optimization")

st.markdown(
    """
    <style>
        :root {
            --ink: #17233c;
            --muted: #5c667a;
            --line: #dfe5ee;
            --panel: #ffffff;
            --soft: #f5f7fb;
            --blue: #246bfe;
            --green: #16a35a;
            --violet: #8a3ffc;
            --pink: #f75ba5;
        }

        .stApp {
            background: #f4f6fa;
            color: var(--ink);
        }

        header[data-testid="stHeader"] {
            height: 2.25rem;
            background: rgba(244, 246, 250, 0.92);
            border-bottom: 1px solid var(--line);
        }

        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: flex;
            visibility: visible;
            opacity: 1;
            z-index: 100000;
        }

        .block-container {
            padding: 2.45rem 0.85rem 0;
            max-width: 100%;
        }

        section[data-testid="stSidebar"] {
            background: #fbfcfe;
            border-right: 1px solid var(--line);
            box-shadow: 12px 0 30px rgba(24, 37, 61, 0.05);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 0.75rem;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--ink);
            letter-spacing: 0;
        }

        [data-testid="stSidebar"] .stSlider {
            padding-top: 0.15rem;
            padding-bottom: 0.65rem;
        }

        [data-testid="stSidebar"] .stSlider label {
            color: var(--ink);
            font-weight: 800;
        }

        [data-testid="stSidebar"] [data-baseweb="slider"] > div:nth-child(1) {
            background: #e2e5eb;
        }

        .topbar {
            display: grid;
            grid-template-columns: minmax(220px, 0.85fr) minmax(520px, 1.4fr);
            align-items: center;
            gap: 0.75rem;
            padding: 0 0.15rem 0.3rem;
            border-bottom: 1px solid var(--line);
            margin: -0.1rem -0.15rem 0.35rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            min-width: 0;
        }

        .brand-mark {
            display: none;
        }

        .divider {
            display: none;
        }

        .title-wrap h1 {
            margin: 0;
            font-size: clamp(1.2rem, 1.55vw, 1.65rem);
            line-height: 1.05;
            color: #000000;
            letter-spacing: 0;
        }

        .title-wrap p {
            margin: 0.12rem 0 0;
            color: #3d465a;
            font-size: 0.78rem;
            line-height: 1.2;
        }

        .metric-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(170px, 1fr));
            gap: 0;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 10px 28px rgba(30, 42, 62, 0.06);
            overflow: hidden;
            min-width: 0;
        }

        .metric {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.38rem 0.75rem;
            border-right: 1px solid var(--line);
        }

        .metric:last-child {
            border-right: 0;
        }

        .metric-icon {
            width: 1.45rem;
            height: 1.45rem;
            display: grid;
            place-items: center;
            border-radius: 8px;
            font-weight: 900;
            font-size: 0.72rem;
            color: white;
        }

        .metric-icon.blue { background: var(--blue); }
        .metric-icon.violet { background: var(--violet); }
        .metric-icon.green { background: var(--green); }

        .metric-value {
            font-size: 0.95rem;
            font-weight: 900;
            line-height: 1;
            color: var(--ink);
        }

        .metric-label {
            margin-top: 0.18rem;
            color: #394258;
            font-size: 0.7rem;
            white-space: nowrap;
        }

        .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            box-shadow: 0 14px 34px rgba(30, 42, 62, 0.08);
        }

        .pipeline {
            display: grid;
            grid-template-columns: auto minmax(0, 1fr);
            gap: 1rem;
            align-items: center;
            padding: 0.48rem 0.8rem;
            margin-bottom: 0.35rem;
        }

        .pipeline h2 {
            margin: 0;
            font-size: 0.82rem;
            color: var(--ink);
            letter-spacing: 0;
            white-space: nowrap;
        }

        .steps {
            display: grid;
            grid-template-columns: repeat(4, minmax(150px, 1fr));
            gap: 0.45rem;
            align-items: center;
        }

        .step {
            display: grid;
            grid-template-columns: 1.65rem 1fr;
            gap: 0.38rem;
            position: relative;
        }

        .step:not(:last-child)::after {
            display: none;
        }

        .step-badge {
            width: 1.65rem;
            height: 1.65rem;
            border-radius: 999px;
            display: grid;
            place-items: center;
            font-weight: 900;
            border: 1px solid;
            font-size: 0.76rem;
        }

        .step-badge.blue { background: #eaf2ff; border-color: #9fc2ff; color: var(--blue); }
        .step-badge.violet { background: #f3ebff; border-color: #d4b8ff; color: var(--violet); }
        .step-badge.pink { background: #ffeaf3; border-color: #ffbfd9; color: var(--pink); }
        .step-badge.green { background: #eafaf1; border-color: #a5e2c0; color: var(--green); }

        .step-title {
            font-size: 0.72rem;
            font-weight: 900;
            color: var(--ink);
            margin-top: 0;
            line-height: 1.15;
        }

        .step-copy {
            margin-top: 0.08rem;
            color: #4e596d;
            font-size: 0.66rem;
            line-height: 1.12;
        }

        .content-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 285px;
            gap: 0.85rem;
            align-items: start;
        }

        .map-card {
            overflow: hidden;
        }

        .map-card iframe {
            border-radius: 8px;
        }

        .insights {
            padding: 0;
            overflow: hidden;
        }

        .insights-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1rem;
            border-bottom: 1px solid var(--line);
            font-weight: 900;
            color: var(--ink);
        }

        .insight-block {
            padding: 1rem;
            border-bottom: 1px solid var(--line);
        }

        .insight-block:last-child {
            border-bottom: 0;
        }

        .insight-kicker {
            color: var(--ink);
            font-weight: 900;
            font-size: 0.92rem;
            margin-bottom: 0.35rem;
        }

        .insight-copy {
            color: #3f485c;
            line-height: 1.35;
            font-size: 0.9rem;
        }

        .candidate-button {
            margin: 0 1rem 1rem;
            padding: 0.75rem 0.95rem;
            border-radius: 8px;
            background: #f2f5f9;
            color: var(--ink);
            font-weight: 900;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .sidebar-title {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            color: var(--ink);
            font-weight: 900;
            font-size: 1.05rem;
            margin-bottom: 0.75rem;
        }

        .sidebar-copy {
            color: #505b70;
            line-height: 1.45;
            margin-bottom: 1rem;
        }

        .sidebar-rule {
            height: 1px;
            background: var(--line);
            margin: 0.45rem 0 1rem;
        }

        .weight-value {
            float: right;
            color: #ff1d25;
            font-weight: 900;
            font-size: 1.05rem;
        }

        .weight-block {
            margin-bottom: 0.25rem;
        }

        .weight-title {
            color: var(--ink);
            font-weight: 900;
            font-size: 0.92rem;
            line-height: 1.2;
        }

        .weight-subtitle {
            color: #525d72;
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }

        .hint {
            border-radius: 8px;
            background: #f2f4f8;
            color: #566074;
            font-size: 0.82rem;
            line-height: 1.4;
            padding: 0.65rem 0.8rem;
            margin: -0.25rem 0 0.8rem;
        }

        .map-utility-row {
            display: block;
            gap: 0.55rem;
            align-items: center;
            margin: 0.12rem 0 0.28rem;
        }

        .map-caption {
            color: #5b6578;
            font-size: 0.74rem;
        }

        .legend-card {
            position: fixed;
            right: 1.65rem;
            bottom: 1.25rem;
            z-index: 999;
            min-width: 270px;
            padding: 0.38rem 0.55rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            box-shadow: 0 14px 28px rgba(8, 14, 28, 0.22);
        }

        .legend-title {
            color: var(--ink);
            font-weight: 900;
            font-size: 0.7rem;
            margin-bottom: 0.25rem;
        }

        .legend-scale {
            height: 0.55rem;
            border-radius: 4px;
            background: linear-gradient(to right, #1255b5 0%, #1255b5 25%, #f4f70b 25%, #f4f70b 50%, #ff970f 50%, #ff970f 75%, #f70d1b 75%, #f70d1b 100%);
            margin-bottom: 0.18rem;
        }

        .legend-labels {
            display: flex;
            justify-content: space-between;
            color: #3d465a;
            font-size: 0.62rem;
            font-weight: 700;
        }

        .ready-card {
            margin-top: 1.35rem;
            padding: 0.9rem 1rem;
            border: 1px solid var(--line);
            border-radius: 9px;
            background: #fff;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            color: var(--ink);
            box-shadow: 0 8px 22px rgba(30, 42, 62, 0.05);
        }

        .ready-dot {
            width: 1.75rem;
            height: 1.75rem;
            border-radius: 999px;
            border: 2px solid var(--green);
            color: var(--green);
            display: grid;
            place-items: center;
            font-weight: 900;
        }

        .ready-title {
            font-weight: 900;
            font-size: 0.9rem;
        }

        .ready-copy {
            color: #697386;
            font-size: 0.76rem;
            margin-top: 0.15rem;
        }

        @media (max-width: 1150px) {
            .topbar,
            .content-grid {
                grid-template-columns: 1fr;
            }

            .metric-strip {
                min-width: 0;
            }

            .steps {
                grid-template-columns: repeat(2, minmax(160px, 1fr));
            }

            .step::after {
                display: none;
            }
        }

        @media (max-width: 680px) {
            .metric-strip,
            .steps {
                grid-template-columns: 1fr;
            }

            .metric {
                border-right: 0;
                border-bottom: 1px solid var(--line);
            }

            .metric:last-child {
                border-bottom: 0;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# 2. Sidebar UI Configuration for Weights
st.sidebar.markdown(
    """
    <div class="sidebar-title"><span>EQ</span><span>Optimization Weights</span></div>
    <div class="sidebar-copy">
        Adjust priorities for the EV location intelligence model.
    </div>
    <div class="sidebar-rule"></div>
    """,
    unsafe_allow_html=True,
)

commercial_display = st.session_state.get("weight_commercial", 0.6)
st.sidebar.markdown(
    f"""
    <div class="weight-block">
        <div class="weight-title">
            Commercial POIs Proximity
            <span class="weight-value">{commercial_display:.2f}</span>
        </div>
        <div class="weight-subtitle">Demand weight from retail, supermarket, and marketplace POIs</div>
    </div>
    """,
    unsafe_allow_html=True,
)
weight_commercial = st.sidebar.slider(
    "Commercial POIs Proximity",
    0.0,
    1.0,
    0.6,
    0.1,
    key="weight_commercial",
    label_visibility="collapsed",
)
st.sidebar.markdown(
    '<div class="hint">Higher values prioritize grid cells closer to commercial POIs.</div>',
    unsafe_allow_html=True,
)

competition_display = st.session_state.get("weight_competition", 0.4)
st.sidebar.markdown(
    f"""
    <div class="weight-block">
        <div class="weight-title">
            Competitor Gap Proximity
            <span class="weight-value">{competition_display:.2f}</span>
        </div>
        <div class="weight-subtitle">Underserved weight from distance to existing charging stations</div>
    </div>
    """,
    unsafe_allow_html=True,
)
weight_competition = st.sidebar.slider(
    "Competitor Gap Proximity",
    0.0,
    1.0,
    0.4,
    0.1,
    key="weight_competition",
    label_visibility="collapsed",
)
st.sidebar.markdown(
    '<div class="hint">Higher values prioritize grid cells farther from competitor charging stations.</div>',
    unsafe_allow_html=True,
)
st.sidebar.caption("Recalculate suitability index and update map.")

# Normalize weights so they sum up to 1.0 automatically
total_w = weight_commercial + weight_competition
if total_w > 0:
    w_comm = weight_commercial / total_w
    w_comp = weight_competition / total_w
else:
    w_comm, w_comp = 0.5, 0.5


# 3. Cached Spatial Data Ingestion
@st.cache_data
def get_ev_spatial_data():
    place_name = "Milan, Italy"

    # Fetch Existing EV Charging Stations
    charging_tags = {"amenity": "charging_station"}
    existing_chargers = ox.features_from_place(place_name, tags=charging_tags)
    existing_chargers = existing_chargers[
        existing_chargers.geometry.type == "Point"
    ][["geometry"]]

    # Fetch Commercial Attractors (Malls and Supermarkets)
    attractor_tags = {
        "shop": "supermarket",
        "amenity": "marketplace",
        "building": "retail",
    }
    attractors = ox.features_from_place(place_name, tags=attractor_tags)
    attractors = attractors[attractors.geometry.type == "Point"][["geometry"]]

    # Project to local metric system (EPSG:32632 for Milan)
    chargers_projected = existing_chargers.to_crs(epsg=32632)
    attractors_projected = attractors.to_crs(epsg=32632)

    return chargers_projected, attractors_projected


with st.spinner("Querying OpenStreetMap API for Milan mobility nodes..."):
    try:
        chargers, attractors = get_ev_spatial_data()
    except Exception as e:
        st.error(f"Error downloading data: {e}")
        st.stop()


# 4. Generate Spatial Analytical Grid (Fishnet)
@st.cache_data
def create_analysis_grid(_attractors):
    minx, miny, maxx, maxy = _attractors.total_bounds
    grid_size = 500  # 500-meter blocks

    x_coords = np.arange(minx, maxx, grid_size)
    y_coords = np.arange(miny, maxy, grid_size)

    grid_cells = []
    for x in x_coords:
        for y in y_coords:
            grid_cells.append(box(x, y, x + grid_size, y + grid_size))

    grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs=32632)
    grid_gdf["centroid"] = grid_gdf.geometry.centroid
    return grid_gdf


grid = create_analysis_grid(attractors)


# 5. Spatial Suitability Computation Engine
grid_centroids = grid["centroid"]
dist_to_comm = grid_centroids.apply(lambda x: attractors.distance(x).min())
dist_to_comp = grid_centroids.apply(lambda x: chargers.distance(x).min())

# Normalize scores
max_comm_dist = dist_to_comm.max() if dist_to_comm.max() > 0 else 1
score_commercial = 1.0 - (dist_to_comm / max_comm_dist)

max_comp_dist = dist_to_comp.max() if dist_to_comp.max() > 0 else 1
score_competition = dist_to_comp / max_comp_dist

# Combine layers with user weights
final_suitability = (score_commercial * w_comm) + (score_competition * w_comp)
grid["suitability_score"] = final_suitability * 100


st.markdown(
    f"""
    <div class="topbar">
        <div class="brand">
            <div class="title-wrap">
                <h1>Milan</h1>
                <p>EV Infrastructure Optimization Dashboard</p>
            </div>
        </div>
        <div class="metric-strip">
            <div class="metric">
                <div class="metric-icon blue">EV</div>
                <div>
                    <div class="metric-value">{len(chargers)}</div>
                    <div class="metric-label">Active Charging Stations</div>
                </div>
            </div>
            <div class="metric">
                <div class="metric-icon violet">H</div>
                <div>
                    <div class="metric-value">{len(attractors)}</div>
                    <div class="metric-label">High-dwell Commercial Hubs</div>
                </div>
            </div>
            <div class="metric">
                <div class="metric-icon green">G</div>
                <div>
                    <div class="metric-value">{len(grid)}</div>
                    <div class="metric-label">Spatial Evaluation Blocks</div>
                </div>
            </div>
        </div>
    </div>

    <div class="panel pipeline">
        <h2>Data Pipeline Status</h2>
        <div class="steps">
            <div class="step">
                <div class="step-badge blue">1</div>
                <div>
                    <div class="step-title">Querying OpenStreetMap API</div>
                    <div class="step-copy">Mobility nodes retrieved</div>
                </div>
            </div>
            <div class="step">
                <div class="step-badge violet">2</div>
                <div>
                    <div class="step-title">Generating 500-m Framework</div>
                    <div class="step-copy">{len(grid)} spatial evaluation blocks</div>
                </div>
            </div>
            <div class="step">
                <div class="step-badge pink">3</div>
                <div>
                    <div class="step-title">Recalculating Suitability Index</div>
                    <div class="step-copy">Based on current weights</div>
                </div>
            </div>
            <div class="step">
                <div class="step-badge green">4</div>
                <div>
                    <div class="step-title">Visualization Ready</div>
                    <div class="step-copy">Map is up to date</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# 6. Advanced 3D Pydeck Canvas Rendering
st.markdown(
    """
    <div class="map-utility-row">
        <div class="map-caption">Rendering GPU-Accelerated 3D Location Intelligence Engine...</div>
    </div>
    <div class="legend-card">
        <div class="legend-title">EV Site Opportunity Index</div>
        <div class="legend-scale"></div>
        <div class="legend-labels">
            <span>0 Low</span>
            <span>25</span>
            <span>50</span>
            <span>75</span>
            <span>100 Prime Gap</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

import pydeck as pdk

# Drop centroid column, re-project grid to WGS84
grid_display = grid.drop(columns=['centroid'])
grid_wgs84 = grid_display.to_crs(epsg=4326)

# Pydeck requires explicit coordinates listed for polygon paths.
# We parse the geometry bounds to make it easily readable by the 3D engine.
def get_polygon_coordinates(geometry):
    if geometry.geom_type == 'Polygon':
        return list(geometry.exterior.coords)
    return []

grid_wgs84['coordinates'] = grid_wgs84['geometry'].apply(get_polygon_coordinates)

# Create an explicit RGBA color array column based on suitability scores for the 3D rendering
def assign_3d_color(score):
    if score > 75: return [255, 0, 0, 180]      # Bright Red (High Opportunity)
    elif score > 50: return [255, 165, 0, 180]  # Orange
    elif score > 25: return [255, 255, 0, 180]  # Yellow
    else: return [0, 0, 255, 80]                # Translucent Blue (Low Priority)

grid_wgs84['fill_color'] = grid_wgs84['suitability_score'].apply(assign_3d_color)
grid_wgs84['score_label'] = grid_wgs84['suitability_score'].round(1).astype(str)

# Define the 3D Polygon Layer
polygon_3d_layer = pdk.Layer(
    "PolygonLayer",
    grid_wgs84,
    id="geojson",
    get_polygon="coordinates",
    get_fill_color="fill_color",
    get_line_color=[0, 0, 0, 50],
    line_width_min_pixels=1,
    extruded=True,                        # TURN ON 3D EXTRUSION
    get_elevation="suitability_score * 15", # Height is proportional to the suitability score!
    pickable=True,
    auto_highlight=True,
)

# Set up the initial 3D camera viewpoint tilted over Milan
view_state = pdk.ViewState(
    latitude=45.4642,
    longitude=9.1900,
    zoom=11.5,
    pitch=50,   # Tilt angle for 3D viewing
    bearing=20  # Rotation angle
)

# Render the 3D map canvas layout
r = pdk.Deck(
    layers=[polygon_3d_layer],
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    tooltip={"text": "Suitability Score: {score_label}"}
)

st.pydeck_chart(r, height=520)
