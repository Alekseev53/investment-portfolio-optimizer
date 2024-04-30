import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

def generate_data(steps, disp, last_n_elem=1000,interest_rate=0.4):
    last_n_elem = int(last_n_elem)
    last  = 0.0
    while last <= 0.0:
        data = []
        for _ in range(steps):
            random_step = np.random.uniform(-1, 1)
            step_size = disp * random_step + 1 + interest_rate/ 365 + disp / 365
            last_step = data[-1] if len(data) > 0 else 1
            data.append(last_step * step_size)
        last = data[-1]
    return data

def plot(steps=1000, disp=0.05):
    data = generate_data(steps, disp)
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.show()
   
interact(plot, disp=(0.01, 0.1, 0.01))



from ipywidgets import interact, IntSlider
import ipywidgets
import matplotlib.pyplot as plt
import numpy as np

def generate_data(steps, disp, last_n_elem=1000,interest_rate=0.4):
    last_n_elem = int(last_n_elem)
    last  = 0.0
    while last <= 0.0:
        data = []
        for _ in range(steps):
            random_step = np.random.uniform(-1, 1)
            step_size = disp * random_step + 1 + interest_rate/ 365 + disp / 365
            last_step = data[-1] if len(data) > 0 else 1
            data.append(last_step * step_size)
        last = data[-1]
    return data




def plot_multiple_datasets(N=5, steps=1000, disp=0.05, interest_rate=0.04):
    last_values = []
    plt.figure(figsize=(10, 5))

    for i in range(N):
        data = generate_data(steps, disp, interest_rate)
        plt.plot(data, label="Data {}".format(i+1))
        last_values.append(data[-1])
    
    min_val = min(last_values)
    max_val = max(last_values)
    avg_val = sum(last_values)/len(last_values)
    median_val = np.median(last_values)
    
    plt.scatter([steps]*4, [min_val, max_val, avg_val, median_val], color=['red', 'blue', 'green', 'purple'])
    plt.text(steps, min_val, 'Min: {:.2f}'.format(min_val), fontsize=10, verticalalignment='bottom')
    plt.text(steps, max_val, 'Max: {:.2f}'.format(max_val), fontsize=10, verticalalignment='top')
    plt.text(steps, avg_val, 'Avg: {:.2f}'.format(avg_val), fontsize=10, verticalalignment='bottom')
    plt.text(steps, median_val, 'Median: {:.2f}'.format(median_val), fontsize=10, verticalalignment='top')

    plt.show()

N_widget = IntSlider(min=1, max=200, step=1, value=5)
steps_widget = IntSlider(min=100, max=5000, step=100, value=1000)
disp_widget = ipywidgets.FloatSlider(min=0.01, max=0.1, step=0.001, value=0.05)
interest_rate_widget = ipywidgets.FloatSlider(min=-0.01, max=0.16, step=0.01, value=0.04)

interact(plot_multiple_datasets, 
         N=N_widget, 
         steps=steps_widget, 
         disp=disp_widget,  
         interest_rate=interest_rate_widget)


from ipywidgets import interact, IntSlider
import ipywidgets
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from math import log10

def generate_data(steps, disp, last_n_elem=1000,interest_rate=0.4):
    last  = 1.0
    for _ in range(steps):
        random_step = np.random.uniform(-1, 1)
        step_size = disp * random_step + 1 + interest_rate/ 365 #+ disp / 365
        last = last * step_size
    return last



def plot_multiple_datasets(N=5, steps=1000, disp=0.05, interest_rate=0.04):
    last_values = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [executor.submit(generate_data, steps, disp, interest_rate) for _ in range(N)]

    last_values = [task.result() for task in tasks]

    # for i in range(N):
    #     last = generate_data(steps, disp, interest_rate)
    #     last_values.append(last)

    max_val = max(last_values)
    avg_val = sum(last_values)/len(last_values)
    median_val = np.median(last_values)
    var_val = np.var(last_values, ddof=1)

    # plot histogram
    plt.hist(last_values, density=True, color='c', alpha=0.7,bins=N//(round(log10(N)+10)))
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    plt.axvline(max_val, color='blue', linestyle='dashed', linewidth=2)
    plt.axvline(avg_val, color='green', linestyle='dashed', linewidth=2)
    plt.axvline(median_val, color='purple', linestyle='dashed', linewidth=2)

    # add dummy plots for legend entries
    plt.plot([], [], ' ', label="Max: {:.2f}".format(max_val))
    plt.plot([], [], ' ', label="Avg: {:.2f}".format(avg_val))
    plt.plot([], [], ' ', label="Median: {:.2f}".format(median_val))
    plt.plot([], [], ' ', label="Variance: {:.2f}".format(var_val))

    # show legend
    plt.legend()

    plt.xlabel(f'Value {N},{steps},{round(disp,2)},{interest_rate}')
    plt.ylabel('Frequency')
    plt.title('Histogram with statistics')
    plt.show()

N_widget = IntSlider(min=1, max=200000, step=1, value=2000)
steps_widget = IntSlider(min=1, max=5000, step=1, value=365)
disp_widget = ipywidgets.FloatSlider(min=0.01, max=0.4, step=0.001, value=0.05)
interest_rate_widget = ipywidgets.FloatSlider(min=-0.01, max=0.16, step=0.01, value=0.0)

interact(plot_multiple_datasets, 
         N=N_widget, 
         steps=steps_widget, 
         disp=disp_widget,  
         interest_rate=interest_rate_widget)