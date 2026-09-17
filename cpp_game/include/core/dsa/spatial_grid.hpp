#pragma once
#include <vector>
#include <unordered_map>
#include <cmath>
#include <algorithm>
#include "raylib.h"

namespace Vimana::DSA {

/**
 * @brief Spatial Partitioning Grid for broadphase collision detection.
 * Reduces collision checks from O(N * M) to O(N) by binning entities into 2D spatial buckets.
 */
class SpatialGrid {
public:
    SpatialGrid(float width, float height, float cell_size = 80.0f)
        : m_width(width), m_height(height), m_cell_size(cell_size) {
        m_cols = static_cast<int>(std::ceil(width / cell_size));
        m_rows = static_cast<int>(std::ceil(height / cell_size));
        m_buckets.resize(m_cols * m_rows);
    }

    void clear() {
        for (auto& bucket : m_buckets) {
            bucket.clear();
        }
    }

    void insert(int entity_id, Vector2 pos, float radius) {
        int min_x = std::max(0, static_cast<int>((pos.x - radius) / m_cell_size));
        int max_x = std::min(m_cols - 1, static_cast<int>((pos.x + radius) / m_cell_size));
        int min_y = std::max(0, static_cast<int>((pos.y - radius) / m_cell_size));
        int max_y = std::min(m_rows - 1, static_cast<int>((pos.y + radius) / m_cell_size));

        for (int y = min_y; y <= max_y; ++y) {
            for (int x = min_x; x <= max_x; ++x) {
                int index = y * m_cols + x;
                m_buckets[index].push_back(entity_id);
            }
        }
    }

    /**
     * @brief Retrieve all potential collision entity IDs near the given position and radius.
     */
    void query(Vector2 pos, float radius, std::vector<int>& out_candidates) const {
        out_candidates.clear();
        int min_x = std::max(0, static_cast<int>((pos.x - radius) / m_cell_size));
        int max_x = std::min(m_cols - 1, static_cast<int>((pos.x + radius) / m_cell_size));
        int min_y = std::max(0, static_cast<int>((pos.y - radius) / m_cell_size));
        int max_y = std::min(m_rows - 1, static_cast<int>((pos.y + radius) / m_cell_size));

        for (int y = min_y; y <= max_y; ++y) {
            for (int x = min_x; x <= max_x; ++x) {
                int index = y * m_cols + x;
                const auto& bucket = m_buckets[index];
                for (int id : bucket) {
                    // Filter duplicates quickly
                    if (std::find(out_candidates.begin(), out_candidates.end(), id) == out_candidates.end()) {
                        out_candidates.push_back(id);
                    }
                }
            }
        }
    }

private:
    float m_width;
    float m_height;
    float m_cell_size;
    int m_cols;
    int m_rows;
    std::vector<std::vector<int>> m_buckets;
};

} // namespace Vimana::DSA
