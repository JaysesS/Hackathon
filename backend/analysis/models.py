from sklearn.linear_model import RidgeCV, LassoCV, SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, ShuffleSplit


scaler = StandardScaler()
ridge = RidgeCV(alphas=[1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
lasso = LassoCV(random_state=42,  max_iter=10000)
skf = StratifiedKFold(n_splits=5)
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
