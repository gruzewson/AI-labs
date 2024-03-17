import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# TODO: calculate closed-form solution
# y = mx + b
#.T transponowanie
#dot iloczyn skalarny
#linalg.inv odwrotna macierz
X_fill = np.column_stack((np.ones((len(x_train), 1)), x_train))
theta_best = np.linalg.inv(X_fill.T.dot(X_fill)).dot(X_fill.T.dot(y_train))
y = theta_best[0] + theta_best[1] * x_train

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
# TODO: calculate error
error_cf = np.mean(np.square(np.subtract(float(theta_best[0]) + float(theta_best[1]) * x_test, y_test)))
print(f"MSE closed_from {error_cf}")
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization
x_standarized = (x_train - np.mean(x_train))/np.std(x_train)
y_standarized = (y_train - np.mean(y_train))/np.std(y_train)

learning_rate = 0.0001
new_theta = np.random.rand(2)
precision = 0.000000001

while True:
    # TODO: calculate theta using Batch Gradient Descent
    y = new_theta[0] + new_theta[1] * x_standarized
    a_copy = new_theta[1]
    b_copy = new_theta[0]
    gradient_a = 2*(np.mean((np.subtract(y_standarized, y))*x_standarized))
    gradient_b = 2*(np.mean(np.subtract(y_standarized, y)))

    new_theta[0] += learning_rate * gradient_b
    new_theta[1] += learning_rate * gradient_a
    if abs(b_copy - new_theta[0]) <= precision and abs(a_copy - new_theta[1]) <= precision:
        break

x_standarized_test = (x_test - np.mean(x_train))/np.std(x_train)
y_standarized_test = (y_test - np.mean(y_train))/np.std(y_train)
# plot the regression line
x = np.linspace(min(x_standarized_test), max(x_standarized_test), 100)
y = float(new_theta[0]) + float(new_theta[1]) * x
# TODO: calculate error
error_test = np.mean(np.square(np.subtract(y_standarized_test, new_theta[0] + new_theta[1] * x_standarized_test)))

print(f"MSE gradient: {error_test}")
plt.plot(x, y)
plt.scatter(x_standarized_test, y_standarized_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

