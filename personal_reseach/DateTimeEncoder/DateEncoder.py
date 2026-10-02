import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DateEncoder(BaseEstimator, TransformerMixin):

    ALLOWED_FEATURES = {"month", "year", "day", "dayofweek"}

    def __init__(self, features=None, drop_original=True):
        self.features = features
        self.drop_original = drop_original

    def fit(self, X, y=None):
        return self

    def _get_selected_features(self):
        """Validates and returns the list of feature names to extract."""
        if self.features is None:
            return ["month", "year", "day", "dayofweek"]

        # Validate provided features
        invalid = set(self.features) - self.ALLOWED_FEATURES
        if invalid:
            raise ValueError(
                f"Invalid feature(s) {invalid}. Allowed options: {self.ALLOWED_FEATURES}"
            )

        return list(self.features)

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            df_in = X.copy()
        else:
            df_in = pd.DataFrame(X)

        selected_features = self._get_selected_features()
        extracted_features = []

        for col in df_in.columns:
            dt = pd.to_datetime(df_in[col], format="mixed", dayfirst=True)

            for feat in selected_features:
                feature_series = getattr(dt.dt, feat).to_frame(name=f"{col}_{feat}")
                extracted_features.append(feature_series)

        return pd.concat(extracted_features, axis=1)

    def get_feature_names_out(self, input_features=None):
        """Returns feature names for output features."""
        if input_features is None:
            return None

        selected_features = self._get_selected_features()
        feature_names = []

        for col in input_features:
            for feat in selected_features:
                feature_names.append(f"{col}_{feat}")

        return feature_names