#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <complex>
#include <sstream>

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
        tri no_z() const {
            const auto nza = vec3(a.x, a.y, 0.0f);
            const auto nzb = vec3(b.x, b.y, 0.0f);
            const auto nzc = vec3(c.x, c.y, 0.0f);
            return {nza, nzb, nzc};
        }
    };

    struct vec4
    {
        long double x, y, z, w;

        vec4() {x = 0.0f; y = 0.0f; z = 0.0f; w = 0.0f;}
        vec4(const float in_x, const float in_y, const float in_z, const float in_w) : x(in_x), y(in_y), z(in_z), w(in_w) {}

        vec4 operator+(vec4 const& vec) const {
            vec4 res;
            res.x = x + vec.x;
            res.y = y + vec.y;
            res.z = z + vec.z;
            res.w = w + vec.w;
            return res;
        }
        vec4 operator-(vec4 const& vec) const
        {
            vec4 res;
            res.x = x - vec.x;
            res.y = y - vec.y;
            res.z = z - vec.z;
            res.w = w - vec.w;
            return res;
        }
        vec4 operator*(float const& num) const
        {
            vec4 res;
            res.x = x*num;
            res.y = y*num;
            res.z = z*num;
            res.w = w*num;
            return res;
        }
        vec4 operator/(float const& num) const
        {
            vec4 res;
            res.x = x/num;
            res.y = y/num;
            res.z = z/num;
            res.w = w/num;
            return res;
        }

        float get_comp(int compidx)
        {
            switch (compidx)
            {
                case 0:
                    return x;
                case 1:
                    return y;
                case 2:
                    return z;
                case 3:
                    return w;
                default:
                    return 0.0f;
            }
        }

        std::string to_string()
        {
            std::ostringstream ss_x;
            ss_x << x;
            std::ostringstream ss_y;
            ss_y << y;
            std::ostringstream ss_z;
            ss_z << z;
            std::ostringstream ss_w;
            ss_w << w;
            return "["+ss_x.str()+", "+ss_y.str()+", "+ss_z.str()+", "+ss_w.str()+"]";
        }
    };

    struct matrix4x4
    {
        // i, j, k and t are all columns of matrix
        vec4 i, j, k, t;

        matrix4x4() {}
        matrix4x4(vec4 in_i, vec4 in_j, vec4 in_k, vec4 in_t) : i(in_i), j(in_j), k(in_k), t(in_t) {}

        vec4 get_row(const int rowidx) const
        {
            switch (rowidx)
                {
                case 0:
                    return vec4(i.x, j.x, k.x, t.x);
                case 1:
                    return vec4(i.y, j.y, k.y, t.y);
                case 2:
                    return vec4(i.z, j.z, k.z, t.z);
                case 3:
                    return vec4(i.w, j.w, k.w, t.w);
                default:
                    return vec4(0.0f, 0.0f, 0.0f, 0.0f);
            }
        }

        void set_row(int rowidx, vec4 new_row_value) {
            switch(rowidx) {
                case 0:
                    i.x = new_row_value.x;
                    j.x = new_row_value.y;
                    k.x = new_row_value.z;
                    t.x = new_row_value.w;
                    break;
                case 1:
                    i.y = new_row_value.x;
                    j.y = new_row_value.y;
                    k.y = new_row_value.z;
                    t.y = new_row_value.w;
                    break;
                case 2:
                    i.z = new_row_value.x;
                    j.z = new_row_value.y;
                    k.z = new_row_value.z;
                    t.z = new_row_value.w;
                    break;
                case 3:
                    i.w = new_row_value.x;
                    j.w = new_row_value.y;
                    k.w = new_row_value.z;
                    t.w = new_row_value.w;
                    break;
                default:
                    std::cout << "";
                    break;
            }
        }

        vec4* get_rows(vec4 in_rows[]) {
            in_rows[0] = get_row(0);
            in_rows[1] = get_row(1);
            in_rows[2] = get_row(2);
            in_rows[3] = get_row(3);
            return in_rows;
        }

        std::string to_string()
        {
            std::string r1s = get_row(0).to_string();
            std::string r2s = get_row(1).to_string();
            std::string r3s = get_row(2).to_string();
            std::string r4s = get_row(3).to_string();
            return r1s+"\n"+r2s+"\n"+r3s+"\n"+r4s+"\n";
        }
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
    float dot(const types::vec4 v1, const types::vec4 v2)
    {
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w;
    }

    float vec_len(const types::vec3 v)
    {
        return std::sqrt(dot(v, v));
    }
    float vec_len(const types::vec4 v)
    {
        return std::sqrt(dot(v, v));
    }

    types::vec3 normalize(const types::vec3 v)
    {
        return v / vec_len(v);
    }
    types::vec4 normalize(const types::vec4 v)
    {
        return v / vec_len(v);
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
    // Get barycentric co-ordinates with point and triangle
    types::vec3 get_bc_coords(const types::vec3 p, const types::tri& t)
    {
        const float t_para_area = vec_len(cross(t.b-t.a, t.c-t.a));
        const float w_area = vec_len(cross(t.b-t.a, p-t.a));
        const float u_area = vec_len(cross(t.c-t.b, p-t.b));
        const float v_area = vec_len(cross(t.a-t.c, p-t.c));
        return {u_area/t_para_area, v_area/t_para_area, w_area/t_para_area};
    }

    types::matrix4x4 invert_matrix4x4(types::matrix4x4 in_matrix) {
        types::matrix4x4 tableL = in_matrix;
        types::matrix4x4 tableR = types::matrix4x4();
        tableR.i = types::vec4(1.0f, 0.0f, 0.0f, 0.0f);
        tableR.j = types::vec4(0.0f, 1.0f, 0.0f, 0.0f);
        tableR.k = types::vec4(0.0f, 0.0f, 1.0f, 0.0f);
        tableR.t = types::vec4(0.0f, 0.0f, 0.0f, 1.0f);
        std::cout << tableL.to_string() << "\n\n";
        std::cout << tableR.to_string() << "\n\n";

        /* Reduction order A to P
           c0 c1 c2 c3
        r0 [M  L  J  I]
        r1 [A  N  K  H]
        r2 [B  E  O  G]
        r3 [C  D  F  P]
        */
        int tar_row_idxs[12] = {
            1, 2, 3, 3, 2, 3,
            2, 1, 0, 0, 1, 0
        };
        int tar_col_idx[12] = {
            0, 0, 0, 1, 1, 2,
            3, 3, 3, 2, 2, 1
        };
        for (int i = 0; i < 12; i++) {
            float target = tableL.get_row(tar_row_idxs[i]).get_comp(tar_col_idx[i]);
            if (target != 0.0f) {
                //msr_cands = get_msr_cands(tar_row_idxs[i], table) // multiplier source row candidates
                types::vec4 tLr[4] = {};
                types::vec4* tableLrows = tableL.get_rows(tLr);
                types::vec4 tRr[4] = {};
                types::vec4* tableRrows = tableR.get_rows(tRr);
                // debug
                /*std::cout << "DEBUG\n";
                for(int r = 0; r<4; r++) {
                    auto v = tableLrows[r];
                    std::cout << v.to_string() << "\n";
                }*/
                // debug end
                float mult;
                float shortest_len = 1000000000.0f;
                types::vec4 rowL_result;
                types::vec4 rowR_result;
                for (int j = 0; j < 4; j++) {
                    // making sure we dont add a multiplied target to the target
                    if (j != tar_row_idxs[i]) {
                        types::vec4 cand_rowL = tableLrows[j];
                        types::vec4 cand_rowR = tableRrows[j];
                        float cand_comp = cand_rowL.get_comp(tar_col_idx[i]);
                        // making sure the candidate row's effective component is something else than zero,
                        // so that adding a multiplied version of it to target will yield 0.
                        if (cand_comp != 0.0f) {
                            float cand_row_len = vec_len(cand_rowL);
                            // checking that the vector4 representing the candidate is the shortest of the bunch
                            if (cand_row_len < shortest_len) {
                                shortest_len = cand_row_len;
                                mult = -target / cand_comp;
                                types::vec4 to_addL = cand_rowL * mult;
                                types::vec4 to_addR = cand_rowR * mult;
                                rowL_result = tableL.get_row(tar_row_idxs[i]) + to_addL;
                                rowR_result = tableR.get_row(tar_row_idxs[i]) + to_addR;
                            }
                        }
                    }
                }
                tableL.set_row(tar_row_idxs[i], rowL_result);
                tableR.set_row(tar_row_idxs[i], rowR_result);
                if(i == 0) {
                    std::cout << "Phase 1:" << "\n";
                    std::cout << tableL.to_string() << "\n\n";
                    std::cout << tableR.to_string() << "\n\n";
                }
            }
        }

        return tableR;
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

void rasterize(const types::intvec2& resolution, types::intvec3 (&f_buffer)[], types::tri* proj_tris, types::tri* world_tris, int tricount)
{
    for(int y = 0; y < resolution.y; y++)
    {
        for(int x = 0; x < resolution.x; x++)
        {
            float tp_x = static_cast<float>(x)/static_cast<float>(resolution.x);
            float tp_y = static_cast<float>(y)/static_cast<float>(resolution.y);
            types::vec3 tp = types::vec3(tp_x*2.0f-1.0f, tp_y*-2.0f+1.0f, 0.0f); // test point
            float shallowest = -BILLION;
            for(int t = 0; t < tricount; t++)
            {
                types::tri p_tri = proj_tris[t];
                if(math::point_in_triangle(tp, p_tri))
                {
                    types::vec3 bc = math::get_bc_coords(tp, p_tri.no_z());
                    float fragment_depth = p_tri.a.z*bc.x + p_tri.b.z*bc.y + p_tri.c.z*bc.z;
                    if(fragment_depth > shallowest)
                    {
                        shallowest = fragment_depth;
                        types::vec3 normal = math::cross(p_tri.b-p_tri.a, p_tri.c-p_tri.a);
                        normal = math::normalize(normal);
                        f_buffer[y*resolution.x+x] = math::vec3_to_rgb(normal);
                    }
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
    if(true)
    {
        types::matrix4x4 my_matrix;
        my_matrix.i = types::vec4(1.0f, 2.0f, -1.0f, 0.0f);
        my_matrix.j = types::vec4(2.0f, 5.0f, -2.0f, 0.0f);
        my_matrix.k = types::vec4(-1.0f, 1.0f, 2.0f, 0.0f);
        my_matrix.t = types::vec4(5.0f, 2.0f, -7.0f, 1.0f);

        types::matrix4x4 my_matrix2;
        my_matrix2.i = types::vec4(0.7f, 1.5f, -2.0f, 0.0f);
        my_matrix2.j = types::vec4(5.0f, 1.0f, 1.5f, 0.0f);
        my_matrix2.k = types::vec4(-1.0f, -1.8f, 2.6f, 0.0f);
        my_matrix2.t = types::vec4(3.7f, 4.1f, -9.5f, 1.0f);

        std::cout << math::invert_matrix4x4(my_matrix).to_string();
        return 0;
    }
    while(static_cast<float>((time_now()-exe_time_start).count())/BILLION < exe_time)
    {
        std::chrono::nanoseconds time_start = time_now();
        // rendering start
        // loading mesh
        // tricount
        int tc = load_tricount("../test_mesh2.json");
        // initializing an array with tricount so that we can keep memory of it in loop scope
        types::tri t[tc];
        // loading triangles
        types::tri* triangles = load_mesh("../test_mesh2.json", tc, t);
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
