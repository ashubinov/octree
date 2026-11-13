# по сути узел это квадрат
# min_cord - минимальная координата, max_cord - максимальная координата, deep - глубина, children ссылки на детей, status - терминальный или нетерминальный
import math


class Node:
    def __init__(self, min_cord, max_cord, deep):
        self.min_cord = min_cord
        self.max_cord = max_cord
        self.deep = deep
        self.children = []
        self.status = ''

    def determine_state(self, obj_min, obj_max):
        self.status = 'FULL'
        for i in range(3):
            if self.max_cord[i] < obj_min[i] or obj_max[i] < self.min_cord[i]:
                self.status = 'EMPTY'
                return self.status
        for e in range(3):
            if not(self.min_cord[e] >= obj_min[e] and self.max_cord[e] <= obj_max[e]):
                self.status = 'PARTIAL'
                return self.status
        return self.status

    def determine_state_sphere(self, center, radius):

        px = min(max(center[0], self.min_cord[0]), self.max_cord[0])
        py = min(max(center[1], self.min_cord[1]), self.max_cord[1])
        pz = min(max(center[2], self.min_cord[2]), self.max_cord[2])

        d_min = math.sqrt((px - center[0])**2+(py - center[1])**2+(pz - center[2])**2)
        if d_min > radius:
            self.status = 'EMPTY'
            return self.status

        ver = self.get_vertices()

        for v in ver:
            d = math.sqrt((v[0] - center[0]) ** 2 + (v[1] - center[1]) ** 2 + (v[2] - center[2]) ** 2)

            if d > radius:
                self.status = 'PARTIAL'
                return self.status

        self.status = 'FULL'
        return self.status

    def is_leaf(self):
        return len(self.children) == 0

    def subdivide(self):
        if not self.is_leaf():
            raise ValueError("Node is already subdivided")
        center = self.get_center()
        for x in range(2):
            for y in range(2):
                for z in range(2):

                    min_cx = center[0] if x == 1 else self.min_cord[0]
                    min_cy = center[1] if y == 1 else self.min_cord[1]
                    min_cz = center[2] if z == 1 else self.min_cord[2]

                    max_cx = self.max_cord[0] if x == 1 else center[0]
                    max_cy = self.max_cord[1] if y == 1 else center[1]
                    max_cz = self.max_cord[2] if z == 1 else center[2]

                    baby = Node(
                        [min_cx, min_cy, min_cz],
                        [max_cx, max_cy, max_cz],
                        self.deep + 1,
                    )
                    self.children.append(baby)

    def get_center(self):
        return [(self.min_cord[0] + self.max_cord[0])/2, (self.min_cord[1] + self.max_cord[1])/2, (self.min_cord[2] + self.max_cord[2])/2]

    def get_octant_index(self, point: list):
        center = self.get_center()
        x = int(point[0] >= center[0])
        y = int(point[1] >= center[1])
        z = int(point[2] >= center[2])
        return x + 2 * y + 4 * z

    def get_vertices(self):
        vertices = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    xk = self.min_cord[0] if x == 0 else self.max_cord[0]
                    yk = self.min_cord[1] if y == 0 else self.max_cord[1]
                    zk = self.min_cord[2] if z == 0 else self.max_cord[2]

                    vertices.append([xk, yk, zk])

        return vertices

    def get_size(self):
        return [self.max_cord[i] - self.min_cord[i] for i in range(3)]

    def get_volume(self):
        size = self.get_size()
        return size[0] * size[1] * size[2]






