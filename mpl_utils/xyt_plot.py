"""Produce an XYT plot"""

import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


def xyt_plot(x, y, *, t=None, **kwargs):
    """Plots an x-y series, colored to show time

    Args:
        x (numpy array): X data series
        y (numpy array): Y data series

        t (numpy array): Time stamps, or None to simply use % of
            trajectory length

    Returns:
        (pyploy.cm.ScalarMappable): A ScalarMappable object that can be
            passed to pyplot.colorbar() to produce a colorbar over the
            trajectory time stamps
    """

    ax = plt.gca()

    # Time variable
    t = t if t is not None else np.linspace(0, 1, x.shape[0])

    # Set up a list of (x,y) points
    points = np.array([x, y]).transpose().reshape(-1, 1, 2)

    # Set up a list of segments
    segs = np.concatenate([points[:-1], points[1:]], axis=1)

    # Make the collection of segments
    lc = LineCollection(segs, cmap=plt.get_cmap(), **kwargs)
    lc.set_array(t)

    # plot the collection
    ax.add_collection(lc)

    # We have to manually adjust the axes, as ax.add_collection doesn't do it
    # automatically
    plt.xlim(math.floor(x.min()), math.ceil(x.max()))
    plt.ylim(math.floor(y.min()), math.ceil(y.max()))

    # Compute scalarmappable for colorbar
    sm = plt.cm.ScalarMappable(
        cmap=plt.get_cmap(),
        norm=plt.Normalize(vmin=np.min(t), vmax=np.max(t))
    )
    sm._A = []

    return sm


def demo():
    """Demo the xyt plot"""

    # Plot a fun spiral trajectory
    t = np.arange(0, 1, 0.001)
    x = np.sin(t * 10*2*np.pi) * t/2 + t/4
    y = np.cos(t * 10*2*np.pi) * t/2

    plt.figure()
    cm = xyt_plot(x, y)
    cb = plt.colorbar(cm, pad=0.005)
    cb.ax.set_title('Time (s)')
    plt.axis("square")
    plt.grid()
    plt.title("Spiral Trajectory")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
