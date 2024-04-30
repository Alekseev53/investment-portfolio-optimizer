import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# определение функции
def func(x, a, b):
    return a*np.sqrt(x) + b

# координаты точек

data = [(0.001,0.52),
        (0.008,4.1),
        (0.018,6.8),
        (0.06,10.81),
        (0.099,12.57)
        ]


xdata = [x[0] for x in data]
ydata = [x[1] for x in data]

# поиск параметров
popt, pcov = curve_fit(func, xdata, ydata)

# вывод параметров
a, b = popt
print(f"a = {a}, b = {b}")

# создание последовательности для визуализации
x = np.linspace(0, 0.1, 400)
y = func(x, *popt)

# визуализация
plt.figure(figsize=(10,6))
plt.plot(xdata, ydata, 'bo', label='данные')
plt.plot(x, y, 'r', label='подгонка: a=%.3f, b=%.3f' % tuple(popt))
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()