#pragma once
#include <string>
#include <vector>
#include <algorithm>
#include <functional>
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/ship_archetypes.hpp"

namespace Vimana {

class CurrencySystem {
public:
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
        if (arch && campaign_max_wave >= arch->unlock_wave) {
            return true;
        }
        return false;
    }

    void set_on_ship_unlocked(std::function<void(const std::string&)> cb) { m_on_ship_unlocked = cb; }

    bool try_unlock_ship_with_prana(const std::string& ship_id, int campaign_max_wave = 1) {
        if (is_ship_unlocked(ship_id, campaign_max_wave)) return false; // Already unlocked
        const ShipArchetype* arch = GetShipArchetype(ship_id);
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
        }
    }
    void set_prana_shards(int shards) { m_prana_shards = shards; }

private:
    CurrencySystem() : m_prana_shards(250) {
        m_unlocked_ships = { "pushpaka", "tripura", "garuda" };
    }
    ~CurrencySystem() = default;

    int m_prana_shards;
    std::vector<std::string> m_unlocked_ships;
    std::function<void(const std::string&)> m_on_ship_unlocked;
};

} // namespace Vimana
