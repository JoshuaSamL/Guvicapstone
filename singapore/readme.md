# Singapore HDB Resale Price Predictor

A machine learning-powered web application that predicts Housing and Development Board (HDB) resale flat prices in Singapore. The application provides accurate price estimates based on various factors like location, flat type, floor area, and proximity to amenities.

## 🎯 Problem Statement

Develop a machine learning model and web application to predict HDB resale flat prices in Singapore, helping potential buyers and sellers make informed decisions in the competitive real estate market.

## 🌟 Features

- Real-time price prediction based on property characteristics
- Interactive map visualization of selected towns
- Market analytics and insights
- User-friendly interface with input validation
- Comprehensive error handling and logging

## 🏗 Project Structure

```
singapore-hdb-predictor/
│
├── app.py                 # Main Streamlit application
├── models/
│   ├── model.pkl         # Trained prediction model
│   ├── model_scaler.pkl  # Feature scaler
│   └── model_encoders.pkl # Label encoders
├── logs/
│   └── app.log          # Application logs
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## 🔧 Technical Stack

- **Python 3.8+**
- **Framework:** Streamlit
- **Machine Learning:** scikit-learn
- **Data Processing:** pandas, numpy
- **Visualization:** folium
- **Logging:** Python logging module
- **Version Control:** Git
- **Cloud Platform:** Render

## 📦 Dependencies

```
streamlit==1.24.0
streamlit-option-menu==0.3.2
pandas==1.5.3
numpy==1.24.3
scikit-learn==1.2.2
folium==0.14.0
streamlit-folium==0.11.1
```

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/singapore-hdb-predictor.git
   cd singapore-hdb-predictor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 💻 Usage

### Price Prediction
1. Navigate to the "Price Prediction" page
2. Enter property details:
   - Town location
   - Flat type and model
   - Floor area
   - Storey range
   - Remaining lease
   - Property age
   - Distance to MRT
3. Click "Predict Price" to get the estimated resale price

### Analytics
- View feature importance charts
- Analyze market trends
- Explore location-based insights

## 🗺 Features in Detail

### Location Analysis
- Interactive map visualization
- Distance calculation to CBD
- MRT proximity analysis

### Property Metrics
- Floor area calculation
- Remaining lease assessment
- Age-based valuation
- Storey range analysis

### Market Intelligence
- Feature importance visualization
- Price trends analysis
- Location-based insights

## 🛠 Development

### Class Structure
The main application is built around the `PropertyPricePredictionApp` class with the following key methods:

- `__init__`: Initializes models and configurations
- `load_models`: Handles model loading and validation
- `preprocess_prediction_input`: Processes user inputs
- `show_prediction_page`: Manages the prediction interface
- `show_analytics_page`: Displays market analytics
- `run`: Orchestrates the application flow

### Error Handling
- Comprehensive input validation
- Graceful error management
- Detailed logging system

## 📊 Model Details

- Algorithm: Gradient Boosting
- Features: 11 key property characteristics
- Preprocessing: Label encoding, scaling
- Evaluation metrics: RMSE, R² Score

## 🔍 Data Source

Data obtained from [Singapore Public Data](https://beta.data.gov.sg/collections/189/view)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

Your Name - [Your Email]

## 🙏 Acknowledgments

- Singapore Housing and Development Board for the data
- Streamlit team for the excellent framework
- Contributors and maintainers of used libraries

## 📞 Support

For support, email [your email] or create an issue in the repository.
