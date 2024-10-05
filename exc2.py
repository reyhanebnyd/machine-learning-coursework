import numpy as np

array1 = np.random.choice(["a", "b", "c"], (100, 20))
array2 = np.random.choice(["a", "b", "c", 'd', 'e', 'f'], (100, 40))

value = np.intersect1d(array1, array2)
array2[np.isin(array2, value)] = '-'
print(array2)