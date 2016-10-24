import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_score

np.random.seed(0)

n_samples = 100
degrees = [1, 4, 15]


def true_fun(x):
    return 0.4*np.power(x, 4) - 3.25*np.power(x, 3) + 7.8*np.power(x, 2) - 5.5*x + 1

X = np.sort(4.0*np.random.rand(n_samples))
y = true_fun(X) + np.random.randn(n_samples) * 0.1

plt.figure(figsize=(14, 5))
for i in range(len(degrees)):
    ax = plt.subplot(1, len(degrees), i + 1)
    plt.setp(ax, xticks=(), yticks=())

    polynomial_features = PolynomialFeatures(degree=degrees[i],
                                             include_bias=False)
    linear_regression = LinearRegression()
    pipeline = Pipeline([("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
    pipeline.fit(X[:, np.newaxis], y)

    # Evaluate the models using crossvalidation
    scores = cross_val_score(pipeline, X[:, np.newaxis], y,
                             scoring="mean_squared_error", cv=10)

    XLIM = 6
    X_test = np.linspace(-2, XLIM, 100)
    plt.plot(X_test, pipeline.predict(X_test[:, np.newaxis]), label="Model")
    plt.plot(X_test, true_fun(X_test), label="True function")
    idxs = np.random.choice(X.shape[0], n_samples * 0.5)
    plt.scatter(X[idxs], y[idxs], label="Samples")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim((-2, XLIM))
    plt.ylim((-3, 4))
    plt.legend(loc="best")
    plt.title("Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degrees[i], -scores.mean(), scores.std()))
plt.show()
