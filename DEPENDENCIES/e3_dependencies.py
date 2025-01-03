import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_stations(ax, x_coords, color='black'):
    
    for i in range(12):  
        ax.add_patch(Rectangle((i+x_coords[i]-50, 0), 100, 25, fc=color))
        
    ax.add_patch(Rectangle((i+x_coords[0]-50, 0), 100, 25, fc='k', label="station"))    # labeled plot object
    
    
def set_figure(ax, x0, xn):
    ax.plot([x0 - 1e3, xn + 1e3], [0, 0], '-k', lw=1)
    ax.set_xlabel("distance [m]")
    ax.set_ylabel("depth [m]")
    ax.set_xlim([x0 - 1e3, xn + 1e3])


def parabola(x_values, a, b, s):
    """Calculate the y-values of a parabola for given x-values and parameters.

    Parameters
    ----------
    x_values : array_like
        The x-values at which to calculate the y-values.
    a : float
        The coefficient of the x^2 term.
    b : float
        The coefficient of the x term.
    s : float
        The scaling factor.
    """

    return (a * x_values**2 + b * x_values) * s


def valley_parabola(n_model, x0, xn, r_std=0.25):
    
    # Generate n_model x-values evenly spaced between x0 and xn
    x_width = (xn - x0) / (n_model)
    x_values = np.linspace(x0 - 0.5*x_width, xn + 0.5*x_width, n_model+2)

    # Generate n_model y-values for the initial model depth, based on a parabola
    j = (xn-x0) / 2    # x value at the vertex of the parabola
    a = j**-2          # coefficient of the x^2 term
    b = -2/j           # coefficient of the x term
    s = -900           # scaling factor

    y_values = parabola(x_values - x0, a, b, s)    # y-values of the parabola

    # Initial model parameters
    m0 = y_values[1:-1]
    m0_x = x_values[1:-1]  
    m0_std = m0 * r_std
    
    return m0, m0_x, m0_std, x_width


def generate_column_outline(midpoints_x, midpoints_y, width):
    """
    Generate the outline of columns given the midpoints and width.
    
    Parameters:
    midpoints_x (array-like): x-coordinates of the midpoints.
    midpoints_y (array-like): y-coordinates (depths) of the midpoints.
    width (float): Width of the columns.
    
    Returns:
    tuple: Arrays of x and y coordinates for the column outlines.
    """
    x_values = []
    y_values = []
    
    half_width = width / 2
    
    x_values.append(midpoints_x[0] - half_width)
    y_values.append(0)
    
    for x, y in zip(midpoints_x, midpoints_y):
        
        x_values.append(x - half_width)
        x_values.append(x + half_width)
        y_values.append(y)
        y_values.append(y)
    
    x_values.append(midpoints_x[-1] + half_width)
    y_values.append(0)
    
    return np.array(x_values), np.array(y_values)            
    
    
def plot_valley_outline(ax, m0_x, m0, x_width, color='k', linestyle=':', label='valley outline'):
    
    x_outline, y_outline = generate_column_outline(m0_x, m0, x_width)
    ax.plot(x_outline, -y_outline, linestyle=linestyle, color=color, label=label)