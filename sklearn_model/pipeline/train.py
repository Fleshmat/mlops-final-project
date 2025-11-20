import os
import joblib
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score

ku = os.getenv("KAGGLE_USERNAME")
key = os.getenv("KAGGLE_KEY")

os.environ['KAGGLE_USERNAME'] = ku
os.environ['KAGGLE_KEY'] = key

from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    data_dir = os.getenv("DATA_DIR")
    os.makedirs(data_dir, exist_ok=True)
    dataset = os.getenv("KAGGLE_DATASET")
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=data_dir, unzip=True)
    return os.path.join(data_dir, "transactions.csv")

def build_pipeline(X: pd.DataFrame) -> Pipeline:
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15, min_samples_split=10, min_samples_leaf=5)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", clf),
    ])

    return pipeline


def train_and_log(save_path: str = os.getenv("MODEL_PATH")):
    data_path = download_dataset()
    df = pd.read_csv(data_path)

    X = df.drop(columns=["is_fraud", "transaction_id", "transaction_time", "bin_country", "user_id"])
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    pipeline = build_pipeline(X)

    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)

    with mlflow.start_run():
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        acc = float(accuracy_score(y_test, preds))

        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 15)
        mlflow.log_param("min_samples_split", 10)
        mlflow.log_param("min_samples_leaf", 5)
        mlflow.log_metric("accuracy", acc)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(pipeline, save_path)
        mlflow.log_artifact(save_path)

    return pipeline, acc


if __name__ == "__main__":
    model, accuracy = train_and_log()
    print(f"Trained fraud detection model accuracy={accuracy}")
