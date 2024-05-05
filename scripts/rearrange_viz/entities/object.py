import os
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image

from .constants import category_color_map, object_category_map


class Object:
    """
    Represents an object in a 2D space and provides methods for plotting it.
    """

    def __init__(self, config, object_id, icon_path=None):
        """
        Initializes an Object instance.

        Parameters:
            config (object): A configuration object containing parameters for object rendering.
            object_id (str): Identifier for the object.
            icon_path (str, optional): Path to the icon image file representing the object.
                                       Defaults to None.
        """
        self.object_id = object_id
        self.icon_path = icon_path
        self.config = config.object
        self.center_position = None

    @property
    def width(self):
        """
        Width of the object.

        Returns:
            float: Width of the object.
        """
        return self.config.width

    @property
    def height(self):
        """
        Height of the object.

        Returns:
            float: Height of the object.
        """
        return self.config.height

    def plot(self, ax=None, position=(0, 0)):
        """
        Plots the object on a matplotlib Axes.

        Parameters:
            ax (matplotlib.axes.Axes, optional): Axes to plot the object on.
                                                 If None, a new figure and Axes will be created.
                                                 Defaults to None.
            position (tuple, optional): Position of the object's bottom-left corner.
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

        if self.icon_path is not None and os.path.exists(self.icon_path):
            icon = Image.open(self.icon_path)
            object_width, object_height = icon.size
            ax.imshow(
                icon,
                extent=(
                    position[0],
                    position[0] + object_width,
                    position[1],
                    position[1] + object_height,
                ),
            )
        else:
            object_rect = FancyBboxPatch(
                (position[0], position[1]),
                self.config.width,
                self.config.height,
                edgecolor="white",
                facecolor=category_color_map[
                    object_category_map[
                        "_".join(self.object_id.split("_")[:-1])
                    ]
                ],
                linewidth=0,
                linestyle="-",
                boxstyle=f"Round, pad=0, rounding_size={self.config.rounding_size}",
                alpha=1.0,
            )

            ax.add_patch(object_rect)

        self.center_position = (
            position[0] + self.config.width / 2,
            position[1] + self.config.height / 2,
        )
        text_position = (
            self.center_position[0],
            self.center_position[1] + self.config.text_margin,
        )
        wrapped_text = textwrap.fill(
            self.object_id, width=self.config.textwrap_width
        )
        ax.annotate(
            wrapped_text,
            xy=text_position,
            ha="center",
            va="top",
            fontsize=self.config.text_size,
        )

        if created_fig:
            return fig, ax
        else:
            return ax
