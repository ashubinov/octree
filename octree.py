from vtkmodules.util.functions import volume
from boolean_operation import apply_boolean_operation
from node import Node

class Octree:
    def __init__(self, root, type_obj, i_max = None, delta = None):
        self.root = root
        self.type_obj = type_obj
        self.i_max = i_max
        self.delta = delta

    def build_octree(self, node, obj_min=None, obj_max=None, center=None, radius=None):

        if self.type_obj == 'box':
            status = node.determine_state(obj_min, obj_max)

        elif self.type_obj == 'sphere':
            status = node.determine_state_sphere(center, radius)

        else:
            raise ValueError("Неизвестный тип объекта")

        if status != 'PARTIAL':
            return

        size = node.get_size()

        depth_limit = (
                self.i_max is not None
                and node.deep >= self.i_max
        )

        size_limit = (
                self.delta is not None
                and min(size) <= self.delta
        )

        if depth_limit or size_limit:
            return

        node.subdivide()

        for child in node.children:
            self.build_octree(
                child, obj_min, obj_max, center, radius
            )

    def count_nodes(self, node=None):
        if node is None:
            node = self.root
        children = node.children
        return 1 + sum(self.count_nodes(child) for child in children)

    def count_status(self):
        result = {
            'EMPTY': 0,
            'FULL': 0,
            'PARTIAL': 0
        }

        def count_recursive(node):
            if not node.is_leaf():
                for child in node.children:
                    count_recursive(child)
            else:
                result[node.status] += 1

        count_recursive(self.root)
        return result

    def get_model_cells(self):
        cells = []
        self.collect_cells(self.root, cells)
        return cells

    def collect_cells(self, node, cells: list):
        if node.status == 'FULL' or (node.status == 'PARTIAL' and node.is_leaf() == True):
            cells.append(node)
            return cells

        for child in node.children:
            self.collect_cells(child, cells)
        return cells

    def get_visualization_data(self):
        points = []
        cells_data = []
        depths = []
        cells = self.get_model_cells()
        for cell in cells:
            vertices = cell.get_vertices()
            start_index = len(points)
            points.extend(vertices)

            order = [0, 4, 6, 2, 1, 5, 7, 3]
            cell_indices = [8] + [start_index + i for i in order]

            cells_data.append(cell_indices)
            depths.append(cell.deep)

        return points, cells_data, depths

    def calculate_volume(self, node, V_0):

        if node.status == 'EMPTY':
            return 0
        elif node.status == 'FULL':
            return V_0 / 8**node.deep

        else:
            if node.is_leaf():
                return V_0 / 8**node.deep
            else:
                v = 0
                for child in node.children:
                    v += self.calculate_volume(child, V_0)
                return v

    def boolean_operation(self, tree_2, operation):
        if (self.root.min_cord != tree_2.root.min_cord or
                self.root.max_cord != tree_2.root.max_cord):
            raise ValueError("Деревья должны иметь одинаковые границы")

        obj_min = self.root.min_cord
        obj_max = self.root.max_cord
        result_root = Node(obj_min, obj_max, 0)
        self._boolean_operation_recursive(self.root, tree_2.root, result_root, operation)
        return Octree(result_root, None, self.i_max, self.delta)

    def _boolean_operation_recursive(self, node_1, node_2, result, operation):

        if node_1.is_leaf() and node_2.is_leaf():
            result_status = apply_boolean_operation(node_1.status, node_2.status, operation)
            result.status = result_status
            return result

        result.subdivide()

        for i in range(8):

            child_1 = node_1.children[i] if not node_1.is_leaf() else node_1
            child_2 = node_2.children[i] if not node_2.is_leaf() else node_2

            self._boolean_operation_recursive(child_1, child_2, result.children[i], operation)

        return result

    def complement(self):
        result_root = Node(
            self.root.min_cord,
            self.root.max_cord,
            0
        )

        self._complement_recursive(self.root, result_root)

        return Octree(
            result_root,
            None,
            self.i_max,
            self.delta
        )

    def _complement_recursive(self, node, result):
        if node.is_leaf():
            if node.status == 'FULL':
                result.status = 'EMPTY'
                return result
            elif node.status == 'EMPTY':
                result.status = 'FULL'
                return result
            else:
                result.status = 'PARTIAL'
                return result

        result.subdivide()

        for i in range(8):

            child = node.children[i]

            self._complement_recursive(child, result.children[i])
        return result







