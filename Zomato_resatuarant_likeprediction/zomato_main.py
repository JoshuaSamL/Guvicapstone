import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set page config - THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Restaurant Price Predictor", layout="wide")

# Load all necessary files
@st.cache_resource
def load_models_and_data():
    with open("restaurant_cost_prediction_model.pkl", 'rb') as file:
        model = pickle.load(file)
    with open("label_encoders.pkl", 'rb') as file:
        label_encoders = pickle.load(file)
    with open("input_scaler.pkl", 'rb') as file:
        input_scaler = pickle.load(file)
    with open("target_scaler.pkl", 'rb') as file:
        target_scaler = pickle.load(file)
    with open("feature_names.pkl", "rb") as file:
        feature_names = pickle.load(file)
    # Load the cleaned data
    df = pd.read_pickle("cleaned_data.pkl")
    return model, label_encoders, input_scaler, target_scaler, feature_names, df

# Function to get unique cuisines from comma-separated values
def get_unique_cuisines(df):
    all_cuisines = []
    for cuisines in df['Cuisines'].dropna():
        all_cuisines.extend([cuisine.strip() for cuisine in str(cuisines).split(',')])
    return sorted(list(set(all_cuisines)))

# Load all resources
model, label_encoders, input_scaler, target_scaler, feature_names, df = load_models_and_data()

# Main title with custom styling
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            font-weight: bold;
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 24px;
            color: #666666;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    <div class="title">Restaurant Cost Prediction App</div>
    <div class="subtitle">Predict dining costs across different cities and cuisines</div>
    """, unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📍 Location & Cuisine")
    # Filter: City
    city_options = sorted(df['City'].unique().tolist())
    selected_city = st.selectbox("Select City", city_options)

    # Filter: Cuisines
    cuisine_options = get_unique_cuisines(df[df['City'] == selected_city])
    selected_cuisine = st.selectbox("Select Cuisine", cuisine_options)

    st.markdown("### ⭐ Rating & Reviews")
    # Rating options
    rating_text_input = st.selectbox("Rating Category", 
                                   ['Excellent', 'Very Good', 'Good', 'Average', 'Poor'])
    votes_input = st.number_input("Number of Reviews", 
                                min_value=0, 
                                max_value=10000, 
                                value=100)
    
    aggregate_rating = st.slider("Aggregate Rating", 
                               min_value=1.0, 
                               max_value=5.0, 
                               value=3.5, 
                               step=0.1)

    st.markdown("### 🎯 Additional Features")
    price_range = st.selectbox("Price Range", 
                             options=[1, 2, 3, 4], 
                             format_func=lambda x: {
                                 1: "Budget",
                                 2: "Mid-Range",
                                 3: "High-End",
                                 4: "Luxury"
                             }[x])
    
    has_online_delivery = st.checkbox("Has Online Delivery")
    is_delivering_now = st.checkbox("Currently Delivering")

with col2:
    st.markdown("### 📊 Restaurant Analysis")
    
    # Show filtered data
    filtered_data = df[
        (df['City'] == selected_city) & 
        (df['Cuisines'].str.contains(selected_cuisine, na=False))
    ].copy()
    
    if not filtered_data.empty:
        st.write(f"Showing {len(filtered_data)} restaurants matching your criteria:")
        
        # Display key statistics
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            avg_cost = filtered_data['Average_Cost_For_Two'].mean()
            st.metric("Average Cost", f"₹{avg_cost:.2f}")
            
        with col_stats2:
            avg_rating = filtered_data['Aggregate_Rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}⭐")
            
        with col_stats3:
            avg_votes = filtered_data['Votes'].mean()
            st.metric("Average Reviews", f"{avg_votes:.0f}")
        
        # Show filtered restaurants with proper columns
        display_columns = [
            'Name',
            'Cuisines', 
            'Average_Cost_For_Two',
            'Aggregate_Rating', 
            'Rating_Text', 
            'Votes'
        ]
        
        # Format the display dataframe
        display_df = filtered_data[display_columns].copy()
        display_df['Average_Cost_For_Two'] = display_df['Average_Cost_For_Two'].round(2)
        display_df['Aggregate_Rating'] = display_df['Aggregate_Rating'].round(1)
        
        # Rename columns for better display
        display_df.columns = [
            'Restaurant',
            'Cuisines',
            'Cost for Two (₹)',
            'Rating',
            'Rating Category',
            'Number of Reviews'
        ]
        
        st.dataframe(display_df)
    else:
        st.warning("No restaurants found matching your criteria.")

    # Prediction Section
    st.markdown("### 💰 Cost Prediction")
    
    if st.button("Predict Cost", use_container_width=True):
        try:
            # Prepare input features
            input_data = {
                'Cuisines': selected_cuisine,
                'Price_Range': price_range,
                'Has_Online_Delivery': int(has_online_delivery),
                'Is_Delivering_Now': int(is_delivering_now),
                'City': selected_city,
                'Aggregate_Rating': aggregate_rating,
                'Rating_Text': rating_text_input,
                'Votes': votes_input
            }
            
            # Create DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Encode categorical variables
            for col in ['Cuisines', 'City', 'Rating_Text']:
                input_df[col] = label_encoders[col].transform(input_df[col].astype(str))
            
            # Scale numerical features
            numerical_features = ['Votes', 'Aggregate_Rating']
            input_df[numerical_features] = input_scaler.transform(input_df[numerical_features])
            
            # Ensure correct column order
            input_df = input_df[feature_names]
            
            # Make prediction
            scaled_prediction = model.predict(input_df)[0]
            
            # Inverse transform the prediction
            prediction = target_scaler.inverse_transform([[scaled_prediction]])[0][0]
            
            # Display prediction with styling
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;
                           text-align: center; margin-top: 20px;'>
                    <h3 style='color: #FF4B4B; margin-bottom: 10px;'>
                        Predicted Cost for Two
                    </h3>
                    <h2 style='color: #1f1f1f; font-size: 36px;'>
                        ₹{prediction:.2f}
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Add price category
            if prediction <= 500:
                category = "Budget-friendly 💰"
            elif prediction <= 1500:
                category = "Mid-range 💰💰"
            else:
                category = "High-end 💰💰💰"
                
            st.markdown(f"""
                <div style='text-align: center; margin-top: 10px;'>
                    <p style='color: #666666; font-size: 18px;'>
                        Price Category: {category}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
            st.info("Please ensure all input fields are filled correctly.")

# Add footer
st.markdown("""
    <div style='text-align: center; color: #666666; padding: 20px;'>
        <p>Built with ❤️ using Streamlit and Random Forest</p>
    </div>
""", unsafe_allow_html=True)