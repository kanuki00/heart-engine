import bpy
import json

# TODO should first check if all mesh polygons are triangulated

mesh = bpy.context.object.data
path = "/home/kanuki/Desktop/heart-engine/"

with open(path+"mesh.json", "w") as f:
    data = {}
    
    vertcount = len(mesh.vertices)
    data["vertices"] = [[0.0, 0.0, 0.0]] * vertcount
    for i in range(vertcount):
        vert = mesh.vertices[i]
        vertexdata = [vert.co[0], vert.co[1], vert.co[2]]
        data["vertices"][i] = vertexdata
        
    
    tricount = len(mesh.polygons)
    data["indices"] = [[0, 0, 0]] * tricount
    for i in range(tricount):
        poly = mesh.polygons[i]
        polydata = []
        
        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
            polydata.append(mesh.loops[loop_index].vertex_index)
            
        data["indices"][i] = polydata
            
    f.write(json.dumps(data, indent=4))