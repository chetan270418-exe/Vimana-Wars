#pragma once
#include "raylib.h"
#include "core/types.hpp"

namespace Vimana {

class IView {
public:
    virtual ~IView() = default;

    virtual void init() = 0;
    virtual void update(float dt, Vector2 mouse_pos) = 0;
    virtual void draw() = 0;
    virtual ViewType next_view() const = 0;
    virtual void reset_next_view() = 0;
};

} // namespace Vimana
