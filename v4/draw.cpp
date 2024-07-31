#include <iostream>
#include <string>
#include <chrono>
#define MILLION 1000000.0f
#define BILLION 1000000000.0f

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

std::chrono::nanoseconds time_now()
{
    return std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch());
}

void draw_frame_buffer(const intvec2& resolution, intvec3 f_buffer[])
{
    std::chrono::nanoseconds time_start = time_now();
    
    std::cout << "\033[H";
    for(int y = 0; y < resolution.y; y++)
    {
        for(int x = 0; x < resolution.x; x++)
        {
            intvec3 color = f_buffer[y*resolution.x + x];
            std::string code_tail = std::to_string(color.x)+";"+std::to_string(color.y)+";"+std::to_string(color.z)+"m";
            std::string fg_code = "\033[38;2;"+code_tail;
            std::string bg_code = "\033[48;2;"+code_tail;
            std::cout << fg_code+bg_code+"A";
        }
        // printing ansi color reset code and newline
        std::cout << "\033[0m\n";
    }

    std::chrono::nanoseconds time_end = time_now();
    std::chrono::nanoseconds time_delta = time_end-time_start;
    std::cout << std::to_string(static_cast<float>(time_delta.count())/MILLION) << "ms \n";
}

int main()
{
    const int exe_time = 10;
    const intvec2 render_resolution = intvec2(100, 50);
    intvec3 frame_buffer[render_resolution.x * render_resolution.y];
    // manual frame buffer manipulation test start
    frame_buffer[3599] = intvec3(255, 0, 0);
    frame_buffer[0] = intvec3(0, 0, 255);
    frame_buffer[2550] = intvec3(255, 255, 255);
    // manual frame buffer manipulation test end

    std::chrono::nanoseconds exe_time_start = time_now();
    while(static_cast<float>((time_now()-exe_time_start).count())/BILLION < exe_time)
    {
        draw_frame_buffer(render_resolution, frame_buffer);
    }
    return 0;
}