# ⚡ EV Charging Network Optimization Dashboard: Milan

An interactive, cloud-native **Location Intelligence & Spatial Suitability App** built to mathematically optimize Electric Vehicle (EV) fast-charging infrastructure placement across Milan, Italy. 

This platform utilizes open-source APIs, vector network calculations, and dynamic **Multi-Criteria Decision Analysis (MCDA)** to evaluate and rank optimal real estate investments in real-time.

---

## 🚀 Live Application
🔗 **[INSERT_YOUR_LIVE_STREAMLIT_URL_HERE]**

---

## 🛠️ The Tech Stack
* **Frontend Interface:** `Streamlit` (Responsive Web Framework)
* **3D Spatial Rendering:** `Pydeck` & `CartoDB Dark Matter GL` (GPU-Accelerated Vector Graphics)
* **Data Ingestion API:** `OSMnx` (OpenStreetMap Network & Feature Extraction)
* **Spatial Computation Engine:** `GeoPandas`, `Shapely`, & `NumPy` (Vector Topology & Coordinate Reference System Transformations)

---

## 🧠 Core Methodology & Spatial Math

Instead of relying on qualitative assumptions, this application divides the study area into **667 vector analytical framework blocks (500-meter fishnet grid)**. For each distinct cell centroid, the engine calculates two conflicting geographic indicators using metrics projected in **EPSG:32632 (WGS 84 / UTM zone 32N)**:

### 1. Proximity to Commercial Demand hubs ($D_{comm}$)
Drivers prefer to charge where they dwell. The app queries live retail anchors (supermarkets, malls, marketplaces) and calculates proximity. Shorter distances equate to higher structural opportunity:
$$\text{Score}_{\text{Demand}} = 1.0 - \left(\frac{D_{comm}}{\text{Max } D_{comm}}\right)$$

### 2. Distance from Existing Competition ($D_{comp}$)
To avoid market saturation, the engine indexes all 199 active charging stations in Milan. Areas further away from existing supply represent highly lucrative "market gaps":
$$\text{Score}_{\text{Gap}} = \frac{D_{comp}}{\text{Max } D_{comp}}$$

### 3. Dynamic Multi-Criteria Synthesis
The final **Suitability Index (0–100)** is re-computed instantly inside the browser using weights ($W$) defined by the user via the interactive sidebar sliders:
$$\text{Final Suitability} = \left[(\text{Score}_{\text{Demand}} \times W_{comm}) + (\text{Score}_{\text{Gap}} \times W_{comp})\right] \times 100$$

Cells hitting the optimal threshold rise as **tall, extruded 3D red pillars**, pinpointing prime real estate opportunities.

---

## 📦 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[hafiz.sarwary]/[INSERT_YOUR_REPO_NAME].git
   cd [INSERT_YOUR_REPO_NAME]