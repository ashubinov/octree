from node import Node
from octree import Octree
from visualizer import Visual


root_sphere = Node([-5, -5, -5], [5, 5, 5], 0)

octree_sphere = Octree(root_sphere, 'sphere', i_max=6)

center = [1, 0, 0]
radius = 4

octree_sphere.build_octree(
    root_sphere,
    center=center,
    radius=radius
)


volume_1 = octree_sphere.calculate_volume(root_sphere, root_sphere.get_volume())
print(volume_1)


cells_sphere = octree_sphere.get_visualization_data()

visualizer_sphere = Visual(
    cells_sphere[0],
    cells_sphere[1],
    cells_sphere[2],
    center=center,
    radius=radius
)

visualizer_sphere.show_sphere()