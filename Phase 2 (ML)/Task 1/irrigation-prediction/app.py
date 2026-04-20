import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(
    page_title="Irrigation Predictor",
    page_icon="🌱",
    layout="wide" 
)

# 2. Header Section
st.title("🌱 Smart Agriculture: Irrigation Predictor")
st.markdown("**Author:** Belal Said | **Architecture:** Optimized XGBoost (96.5% Balanced Accuracy)")
st.divider()

# 3. Load the Model 
@st.cache_resource
def load_model():
    try:
        return joblib.load('optimized_champion_model.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# 4. The User Interface (Organized into 3 logical columns)
st.subheader("Enter Environmental, Soil & Crop Conditions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🪨 Soil & Land")
    soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loam", "Silt"])
    soil_ph = st.number_input("Soil pH", value=6.5, step=0.1)
    soil_moisture = st.number_input("Soil Moisture (%)", value=45.0, step=0.5)
    organic_carbon = st.number_input("Organic Carbon (%)", value=1.5, step=0.1)
    electrical_conductivity = st.number_input("Electrical Conductivity", value=1.2, step=0.1)
    field_area = st.number_input("Field Area (Hectare)", value=5.0, step=0.5)
    region = st.selectbox("Region", ["North", "South", "East", "West"])

with col2:
    st.markdown("### ☀️ Weather Conditions")
    temperature = st.number_input("Temperature (°C)", value=28.5, step=0.1)
    humidity = st.number_input("Humidity (%)", value=60.0, step=1.0)
    rainfall = st.number_input("Rainfall (mm)", value=10.0, step=1.0)
    sunlight = st.number_input("Sunlight Hours", value=8.0, step=0.5)
    wind_speed = st.number_input("Wind Speed (km/h)", value=12.0, step=0.5)
    season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])

with col3:
    st.markdown("### 🌾 Crop & Management")
    crop_type = st.selectbox("Crop Type", ["Wheat", "Corn", "Rice", "Cotton", "Soybean"])
    growth_stage = st.selectbox("Crop Growth Stage", ["Seedling", "Vegetative", "Flowering", "Fruiting", "Mature"])
    irrigation_type = st.selectbox("Current Irrigation Type", ["Drip", "Sprinkler", "Flood", "Furrow"])
    water_source = st.selectbox("Water Source", ["Well", "River", "Canal", "Rainwater"])
    mulching_used = st.selectbox("Mulching Used", ["Yes", "No"])
    previous_irrigation = st.number_input("Previous Irrigation (mm)", value=20.0, step=1.0)

st.divider()

# 5. The Prediction Engine
if st.button("Predict Irrigation Need", type="primary", use_container_width=True):
    if model is not None:
        input_data = pd.DataFrame([[
            soil_type, soil_ph, soil_moisture, organic_carbon, electrical_conductivity,
            temperature, humidity, rainfall, sunlight, wind_speed,
            crop_type, growth_stage, season, irrigation_type, water_source,
            field_area, mulching_used, previous_irrigation, region
        ]], columns=[
            'Soil_Type', 'Soil_pH', 'Soil_Moisture', 'Organic_Carbon', 'Electrical_Conductivity',
            'Temperature_C', 'Humidity', 'Rainfall_mm', 'Sunlight_Hours', 'Wind_Speed_kmh',
            'Crop_Type', 'Crop_Growth_Stage', 'Season', 'Irrigation_Type', 'Water_Source',
            'Field_Area_hectare', 'Mulching_Used', 'Previous_Irrigation_mm', 'Region'
        ])
        
        with st.spinner('Analyzing 19 environmental factors...'):
            # Predict
            prediction_code = model.predict(input_data)[0]
            
            class_map = {0: 'Low', 1: 'Medium', 2: 'High'}
            result = class_map.get(prediction_code, "Unknown")

            if result == 'High':
                st.error(f"Recommended Action: **{result} Irrigation Needed**")
            elif result == 'Medium':
                st.warning(f"Recommended Action: **{result} Irrigation Needed**")
            else:
                st.success(f"Recommended Action: **{result} Irrigation Needed**")