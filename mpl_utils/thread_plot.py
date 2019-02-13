"""Produce a matrix thread plot"""

import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import colors

def thread_plot(
        mat,
        *,
        peak_size=1,
        x_extra=0.75,
        color='tab:blue',
        **kwargs
):
    """Plots rows of a matrix as stacked interpolated line plots

    Args:
        mat (numpy array): Matrix to plot

        peak_size (float): Number of rows a the largest matrix entry should
            vertically span
        x_extra (float): Extra horizontal padding at the left and right of
            each row
        color (matplotlib color): Color to draw lines. A value of None will
            use automatic colring
    """

    # Get axis handle
    ax = plt.gcf().gca()

    # Measure matrix dimensions
    rows, cols = mat.shape

    # Normalize matrix values
    mat = mat.copy() / np.amax(np.abs(mat)) * peak_size

    # Draw grid lines
    ax.set_xticks([])
    #ax.set_xticks(np.arange(1, cols+1, 1))
    ax.set_yticks(np.arange(1, rows+1, 1))
    ax.grid(True)

    # Hide ticks and labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)

    # Hide frame border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Up-sampled x axis points
    x_fine = np.arange(1-x_extra, cols+x_extra, 0.1)

    # Loop over matrix rows
    for row in range(rows):

        # Find color adjustment for this row
        row_color = None
        if color is not None:
            color_adjust = row / (rows - 1) * 0.5 + 1
            row_color = np.array(colors.to_rgb(color)) * color_adjust
            row_color = tuple((
                max(min(c, 1), 0) for c in row_color
            ))

        # Find y-val for this row
        y_val = rows - row

        # Expand row width a bit
        x = np.concatenate((
            [1-x_extra],
            np.arange(1, cols+1, 1),
            [cols+x_extra]
        ))
        y = y_val + np.concatenate((
            [0],
            np.array(mat[row, :]),
            [0]
        ))

        # Interpolate row curve
        y_fine = interp1d(
            x,
            y,
            kind=2,
            fill_value=0,
            bounds_error=False
        )(x_fine)

        # Plot the row
        plt.plot(
            x_fine,
            y_fine,
            color=row_color,
            **kwargs
        )

    # Set square axis
    plt.axis("square")

    # Set x limits
    plt.xlim((0, cols+1))


if __name__ == "__main__":
    """Demo the thread plot"""

    # Plot identity matrix
    plt.figure()
    size = 10
    thread_plot(np.eye(size))
    plt.title(r"Identity Matrix $I_{10}$")
    plt.tight_layout()
    plt.show()

    # Plot random normal matrix
    plt.figure()
    size = 20
    plt.title(r"Random Normal Matrix $\mathcal{N}_{20}(0, 1)$")
    thread_plot(
        np.random.normal(size=(size, size)),
        color=None
    )
    plt.tight_layout()
    plt.show()

    # Plot some rotation matrices
    plt.figure()

    plt.subplot(1, 3, 1)
    roll = pitch = yaw = np.deg2rad(45)
    thread_plot(
        np.array([
            [1, 0, 0],
            [0, np.cos(roll), np.sin(roll)],
            [0, -np.sin(roll), np.cos(roll)]
        ]),
        color='C1'
    )
    plt.ylim((0, 5))
    plt.title(r"$R_x(\alpha=45°)$")

    plt.subplot(1, 3, 2)
    thread_plot(
        np.array([
            [np.cos(pitch), 0, -np.sin(pitch)],
            [0, 1, 0],
            [np.sin(pitch), 0, np.cos(pitch)]
        ]),
        color='C2'
    )
    plt.ylim((0, 5))
    plt.title(r"$R_y(\beta=45°)$")

    plt.subplot(1, 3, 3)
    thread_plot(
        np.array([
            [np.cos(yaw), np.sin(yaw), 0],
            [-np.sin(yaw), np.cos(roll), 0],
            [0, 0, 1]
        ]),
        color='C3'
    )
    plt.ylim((0, 5))
    plt.title(r"$R_z(\gamma=45°)$")

    plt.suptitle("Rotation Matrices")
    plt.tight_layout()
    plt.show()
