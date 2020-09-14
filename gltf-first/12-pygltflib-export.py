from pygltflib import *

# create gltf objects for a scene with a primitive triangle with indexed geometry
gltf = GLTF2()
scene = Scene()
mesh = Mesh()
primitive = Primitive()
node = Node()
buffer = Buffer()
bufferView1 = BufferView()
bufferView2 = BufferView()
accessor1 = Accessor()
accessor2 = Accessor()

# add data
buffer.uri = "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAAACAPwAAAAA="
buffer.byteLength = 44

bufferView1.buffer = 0
bufferView1.byteOffset = 0
bufferView1.byteLength = 6
bufferView1.target = ELEMENT_ARRAY_BUFFER

bufferView2.buffer = 0
bufferView2.byteOffset = 8
bufferView2.byteLength = 36
bufferView2.target = ARRAY_BUFFER

accessor1.bufferView = 0
accessor1.byteOffset = 0
accessor1.componentType = UNSIGNED_SHORT
accessor1.count = 3
accessor1.type = SCALAR
accessor1.max = [2]
accessor1.min = [0]

accessor2.bufferView = 1
accessor2.byteOffset = 0
accessor2.componentType = FLOAT
accessor2.count = 3
accessor2.type = VEC3
accessor2.max = [1.0, 1.0, 0.0]
accessor2.min = [0.0, 0.0, 0.0]

primitive.attributes.POSITION = 1
node.mesh = 0
scene.nodes = [0]

# assemble into a gltf structure
gltf.scenes.append(scene)
gltf.meshes.append(mesh)
gltf.meshes[0].primitives.append(primitive)
gltf.nodes.append(node)
gltf.buffers.append(buffer)
gltf.bufferViews.append(bufferView1)
gltf.bufferViews.append(bufferView2)
gltf.accessors.append(accessor1)
gltf.accessors.append(accessor2)

# save to file
gltf.save("triangle2.gltf")
