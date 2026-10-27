from src.MHData import MHData

data_dir = "examples\example_data\linear-hall_8e-05.vtk"
mhd = MHData(data_dir)

print(mhd.scalar_values())
print(mhd.vector_values())
print(mhd.mesh_bounds())
print(mhd.mesh_centre())

mhd.plot()
mhd.plot_2d_colour_map('Potential', mhd.mesh_centre()[2])
mhd.show()

# mhd.save_fig("./test_fig.png", fig_title="Potential")
mhd.plot_all_scalar_slices("./examples/test2_fig.pdf", mhd.mesh_centre()[2])
