# Airbnb Data Analysis and Visualization

This project focuses on analyzing Airbnb data using MongoDB Atlas, performing data analysis, and creating interactive visualizations through a Streamlit web application. The dashboard provides insights into pricing variations, availability patterns, and location-based trends of Airbnb listings.

## Features

### 1. Interactive Map Visualization
- Geospatial visualization of Airbnb listings
- Interactive markers showing property details
- Price and location information on hover

### 2. Price Analysis
- Average price by property type
- Price distribution visualization
- Interactive price range filters

### 3. Seasonal Analysis
- Availability patterns over time
- Monthly booking trends
- Seasonal pricing variations

### 4. Location-Based Insights
- Region-specific property analysis
- Address-based filtering
- Geographical distribution of listings

### 5. Host Information
- Detailed host statistics
- Host rating analysis
- Superhost status information

## Tech Stack

- **Python 3.x**
- **MongoDB Atlas**: Database storage and management
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Folium**: Map visualizations
- **JSON**: Data format handling

## Prerequisites

1. Python 3.x installed
2. MongoDB Atlas account
3. Required Python packages:
```bash
pandas
streamlit
folium
streamlit-folium
plotly
json
```

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB Atlas:
- Create a MongoDB Atlas account
- Set up a new cluster
- Load the Airbnb sample dataset
- Configure network access and database user

## Project Structure
```
├── app.py                     # Main Streamlit application
├── data_preprocessing.ipynb   # Data cleaning and preprocessing
├── requirements.txt          # Required Python packages
├── README.md                # Project documentation
└── sample_airbnb.json       # Sample dataset
```

## Data Preprocessing

The preprocessing steps include:
1. Handling nested JSON structures
2. Cleaning price fields
3. Managing missing values
4. Processing host information
5. Removing duplicates
6. Converting data types

## Running the Application

1. Navigate to the project directory:
```bash
cd airbnb-analysis
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Access the dashboard at `http://localhost:8501`

## Application Components

### 1. Data Loading
```python
def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)
```

### 2. Data Cleaning
```python
def clean_data(data):
    # Price field cleaning
    # Missing value handling
    # Host information processing
    # Duplicate removal
```

### 3. Visualization Functions
- `display_map()`: Interactive map visualization
- `price_analysis()`: Price trend analysis
- `seasonal_availability()`: Seasonal patterns
- `location_insights()`: Geographic analysis

## Features Breakdown

### Interactive Map
- Displays property locations
- Popup information for each listing
- Price and property details on hover

### Price Analysis Dashboard
- Price distribution charts
- Property type comparison
- Interactive price filters

### Seasonal Trends
- Monthly availability patterns
- Booking trend analysis
- Time-based visualizations

## Data Structure

The project uses the following data structure:
```json
{
    "_id": "unique_listing_id",
    "name": "listing_title",
    "price": "listing_price",
    "host": {
        "host_id": "id",
        "host_name": "name"
    },
    "location": {
        "latitude": "lat",
        "longitude": "long"
    }
}
```

## Future Enhancements

1. Advanced filtering options
2. More detailed price predictions
3. Review sentiment analysis
4. Additional visualization types
5. Real-time data updates

## Troubleshooting

Common issues and solutions:
1. MongoDB Connection:
   - Check network connectivity
   - Verify credentials
   - Ensure proper IP whitelisting

2. Data Loading:
   - Verify JSON file path
   - Check file permissions
   - Validate JSON structure

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MongoDB Atlas for the sample dataset
- Streamlit for the web application framework
- The open-source community for various tools and libraries
