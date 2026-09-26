#pragma once
#include <array>

namespace Vimana {

struct CampaignStoryEvent {
    int wave;
    const char* speaker;
    const char* title;
    const char* message;
};

inline constexpr std::array<CampaignStoryEvent, 20> CAMPAIGN_STORY_EVENTS = {{
    { 1,   "MAITREYI // ARCHIVIST", "The Hidden Anchor", "The first armada is screening a rift anchor. Break its front line." },
    { 16,  "VIBHISHANA // ALLY", "Foundry Supply Route", "Lanka's foundries feed the portals. Cut the escort convoys." },
    { 31,  "ARUNI // WING COMMAND", "Crossing the Nectar Sea", "Vortex currents bend hostile fire. Hold formation through the drift." },
    { 46,  "MAITREYI // ARCHIVIST", "A Broken Route Seal", "Wreckage confirms the next jump is exposed. Keep the fleet together." },
    { 61,  "VIBHISHANA // ALLY", "Silence in Dandaka", "Sensor shadows hide hunter wings. Trust the attack warnings, not the radar." },
    { 76,  "ARUNI // WING COMMAND", "The False Beacon", "The beacon is bait. Follow the marked route through the asteroid forest." },
    { 91,  "MAITREYI // ARCHIVIST", "Lanka's Outer Wall", "Molten flak guards the approach. Keep moving and break their firing line." },
    { 106, "VIBHISHANA // ALLY", "Gate of the Citadel", "The outer seal is failing. Ravana's inner fleet is mustering." },
    { 121, "ARUNI // WING COMMAND", "The Setu Current", "The drifting current can carry your dash farther. Use it to cross open lanes." },
    { 136, "MAITREYI // ARCHIVIST", "Shield-Core Convoy", "Enemy transports carry the citadel's shield cores. Intercept before they dock." },
    { 151, "VIBHISHANA // ALLY", "Naraka Foundry", "The forge feeds every armada. Silence its flak batteries." },
    { 166, "ARUNI // WING COMMAND", "Assembly-Line Breach", "The shipyard is exposed when its escort screen breaks. Press the opening." },
    { 181, "MAITREYI // ARCHIVIST", "Distorted Skies", "Reality is bending near the throne. Read projectile paths, not their echoes." },
    { 196, "VIBHISHANA // ALLY", "The True Route", "I have marked the real passage. Ignore the false beacon to port." },
    { 211, "ARUNI // WING COMMAND", "Thunderhead Ascent", "Charged air is pulling fire across every lane. Keep changing vectors." },
    { 226, "MAITREYI // ARCHIVIST", "Mirage Doctrine", "Indrajit's echoes are decoys. Track the live attack markers." },
    { 241, "VIBHISHANA // ALLY", "The Ananta Loop", "The rift repeats navigation signals. Trust your wave counter and squad." },
    { 256, "ARUNI // WING COMMAND", "Exit Seam Located", "We found a way out. A serpent armada is holding the seam." },
    { 271, "MAITREYI // ARCHIVIST", "The Last Stand", "Every armada has converged. This is the final defense of the realms." },
    { 286, "VIBHISHANA // ALLY", "Homeward Passage", "No more portals remain. Break the command fleet and bring everyone home." }
}};

struct MiniBossIntel {
    int act_wave;
    const char* name;
    const char* title;
    const char* warning;
    const char* counter;
    const char* sprite_file;
};

inline constexpr std::array<MiniBossIntel, 3> MINI_BOSS_INTEL = {{
    { 8,  "RIFT MAULER", "Armored breach captain", "A three-lane heavy burst covers its advance.", "Circle wide, then punish its slow turn.", "boss_vritra.png" },
    { 18, "SILENCE WARDEN", "Sensor-hunter marksman", "A fast beam tracks the pilot after a short charge.", "Break line-of-sight and dash across its aim.", "boss_indrajit.png" },
    { 28, "EMBER TYRANT", "Foundry strike commander", "A burning crossfire punishes stationary pilots.", "Keep moving and attack between volleys.", "boss_meghnada.png" }
}};

inline const CampaignStoryEvent* GetCampaignStoryEvent(int wave) {
    for (const auto& event : CAMPAIGN_STORY_EVENTS) {
        if (event.wave == wave) return &event;
    }
    return nullptr;
}

inline const MiniBossIntel* GetMiniBossIntelForActWave(int act_wave) {
    for (const auto& intel : MINI_BOSS_INTEL) {
        if (intel.act_wave == act_wave) return &intel;
    }
    return nullptr;
}

} // namespace Vimana
