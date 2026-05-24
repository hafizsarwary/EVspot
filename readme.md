# ⚡ EVspot — EV Charging Site Selection Dashboard: Milan

An interactive **Location Intelligence & Spatial Suitability App** for optimizing Electric Vehicle fast-charging infrastructure placement across Milan, Italy.

Built with open geospatial data, vector network calculations, and dynamic **Multi-Criteria Decision Analysis (MCDA)** — the suitability index updates in real-time as you adjust weights.

---

## 🚀 Live App
🔗 **https://evspot-milan.streamlit.app/**

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Frontend | `Streamlit` |
| 3D Map Rendering | `Pydeck` + CartoDB Dark Matter |
| Geospatial Data | `OSMnx` (OpenStreetMap) |
| Spatial Computation | `GeoPandas`, `Shapely`, `NumPy` |
| Coordinate System | EPSG:32632 — WGS 84 / UTM zone 32N |

---

## 🧠 Methodology

The study area is divided into **667 analytical grid cells (500m fishnet)**. For each cell centroid, two spatial indicators are computed:

### 1. Proximity to Commercial Demand ($D_{comm}$)
Queries OSM retail anchors (supermarkets, malls, marketplaces). Shorter distance = higher demand score:

$$\text{Score}_{\text{Demand}} = 1.0 - \left(\frac{D_{comm}}{\text{Max } D_{comm}}\right)$$

### 2. Distance from Existing Charging Stations ($D_{comp}$)
Indexes 199 active charging stations in Milan. Cells further from existing supply represent underserved areas:

$$\text{Score}_{\text{Gap}} = \frac{D_{comp}}{\text{Max } D_{comp}}$$

### 3. MCDA Suitability Index
The final **Suitability Index (0–100)** is computed dynamically using user-defined weights via the sidebar sliders:

$$\text{Suitability} = \left[(\text{Score}_{\text{Demand}} \times W_{comm}) + (\text{Score}_{\text{Gap}} \times W_{comp})\right] \times 100$$

High-scoring cells are extruded as 3D pillars on the map, highlighting priority locations.

---

## 📌 Context

Built as a portfolio project exploring GeoAI-adjacent methods for urban infrastructure planning — part of ongoing work in Location Intelligence and spatial decision support during my MSc in Geoinformatics Engineering at Politecnico di Milano.

---

## 📦 Local Setup

```bash
git clone https://github.com/hafizsarwary/EVspot.git
cd EVspot
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure
EVspot/
├── app.py              # Main Streamlit application
├── requirements.txt
└── README.md

---

## 👤 Author

**Hafizullah Sarwary**  
MSc Geoinformatics Engineering — Politecnico di Milano  
[LinkedIn](https://www.linkedin.com/in/hafizullah-sarwary) · [GitHub](https://github.com/hafizsarwary)