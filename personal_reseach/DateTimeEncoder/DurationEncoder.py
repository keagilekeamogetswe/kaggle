import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DurationEncoder(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def _parse_duration(self, val):
        if pd.isna(val):
            return 0
        hours, mins = 0, 0
        for part in str(val).split():
            if "h" in part:
                hours = int(part.replace("h", ""))
            elif "m" in part:
                mins = int(part.replace("m", ""))
        return hours * 60 + mins

    def transform(self, X):
        df_in = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        extracted_features = []

        for col in df_in.columns:
            minutes_series = (
                df_in[col]
                .apply(self._parse_duration)
                .to_frame(name=f"{col}_minutes")
            )
            extracted_features.append(minutes_series)

        return pd.concat(extracted_features, axis=1)

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return None
        return [f"{col}_minutes" for col in input_features]