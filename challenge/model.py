import logging
import numpy as np
import pandas as pd
import xgboost as xgb

from typing import Tuple, Union, List
from challenge.delay_data_processor import DelayDataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        logger.info("Starting data preprocessing")

        # Validate input parameters
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")

        data['period_day'] = data['Fecha-I'].apply(DelayDataProcessor.get_period_day)
        data['high_season'] = data['Fecha-I'].apply(DelayDataProcessor.is_high_season)
        data['min_diff'] = data.apply(DelayDataProcessor.get_min_diff, axis=1)
        data['delay'] = np.where(data['min_diff'] > DelayDataProcessor.THRESHOLD_IN_MINUTES, 1, 0)

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)

        if target_column is None:
            return features[DelayDataProcessor.TOP_10_FEATURES]

        target = data[[target_column]]
        logger.info("Data preprocessing completed")
        return features[DelayDataProcessor.TOP_10_FEATURES], target

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        logger.info("Starting model training")

        n_y0 = len(target[target['delay'] == 0])
        n_y1 = len(target[target['delay'] == 1])
        scale = n_y0/n_y1

        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model.fit(features, target)

        logger.info("Model training completed")

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        logger.info("Making predictions")
        predictions = self._model.predict(features)
        return list(map(int, predictions))