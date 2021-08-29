from joblib import load
import os

path = os.path.abspath(os.path.join("analysis"))
path_model = os.path.join(path, "lasso.joblib")  # ridge.joblib
path_scaller = os.path.join(path, "scaler.joblib")

model = load(path_model)
scaler = load(path_scaller)
