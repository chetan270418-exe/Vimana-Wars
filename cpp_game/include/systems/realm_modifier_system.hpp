#pragma once
#include <algorithm>
#include <cmath>
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

class RealmModifierSystem {
public:
    static RealmModifierType active_modifier(int wave) {
        return GetCampaignRealmForWave(wave).modifier_type;
    }

    static float player_speed_mult(int wave) {
        if (active_modifier(wave) == RealmModifierType::SWARGA_AETHER) return 1.15f;
        return 1.0f;
    }

    static float dash_distance_mult(int wave) {
        if (active_modifier(wave) == RealmModifierType::SETU_DRIFT) return 1.20f;
        return 1.0f;
    }

    static float fire_damage_mult(int wave) {
        if (active_modifier(wave) == RealmModifierType::LANKA_MOLTEN_FIRE) return 1.15f;
        return 1.0f;
    }

    static bool has_vortex_drift(int wave) {
        return active_modifier(wave) == RealmModifierType::KSHIRA_VORTEX;
    }

    static bool has_sensor_jamming(int wave) {
        return active_modifier(wave) == RealmModifierType::DANDAKA_JAMMING;
    }

    static float sniper_telegraph_multiplier(int wave) {
        return has_sensor_jamming(wave) ? 0.55f : 1.0f;
    }

    static bool sensors_jammed(int wave, float elapsed_time) {
        return has_sensor_jamming(wave) && std::fmod(std::max(0.0f, elapsed_time), 4.0f) < 0.55f;
    }

    static int extra_flak_projectiles(int wave) {
        if (active_modifier(wave) == RealmModifierType::NARAKA_FLAK) return 1;
        return 0;
    }

    static bool has_reality_distortion(int wave) {
        return active_modifier(wave) == RealmModifierType::MAHAYUDDHA_DISTORT;
    }
};

} // namespace Vimana
