#pragma once
#include <string>
#include <vector>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/ship_archetypes.hpp"

namespace Vimana {

class CurrencySystem {
public:
    static constexpr int MAX_SHIP_UPGRADE_LEVEL = 10;
    static CurrencySystem& instance() {
        static CurrencySystem sys;
        return sys;
    }

    int prana_shards() const { return m_prana_shards; }
    void add_prana_shards(int amount) { m_prana_shards += amount; }
    bool spend_prana_shards(int amount) {
        if (m_prana_shards >= amount) {
            m_prana_shards -= amount;
            return true;
        }
        return false;
    }

    bool is_ship_unlocked(const std::string& ship_id, int campaign_max_wave) const {
        // Free starters
        if (ship_id == "pushpaka" || ship_id == "tripura" || ship_id == "garuda") {
            return true;
        }
        // Purchased with Prana
        if (std::find(m_unlocked_ships.begin(), m_unlocked_ships.end(), ship_id) != m_unlocked_ships.end()) {
            return true;
        }
        // Campaign wave gate
        const ShipArchetype* arch = GetShipArchetype(ship_id);
        if (arch && !arch->boss_unlock_id.empty()) return false;
        if (arch && campaign_max_wave >= arch->unlock_wave) {
            return true;
        }
        return false;
    }

    void set_on_ship_unlocked(std::function<void(const std::string&)> cb) { m_on_ship_unlocked = cb; }

    bool try_unlock_ship_with_prana(const std::string& ship_id, int campaign_max_wave = 1) {
        if (is_ship_unlocked(ship_id, campaign_max_wave)) return false; // Already unlocked
        const ShipArchetype* arch = GetShipArchetype(ship_id);
        if (arch && !arch->boss_unlock_id.empty()) return false;
        int cost = arch ? arch->prana_cost : COST_EARLY_SHIP_UNLOCK;
        if (spend_prana_shards(cost)) {
            m_unlocked_ships.push_back(ship_id);
            if (m_on_ship_unlocked) m_on_ship_unlocked(ship_id);
            return true;
        }
        return false;
    }

    bool buy_consumable(ConsumableInventory& inv, const std::string& item) {
        if (item == "kavach" && spend_prana_shards(COST_KAVACH_SHIELD)) {
            inv.kavach_charges++;
            return true;
        } else if (item == "soma" && spend_prana_shards(COST_SOMA_VIAL)) {
            inv.soma_vials++;
            return true;
        } else if (item == "vajra" && spend_prana_shards(COST_VAJRA_FLARE)) {
            inv.vajra_flares++;
            return true;
        }
        return false;
    }

    const std::vector<std::string>& unlocked_ships() const { return m_unlocked_ships; }
    void set_unlocked_ships(const std::vector<std::string>& ships) { m_unlocked_ships = ships; }
    void unlock_ship(const std::string& ship_id) {
        if (std::find(m_unlocked_ships.begin(), m_unlocked_ships.end(), ship_id) == m_unlocked_ships.end()) {
            m_unlocked_ships.push_back(ship_id);
            if (m_on_ship_unlocked) m_on_ship_unlocked(ship_id);
        }
    }

    std::string unlock_boss_reward(const std::string& boss_unlock_id) {
        for (const auto& ship : SHIP_FLEET) {
            if (ship.boss_unlock_id == boss_unlock_id &&
                std::find(m_unlocked_ships.begin(), m_unlocked_ships.end(), ship.id) == m_unlocked_ships.end()) {
                unlock_ship(ship.id);
                return ship.id;
            }
        }
        return {};
    }
    void set_prana_shards(int shards) { m_prana_shards = shards; }

    int ship_upgrade_level(const std::string& ship_id) const {
        auto it = m_ship_upgrade_levels.find(ship_id);
        return it == m_ship_upgrade_levels.end() ? 0 : std::clamp(it->second, 0, MAX_SHIP_UPGRADE_LEVEL);
    }

    static constexpr int SHIP_MASTERY_SORTIES = 50;
    int ship_sorties(const std::string& ship_id) const {
        const auto it = m_ship_sorties.find(ship_id);
        return it == m_ship_sorties.end() ? 0 : std::clamp(it->second, 0, SHIP_MASTERY_SORTIES);
    }
    bool is_ship_mastered(const std::string& ship_id) const {
        return ship_sorties(ship_id) >= SHIP_MASTERY_SORTIES;
    }
    int record_ship_sortie(const std::string& ship_id) {
        if (ship_id.empty()) return 0;
        int& sorties = m_ship_sorties[ship_id];
        sorties = std::min(SHIP_MASTERY_SORTIES, sorties + 1);
        return sorties;
    }
    const std::unordered_map<std::string, int>& ship_sortie_counts() const { return m_ship_sorties; }
    void merge_ship_sortie_counts(const std::unordered_map<std::string, int>& counts) {
        for (const auto& [ship_id, count] : counts) {
            if (!ship_id.empty()) m_ship_sorties[ship_id] = std::clamp(std::max(m_ship_sorties[ship_id], count), 0, SHIP_MASTERY_SORTIES);
        }
    }
    void set_ship_sortie_counts(const std::unordered_map<std::string, int>& counts) {
        m_ship_sorties.clear();
        merge_ship_sortie_counts(counts);
    }

    int next_ship_upgrade_cost(const std::string& ship_id) const {
        const int level = ship_upgrade_level(ship_id);
        if (level >= MAX_SHIP_UPGRADE_LEVEL) return 0;
        return 200 + level * 175 + level * level * 75;
    }

    bool upgrade_ship(const std::string& ship_id, int campaign_max_wave) {
        if (!is_ship_unlocked(ship_id, campaign_max_wave)) return false;
        const int level = ship_upgrade_level(ship_id);
        if (level >= MAX_SHIP_UPGRADE_LEVEL) return false;
        if (!spend_prana_shards(next_ship_upgrade_cost(ship_id))) return false;
        m_ship_upgrade_levels[ship_id] = level + 1;
        return true;
    }

    const std::unordered_map<std::string, int>& ship_upgrade_levels() const { return m_ship_upgrade_levels; }
    void set_ship_upgrade_levels(const std::unordered_map<std::string, int>& levels) {
        m_ship_upgrade_levels.clear();
        for (const auto& [ship_id, level] : levels) {
            if (level > 0) m_ship_upgrade_levels[ship_id] = std::clamp(level, 0, MAX_SHIP_UPGRADE_LEVEL);
        }
    }

private:
    CurrencySystem() : m_prana_shards(250) {
        m_unlocked_ships = { "pushpaka", "tripura", "garuda" };
    }
    ~CurrencySystem() = default;

    int m_prana_shards;
    std::vector<std::string> m_unlocked_ships;
    std::unordered_map<std::string, int> m_ship_upgrade_levels;
    std::unordered_map<std::string, int> m_ship_sorties;
    std::function<void(const std::string&)> m_on_ship_unlocked;
};

} // namespace Vimana
