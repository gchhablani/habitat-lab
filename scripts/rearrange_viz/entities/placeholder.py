import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


class Placeholder:
    """
    Represents a placeholder object in a 2D space and provides methods for plotting it.
    """

    def __init__(self, config):
        """
        Initializes a Placeholder instance.

        Parameters:
            config (object): A configuration object containing parameters for placeholder rendering.
        """
        self.config = config.placeholder
        self.center_position = None

    @property
    def width(self):
        """
        Width of the placeholder.

        Returns:
            float: Width of the placeholder.
        """
        return self.config.width

    @property
    def height(self):
        """
        Height of the placeholder.

        Returns:
            float: Height of the placeholder.
        """
        return self.config.height

    def plot(self, ax=None, position=(0, 0)):
        """
        Plots the placeholder on a matplotlib Axes.

        Parameters:
            ax (matplotlib.axes.Axes, optional): Axes to plot the placeholder on.
                                                 If None, a new figure and Axes will be created.
                                                 Defaults to None.
            position (tuple, optional): Position of the placeholder's bottom-left corner.
                                        Defaults to (0, 0).

        Returns:
            matplotlib.figure.Figure, matplotlib.axes.Axes or matplotlib.axes.Axes: If ax is None,
            returns the created figure and axes. Otherwise, returns the modified axes.
        """
        if ax is None:
            fig, ax = plt.subplots()
            created_fig = True
        else:
            created_fig = False

        object_rect = FancyBboxPatch(
            (position[0], position[1]),
            self.width,
            self.height,
            edgecolor="white",
            facecolor="black",
            linewidth=0,
            linestyle="-",
            boxstyle=f"Round, pad=0, rounding_size={self.config.rounding_size}",
            alpha=1.0,
        )

        ax.add_patch(object_rect)

        self.center_position = (
            position[0] + self.width / 2,
            position[1] + self.height / 2,
        )  # Update center position

        if created_fig:
            return fig, ax
        else:
            return ax
