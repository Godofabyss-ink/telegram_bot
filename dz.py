from sklearn.linear_model import Perceptron
import numpy as np

X_train = np.array([
    [1, 0, 1, 0, 1],  # Предположим, что это признаки
    [0, 1, 0, 1, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
])

# Метки (ответы): 1 — придут, 0 — не придут
y_train = np.array([1, 0, 1, 0, 1])


perceptron = Perceptron()


perceptron.fit(X_train, y_train)


test_example = np.array([[1, 0, 1, 0, 0]])
prediction = perceptron.predict(test_example)

print("Результат после собрания:", "да" if prediction[0] == 1 else "нет")
