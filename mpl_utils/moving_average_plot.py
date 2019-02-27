"""Produce a moving average plot"""

import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import colors


def moving_average(x, w):
    """Running mean filter over a signal

    Args:
        x (numpy array): Signal to filter
        w (int): Window size <= len(x)

    Returns:
        (numpy array): Signal after moving average
    """
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[w:] - cumsum[:-w]) / float(w)


def moving_average_plot(
        x,
        y,
        *,
        w=None,
        **kwargs
):
    """Plots the moving average of a signal

    Args:
        x (numpy array): x-axis points
        y (numpy array): y-axis points

        w (int): Size of moving average window <= len(x). If not provided, 5%
            of the length of the signal vector is used.
    """

    # Get axis handle
    ax = plt.gcf().gca()

    if w is None:
        w = int(len(x) * 0.05)

    y_filtered = np.array(
        [np.nan] * (w - 1) +
        list(moving_average(y, w))
    )

    # Plot the row
    plt.plot(
        x,
        y_filtered,
        **kwargs
    )


def demo():
    """Demo the moving average plot"""

    print(f"Demonstration of {moving_average_plot.__name__}")

    # Prepare a very noisy signal for plotting
    num_pts = 10000
    x = np.arange(num_pts)
    y = (
        3 * x / num_pts +
        0.75 * np.sin(3 * x / num_pts * 2 * np.pi) +
        3 * np.random.normal(size=num_pts)
    )

    plt.figure()

    plt.plot(
        x,
        y,
        color='tab:blue',
        alpha=0.25,
        lw=0.5,
        label="y"
    )

    for window, color in zip((50, 500), ('tab:orange', 'tab:green')):

        moving_average_plot(
            x,
            y,
            w=window,
            color=color,
            lw=0.5,
            label=f"$y_{{{window}}}$"
        )

    plt.xlim((0, num_pts))
    plt.title("Moving average filter demo")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
