import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import logging
import warnings
import sys
from pathlib import Path

# Suppress warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('training.log')
    ]
)
logger = logging.getLogger(__name__)

class PropertyPriceModel:
    """A class to train and manage a property price prediction model."""
    
    def __init__(self):
        """Initialize the model with necessary attributes."""
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        # Updated to match actual dataset column names
        self.feature_columns = [
            'town', 'flat_type', 'flat_model', 'floor_area_sqm',
            'storey_range', 'remaining_lease', 'property_age',  # Using original column names
            'month_number', 'cbd_dist', 'min_dist_mrt', 'is_near_mrt'
        ]
        
    def extract_lease_years(self, lease_str):
        """
        Extract years from lease string.
        
        Args:
            lease_str: String containing lease information
            
        Returns:
            float: Number of years extracted from the lease string
        """
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
        """
        Extract median storey from range.
        
        Args:
            x: String containing storey range
            
        Returns:
            float: Median storey number
        """
        try:
            if pd.isna(x):
                return 0
            split_list = str(x).split(' TO ')
            return np.mean([float(i) for i in split_list])
        except:
            return 0

    def preprocess_data(self, df):
        """
        Preprocess the dataset with enhanced feature engineering and NaN handling."""
        
        logger.info("Starting data preprocessing...")
        try:
            processed_df = df.copy()
            
            # Check for required columns
            required_columns = ['resale_price'] + [col for col in self.feature_columns 
                                                if col not in ['property_age', 'month_number', 'is_near_mrt']]
            missing_columns = [col for col in required_columns if col not in processed_df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            # Remove rows with NaN in target variable
            initial_rows = len(processed_df)
            processed_df = processed_df.dropna(subset=['resale_price'])
            rows_removed = initial_rows - len(processed_df)
            logger.info(f"Removed {rows_removed} rows with NaN in resale_price")

            # Handle storey_range - convert to numeric values
            if 'storey_range' in processed_df.columns:
                processed_df['storey_range'] = processed_df['storey_range'].apply(self._get_storey_median)

            # Handle remaining_lease - convert to numeric values
            if 'remaining_lease' in processed_df.columns:
                processed_df['remaining_lease'] = processed_df['remaining_lease'].apply(self.extract_lease_years)

            # Handle categorical variables
            categorical_features = ['town', 'flat_type', 'flat_model']
            for feature in categorical_features:
                if feature in processed_df.columns:
                    self.label_encoders[feature] = LabelEncoder()
                    processed_df[feature] = self.label_encoders[feature].fit_transform(
                        processed_df[feature].fillna('Unknown').astype(str)
                    )

            # Calculate property age
            current_year = 2024
            if 'lease_commence_date' in processed_df.columns:
                processed_df['property_age'] = current_year - processed_df['lease_commence_date']

            # Process month
            if 'month' in processed_df.columns:
                processed_df['month_number'] = pd.to_datetime(processed_df['month']).dt.month

            # Create proximity features
            if 'min_dist_mrt' in processed_df.columns:
                processed_df['min_dist_mrt'] = processed_df['min_dist_mrt'].fillna(
                    processed_df['min_dist_mrt'].median()
                )
                median_mrt_dist = processed_df['min_dist_mrt'].median()
                processed_df['is_near_mrt'] = (processed_df['min_dist_mrt'] < median_mrt_dist).astype(int)

            # Handle missing columns
            for col in self.feature_columns:
                if col not in processed_df.columns:
                    logger.warning(f"Missing column: {col}. Adding dummy values.")
                    processed_df[col] = 0

            # Select features and target
            X = processed_df[self.feature_columns]
            y = processed_df['resale_price']

            # Final handling of any remaining NaN values in features
            for col in X.columns:
                if X[col].dtype.kind in 'fcb':  # float, complex, or boolean
                    X[col] = X[col].fillna(X[col].median())
                else:  # integer or object
                    X[col] = X[col].fillna(0)

            logger.info(f"Final dataset shape: {X.shape}")
            logger.info("Data preprocessing completed successfully")
            return X, y

        except Exception as e:
            logger.error(f"Error in preprocessing data: {str(e)}")
            raise

    def train(self, X, y):
        """
        Train the model with optimized parameters.
        
        Args:
            X: preprocessed features
            y: target variable
            
        Returns:
            self: trained model instance
        """
        logger.info("Starting model training...")
        try:
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Initialize and train model
            self.model = RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )

            self.model.fit(X_train_scaled, y_train)

            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            self._evaluate_model(y_test, y_pred)

            # Feature importance
            self._print_feature_importance()

            logger.info("Model training completed successfully")
            return self

        except Exception as e:
            logger.error(f"Error in training model: {str(e)}")
            raise

    def _evaluate_model(self, y_true, y_pred):
        """Calculate and log model performance metrics."""
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)

        logger.info("Model Performance Metrics:")
        logger.info(f"Mean Squared Error: {mse:,.2f}")
        logger.info(f"Mean Absolute Error: {mae:,.2f}")
        logger.info(f"Root Mean Squared Error: {rmse:,.2f}")
        logger.info(f"R-squared Score: {r2:.4f}")

    def _print_feature_importance(self):
        """Print feature importance scores."""
        importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        })
        importance = importance.sort_values('importance', ascending=False)
        logger.info("\nFeature Importance:")
        for idx, row in importance.iterrows():
            logger.info(f"{row['feature']}: {row['importance']:.4f}")

    def save_model(self, filepath_prefix='model'):
        """
        Save the model and preprocessing objects.
        
        Args:
            filepath_prefix: prefix for the saved model files
        """
        logger.info("Saving model and preprocessing objects...")
        try:
            # Create output directory if it doesn't exist
            output_dir = Path('models')
            output_dir.mkdir(exist_ok=True)
            
            # Save model and preprocessing objects
            model_path = output_dir / f'{filepath_prefix}.pkl'
            scaler_path = output_dir / f'{filepath_prefix}_scaler.pkl'
            encoders_path = output_dir / f'{filepath_prefix}_encoders.pkl'
            
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            with open(encoders_path, 'wb') as f:
                pickle.dump(self.label_encoders, f)

            logger.info(f"Model and preprocessing objects saved successfully in {output_dir}")

        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

def main():
    """Main function to run the training pipeline."""
    logger.info("Starting the training pipeline...")
    
    try:
        # Load data
        data_path = Path('combined.csv')
        if not data_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
            
        df = pd.read_csv(data_path)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        
        # Initialize and train model
        model = PropertyPriceModel()
        X, y = model.preprocess_data(df)
        model.train(X, y)
        model.save_model()
        
        logger.info("Training pipeline completed successfully")
    
    except Exception as e:
        logger.error(f"Error in training pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()