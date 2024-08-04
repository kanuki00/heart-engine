#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <complex>

#include "/home/kanuki/Desktop/json/single_include/nlohmann/json.hpp"

#define MILLION 1000000.0f
#define BILLION 1000000000.0f

using json = nlohmann::json;

namespace types
{
    struct vec3
    {
        float x, y, z;
        vec3(float in_x, float in_y, float in_z) : x(in_x), y(in_y), z(in_z) {}
        vec3() : x(0.0f), y(0.0f), z(0.0f)  {}
        vec3 operator-(vec3 const& vec) const
        {
            vec3 res;
            res.x = x - vec.x;
            res.y = y - vec.y;
            res.z = z - vec.z;
            return res;
        }
        vec3 operator/(float const& num) const
        {
            vec3 res;
            res.x = x/num;
            res.y = y/num;
            res.z = z/num;
            return res;
        }
    };

    struct intvec3
    {
        int x, y, z;
        intvec3(int in_x, int in_y, int in_z) : x(in_x), y(in_y), z(in_z) {}
        intvec3() {x = 0; y = 0; z = 0;}
    };

    struct intvec2
    {
        int x, y;
        intvec2(int in_x, int in_y) : x(in_x), y(in_y) {}
    };

    struct tri
    {
        vec3 a, b, c;
        tri(vec3 in_a, vec3 in_b, vec3 in_c) : a(in_a), b(in_b), c(in_c) {}
        tri() : a(vec3()), b(vec3()), c(vec3()) {}
    };

}

namespace math
{
    bool edge_func(types::vec3 a, types::vec3 b, types::vec3 p)
    {
        float side = (p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x);
        return side <= 0.0f;
    }

    bool point_in_triangle(types::vec3 p, types::tri tri)
    {
        if(!edge_func(tri.a, tri.b, p))
        {
            return false;
        }
        if(!edge_func(tri.b, tri.c, p))
        {
            return false;
        }
        if(!edge_func(tri.c, tri.a, p))
        {
            return false;
        }
        return true;
    }

    types::vec3 cross(const types::vec3 v1, const types::vec3 v2)
    {
        float x = v1.y * v2.z - v1.z * v2.y;
        float y = v1.z * v2.x - v1.x * v2.z;
        float z = v1.x * v2.y - v1.y * v2.x;
        return {x, y, z};
    }

    float dot(const types::vec3 v1, const types::vec3 v2)
    {
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
    }

    float vec3_len(const types::vec3 v)
    {
        return std::sqrt(dot(v, v));
    }

    types::vec3 normalize(const types::vec3 v)
    {
        return v / vec3_len(v);
    }

    types::intvec3 vec3_to_rgb(types::vec3 v)
    {
        float r = v.x * 255.0f;
        float g = v.y * 255.0f;
        float b = v.z * 255.0f;
        r = std::clamp(r, 0.0f, 255.0f);
        g = std::clamp(g, 0.0f, 255.0f);
        b = std::clamp(b, 0.0f, 255.0f);
        return types::intvec3(r, g, b);
    }
}

std::chrono::nanoseconds time_now()
{
    return std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch());
}

int load_tricount(const char path[])
{
    auto file = std::ifstream(path);
    json data = json::parse(file);
    return data["indices"].size();
}

types::tri* load_mesh(const char path[], int tricount, types::tri triangles[])
{
    auto file = std::ifstream(path);
    json data = json::parse(file);
    for(int i = 0; i<tricount; i++)
    {
        types::tri from_data;
        const int idx_a = data["indices"][i][0];
        from_data.a = types::vec3(
            data["vertices"][idx_a][0],
            data["vertices"][idx_a][1],
            data["vertices"][idx_a][2]);

        const int idx_b = data["indices"][i][1];
        from_data.b = types::vec3(
            data["vertices"][idx_b][0],
            data["vertices"][idx_b][1],
            data["vertices"][idx_b][2]);

        const int idx_c= data["indices"][i][2];
        from_data.c = types::vec3(
            data["vertices"][idx_c][0],
            data["vertices"][idx_c][1],
            data["vertices"][idx_c][2]);
        triangles[i] = from_data;
    }
    return triangles;
}

int* test(int arr[])
{
    arr[0] = 45;
    arr[1] = 69;
    return arr;
}

//template<int N>
void rasterize(const types::intvec2& resolution, types::intvec3 (&f_buffer)[], types::tri* proj_tris, types::tri* world_tris, int tricount)
{
    for(int y = 0; y < resolution.y; y++)
    {
        for(int x = 0; x < resolution.x; x++)
        {
            float tp_x = static_cast<float>(x)/static_cast<float>(resolution.x);
            float tp_y = static_cast<float>(y)/static_cast<float>(resolution.y);
            types::vec3 tp = types::vec3(tp_x*2.0f-1.0f, tp_y*-2.0f+1.0f, 0.0f); // test point
            for(int t = 0; t < tricount; t++)
            {
                types::tri p_tri = proj_tris[t];
                if(math::point_in_triangle(tp, p_tri))
                {
                    types::vec3 normal = math::cross(p_tri.b-p_tri.a, p_tri.c-p_tri.a);
                    normal = math::normalize(normal);
                    f_buffer[y*resolution.x+x] = math::vec3_to_rgb(normal);
                }
            }
        }
    }
}

void draw_frame_buffer(const types::intvec2& resolution, types::intvec3 f_buffer[])
{
    std::cout << "\033[H";
    for(int y = 0; y < resolution.y; y++)
    {
        for(int x = 0; x < resolution.x; x++)
        {
            types::intvec3 color = f_buffer[y*resolution.x + x];
            std::string code_tail = std::to_string(color.x)+";"+std::to_string(color.y)+";"+std::to_string(color.z)+"m";
            std::string fg_code = "\033[38;2;"+code_tail;
            std::string bg_code = "\033[48;2;"+code_tail;
            std::cout << fg_code+bg_code+"A";
        }
        // printing ansi color reset code and newline
        std::cout << "\033[0m\n";
    }
}

int main()
{
    const int exe_time = 10;
    const types::intvec2 render_resolution = types::intvec2(100, 50);
    types::intvec3 frame_buffer[render_resolution.x * render_resolution.y];

    std::chrono::nanoseconds exe_time_start = time_now();
    if(false)
    {
        int my_arr[2];
        int* ap = test(my_arr);
        std::cout << ap[1] << "\n";
        return 0;
    }
    while(static_cast<float>((time_now()-exe_time_start).count())/BILLION < exe_time)
    {
        std::chrono::nanoseconds time_start = time_now();
        // rendering start
        // loading mesh
        // tricount
        int tc = load_tricount("test_mesh2.json");
        // initializing an array with tricount so that we can keep memory of it in loop scope
        types::tri t[tc];
        // loading triangles
        types::tri* triangles = load_mesh("test_mesh2.json", tc, t);
        // rasterizing
        rasterize(render_resolution, frame_buffer, triangles, triangles, tc);
        // drawing to screen
        draw_frame_buffer(render_resolution, frame_buffer);
        // rendering end
        std::chrono::nanoseconds time_end = time_now();
        std::chrono::nanoseconds time_delta = time_end-time_start;
        std::cout << std::to_string(static_cast<float>(time_delta.count())/MILLION) << "ms \n";
    }
    return 0;
}
