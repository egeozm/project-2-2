#  Forecasting Renewable Energy ☀️💨 KEN 6

### A Deep Learning Approach to Predicting Solar and Wind Power Generation

This project introduces a prototype for predicting renewable energy production using **Feed-Forward Neural Networks (FFN)** and **Gated Recurrent Units (GRU)**. By leveraging historical energy and meteorological data, we aim to tackle the intermittency of solar and wind power, paving the way for a more stable and efficient energy grid. ⚡

---

## 🎯 Project Goals

-   **Enhance Grid Stability:** Provide accurate energy forecasts to better manage the fluctuating nature of renewable sources.
-   **Optimize Energy Management:** Enable smarter resource allocation and deployment of energy.
-   **Support the Energy Market:** Contribute to a more stable and predictable energy market through reliable forecasting.

---

## 📦 Required Packages

To get started, make sure you have the following packages installed.

```bash
pip install pandas numpy scikit-learn tensorflow matplotlib plotly requests seaborn keras shap
```

---

## ✨ Features

-   **Data Retrieval and Preprocessing 🔄**
    -   Fetches historical weather data for various European regions using bidding zone coordinates.
    -   Cleans, preprocesses, and prepares complex **time-series data** for robust modeling.

-   **Energy Prediction Modeling 🧠**
    -   Implements both **FFN** and **GRU** models to forecast solar and wind energy generation.
    -   Integrates time-based features (like seasonality) and crucial **meteorological variables** to boost prediction accuracy.

-   **Research and Analysis 📊**
    -   Analyzes the geographical potential for solar and wind energy across different European regions.
    -   Compares the performance of GRU vs. FFN models to determine the best fit for energy forecasting.
    -   Evaluates the impact and contribution of different weather variables on the models' predictive power.

---

## 🔥 Heatmap Usage
A custom heatmap can be generated from the heatmap.py file.

- ⚠️ Input data must be manually specified in heatmap.py on line 176.
- When you run the file, an interactive heatmap is generated and made locally accessible via a tab in your browser (this will open automatically).