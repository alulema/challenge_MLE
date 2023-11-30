import logging
import numpy as np
import pandas as pd
import xgboost as xgb

from typing import Tuple, Union, List
from challenge.utils.delay_data_processor import DelayDataProcessor
from challenge.utils.exceptions import InvalidMonthValueException, InvalidTipoVueloValueException

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

        if 'MES' in data.columns:
            invalid_months = data['MES'].apply(lambda x: x < 1 or x > 12)
            if invalid_months.any():
                raise InvalidMonthValueException("Invalid 'MES' value detected in features")

        if 'TIPOVUELO' in data.columns and not all(data['TIPOVUELO'].isin(['N', 'I'])):
            raise InvalidTipoVueloValueException("Invalid 'TIPOVUELO' value detected in data")

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)

        for col in DelayDataProcessor.TOP_10_FEATURES:
            if col not in features.columns:
                features[col] = 0

        if target_column is None:
            return features[DelayDataProcessor.TOP_10_FEATURES]

        data['period_day'] = data['Fecha-I'].apply(DelayDataProcessor.get_period_day)
        data['high_season'] = data['Fecha-I'].apply(DelayDataProcessor.is_high_season)
        data['min_diff'] = data.apply(DelayDataProcessor.get_min_diff, axis=1)
        data['delay'] = np.where(data['min_diff'] > DelayDataProcessor.THRESHOLD_IN_MINUTES, 1, 0)

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