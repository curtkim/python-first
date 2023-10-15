import pygfx as gfx

cube = gfx.Mesh(
    gfx.box_geometry(200, 200, 200),
    gfx.MeshPhongMaterial(color="#336699"),
)

if __name__ == "__main__":
    gfx.show(cube)
