from node import Node
from octree import Octree
from visualizer import Visual

root_box = Node([0, 0, 0], [10, 10, 10], 0)
root_box_2 = Node([0, 0, 0], [10, 10, 10], 0)

octree_box = Octree(root_box, 'box', i_max=8)
octree_box_2 = Octree(root_box_2, 'sphere', i_max=8)

obj_min = [1, 1, 1]
obj_max = [6, 6, 6]
obj_min_2 = [6, 6, 6]
obj_max_2 = 3

octree_box.build_octree(
    root_box,
    obj_min=obj_min,
    obj_max=obj_max

)

octree_box_2.build_octree(
    root_box_2,
    center=obj_min_2,
    radius=obj_max_2
)

volume_1 = octree_box.calculate_volume(root_box, root_box.get_volume())
print(volume_1)
volume_2 = octree_box_2.calculate_volume(root_box_2, root_box_2.get_volume())
print(volume_2)

result_octree = octree_box_2.boolean_operation(octree_box, 'difference')

volume_3 = result_octree.calculate_volume(result_octree.root, result_octree.root.get_volume())
print(volume_3)

cells_box = octree_box.get_visualization_data()
cells_box_2 = octree_box_2.get_visualization_data()
cells_box_3 = result_octree.get_visualization_data()


visualizer_box = Visual(
    [cells_box[0], cells_box_2[0]],
    [cells_box[1], cells_box_2[1]],
    [cells_box[2], cells_box_2[2]],
    objects = [
        {
            'type': 'box',
            'obj_min': obj_min,
            'obj_max': obj_max
        },
        {
            'type': 'sphere',
            'center': obj_min_2,
            'radius': obj_max_2
        }

    ]
)

visualizer_box_1 = Visual(
    [cells_box_3[0]],
    [cells_box_3[1]],
    [cells_box_3[2]],
)

visualizer_box.show()
visualizer_box_1.show_result()


            
