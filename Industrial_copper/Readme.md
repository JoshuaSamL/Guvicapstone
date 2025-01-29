# Industrial Copper Modeling

This project implements machine learning models to predict selling prices and status (Won/Lost) for industrial copper sales, along with a Streamlit web interface for easy interaction with the models.

## Problem Statement

The copper industry faces challenges in:
1. Predicting accurate selling prices due to data skewness and noise
2. Classifying lead status (Won/Lost) for better sales forecasting

This solution addresses these challenges through machine learning models and provides an interactive interface for predictions.

## Project Structure

```
industrial-copper-modeling/
│
├── notebooks/
│   └── copper_modeling.ipynb       # Main analysis and model development
│
├── models/
│   ├── model.pkl                   # Regression model for price prediction
│   ├── clsmodel.pkl               # Classification model for status prediction
│   ├── scaler.pkl                 # Standard scaler for regression
│   ├── cscaler.pkl               # Standard scaler for classification
│   ├── t.pkl                      # Transformer for regression features
│   ├── ct.pkl                     # Transformer for classification features
│   └── s.pkl                      # Status encoder
│
├── app.py                          # Streamlit web application
└── README.md                       # Project documentation
```

## Features

- Data preprocessing and cleaning
- Handling skewness and outliers
- Feature engineering and scaling
- Machine learning models:
  - Regression model for selling price prediction
  - Classification model for status prediction
- Interactive Streamlit web interface
- Comprehensive error handling and input validation

## Technical Details

### Dependencies

```python
pandas
numpy
scikit-learn
streamlit
joblib
```

### Data Preprocessing Steps

1. Missing value treatment
2. Outlier detection and handling using IQR/Isolation Forest
3. Skewness treatment using log transformation
4. Feature encoding:
   - One-hot encoding for categorical variables
   - Label encoding for status
5. Feature scaling using StandardScaler

### Models

- **Regression Model**: Predicts the selling price
  - Input features include quantity, dimensions, country, etc.
  - Log transformation applied to handle price skewness
  - Evaluation metrics: RMSE, R-squared

- **Classification Model**: Predicts Won/Lost status
  - Binary classification problem
  - Features include price, quantity, and customer details
  - Evaluation metrics: Accuracy, Precision, Recall, F1-score

## Usage

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Access the web interface through your browser:
   - Select the desired prediction type (Selling Price or Status)
   - Enter the required information in the input fields
   - Click the prediction button to get results

## Input Fields

### Selling Price Prediction
- Status
- Item Type
- Country
- Application
- Product Reference
- Quantity (tons)
- Thickness
- Width
- Customer ID

### Status Prediction
- Quantity (tons)
- Thickness
- Width
- Customer ID
- Selling Price
- Item Type
- Country
- Application
- Product Reference

## Model Performance

The models have been optimized using:
- Cross-validation
- Hyperparameter tuning using GridSearchCV
- Feature importance analysis
- Robust error handling and input validation

## Future Improvements

1. Implementation of more advanced models
2. Additional feature engineering
3. Real-time model updating
4. Enhanced visualization of predictions
5. API endpoint development

## Notes

- All numerical inputs should be positive values
- The application includes input validation to prevent invalid entries
- Models have been trained on historical data and may need periodic retraining
- Log transformations are automatically handled in the backend

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
