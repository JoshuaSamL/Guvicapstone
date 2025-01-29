# PhonePe Pulse Data Visualization and Analysis

This project involves extracting, processing, and visualizing data from the PhonePe Pulse GitHub repository to create an interactive dashboard that displays various insights about digital payment trends in India.

## Project Overview
The PhonePe Pulse Data Visualization project aims to extract data from the PhonePe Pulse GitHub repository, transform it, store it in a MySQL database, and create an interactive dashboard using Streamlit. The dashboard provides insights into transaction patterns, user behavior, and digital payment trends across different states and districts in India.

## Tools and Libraries Used

### Primary Tools
- **Python**: Main programming language used for data processing and analysis
- **Streamlit**: Creates the interactive web-based dashboard
- **MySQL**: Stores and manages the processed data
- **Git**: Used for data extraction from PhonePe Pulse repository

### Python Libraries
1. `pandas`: Data manipulation and analysis
2. `geopandas`: Handling geographical data
3. `mysql-connector-python`: MySQL database connection
4. `folium`: Creating interactive maps
5. `plotly`: Advanced data visualization
6. `streamlit_option_menu`: Navigation menu in Streamlit
7. `streamlit_folium`: Displaying Folium maps in Streamlit

## Features

### 1. Data Extraction and Processing
- Clone and extract data from PhonePe Pulse GitHub repository
- Process and transform the data into suitable format
- Store processed data in MySQL database

### 2. Interactive Dashboard
- **Geographic Visualization**: Interactive choropleth map of India showing state-wise transaction data
- **Temporal Analysis**: Year and quarter-wise transaction trends
- **Transaction Insights**: Analysis of transaction types, amounts, and user statistics
- **State-wise Analysis**: Detailed state-level transaction and user metrics
- **District-level Insights**: Transaction patterns at district level

### 3. Analysis Features
- Top transaction analysis by state and district
- Mobile brand usage statistics
- App opens analysis
- Transaction amount and count analysis
- User registration patterns

## Database Structure
The MySQL database 'phonepe' contains the following tables:
1. `aggregated_transaction`
2. `aggregated_user`
3. `map_transaction`
4. `map_user`
5. `top_transaction`
6. `top_user`

## Installation and Setup

1. **Clone the Repository**
```bash
git clone <your-repository-url>
```

2. **Install Required Libraries**
```bash
pip install -r requirements.txt
```

3. **Database Configuration**
```python
mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="phonepe"
)
```

4. **Run the Application**
```bash
streamlit run app.py
```

## Project Structure
```
├── app.py                     # Main Streamlit application
├── data_preprocessing.ipynb   # Data preprocessing and transformation
├── requirements.txt          # Required Python packages
├── README.md                # Project documentation
└── gadm41_IND_1.shp        # India shapefile for visualization
```

## Dashboard Sections

### 1. Home
- Project overview
- Basic statistics
- Interactive map preview

### 2. Data Exploration
- **Map Analysis**
  - Interactive choropleth map
  - State-wise transaction visualization
  - Year and quarter selection
- **Transaction Analysis**
  - Transaction summaries
  - Top performing states
  - Trend analysis

### 3. Top Charts
- Mobile brands analysis
- Transaction metrics
- State and district rankings
- App usage patterns

## Data Source
- PhonePe Pulse GitHub repository
- India GIS shapefile data

## Future Enhancements
1. Add more interactive features
2. Include predictive analytics
3. Enhance visualization capabilities
4. Add user authentication
5. Implement real-time data updates

## Troubleshooting
For common issues:
1. Ensure all dependencies are installed
2. Verify database connection parameters
3. Check if required data files are present
4. Ensure proper Python version (3.x recommended)

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
