#include <iostream>
#include <string>
#include <chrono>
#define MILLION 1000000.0f
#define BILLION 1000000000.0f

struct vec3
{
    float x, y, z;
    vec3(float in_x, float in_y, float in_z) : x(in_x), y(in_y), z(in_z) {}
};

std::chrono::nanoseconds timeNow()
{
    return std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch());
}

int main()
{
    int exe_time = 10;
    std::chrono::nanoseconds exe_time_start = timeNow();
    while(static_cast<float>((timeNow()-exe_time_start).count())/BILLION < exe_time)
    {
        std::chrono::nanoseconds time_start = timeNow();

        std::cout << "\033[H";
        for(int i = 0; i < 5000; i++)
        {
            
        }

        std::chrono::nanoseconds time_end = timeNow();
        std::chrono::nanoseconds time_delta = time_end-time_start;
        std::cout << std::to_string(static_cast<float>(time_delta.count())/MILLION) << "ms \n";
    }
    return 0;
}