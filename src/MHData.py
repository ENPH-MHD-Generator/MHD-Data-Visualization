# Author: Rylan Stutters - github.com/RylanDS7
"""Module for MHData class

MHData parses VTK files into and provides manipulation and
visualization functionality.
"""

import numpy as np
import pyvista as pv

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


    def plot_2d_colour_map(self, scalar,  cut_val, normal='z'):
        """Plots 2D colour map cross-section for the specified scalar value.

        Args:
            scalar (str): label for scalar value to plot
            cut_val (float): value of the normal to cut along
            normal (literal): normal direction to take cross-section from: 'x','y','z'
        """

        cut_mesh = self.data.slice(normal=normal, origin={
            'x': (cut_val, 0, 0),
            'y': (0, cut_val, 0),
            'z': (0, 0, cut_val),
        }[normal])
        cut_mesh.set_active_scalars(scalar)

        self.plotter.add_mesh(cut_mesh, show_edges=True)



