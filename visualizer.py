import numpy as np
import pyvista as pv



#pip install pyvista

class Visual:
    def __init__(self, points, cells_data = None, depths = None,
                 objects = None):

        self.points = points
        self.cells_data = cells_data
        self.depths = depths
        self.objects = objects



    def create_object(self):
        bounds = (
            self.objects[0]['obj_min'][0], self.objects[0]['obj_max'][0],
            self.objects[0]['obj_min'][1], self.objects[0]['obj_max'][1],
            self.objects[0]['obj_min'][2], self.objects[0]['obj_max'][2]
        )

        return pv.Box(bounds=bounds)

    def create_sphere(self):
        if self.objects[1]['center'] is None or self.objects[1]['radius'] is None:
            return None

        sphere = pv.Sphere(
            radius=self.objects[1]['radius'],
            center=self.objects[1]['center'],
            theta_resolution=40,
            phi_resolution=40
        )

        return sphere

    def create_grid(self):
        grid = []
        for i in range(len(self.cells_data)):
            cells = np.array(self.cells_data[i]).flatten()
            cell_types = np.full(
                len(self.cells_data[i]),
                pv.CellType.HEXAHEDRON
            )

            grid.append(pv.UnstructuredGrid(
                cells,
                cell_types,
                self.points[i]
            ))
        return grid

    def show(self):
        grid = self.create_grid()

        plotter = pv.Plotter()
        for g in grid:
            # Ячейки Octree
            plotter.add_mesh(
                g,
                color='lightblue',
                opacity=0.3,
                show_edges=True,
                edge_color='black',
                line_width=1
            )


        for obj in self.objects:

            if obj['type'] == 'box':


                box = pv.Box(bounds=(
                    obj['obj_min'][0], obj['obj_max'][0],
                    obj['obj_min'][1], obj['obj_max'][1],
                    obj['obj_min'][2], obj['obj_max'][2]
                ))

                plotter.add_mesh(
                    box,
                    color='orange',
                    opacity=0.3,
                    show_edges=True,
                    edge_color='red'
                )

            elif obj['type'] == 'sphere':
                sphere = pv.Sphere(
                    radius=obj['radius'],
                    center=obj['center'],
                    theta_resolution=40,
                    phi_resolution=40
                )

                plotter.add_mesh(
                    sphere,
                    color='orange',
                    opacity=0.5,
                    show_edges=True,
                    edge_color='red'
                )

        plotter.show()

    def show_result(self):
        grid = self.create_grid()
        plotter = pv.Plotter()
        for g in grid:
            plotter.add_mesh(
                g,
                color='lightblue',
                opacity=0.3,
                show_edges=True,
                edge_color='black',
                line_width=1
            )

        plotter.show()


