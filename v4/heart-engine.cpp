#include <iostream>
#include <string>
#include <chrono>
#define MILLION 1000000.0f
#define BILLION 1000000000.0f

namespace types
{
    struct vec3
    {
        float x, y, z;
        vec3(float in_x, float in_y, float in_z) : x(in_x), y(in_y), z(in_z) {}
        vec3() {x = 0.0f; y = 0.0f; z = 0.0f;}
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
}

std::chrono::nanoseconds time_now()
{
    return std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch());
}

void rasterize(const types::intvec2& resolution, types::intvec3 (&f_buffer)[], types::tri (&proj_tris)[], const types::tri (&world_tris)[], int tricount)
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
                if(math::point_in_triangle(tp, proj_tris[t]))
                {
                    f_buffer[y*resolution.x+x] = types::intvec3(255, 255, 255);
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
    while(static_cast<float>((time_now()-exe_time_start).count())/BILLION < exe_time)
    {
        std::chrono::nanoseconds time_start = time_now();
        // rendering start
        types::tri proj_tris[] = { // TODO load mesh from json (requires 3rd party json lib and docker container)
            types::tri(types::vec3(0.0f, 0.5f, 0.0f), types::vec3(-0.5f, -0.5f, 0.0f), types::vec3(0.5f, -0.5f, 0.0f)),
            types::tri(types::vec3(1.0f, 0.5f, 0.0f), types::vec3(0.0f, 0.5f, 0.0f), types::vec3(0.5f, -0.5f, 0.0f))
        };
        int tricount = sizeof(proj_tris)/sizeof(types::tri); // TODO figure out a more portable way of getting array length
        rasterize(render_resolution, frame_buffer, proj_tris, proj_tris, tricount);
        draw_frame_buffer(render_resolution, frame_buffer);
        // rendering end
        std::chrono::nanoseconds time_end = time_now();
        std::chrono::nanoseconds time_delta = time_end-time_start;
        std::cout << std::to_string(static_cast<float>(time_delta.count())/MILLION) << "ms \n";
    }
    return 0;
}