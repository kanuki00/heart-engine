import sys
import json
from timeit import default_timer

import engine_types as et
import engine_draw as ed

fbuffer = {}
plist = []
rres = et.vector3(100, 50, 0)
bgcol = et.vec3_to_rgb(et.vector3(0.5, 0.5, 0.5))
exetime = 10

def loadmeshjson(file):
    with open(file) as meshfile:
        raw_data = json.load(meshfile)
        result = []
        for tri in raw_data["Triangles"]:
            a = tri["A"]
            b = tri["B"]
            c = tri["C"]
            r_tri = et.triangle(et.vector3(a[0], a[1], a[2]), et.vector3(b[0], b[1], b[2]), et.vector3(c[0], c[1], c[2]))
            result.append(r_tri)
        return result

def make_pixel_list(resolution):
    result = []
    for x in range(resolution.x):
        for y in range(resolution.y):
            result.append(et.vector3(x, y, 0))
    return result


def get_bounds(tris):
    result = []
    for tri in tris:
        ax = min(tri.a.x, tri.b.x, tri.c.x)
        ay = max(tri.a.y, tri.b.y, tri.c.y)
        bx = max(tri.a.x, tri.b.x, tri.c.x)
        by = min(tri.a.y, tri.b.y, tri.c.y)
        result.append(et.bounds(et.vector3(ax, ay, 0), et.vector3(bx, by, 0)))
    return result


def rasterize_pixel(frame_buffer, in_pixel, render_resolution, in_proj_triangles, in_triangles, in_tri_bounds):
    result = bgcol
    test_x = in_pixel.x / render_resolution.x
    test_y = in_pixel.y / render_resolution.y
    test_loc = et.vector3(test_x * 2 - 1, test_y * 2 - 1, 0)
    test_loc.x += 1 / render_resolution.x
    test_loc.y += 1 / render_resolution.y
    shallowest = -10000000000
    for i in range(len(in_proj_triangles)):
        p_tri = in_proj_triangles[i]
        p_tri_2d = et.triangle_omit_z(p_tri)
        tri = in_triangles[i]
        bounds = in_tri_bounds[i]
        if test_loc.x < bounds.a.x or test_loc.x > bounds.b.x or test_loc.y < bounds.b.y or test_loc.y > bounds.a.y:
            # skipping point in tri if test location is not in triangle bounding box
            continue
        if et.point_in_triangle_v2(test_loc, p_tri_2d):
            bc = et.bary_coords(test_loc, p_tri_2d)
            depth = p_tri.a.z*bc.x + p_tri.b.z*bc.y + p_tri.c.z*bc.z
            if depth > shallowest:
                shallowest = depth
                n = tri.compute_normal()
                result = et.vec3_to_rgb(n)
    pixel_keyform = "%d,%d" % (in_pixel.x, in_pixel.y)
    frame_buffer[pixel_keyform] = result  # setting a dict key that doesn't exist adds the key to the dict


def render_frame(frame_buffer, render_resolution, pixel_list, tris):
    start = default_timer()
    # Step 1: perspective projection
    persp_proj_tris = et.perspective_project(None, tris)
    # Step 2: getting projected triangle's bounding boxes
    ppt_bounds = get_bounds(persp_proj_tris)
    # Step 3: rasterize pixel and write it into frame buffer
    for i in range(len(pixel_list)):
        pixel = pixel_list[i]
        rasterize_pixel(frame_buffer, pixel, render_resolution, persp_proj_tris, tris, ppt_bounds)
    # Step 4: draw the frame buffer to the screen
    ed.draw_frame(frame_buffer, render_resolution)
    end = default_timer()
    sys.stdout.write(str(round((end - start) * 1000, 3)) + "ms       \n")


def main():
    start = default_timer()
    plist = make_pixel_list(rres)
    scene_triangles = loadmeshjson("mesh.json")
    #scene_camera TODO
    while default_timer() - start < exetime:
        render_frame(fbuffer, rres, plist, scene_triangles)
    ed.home()


if __name__ == "__main__":
    main()
