# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 20:59:27 2024

@author: Saman Qayyum
"""

import numpy as np
import matplotlib.pyplot as plt


def read_data(file_path):
    """
    Reads data from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - data (numpy.ndarray): Array containing the data.
    """

    # Use NumPy's genfromtxt to read data from the CSV file
    data = np.genfromtxt(file_path, delimiter=',')

    return data


def calculate_bin_size(df_bin):
    """
    Use the Freedman-Diaconis rule calcualte the bin size for given data.

    Parameters
    ----------
    df_bin : numpy array
        Data for which bin size is to be calculated.

    Returns
    -------
    bin_size : int
        calculated bin size.

    """
    # Calculate bin size using Freedman-Diaconis rule:
    # Calculate Interquartile Range (IQR)
    iqr = np.percentile(df_bin, 75) - np.percentile(df_bin, 25)

    # Calculate bin width using Freedman-Diaconis rule
    binw = int(2 * iqr / (len(df_bin) ** (1/3)))

    # Calculate the number of bins using the bin width
    bins = np.ceil((max(df_bin) - min(df_bin))/binw).astype(int)

    # Print the calculated bin size
    print("bin size", bins)

    return bins


def calculate_distribution(data):
    """
    Calculates the distribution of values by binning them.

    Parameters:
    - data (numpy.ndarray): Input data.

    Returns:
    - ohist (numpy.ndarray): Numbers of entries in each bin.
    - oedge (numpy.ndarray): Bin boundaries.
    - xdst (numpy.ndarray): Bin center locations.
    - wdst (numpy.ndarray): Bin widths.
    - ydst (numpy.ndarray): Discrete Probability Distribution Function (PDF).
    - cdst (numpy.ndarray): Cumulative distribution.
    """

    # Calculate the number of bins using a helper function (calculate_bin_size)
    num_bins = calculate_bin_size(data)

    # Use NumPy's histogram function to calculate the histogram and bin edges
    ohist, oedge = np.histogram(data, bins=num_bins)

    # Calculate bin center locations
    xdst = (oedge[1:] + oedge[:-1]) / 2

    # Calculate bin widths
    wdst = oedge[1:] - oedge[:-1]

    # Calculate the Discrete Probability Distribution Function (PDF)
    ydst = ohist / np.sum(ohist)

    # Calculate the cumulative distribution
    cdst = np.cumsum(ydst)

    return ohist, oedge, xdst, wdst, ydst, cdst


def plot_distribution(xdst, ydst, wdst, cdst, xmean, xmean08, xmean12):
    """
    Plot the Probability Distribution Function (PDF) and additional \
    information.

    Parameters:
    - xdst (numpy.ndarray): Bin center locations.
    - ydst (numpy.ndarray): Discrete Probability Distribution Function (PDF).
    - wdst (numpy.ndarray): Bin widths.
    - cdst (numpy.ndarray): Cumulative distribution.
    - xmean (float): PDF Mean value of the data.
    - xmean08 (float): 0.8 times the mean value.
    - xmean12 (float): 1.2 times the mean value.
    """

    # Set up a new figure with higher dpi for better quality
    plt.figure(0, dpi=300)

    # Adjust the bar width to remove spaces between bars
    bar_width = xdst[1] - xdst[0]

    # Plot the PDF using a bar plot
    plt.bar(xdst, ydst, width=bar_width, align='edge',
            color='darkgreen', edgecolor='white')

    # Plot a vertical line at the mean value and display mean value to plot
    plt.plot([xmean, xmean], [0.0, max(ydst)], c='darkred')
    text = ''' PDF Mean(W̄): {}'''.format(xmean.astype(float))
    plt.text(x=100000, y=max(ydst) - 0.003, s=text,
             fontsize=10, c='darkred')

   # Highlight the range between 0.8 times and 1.2 times the mean value
    hdst = ydst * ((xdst >= xmean08) & (xdst <= xmean12))
    plt.bar(xdst, hdst, width=bar_width, align='edge', color='peru',
            edgecolor='None', alpha=0.7)

    # display the fraction of the population of specified range
    # in graph
    hsum = (np.sum(hdst)*100.0).round()
    text = ''' {}% of population is with salaries between 0.8W̄ and 1.2W̄'''\
        .format(
            hsum.astype(float))
    plt.text(x=-0.5, y=max(ydst) + 0.002, s=text, fontsize=10.4, c='black')

    # Print the percentage of population with salaries in given range on plot
    print('Fraction of population with salaries between 0.8W̄ and 1.2W̄ =', hsum)

    # display the mean*0.8 value on plot
    text08 = ''' Mean*0.8: {}'''.format(xmean08.astype(float))
    plt.text(x=100000, y=max(ydst) - 0.0075, s=text08, fontsize=10,
             c='darkgreen')

    # display the mean*1.2  value on plot
    text125 = ''' Mean*1.2: {}'''.format(xmean12.astype(float))
    plt.text(x=100000, y=max(ydst) - 0.0123, s=text125, fontsize=10,
             c='peru')

    # Add title and labels to the plot
    plt.title('Probability Distribution Function (PDF)', fontsize=14,
              fontweight='bold', c='darkred', x=0.5, y=1.01)
    plt.xlabel('Salaries (Euros)', fontsize=10)
    plt.ylabel('Probability', fontsize=10)

    # Set y-axis limits for better visualization
    plt.ylim(0, 1.1 * max(ydst))

    # Add legend manually
    plt.legend(['Mean Value (W̄)', 'PDF', '0.8W̄ to 1.2W̄  Range'],
               loc='center right', fontsize=9, frameon=False,
               bbox_to_anchor=(0.99, 0.2))

    # Save the plot as png
    plt.savefig("PDF.png")

    # Show the plot
    plt.show()

    return xdst, ydst, wdst, cdst, xmean, xmean08, xmean12


def main():
    """
    Main function to analyze and visualize salary distribution.

    Returns
    -------
    None.
    """

    # File path for the data
    file_path = 'data9-1.csv'

    # Read data from the CSV file
    data = read_data(file_path)

    # Calculate the distribution of values
    ohist, oedge, xdst, wdst, ydst, cdst = calculate_distribution(data)

    # PDF Mean annual salary of the population
    xmean = np.sum(xdst * ydst).round(2)

    # print both the mean and pdf mean of salaries
    print('PDF Mean Annual Salary =', xmean)
    print('Mean Annual Salary =', data.mean().round(2))

    # Calculate mean value*0.8 and mean value*1.2
    xmean08 = (xmean * 0.8).round(2)
    xmean12 = (xmean * 1.2).round(2)

    # Plot the Probability Distribution Function (PDF) and additional
    # information
    plot_distribution(xdst, ydst, wdst, cdst, xmean, xmean08, xmean12)


if __name__ == "__main__":
    main()
