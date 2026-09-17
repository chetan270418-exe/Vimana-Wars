#pragma once
#include <functional>
#include <unordered_map>

namespace Vimana::DSA {

/**
 * @brief Generic Finite State Machine (FSM) template for Boss AI and Screen transitions.
 */
template <typename StateEnum>
class StateMachine {
public:
    using Callback = std::function<void()>;
    using UpdateCallback = std::function<void(float dt)>;

    StateMachine(StateEnum initial_state) : m_current_state(initial_state), m_previous_state(initial_state) {}

    void register_state(StateEnum state, Callback on_enter, UpdateCallback on_update, Callback on_exit) {
        m_states[state] = { on_enter, on_update, on_exit };
    }

    void transition_to(StateEnum new_state) {
        if (m_current_state == new_state) return;

        auto it_current = m_states.find(m_current_state);
        if (it_current != m_states.end() && it_current->second.on_exit) {
            it_current->second.on_exit();
        }

        m_previous_state = m_current_state;
        m_current_state = new_state;

        auto it_new = m_states.find(m_current_state);
        if (it_new != m_states.end() && it_new->second.on_enter) {
            it_new->second.on_enter();
        }
    }

    void update(float dt) {
        auto it = m_states.find(m_current_state);
        if (it != m_states.end() && it->second.on_update) {
            it->second.on_update(dt);
        }
    }

    StateEnum current_state() const { return m_current_state; }
    StateEnum previous_state() const { return m_previous_state; }

private:
    struct StateHandlers {
        Callback on_enter;
        UpdateCallback on_update;
        Callback on_exit;
    };

    StateEnum m_current_state;
    StateEnum m_previous_state;
    std::unordered_map<StateEnum, StateHandlers> m_states;
};

} // namespace Vimana::DSA
