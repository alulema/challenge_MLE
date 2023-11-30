import pandas as pd

from challenge.model import DelayModel
from pathlib import Path


class ModelService:
    def __init__(self):
        self.model = DelayModel()
        self._initialize_model()

    def _initialize_model(self):
        root_dir = Path(__file__).parents[2]
        data_file_paths = list(root_dir.glob('data/data.csv'))
        data = pd.read_csv(data_file_paths[0])
        features, target = self.model.preprocess(data=data, target_column="delay")
        self.model.fit(features=features, target=target)

    def predict(self, input_data):
        features = self.model.preprocess(input_data)
        predictions = self.model.predict(features)
        return predictions
