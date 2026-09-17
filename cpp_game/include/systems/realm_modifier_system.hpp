#pragma once
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

    static int extra_flak_projectiles(int wave) {
        if (active_modifier(wave) == RealmModifierType::NARAKA_FLAK) return 1;
        return 0;
    }

    static bool has_reality_distortion(int wave) {
        return active_modifier(wave) == RealmModifierType::MAHAYUDDHA_DISTORT;
    }
};

} // namespace Vimana
