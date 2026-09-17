#pragma once
#include <vector>
#include <cstddef>
#include <cassert>

namespace Vimana::DSA {

/**
 * @brief Zero-allocation contiguous object pool with an O(1) free-list stack.
 * Eliminates malloc/free heap thrashing during intense 60 FPS bullet hell gameplay.
 */
template <typename T, size_t Capacity>
class ObjectPool {
public:
    ObjectPool() {
        m_pool.resize(Capacity);
        m_free_indices.reserve(Capacity);
        for (size_t i = 0; i < Capacity; ++i) {
            m_free_indices.push_back(Capacity - 1 - i);
        }
    }

    T* acquire() {
        if (m_free_indices.empty()) {
            return nullptr; // Pool exhausted
        }
        size_t index = m_free_indices.back();
        m_free_indices.pop_back();
        m_pool[index] = T(); // Reset with default construct
        return &m_pool[index];
    }

    void release(T* object) {
        if (!object) return;
        ptrdiff_t diff = object - m_pool.data();
        if (diff >= 0 && static_cast<size_t>(diff) < Capacity) {
            m_free_indices.push_back(static_cast<size_t>(diff));
        }
    }

    void reset() {
        m_free_indices.clear();
        for (size_t i = 0; i < Capacity; ++i) {
            m_free_indices.push_back(Capacity - 1 - i);
        }
    }

    size_t capacity() const { return Capacity; }
    size_t available() const { return m_free_indices.size(); }
    size_t active_count() const { return Capacity - m_free_indices.size(); }

    std::vector<T>& raw_storage() { return m_pool; }
    const std::vector<T>& raw_storage() const { return m_pool; }

private:
    std::vector<T> m_pool;
    std::vector<size_t> m_free_indices;
};

} // namespace Vimana::DSA
