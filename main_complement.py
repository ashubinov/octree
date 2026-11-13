
from node import Node
from octree import Octree
from visualizer import Visual

root_box = Node([0, 0, 0], [10, 10, 10], 0)

octree_box = Octree(root_box, 'box', i_max=4)

obj_min = [6, 6, 6]
obj_max = [11, 11, 11]

octree_box.build_octree(
    root_box,
    obj_min=obj_min,
    obj_max=obj_max
)

# Объём исходного объекта
volume_1 = octree_box.calculate_volume(
    root_box,
    root_box.get_volume()
)
print('Объём исходного объекта:', volume_1)

# Дополнение октодерева
complement_octree = octree_box.complement()

print('Статусы дополнения:', complement_octree.count_status())

volume_2 = complement_octree.calculate_volume(
    complement_octree.root,
    complement_octree.root.get_volume()
)
print('Объём дополнения:', volume_2)

# Данные исходного октодерева
cells_box = octree_box.get_visualization_data()

# Данные дополненного октодерева
cells_complement = complement_octree.get_visualization_data()

# Визуализация исходного объекта
visualizer_box = Visual(
    [cells_box[0]],
    [cells_box[1]],
    [cells_box[2]],
    objects=[
        {
            'type': 'box',
            'obj_min': obj_min,
            'obj_max': obj_max
        }
    ]
)

visualizer_complement = Visual(
    [cells_complement[0]],
    [cells_complement[1]],
    [cells_complement[2]],
    objects=[
        {
            'type': 'box',
            'obj_min': obj_min,
            'obj_max': obj_max
        }
    ]
)

visualizer_box.show()
visualizer_complement.show()
