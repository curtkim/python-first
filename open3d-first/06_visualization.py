import numpy as np
import open3d as o3d

'''
{
    "class_name" : "ViewTrajectory",
    "interval" : 29,
    "is_loop" : false,
    "trajectory" : 
    [
        {
            "boundingbox_max" : [ 3.9660897254943848, 2.427476167678833, 2.55859375 ],
            "boundingbox_min" : [ 0.55859375, 0.83203125, 0.56663715839385986 ],
            "field_of_view" : 60.0,
            "front" : [ 0.11458675185263953, -0.049071467672075555, -0.99220051771825335 ],
            "lookat" : [ 2.2623417377471924, 1.6297537088394165, 1.5626154541969299 ],
            "up" : [ -0.089188239253320034, -0.99525399172849682, 0.038922357680205626 ],
            "zoom" : 0.69999999999999996
        }
    ],
    "version_major" : 1,
    "version_minor" : 0
}
'''

def draw_lineset():
    print("Let's draw a cubic using o3d.geometry.LineSet.")
    points = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
    ]
    lines = [
        [0, 1],
        [0, 2],
        [1, 3],
        [2, 3],
        [4, 5],
        [4, 6],
        [5, 7],
        [6, 7],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7],
    ]
    colors = [[1, 0, 0] for i in range(len(lines))]
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines),
    )
    line_set.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([line_set])

def draw_textured():
    print("Let's draw a textured triangle mesh from obj file.")
    textured_mesh = o3d.io.read_triangle_mesh("test_data/crate/crate.obj")
    textured_mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([textured_mesh])

def draw_premitives():
    mesh_box = o3d.geometry.TriangleMesh.create_box(width=1.0,height=1.0,depth=1.0)
    mesh_box.compute_vertex_normals()
    mesh_box.paint_uniform_color([0.9, 0.1, 0.1])

    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
    mesh_sphere.compute_vertex_normals()
    mesh_sphere.paint_uniform_color([0.1, 0.1, 0.7])

    mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=0.3,height=4.0)
    mesh_cylinder.compute_vertex_normals()
    mesh_cylinder.paint_uniform_color([0.1, 0.9, 0.1])

    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6, origin=[-2, -2, -2])

    print("We draw a few primitives using collection.")
    o3d.visualization.draw_geometries(
        [mesh_box, mesh_sphere, mesh_cylinder, mesh_frame])

    #o3d.visualization.draw_geometries([mesh_box + mesh_sphere + mesh_cylinder + mesh_frame])

if __name__ == "__main__":
    draw_premitives()
    #draw_lineset()
    #draw_textured()
