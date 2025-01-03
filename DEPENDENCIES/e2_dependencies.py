import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable



def add_colorbar(fig, ax, label="", image=[], cmap_norm=[]):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.1)
    if image: 
        cbar = fig.colorbar(image, cax=cax)
    elif cmap_norm: 
        cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap_norm[0], norm=cmap_norm[1]), cax=cax)
    cbar.set_label(label, rotation=90, fontsize=10, labelpad=10)

    
def set_figure(ax):
    ax.set_xlabel("distance [km]")
    ax.set_ylabel("depth [km]")
    ax.set_xlim([0, 13])
    ax.set_ylim([11, 0])
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(0, 14, 2))
    
def plot_path_arrows(ax, color='black', range=[0, 19]):
    for i in np.arange(range[0], range[1]+1):
        if i <= 9:
            ax.arrow(0, i+2, i+2, -(i+2), length_includes_head=True, lw=0.5, head_width=0.3, facecolor=color, edgecolor=color)
        elif i > 9 and i <= 19:
            ax.arrow(13, 21-i, -(21-i), -(21-i), length_includes_head=True, lw=0.5, head_width=0.3, facecolor=color, edgecolor=color)
        else:
            print("range values out of range")
        
def plot_stations(ax, color='black', values=[]):
    
    if len(values) == 0:
        for i in np.arange(0, 10):
            ax.add_patch(Rectangle((i-0.2+2, 0), 0.4, -0.5, clip_on=False, facecolor=color, edgecolor=color))
    elif len(values) == 10:
        norm = mcolors.Normalize(vmin=np.min(values), vmax=np.max(values))      # Create colormap to use with values, if given
        cmap = plt.cm.get_cmap('viridis')
        for i in np.arange(0, 10):
            ax.add_patch(Rectangle((i-0.2+2, 0), 0.4, -0.5, clip_on=False, facecolor=cmap(norm(values[i])), edgecolor=color))
        return cmap, norm
    else:
        raise("Variable values must have exactly 10 elements.")
            
    
        
def plot_grid(ax, color='lightgrey', linewidth=0.5, alpha=0.8):
    for i in np.arange(1, 13):
        ax.plot([i, i], [11, 0], color=color, alpha=alpha, linewidth=linewidth)
        
    for i in np.arange(1, 12):
        ax.plot([0, 13], [i, i], color=color, alpha=alpha, linewidth=linewidth)