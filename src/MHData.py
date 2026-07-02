# Author: Rylan Stutters - github.com/RylanDS7
"""Module for MHData class

MHData parses VTK files into and provides manipulation and
visualization functionality.
"""

import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class MHData:
    """Class for parsing and plotting VTK files from MHD simulations.

    This class contains methods for plotting, manipulating, and
    visualizing VTK data. It also allows for direct access to scalar
    and vector quantities defined on the mesh, including calculated values.

    """
    def __init__(self, data_file):
        """Initializes the MHData object

        Args:
            data_file (string): Path to the MHD simulation file.
        """
        if not data_file.lower().endswith('.vtk'):
            raise ValueError(f"MHData requires a VTK file, got: '{data_file}'")

        self.data = pv.read(data_file)
        self.plotter = pv.Plotter()


    def scalar_values(self):
        """Retrieves scalar values defined on the mesh.

        Returns:
            Dictionary containing list[str] of scalar variables defined
            at the mesh points and cells. Expected keys:
            'point', 'cell'
        """
        point_scalars = [
            name for name, array in self.data.point_data.items()
            if array.ndim == 1
        ]

        cell_scalars = [
            name for name, array in self.data.cell_data.items()
            if array.ndim == 1
        ]

        return {'point': point_scalars, 'cell': cell_scalars}


    def vector_values(self):
        """Retrieves vector values defined on the mesh.

        Returns:
            Dictionary containing list[str] of vector variables defined
            at the mesh points and cells. Expected keys:
            'point', 'cell'
        """
        point_vectors = [
            name for name, array in self.data.point_data.items()
            if array.ndim == 2 and array.shape[1] == 3
        ]

        cell_vectors = [
            name for name, array in self.data.cell_data.items()
            if array.ndim == 2 and array.shape[1] == 3
        ]

        return {'point': point_vectors, 'cell': cell_vectors}


    def mesh_bounds(self):
        """Retrieves the coordinate bounds of the mesh.

        Returns:
            tuple[float]: mesh bounds structured
                [x_min, x_max, y_min, y_max, z_min, z_max]
        """
        return self.data.bounds


    def mesh_centre(self):
        """Retrieves the coordinates of the mesh centre.

        Returns:
            list[float]: xyz coordinates of the mesh centre
        """
        return self.data.center


    def plot(self):
        """Create a new plotter object

        """
        self.plotter = pv.Plotter()


    def show(self):
        """Show MHData plot

        """
        self.plotter.show()


    def save_fig(self, filename, fig_title=None):
        """Save MHData plot as figure

        Args:
            filename (str): path and filename to save figure to
            fig_title (str): title to display on figure
        """
        self.plotter.add_text(fig_title, position='upper_edge', color='black', font_size=12)
        self.plotter.screenshot(filename)


    def plot_2d_colour_map(self, scalar,  cut_val, normal='z'):
        """Plots 2D colour map cross-section for the specified scalar value.

        Args:
            scalar (str): label for scalar value to plot
            cut_val (float): value of the normal to cut along
            normal (literal): normal direction to take cross-section from: 'x','y','z'
        """
        self.plot()

        cut_mesh = self.data.slice(normal=normal, origin={
            'x': (cut_val, 0, 0),
            'y': (0, cut_val, 0),
            'z': (0, 0, cut_val),
        }[normal])
        cut_mesh.set_active_scalars(scalar)

        self.plotter.add_mesh(cut_mesh, show_edges=True, show_scalar_bar=False)
        self.plotter.add_scalar_bar(title=scalar, height=0.9, position_x=0.9, vertical=True)

        self.plotter.camera_position = {
            'x': 'yz',
            'y': 'xz',
            'z': 'xy',
        }[normal]

        self.plotter.camera.tight(padding=0.4)


    def plot_all_scalar_slices(self, filename, cut_val, normal='z'):
        """Plots 2D colour map cross-sections for all scalars available for
        plotting on the mesh. Results are saved into a single pdf

        Args:
            filename (str): path and filename to save figure to. Must be .pdf file
            cut_val (float): value of the normal to cut along
            normal (literal): normal direction to take cross-section from: 'x','y','z'
        """

        with PdfPages(filename) as pdf:
            for scalar in self.scalar_values()['point']:
                self.plot_2d_colour_map(scalar, cut_val, normal)

                self.plotter.add_text(scalar, position='upper_edge', color='black', font_size=12)
                figure = self.plotter.screenshot(filename=None)

                fig, ax = plt.subplots(figsize=(8, 6))

                ax.imshow(figure)
                ax.axis('off')

                pdf.savefig(fig)
                plt.close(fig)




