class LinearRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples = len(X)
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.n_iterations):
            y_predicted = []
            for i in range(n_samples):
                prediction = self.bias
                for j in range(n_features):
                    prediction += X[i][j] * self.weights[j]
                y_predicted.append(prediction)

            dw = [0.0] * n_features
            db = 0.0
            
            for i in range(n_samples):
                error = y_predicted[i] - y[i]
                for j in range(n_features):
                    dw[j] += X[i][j] * error
                db += error

            for j in range(n_features):
                self.weights[j] -= (self.learning_rate * (1/n_samples) * dw[j])
            self.bias -= (self.learning_rate * (1/n_samples) * db)

    def predict(self, X):
        predictions = []
        for i in range(len(X)):
            prediction = self.bias
            for j in range(len(self.weights)):
                prediction += X[i][j] * self.weights[j]
            predictions.append(prediction)
        return predictions