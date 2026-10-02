import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DateEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, drop_original=True):
        self.drop_original = drop_original

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            df_in = X.copy()
        else:
            df_in = pd.DataFrame(X)

        extracted_features = []
        for col in df_in.columns:
            dt = pd.to_datetime(df_in[col], format="mixed", dayfirst=True)

            month = dt.dt.month.to_frame(name=f"{col}_month")
            year = dt.dt.year.to_frame(name=f"{col}_year")
            day = dt.dt.day.to_frame(name=f"{col}_day")
            dayofweek = dt.dt.dayofweek.to_frame(name=f"{col}_dayofweek")

            extracted_features.extend([month, year, day, dayofweek])

        return pd.concat(extracted_features, axis=1)

    def get_feature_names_out(self, input_features=None):
        """Returns feature names for output features."""
        if input_features is None:
            return None

        feature_names = []
        for col in input_features:
            feature_names.extend(
                [f"{col}_month", f"{col}_year", f"{col}_day", f"{col}_dayofweek"]
            )
        return list(feature_names)