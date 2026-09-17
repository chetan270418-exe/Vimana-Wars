#pragma once
#include <vector>
#include <cstddef>

namespace Vimana::DSA {

/**
 * @brief Circular Ring Buffer with fixed capacity.
 * Guarantees zero runtime allocations for streaming items like floating damage text.
 */
template <typename T, size_t Capacity>
class RingBuffer {
public:
    RingBuffer() : m_head(0), m_tail(0), m_size(0) {
        m_buffer.resize(Capacity);
    }

    void push(const T& item) {
        m_buffer[m_head] = item;
        m_head = (m_head + 1) % Capacity;
        if (m_size < Capacity) {
            m_size++;
        } else {
            m_tail = (m_tail + 1) % Capacity; // Overwrite oldest item
        }
    }

    bool empty() const { return m_size == 0; }
    size_t size() const { return m_size; }
    size_t capacity() const { return Capacity; }

    void clear() {
        m_head = 0;
        m_tail = 0;
        m_size = 0;
    }

    T& operator[](size_t index) {
        size_t actual_idx = (m_tail + index) % Capacity;
        return m_buffer[actual_idx];
    }

    const T& operator[](size_t index) const {
        size_t actual_idx = (m_tail + index) % Capacity;
        return m_buffer[actual_idx];
    }

private:
    std::vector<T> m_buffer;
    size_t m_head;
    size_t m_tail;
    size_t m_size;
};

} // namespace Vimana::DSA
