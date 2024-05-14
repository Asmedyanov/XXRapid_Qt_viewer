from J_ratio_function import decrement_space_function

import matplotlib.pyplot as plt
import numpy as np

h = 3.5e-2
w = 3.5

a = np.arange(0, 1.0e0 / h, 1e-3 / w)
f = decrement_space_function(a, w, h)
plt.plot(a, f)
plt.show()
