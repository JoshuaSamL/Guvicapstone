# Restaurant Price Predictor

A web-based application that predicts dining costs across different cities and cuisines, built with Streamlit and Random Forest. The application provides restaurant recommendations based on user preferences and predicts the average cost for two people dining.

## 🌟 Features

- Location-based restaurant filtering
- Cuisine-specific searches
- Price prediction based on multiple parameters
- Interactive visualizations of restaurant data
- Real-time statistics and metrics
- User-friendly interface with responsive design

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Machine Learning:** Scikit-learn (Random Forest)
- **Data Processing:** Pandas, NumPy
- **Cloud Platform:** AWS (EC2, S3, RDS)
- **Database:** SQL
- **Version Control:** Git

## 📦 Prerequisites

- Python 3.8+
- pip
- AWS Account (for deployment)
- Git

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/restaurant-price-predictor.git
cd restaurant-price-predictor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your AWS credentials (if deploying to AWS)

## 📁 Project Structure

```
restaurant-price-predictor/
├── app/
│   ├── main.py                    # Main Streamlit application
│   └── utils/                     # Utility functions
├── models/
│   ├── restaurant_cost_prediction_model.pkl
│   ├── label_encoders.pkl
│   ├── input_scaler.pkl
│   ├── target_scaler.pkl
│   └── feature_names.pkl
├── data/
│   └── cleaned_data.pkl
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Running the Application

1. Navigate to the project directory:
```bash
cd restaurant-price-predictor
```

2. Run the Streamlit app:
```bash
streamlit run app/main.py
```

3. Open your browser and go to `http://localhost:8501`

## 🌐 Deployment

### AWS EC2 Deployment Steps:

1. Launch an EC2 instance
2. Configure security groups
3. SSH into your instance
4. Install required dependencies
5. Clone the repository
6. Set up environment variables
7. Run the application using screen or tmux

Detailed deployment instructions can be found in the [deployment guide](docs/deployment.md).

## 💽 Data Management

The application uses several preprocessed files:
- `restaurant_cost_prediction_model.pkl`: Trained Random Forest model
- `label_encoders.pkl`: Encoders for categorical variables
- `input_scaler.pkl`: Scaler for input features
- `target_scaler.pkl`: Scaler for target variable
- `feature_names.pkl`: List of feature names
- `cleaned_data.pkl`: Preprocessed restaurant data

## 📊 Model Information

The price prediction model:
- Algorithm: Random Forest Regressor
- Features: Location, Cuisine, Ratings, Reviews, Delivery Options
- Target Variable: Average Cost for Two
- Evaluation Metrics: RMSE, MAE

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- Zomato for providing the dataset
- Streamlit for the amazing web framework
- AWS for cloud infrastructure support
