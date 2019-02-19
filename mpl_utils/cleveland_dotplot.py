"""Produce a Cleveland dot plot"""

from matplotlib import pyplot as plt
import pandas as pd


def cleveland_dotplot(df, x, bars=None, *, category=None, right_label=None):
    """Produce a Cleveland dot plot from a DataFrame

    Cleveland dot plots are a dot plot of categorical variable observations
    showing some range for each observation (e.g. standard deviation). See
    https://uc-r.github.io/cleveland-dot-plots for an example.

    Args:
        df (pandas.DataFrame): DataFrame to plot
        x (string): Column to use for dot locations
        bars (string): Column to use for dot bars

        category (string): Optional category column
        right_label (string): Optional column to use as right y labels
    """

    def get_mpl_colors(ax):
        """Get a list of the curent Matplotlib color scheme's colors
        """
        cycle = ax._get_lines.prop_cycler
        first = next(cycle)
        result = [first]
        for current in cycle:
            if current == first:
                break
            result.append(current)

        # Reset iterator state:
        for current in cycle:
            if current == result[-1]:
                break
        return [kv["color"] for kv in result]

    # Get axis and current set of colors
    ax = plt.gca()
    colorset = get_mpl_colors(ax)

    # Add a column for the y coords
    df["_y_coord"] = pd.Series(range(len(df), 0, -1), index=df.index)

    y_tick_labels = []
    y_tick_labels_right = []
    if category is not None:
        for cat_id, thing in enumerate(df.groupby(category)):
            cat, _df = thing
            y_tick_labels += _df.index.tolist()
            if right_label is not None:
                y_tick_labels_right += [
                    _df[right_label][i] for i in _df.index.tolist()
                ]
            plt.errorbar(
                _df[x].tolist(),
                _df["_y_coord"].tolist(),
                xerr=_df[bars].tolist(),
                marker="o",
                color=colorset[cat_id],
                linestyle='',
                elinewidth=0.75,
                label=cat
            )
    else:
        y_tick_labels += df.index.tolist()
        if right_label is not None:
            y_tick_labels_right += [
                df[right_label][i] for i in df.index.tolist()
            ]
        plt.errorbar(
            df[x].tolist(),
            df["_y_coord"].tolist(),
            xerr=df[bars].tolist(),
            marker="o",
            color=colorset[0],
            linestyle='',
            elinewidth=0.75,
            label=x
        )

    # Configure labels
    plt.xlabel(x)
    ax.set_yticks(df["_y_coord"].tolist())
    ax.set_yticklabels(y_tick_labels, {"size": 6})
    plt.tick_params(axis="y", length=0)

    # Add optional right axis labels
    if right_label is not None:
        ax2 = plt.gca().twinx()
        plt.ylim(ax.get_ylim())
        ax2.set_yticks(df["_y_coord"].tolist())
        ax2.set_yticklabels(y_tick_labels_right, {"size": 6})
        plt.tick_params(axis="y", length=0)

    # Show categorical variable gridlines
    ax.set_axisbelow(True)
    ax.grid(color="#eeeeee")

    if category is not None:
        # Add legend
        ax.legend()


def demo():
    """Demo the Cleveland dotplot"""

    print(f"Demonstration of {cleveland_dotplot.__name__}")

    # Load the autompg dataset from UCI Machine Learning Repository
    autompg_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
    print(f"Downloading autompg dataset from {autompg_url}")
    autompg = pd.read_csv(
        autompg_url,
        sep='\s+',
        header=None,
        names=[
            "mpg",
            "cylinders",
            "displacement",
            "horsepower",
            "weight",
            "acceleration",
            "modelyear",
            "origin",
            "carname"
        ]
    )

    # Keep only mpg and modelyear columns
    autompg = autompg[["mpg", "modelyear"]]

    # Collapse over modelyear
    autompg = pd.concat((
        autompg.groupby("modelyear").mean().rename(
            lambda x: "{}_mean".format(x), axis=1
        ),
        autompg.groupby("modelyear").std().rename(
            lambda x: "{}_std".format(x), axis=1
        ),
    ), axis=1)

    # Sort by modelyear
    autompg = autompg.sort_values("modelyear")

    # Prettify the years
    autompg.index = "19" + autompg.index.astype(str)

    # Show the data
    with pd.option_context(
            'display.max_rows',
            None,
            'display.max_columns',
            None
    ):
        print(autompg)

    # Plot with a cleveland dotplot
    plt.figure()
    cleveland_dotplot(
        autompg,
        "mpg_mean",
        "mpg_std",
    )
    plt.title("Auto MPG Dataset")
    plt.xlabel("Miles Per Gallon")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
