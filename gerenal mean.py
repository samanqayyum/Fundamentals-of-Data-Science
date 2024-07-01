# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 11:12:15 2024

@author: HP
"""


import numpy as np
import matplotlib.pyplot as plt

# Read data from the data file
data = np.loadtxt('data9-1.csv')

# Create a probability density function (PDF) as a histogram
plt.hist(data, bins=30, density=True, alpha=0.5, color='g', edgecolor='black')

# Calculate the mean annual salary (˜W)
mean_salary = np.mean(data)


# Add a vertical line to the histogram representing the mean salary
plt.axvline(mean_salary, color='red', linestyle='dashed', linewidth=2, 
            label='Mean Salary')

# Set labels and title
plt.xlabel('Annual Salary')
plt.ylabel('Probability Density')
plt.title('Probability Density Function of Annual Salaries')

# Show legend
plt.legend()

# Show the plot
plt.show()

# Print the mean annual salary
print(f"Mean Annual Salary (˜W): {mean_salary}")



