# app.py
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import folium
from streamlit_folium import folium_static
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

class PropertyPricePredictionApp:
    def __init__(self):
        self.feature_columns = [
            'town', 'flat_type', 'flat_model', 'floor_area_sqm',
            'storey_range', 'remaining_lease', 'property_age',
            'month_number', 'cbd_dist', 'min_dist_mrt', 'is_near_mrt'
        ]
        self.load_models()
        self.setup_page()
        self.town_coordinates = self.load_town_coordinates()

    def load_models(self):
        """Load the trained model and preprocessing objects."""
        try:
            models_dir = Path('models')
            with open(models_dir / 'model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open(models_dir / 'model_scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            with open(models_dir / 'model_encoders.pkl', 'rb') as f:
                self.label_encoders = pickle.load(f)
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            st.error("Error loading the prediction model. Please check if model files exist in the 'models' directory.")

    def setup_page(self):
        """Configure the Streamlit page."""
        st.set_page_config(
            page_title="Singapore Resale Flat Price Predictor",
            page_icon="🏢",
            layout="wide"
        )

    def extract_lease_years(self, lease_str):
        """Extract years from lease string."""
        try:
            if pd.isna(lease_str):
                return 0
            if isinstance(lease_str, str):
                years = lease_str.split(' years')[0]
                return float(years)
            return float(lease_str)
        except:
            return 0

    def _get_storey_median(self, x):
        """Extract median storey from range."""
        try:
            if pd.isna(x):
                return 0
            split_list = str(x).split(' TO ')
            return np.mean([float(i) for i in split_list])
        except:
            return 0

    def show_prediction_page(self):
        """Display the prediction interface."""
        st.title("Predict HDB Resale Price")
        
        col1, col2 = st.columns(2)
        
        with col1:
            town = st.selectbox(
                "Town",
                sorted(self.label_encoders['town'].classes_)
            )
            
            flat_type = st.selectbox(
                "Flat Type",
                sorted(self.label_encoders['flat_type'].classes_)
            )
            
            flat_model = st.selectbox(
                "Flat Model",
                sorted(self.label_encoders['flat_model'].classes_)
            )
            
            floor_area = st.number_input(
                "Floor Area (sqm)",
                min_value=20.0,
                max_value=200.0,
                value=85.0
            )

        with col2:
            storey_range = st.text_input(
                "Storey Range (e.g., '06 TO 10')",
                "06 TO 10"
            )
            
            remaining_lease = st.number_input(
                "Remaining Lease (years)",
                min_value=0,
                max_value=99,
                value=70
            )
            
            property_age = st.number_input(
                "Property Age (years)",
                min_value=0,
                max_value=60,
                value=20
            )
            
            mrt_distance = st.number_input(
                "Distance to MRT (meters)",
                min_value=0.0,
                max_value=5000.0,
                value=500.0
            )

        if st.button("Predict Price", type="primary"):
            try:
                # Prepare input data
                input_data = pd.DataFrame({
                    'town': [town],
                    'flat_type': [flat_type],
                    'flat_model': [flat_model],
                    'floor_area_sqm': [floor_area],
                    'storey_range': [storey_range],
                    'remaining_lease': [remaining_lease],
                    'property_age': [property_age],
                    'month_number': [datetime.now().month],
                    'cbd_dist': [self.calculate_cbd_distance(town)],
                    'min_dist_mrt': [mrt_distance],
                    'is_near_mrt': [1 if mrt_distance < 1000 else 0]
                })

                # Preprocess input
                processed_input = self.preprocess_prediction_input(input_data)
                
                # Make prediction
                prediction = self.model.predict(processed_input)[0]
                
                # Display result
                st.success(f"Estimated Resale Price: SGD {prediction:,.2f}")
                
                # Show location on map
                if town in self.town_coordinates:
                    self.show_location_map(town)
                
            except Exception as e:
                logger.error(f"Prediction error: {str(e)}")
                st.error("An error occurred while making the prediction. Please check your inputs.")

    def preprocess_prediction_input(self, input_df):
        """Preprocess input data for prediction."""
        try:
            processed_df = input_df.copy()
            
            # Handle storey range
            processed_df['storey_range'] = processed_df['storey_range'].apply(self._get_storey_median)
            
            # Handle categorical variables
            for feature in ['town', 'flat_type', 'flat_model']:
                processed_df[feature] = self.label_encoders[feature].transform(processed_df[feature].astype(str))
            
            # Ensure correct column order
            processed_df = processed_df[self.feature_columns]
            
            # Scale features
            scaled_input = self.scaler.transform(processed_df)
            
            return scaled_input
            
        except Exception as e:
            logger.error(f"Error in preprocessing prediction input: {str(e)}")
            raise

    def show_analytics_page(self):
        """Display analytics and insights."""
        st.title("Market Analytics")
        
        # Display feature importance
        if hasattr(self.model, 'feature_importances_'):
            st.subheader("Feature Importance")
            importance = pd.DataFrame({
                'Feature': self.feature_columns,
                'Importance': self.model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            st.bar_chart(importance.set_index('Feature'))

    def load_town_coordinates(self):
        """Load Singapore town coordinates for mapping."""
        # This would typically load from a JSON/CSV file
        return {
            "ANG MO KIO": (1.3691, 103.8454),
            "BEDOK": (1.3236, 103.9273),
            "BISHAN": (1.3526, 103.8352),
            "BUKIT BATOK": (1.3590, 103.7637),
            "BUKIT MERAH": (1.2819, 103.8239),
            "BUKIT PANJANG": (1.3774, 103.7719),
            "BUKIT TIMAH": (1.3294, 103.8021),
            "CENTRAL AREA": (1.2789, 103.8536),
            "CHOA CHU KANG": (1.3840, 103.7470),
            "CLEMENTI": (1.3162, 103.7649),
            "GEYLANG": (1.3201, 103.8918),
            "HOUGANG": (1.3612, 103.8863),
            "JURONG EAST": (1.3329, 103.7436),
            "JURONG WEST": (1.3404, 103.7090),
            "KALLANG/WHAMPOA": (1.3100, 103.8651),
            "MARINE PARADE": (1.3020, 103.9072),
            "PASIR RIS": (1.3721, 103.9474),
            "PUNGGOL": (1.3984, 103.9072),
            "QUEENSTOWN": (1.2942, 103.7861),
            "SEMBAWANG": (1.4491, 103.8185),
            "SENGKANG": (1.3868, 103.8914),
            "SERANGOON": (1.3554, 103.8679),
            "TAMPINES": (1.3496, 103.9568),
            "TOA PAYOH": (1.3343, 103.8563),
            "WOODLANDS": (1.4382, 103.7891),
            "YISHUN": (1.4304, 103.8354)
        }

    def show_location_map(self, town):
        """Display a map with the selected town location."""
        if town in self.town_coordinates:
            lat, lon = self.town_coordinates[town]
            m = folium.Map(location=[lat, lon], zoom_start=14)
            folium.Marker([lat, lon], popup=town).add_to(m)
            folium_static(m)
        else:
            st.warning(f"Coordinates not available for {town}")

    def calculate_cbd_distance(self, town):
        """Calculate distance to CBD."""
        cbd_coords = self.town_coordinates.get("CENTRAL AREA", (1.2789, 103.8536))
        if town in self.town_coordinates:
            town_coords = self.town_coordinates[town]
            return np.sqrt(
                (cbd_coords[0] - town_coords[0])**2 + 
                (cbd_coords[1] - town_coords[1])**2
            ) * 111000  # Convert to meters (approximate)
        return 5000  # Default value

    def show_home_page(self):
        """Display the home page content."""
        st.title("Singapore Resale Flat Price Predictor")
        st.markdown("""
        ### About This Project
        This application predicts HDB resale flat prices in Singapore using machine learning. 
        Our model considers various factors including:
        
        - Location and town characteristics
        - Flat type and model
        - Floor area and storey height
        - Remaining lease and property age
        - Proximity to MRT stations and CBD
        
        ### How to Use
        1. Navigate to the 'Price Prediction' page
        2. Fill in the required details about the flat
        3. Click 'Predict' to get an estimated resale price
        
        ### Model Features
        The prediction model takes into account:
        - Town-specific pricing patterns
        - Property characteristics
        - Location advantages
        - Market trends
        """)

    def run(self):
        """Run the Streamlit application."""
        selected = option_menu(
            "Navigation",
            ["Home", "Price Prediction", "Analytics"],
            icons=["house", "cash", "graph-up"],
            menu_icon="menu-button-wide",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px"},
                "nav-link-selected": {"background-color": "#0083B8"},
            }
        )
        
        if selected == "Home":
            self.show_home_page()
        elif selected == "Price Prediction":
            self.show_prediction_page()
        elif selected == "Analytics":
            self.show_analytics_page()

if __name__ == "__main__":
    app = PropertyPricePredictionApp()
    app.run()