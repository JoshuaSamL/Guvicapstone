import pandas as pd
import json
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px

# Load data from JSON file
def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Clean and preprocess the dataset
def clean_data(data):
    # Extract nested picture_url
    data['picture_url'] = data['images'].apply(
        lambda x: x.get('picture_url') if isinstance(x, dict) else None
    )
    data.drop(columns=['images'], inplace=True, errors='ignore')

    # Convert price fields to numeric
    for col in ['price', 'cleaning_fee', 'extra_people']:
        if col in data.columns:
            data[col] = data[col].replace('[\$,]', '', regex=True).astype(float, errors='ignore')

    # Fill missing numeric values
    numeric_cols = ['price', 'beds', 'bedrooms', 'bathrooms']
    for col in numeric_cols:
        if col in data.columns:
            data[col] = data[col].fillna(0)

    # Handle nested host details
    if 'host' in data.columns:
        host_details = data['host'].apply(
            lambda x: pd.Series(x) if isinstance(x, dict) else pd.Series()
        )
        host_fields = ['host_id', 'host_name', 'host_since', 'host_response_rate', 'host_is_superhost']
        
        # Ensure only existing columns are selected
        available_host_fields = [field for field in host_fields if field in host_details.columns]
        host_data = host_details[available_host_fields].drop_duplicates()
        
        # Fill missing fields with None for consistency
        for field in host_fields:
            if field not in host_data.columns:
                host_data[field] = None
    else:
        host_data = pd.DataFrame(columns=['host_id', 'host_name', 'host_since', 'host_response_rate', 'host_is_superhost'])

    # Drop host column after processing
    data.drop(columns=['host'], inplace=True, errors='ignore')

    # Convert non-hashable data (e.g., lists or dictionaries) to strings before deduplication
    data = data.applymap(lambda x: str(x) if isinstance(x, (list, dict)) else x)

    # Remove duplicates
    data = data.drop_duplicates()

    return data, host_data

# Generate an interactive map
def display_map(data):
    st.header("Airbnb Listings Map")
    map_center = [37.7749, -122.4194]  # Default center (San Francisco)
    m = folium.Map(location=map_center, zoom_start=12)

    for _, row in data.iterrows():
        if 'latitude' in row and 'longitude' in row:
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Name: {row['name']}\nPrice: ${row['price']}",
                tooltip=row['name']
            ).add_to(m)

    st_folium(m, width=700, height=500)

# Perform price analysis
def price_analysis(data):
    st.header("Price Analysis")
    if 'price' in data.columns and 'property_type' in data.columns:
        avg_price = data.groupby('property_type')['price'].mean().reset_index()
        fig = px.bar(avg_price, x='property_type', y='price', title="Average Price by Property Type")
        st.plotly_chart(fig)
    else:
        st.warning("Price or Property Type data is not available for analysis.")

# Analyze seasonal availability patterns
def seasonal_availability(data):
    st.header("Seasonal Availability")
    if 'last_scraped' in data.columns:
        data['last_scraped'] = pd.to_datetime(data['last_scraped'], errors='coerce')
        availability_by_month = data.groupby(data['last_scraped'].dt.month).size().reset_index(name='count')
        fig = px.line(availability_by_month, x='last_scraped', y='count', title="Availability Over Time")
        st.plotly_chart(fig)
    else:
        st.warning("Last Scraped data is not available for analysis.")

# Display location-based insights
def location_insights(data):
    st.header("Location-Based Insights")
    if 'address' in data.columns:
        region = st.text_input("Enter a region or city (e.g., San Francisco):")
        if region:
            location_data = data[data['address'].str.contains(region, na=False, case=False)]
            st.dataframe(location_data)
    else:
        st.warning("Address data is not available for analysis.")

# Main Streamlit app
def main():
    st.title("Airbnb Analysis Dashboard")
    st.sidebar.header("Filters")

    # Step 1: Load Data
    json_file_path = "J:\\Studies\\GUVI\\projects\\capstone\\Airbnb\\sample_airbnb.json"
    data = load_data(json_file_path)

    # Step 2: Clean Data
    data, host_data = clean_data(data)

    # Step 3: Sidebar Filters
    if 'price' in data.columns:
        min_price = st.sidebar.slider("Minimum Price", min_value=int(data['price'].min()), max_value=int(data['price'].max()), value=50)
        max_price = st.sidebar.slider("Maximum Price", min_value=int(data['price'].min()), max_value=int(data['price'].max()), value=500)
        filtered_data = data[(data['price'] >= min_price) & (data['price'] <= max_price)]
    else:
        filtered_data = data

    # Step 4: Call Analysis Functions
    display_map(filtered_data)
    price_analysis(data)
    seasonal_availability(data)
    location_insights(data)

    # Step 5: Display Host Details (Optional)
    st.header("Host Details")
    if not host_data.empty:
        st.dataframe(host_data)

if __name__ == "__main__":
    main()
