# 🌊 Ghost Waters AI: Delhi/NCR Environmental Intelligence Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://e3r3dy7phsunrjgnqqcqui.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **AI-Powered Multi-Temporal Satellite Monitoring & Municipal Advisory Platform for Urban Water Bodies.** Built for the *1M1B AI for Sustainability Virtual Internship* (in collaboration with IBM SkillsBuild & AICTE).

---

## 🌐 Live Application
Experience the live web platform here: **[Ghost Waters AI Live Portal](https://e3r3dy7phsunrjgnqqcqui.streamlit.app)**

---

## 🚀 Overview
Rapid urbanization, thermal stress, and unmonitored commercial encroachment are quietly degrading vital water ecosystems across Delhi/NCR (including Yamuna stretches, Najafgarh Drain, Sanjay Lake, and Bhalswa Lake). **Ghost Waters AI** bridges the gap between raw satellite data and actionable municipal governance by automating multi-year water body tracking using cloud geospatial infrastructure and generative AI.

---

## 🎯 Sustainable Development Goals (SDG) Alignment
* **Primary Focus:** **SDG 6 (Clean Water and Sanitation)** – Protecting and restoring water-related urban ecosystems and wetlands.
* **Secondary Focus:** **SDG 11 (Sustainable Cities and Communities)** – Tracking urban expansion and providing data-driven early warnings for municipal planning.

---

## 📊 Key Features
1. **Multi-Temporal Satellite Extraction:** Connects with Google Earth Engine (Sentinel-2 Harmonized imagery) to extract real pixel-level environmental metrics.
2. **Advanced Spectral Indexing:** Computes year-on-year changes for:
   * **NDWI** (Normalized Difference Water Index - Surface Moisture)
   * **NDVI** (Normalized Difference Vegetation Index - Eco-Stress)
   * **NDBI** (Normalized Difference Built-up Index - Urban Encroachment)
3. **Automated Risk Classification:** Instantly flags water bodies under critical shrinkage risk ($>10\%$ annual surface area reduction).
4. **IBM watsonx / Granite Advisory Engine:** Generates dynamic, context-aware municipal impact reports and policy recommendations based on live spectral shifts.
5. **Interactive Streamlit Web Portal:** Features multi-site selection, historical trend lines, and one-click CSV audit report exports.

---

## 🏗️ System Architecture & Workflow
```text
[ Sentinel-2 Satellite (COPERNICUS/S2_SR_HARMONIZED) ]
                        ↓ (Google Earth Engine API)
     [ Pixel Masking & Spectral Feature Extraction ]
                        ↓
    [ Temporal Feature Engineering (Δ Area %, Δ NDWI, Δ NDBI) ]
                        ↓
     [ IBM watsonx / Granite Foundation Model API Integration ]
                        ↓
        [ Deployed Streamlit Public Web Portal ]
