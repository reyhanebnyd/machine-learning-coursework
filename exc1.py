import numpy as np

array = np.random.randint(-10, 11, (100, 100))

print(np.min(array, axis=0))
print(np.max(array, axis=0))
mean = np.mean(array, axis=0)
print(np.mean(array, axis=0))
result = np.where(array == 0, mean, array)
print(result)

