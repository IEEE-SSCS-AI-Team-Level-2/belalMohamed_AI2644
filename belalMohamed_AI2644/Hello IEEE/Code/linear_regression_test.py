import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt

X, Y = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=1)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)


from linear_regression import LinearRegression

regressor = LinearRegression()
regressor.fit(X_train, Y_train)
predicted = regressor.predict(X_test)

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

mse_value = mse(Y_test, predicted)
print(f'Mean Squared Error: {mse_value}')

y_pred_line = regressor.predict(X)
plt.scatter(X, Y, color='blue', marker='o', s=30)
plt.plot(X, y_pred_line, color='red')
plt.show()