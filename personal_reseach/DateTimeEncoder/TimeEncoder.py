import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TimeEncoder(BaseEstimator, TransformerMixin):

    ALLOWED_FEATURES = {"hour", "minute"}

    def __init__(self, features=None):
        self.features = features

    def fit(self, X, y=None):
        return self

    def _get_selected_features(self):
        if self.features is None:
            return ["hour", "minute"]

        invalid = set(self.features) - self.ALLOWED_FEATURES
        if invalid:
            raise ValueError(
                f"Invalid feature(s) {invalid}. Allowed options: {self.ALLOWED_FEATURES}"
            )

        return list(self.features)

    def transform(self, X):
        df_in = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        selected_features = self._get_selected_features()
        extracted_features = []

        for col in df_in.columns:
            dt = pd.to_datetime(df_in[col], format="mixed")
            for feat in selected_features:
                feature_series = getattr(dt.dt, feat).to_frame(
                    name=f"{col}_{feat}"
                )
                extracted_features.append(feature_series)

        return pd.concat(extracted_features, axis=1)

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return None

        selected_features = self._get_selected_features()
        feature_names = []

        for col in input_features:
            for feat in selected_features:
                feature_names.append(f"{col}_{feat}")

        return feature_names