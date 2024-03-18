import numpy as np
import matplotlib.pyplot as plt

class StatValues:
    def __init__(self, stat_gain, stat_stdev):
        self.stat_gain = stat_gain
        self.stat_stdev = stat_stdev

    def plot(self, color):
        plt.scatter(self.stat_stdev, self.stat_gain, c=color, alpha=0.7)

# Определим параметры распределения
mean_gain = 0  # Среднее значение для stat_gain
std_dev_gain = 2  # Стандартное отклонение для stat_gain
mean_stdev = 0  # Среднее значение для stat_stdev
std_dev_stdev = 1  # Стандартное отклонение для stat_stdev
array_size = 500  # Размер массива

# Создадим массив объектов класса StatValues
stat_values_array = []
for _ in range(array_size):
    stat_gain = np.random.normal(mean_gain, std_dev_gain)
    stat_stdev = np.random.normal(mean_stdev, std_dev_stdev)
    stat_values_array.append(StatValues(stat_gain, stat_stdev))

# Визуализируем scatter plot
plt.figure(figsize=(8, 6))
for stat_values in stat_values_array:
    stat_values.plot('blue')

# Сортируем по stat_stdev_values
sorted_stat_values_array = sorted(stat_values_array, key=lambda x: x.stat_stdev)

# Применяем алгоритм
new_result_array = []
max_gain = -1
for stat_values in sorted_stat_values_array:
    if stat_values.stat_gain > max_gain:
        new_result_array.append(stat_values)
        max_gain = max(max_gain, stat_values.stat_gain)

# Визуализируем новые точки
for stat_values in new_result_array:
    stat_values.plot('red')

# Соединяем точки в new_result_array ломанной линией
plt.plot([stat_values.stat_stdev for stat_values in new_result_array],
         [stat_values.stat_gain for stat_values in new_result_array],
         c='green', alpha=0.7, label='Connected Line')

plt.title('Scatter Plot от Result Array и New Result Array с ломанной линией')
plt.xlabel('Stat Stdev')
plt.ylabel('Stat Gain')
plt.grid(True)
plt.legend()
plt.show()
