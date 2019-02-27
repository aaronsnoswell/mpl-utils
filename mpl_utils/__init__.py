
# Load modules so we can collect demonstration functions
import mpl_utils.thread_plot
import mpl_utils.xyt_plot
import mpl_utils.cleaveland_dotplot
import mpl_utils.moving_average_plot

demos = {
    "thread_plot": thread_plot.demo,
    "xyt_plot": xyt_plot.demo,
    "cleveland_dotplot": cleveland_dotplot.demo,
    "moving_average_plot": moving_average_plot.demo
}

from mpl_utils.thread_plot import thread_plot
from mpl_utils.xyt_plot import xyt_plot
from mpl_utils.cleveland_dotplot import cleveland_dotplot
from mpl_utils.moving_average_plot import moving_average, moving_average_plot

# Don't include demos if the user does global import
__all__ = [
    "thread_plot",
    "xyt_plot",
    "cleveland_dotplot",
    "moving_average",
    "moving_average_plot",
]
