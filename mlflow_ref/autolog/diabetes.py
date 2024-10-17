import mlflow
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

mlflow.set_tracking_uri("http://127.0.0.1:5000")
apple_experiment = mlflow.set_experiment("Diabetes_Models")

nw = datetime.now()

extra_tags = {
        "project_name": "diabetes_regressor",
        "autologging": "Enabled",
        "date_logged": nw.strftime('%B-%d-%Y')
}
mlflow.autolog(
    extra_tags=extra_tags
)

db = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

rf = RandomForestRegressor(n_estimators=200, max_depth=10, max_features=4)

# MLflow triggers logging automatically upon model fitting
rf.fit(X_train, y_train)