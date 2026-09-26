#include <array>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

#include "entities/boss.hpp"
#include "entities/player_controller.hpp"
#include "entities/ship_archetypes.hpp"
#include "systems/db_system.hpp"
#include "systems/network_manager.hpp"
#include "systems/realm_modifier_system.hpp"
#include "systems/transition_manager.hpp"
#include "systems/wave_manager.hpp"
#include "views/campaign_map_view.hpp"

using namespace Vimana;

int main() {
    const Color standard_shot = { 210, 180, 60, 255 };
    g_colorblind_mode = false;
    assert(accessible_projectile_color(standard_shot, false).r == standard_shot.r);
    g_colorblind_mode = true;
    const Color accessible_player_shot = accessible_projectile_color(standard_shot, false);
    const Color accessible_hostile_shot = accessible_projectile_color(standard_shot, true);
    assert(accessible_player_shot.g != accessible_hostile_shot.g);
    assert(accessible_player_shot.b > accessible_hostile_shot.b);
    g_colorblind_mode = false;

    auto& transitions = TransitionManager::instance();
    transitions.start_transition(ViewType::MENU, 0.2f);
    ViewType transition_target = ViewType::BOOT;
    assert(!transitions.update(0.0f, transition_target));
    assert(!transitions.update(0.09f, transition_target));
    assert(transitions.update(0.02f, transition_target));
    assert(transition_target == ViewType::MENU);
    assert(!transitions.update(0.12f, transition_target));
    assert(!transitions.is_transitioning());

    assert(CAMPAIGN_REALMS.size() == 10);
    assert(CAMPAIGN_STORY_EVENTS.size() == 20);
    assert(GetCampaignStoryEvent(1) && GetCampaignStoryEvent(286));
    assert(!GetCampaignStoryEvent(2));
    assert(GetMiniBossIntelForActWave(8)->name == std::string("RIFT MAULER"));
    assert(GetMiniBossIntelForActWave(18)->name == std::string("SILENCE WARDEN"));
    assert(GetMiniBossIntelForActWave(28)->name == std::string("EMBER TYRANT"));
    WaveManager transmission_check;
    transmission_check.prepare_wave(286);
    assert(transmission_check.get_story_transmission().find("No more portals remain") != std::string::npos);
    transmission_check.prepare_wave(18);
    assert(transmission_check.get_story_transmission().find("SILENCE WARDEN") != std::string::npos);
    assert(RealmModifierSystem::player_speed_mult(1) == 1.15f);
    assert(RealmModifierSystem::has_vortex_drift(31));
    assert(RealmModifierSystem::has_sensor_jamming(61));
    assert(RealmModifierSystem::sniper_telegraph_multiplier(61) == 0.55f);
    assert(RealmModifierSystem::sensors_jammed(61, 0.2f));
    assert(!RealmModifierSystem::sensors_jammed(61, 1.0f));
    assert(RealmModifierSystem::fire_damage_mult(91) == 1.15f);
    assert(RealmModifierSystem::dash_distance_mult(121) == 1.20f);
    assert(RealmModifierSystem::extra_flak_projectiles(151) == 1);
    assert(RealmModifierSystem::has_reality_distortion(181));

    assert(CurrencySystem::calculate_run_payout(0, 0, false) == 40);
    assert(CurrencySystem::calculate_run_payout(2345, 7, false) == 116);
    assert(CurrencySystem::calculate_run_payout(2345, 7, true) == 616);
    assert(CurrencySystem::calculate_run_payout(-20, -3, false) == 40);
    const int initial_prana = CurrencySystem::instance().prana_shards();
    assert(!CurrencySystem::instance().spend_prana_shards(-1));
    assert(CurrencySystem::instance().prana_shards() == initial_prana);
    assert(!CurrencySystem::instance().try_unlock_ship_with_prana("not-a-real-ship", 1000));
    ConsumableInventory capped_inventory;
    capped_inventory.kavach_charges = 3;
    capped_inventory.soma_vials = 5;
    capped_inventory.vajra_flares = 5;
    CurrencySystem::instance().set_prana_shards(10000);
    assert(!CurrencySystem::instance().buy_consumable(capped_inventory, "kavach"));
    assert(!CurrencySystem::instance().buy_consumable(capped_inventory, "soma"));
    assert(!CurrencySystem::instance().buy_consumable(capped_inventory, "vajra"));
    assert(CurrencySystem::instance().prana_shards() == 10000);

    InputPacket input;
    input.move_x = 4.0f;
    input.move_y = -2.0f;
    input.aim_x = -20.0f;
    input.aim_y = 9999.0f;
    assert(NetworkManager::sanitize_input_packet(input));
    assert(input.move_x == 1.0f && input.move_y == -1.0f);
    assert(input.aim_x == 0.0f && input.aim_y == static_cast<float>(SCREEN_HEIGHT));
    input.move_x = std::numeric_limits<float>::quiet_NaN();
    assert(!NetworkManager::sanitize_input_packet(input));
    assert(NetworkManager::sequence_is_newer(0, UINT32_MAX));
    assert(!NetworkManager::sequence_is_newer(10, 10));
    SnapshotPacket snapshot;
    assert(NetworkManager::validate_snapshot(snapshot));
    snapshot.players[0].pos_x = std::numeric_limits<float>::infinity();
    assert(!NetworkManager::validate_snapshot(snapshot));

    // Exercise both local pilots through the same input-to-gameplay path used
    // by the keyboard sampler, without requiring a live keyboard/window.
    std::vector<Player> local_squad(2);
    local_squad[0].init(GetShipArchetype("pushpaka"));
    local_squad[1].init(GetShipArchetype("tripura"));
    local_squad[0].player_id = 0;
    local_squad[1].player_id = 1;
    local_squad[0].hp -= 40;
    local_squad[1].hp -= 40;
    const int p1_dash_before = local_squad[0].dash_charges;
    const int p2_dash_before = local_squad[1].dash_charges;
    const int p1_hp_before = local_squad[0].hp;
    const int p2_hp_before = local_squad[1].hp;
    HumanController p1_controller(0);
    HumanController p2_controller(1);
    PlayerControlInput p1_input;
    p1_input.move = { 1.0f, 0.0f };
    p1_input.aim = { SCREEN_WIDTH, SCREEN_HEIGHT * 0.75f };
    p1_input.fire = p1_input.dash = p1_input.chakram = p1_input.use_soma = p1_input.use_vajra = true;
    PlayerControlInput p2_input;
    p2_input.move = { -1.0f, 0.0f };
    p2_input.fire = p2_input.dash = p2_input.chakram = p2_input.use_soma = p2_input.use_vajra = true;
    std::vector<Bullet> coop_bullets;
    p1_controller.update_from_input(1.0f / 60.0f, local_squad[0], coop_bullets, local_squad, p1_input);
    p2_controller.update_from_input(1.0f / 60.0f, local_squad[1], coop_bullets, local_squad, p2_input);
    local_squad[0].update(1.0f / 60.0f);
    local_squad[1].update(1.0f / 60.0f);
    assert(local_squad[0].pos.x > SCREEN_WIDTH / 2.0f);
    assert(local_squad[1].pos.x < SCREEN_WIDTH / 2.0f);
    assert(local_squad[0].is_dashing && local_squad[1].is_dashing);
    assert(local_squad[0].dash_charges == p1_dash_before - 1);
    assert(local_squad[1].dash_charges == p2_dash_before - 1);
    assert(local_squad[0].hp > p1_hp_before && local_squad[1].hp > p2_hp_before);
    assert(local_squad[0].inventory.soma_vials == 0 && local_squad[1].inventory.soma_vials == 0);
    assert(local_squad[0].inventory.vajra_flares == 0 && local_squad[1].inventory.vajra_flares == 0);
    assert(coop_bullets.size() >= 50);
    for (const auto& bullet : coop_bullets) {
        assert(bullet.is_player_owned);
        assert(bullet.owner_player_id < 2);
        assert(std::isfinite(bullet.vel.x) && std::isfinite(bullet.vel.y));
    }

    // Downed pilots can crawl but cannot fire or spend abilities.
    local_squad[0].is_downed = true;
    const auto shots_before_downed_input = local_squad[0].shots_fired;
    const auto bullets_before_downed_input = coop_bullets.size();
    p1_controller.update_from_input(1.0f / 60.0f, local_squad[0], coop_bullets, local_squad, p1_input);
    assert(local_squad[0].vel.x == 40.0f && local_squad[0].vel.y == 0.0f);
    assert(local_squad[0].shots_fired == shots_before_downed_input);
    assert(coop_bullets.size() == bullets_before_downed_input);

    // Existing SQLite score rows survive the death-cause schema migration and
    // a second migration pass is harmless.
    sqlite3* memory_db = nullptr;
    assert(sqlite3_open(":memory:", &memory_db) == SQLITE_OK);
    assert(sqlite3_exec(memory_db,
        "CREATE TABLE scores (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT NOT NULL, score INTEGER NOT NULL, "
        "level_reached INTEGER NOT NULL, difficulty TEXT DEFAULT 'normal', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        "ship_class TEXT DEFAULT 'pushpaka', kills INTEGER DEFAULT 0, total_damage INTEGER DEFAULT 0, duration_seconds REAL DEFAULT 0);"
        "INSERT INTO scores (id, player_name, score, level_reached) VALUES (1, 'legacy-pilot', 100, 1);",
        nullptr, nullptr, nullptr) == SQLITE_OK);
    assert(DBSystem::ensure_death_cause_column(memory_db));
    assert(DBSystem::ensure_death_cause_column(memory_db));
    sqlite3_stmt* legacy_row = nullptr;
    assert(sqlite3_prepare_v2(memory_db, "SELECT id, death_cause FROM scores;", -1, &legacy_row, nullptr) == SQLITE_OK);
    assert(sqlite3_step(legacy_row) == SQLITE_ROW);
    assert(sqlite3_column_int(legacy_row, 0) == 1);
    const auto* migrated_cause = sqlite3_column_text(legacy_row, 1);
    assert(migrated_cause && std::string(reinterpret_cast<const char*>(migrated_cause)).empty());
    sqlite3_finalize(legacy_row);
    ScoreEntry recorded;
    recorded.player_name = "audit-pilot";
    recorded.score = 12345;
    recorded.level_reached = 29;
    recorded.difficulty = "asura_slayer";
    recorded.ship_class = "garuda";
    recorded.kills = 40;
    recorded.total_damage = 777;
    recorded.duration_seconds = 91.5f;
    recorded.death_cause = "Prince Indrajit";
    assert(DBSystem::insert_score_record(memory_db, recorded));
    sqlite3_stmt* recorded_row = nullptr;
    assert(sqlite3_prepare_v2(memory_db,
        "SELECT score, level_reached, difficulty, ship_class, death_cause FROM scores WHERE player_name = ?;",
        -1, &recorded_row, nullptr) == SQLITE_OK);
    sqlite3_bind_text(recorded_row, 1, recorded.player_name.c_str(), -1, SQLITE_TRANSIENT);
    assert(sqlite3_step(recorded_row) == SQLITE_ROW);
    assert(sqlite3_column_int(recorded_row, 0) == recorded.score);
    assert(sqlite3_column_int(recorded_row, 1) == recorded.level_reached);
    assert(std::string(reinterpret_cast<const char*>(sqlite3_column_text(recorded_row, 2))) == recorded.difficulty);
    assert(std::string(reinterpret_cast<const char*>(sqlite3_column_text(recorded_row, 3))) == recorded.ship_class);
    assert(std::string(reinterpret_cast<const char*>(sqlite3_column_text(recorded_row, 4))) == recorded.death_cause);
    sqlite3_finalize(recorded_row);
    sqlite3_close(memory_db);

    // Exercise JSON save/load and corrupt-save backup under an isolated profile
    // directory so the audit never reads or overwrites a real player's save.
    const char* old_profile_value = std::getenv("USERPROFILE");
    const std::string old_profile = old_profile_value ? old_profile_value : "";
    const auto audit_save_root = std::filesystem::temp_directory_path() /
        ("vimana-wars-audit-" + std::to_string(std::chrono::steady_clock::now().time_since_epoch().count()));
    std::filesystem::create_directories(audit_save_root);
    assert(_putenv_s("USERPROFILE", audit_save_root.string().c_str()) == 0);
    auto& save_db = DBSystem::instance();
    save_db.set_player_name("audit-save-pilot");
    assert(DBSystem::calculate_pilot_xp(2345, 7, false) == 160);
    assert(DBSystem::calculate_pilot_xp(2345, 7, true) == 410);
    save_db.add_pilot_xp(1250);
    const int saved_pilot_xp = save_db.pilot_xp();
    assert(save_db.pilot_level() == 1 + saved_pilot_xp / DBSystem::PILOT_XP_PER_LEVEL);
    assert(save_db.pilot_xp_progress() == saved_pilot_xp % DBSystem::PILOT_XP_PER_LEVEL);
    save_db.update_high_score(765432);
    save_db.update_max_wave(36);
    save_db.set_continue_wave(18);
    save_db.set_tutorial_shown(true);
    assert(save_db.set_equipped_ship("tripura"));
    save_db.set_coop_rule(CoopRule::SQUAD_LIVES);
    ConsumableInventory saved_armory;
    saved_armory.kavach_charges = 2;
    saved_armory.soma_vials = 3;
    saved_armory.vajra_flares = 4;
    save_db.set_armory_inventory(saved_armory);
    CurrencySystem::instance().set_prana_shards(1234);
    CurrencySystem::instance().set_unlocked_ships({ "pushpaka", "tripura", "audit-ship" });
    CurrencySystem::instance().set_ship_upgrade_levels({ { "garuda", 3 } });
    CurrencySystem::instance().set_ship_sortie_counts({ { "garuda", 17 } });
    CurrencySystem::instance().set_ship_last_death_causes({ { "garuda", "audit boss" } });
    SoundSystem::instance().set_master_volume(0.37f);
    SoundSystem::instance().set_sfx_volume(0.41f);
    SoundSystem::instance().set_music_volume(0.52f);
    SoundSystem::instance().set_ui_volume(0.63f);
    SoundSystem::instance().set_boss_volume(0.74f);
    g_colorblind_mode = true;
    g_screen_shake_enabled = false;
    g_scanlines_enabled = true;
    g_fullscreen_enabled = true;
    save_db.save_game();

    save_db.set_player_name("changed");
    save_db.add_pilot_xp(350);
    save_db.set_continue_wave(1);
    save_db.set_tutorial_shown(false);
    assert(save_db.set_equipped_ship("pushpaka"));
    save_db.set_coop_rule(CoopRule::HARDCORE);
    save_db.set_armory_inventory(ConsumableInventory{});
    CurrencySystem::instance().set_prana_shards(1);
    CurrencySystem::instance().set_unlocked_ships({ "pushpaka" });
    CurrencySystem::instance().set_ship_upgrade_levels({});
    CurrencySystem::instance().set_ship_sortie_counts({});
    CurrencySystem::instance().set_ship_last_death_causes({});
    SoundSystem::instance().set_master_volume(0.0f);
    SoundSystem::instance().set_sfx_volume(0.0f);
    SoundSystem::instance().set_music_volume(0.0f);
    SoundSystem::instance().set_ui_volume(0.0f);
    SoundSystem::instance().set_boss_volume(0.0f);
    g_colorblind_mode = false;
    g_screen_shake_enabled = true;
    g_scanlines_enabled = false;
    g_fullscreen_enabled = false;
    save_db.load_save_game();
    assert(save_db.player_name() == "audit-save-pilot");
    assert(save_db.pilot_xp() == saved_pilot_xp);
    assert(save_db.high_score() == 765432 && save_db.max_wave() == 36 && save_db.continue_wave() == 18);
    assert(save_db.tutorial_shown() && CurrencySystem::instance().prana_shards() == 1234);
    assert(save_db.equipped_ship() == "tripura");
    assert(save_db.coop_rule() == CoopRule::SQUAD_LIVES);
    assert(save_db.armory_inventory().kavach_charges == 2);
    assert(save_db.armory_inventory().soma_vials == 3);
    assert(save_db.armory_inventory().vajra_flares == 4);
    assert(CurrencySystem::instance().unlocked_ships().size() == 3);
    assert(CurrencySystem::instance().ship_upgrade_level("garuda") == 3);
    assert(CurrencySystem::instance().ship_sorties("garuda") == 17);
    assert(CurrencySystem::instance().ship_last_death_causes().at("garuda") == "audit boss");
    assert(SoundSystem::instance().master_volume() == 0.37f);
    assert(SoundSystem::instance().sfx_volume() == 0.41f);
    assert(SoundSystem::instance().music_volume() == 0.52f);
    assert(SoundSystem::instance().ui_volume() == 0.63f);
    assert(SoundSystem::instance().boss_volume() == 0.74f);
    assert(g_colorblind_mode && !g_screen_shake_enabled && g_scanlines_enabled && g_fullscreen_enabled);

    const auto audit_save_path = audit_save_root / ".vimana_wars" / "save.json";
    {
        std::ofstream corrupt_save(audit_save_path, std::ios::trunc);
        corrupt_save << "{ invalid json";
    }
    save_db.load_save_game();
    bool corrupt_backup_found = false;
    for (const auto& entry : std::filesystem::directory_iterator(audit_save_path.parent_path())) {
        if (entry.path().filename().string().find("save.json.corrupt.") == 0 &&
            std::filesystem::file_size(entry.path()) > 0) {
            corrupt_backup_found = true;
            break;
        }
    }
    assert(corrupt_backup_found);
    assert(_putenv_s("USERPROFILE", old_profile.c_str()) == 0);
    std::error_code cleanup_error;
    std::filesystem::remove_all(audit_save_root, cleanup_error);
    assert(!cleanup_error);

    // Continue restores the precise unlocked wave instead of jumping to the
    // selected realm's first wave.
    DBSystem::instance().update_max_wave(35);
    DBSystem::instance().set_continue_wave(34);
    CampaignMapView campaign;
    assert(campaign.selected_realm_id() == 2);
    assert(campaign.starting_wave() == 34);

    // Registry integrity: all advertised ships have unique IDs and usable stats.
    assert(SHIP_FLEET.size() == 62);
    assert(GetShipArchetype("amogha_lancer")->sprite_file == "phase9_commander_ship_49.png");
    assert(GetShipArchetype("nandi_aegis")->sprite_file == "phase9_commander_ship_50.png");
    assert(ShipSignatureName(*GetShipArchetype("amogha_lancer")) == "Needle Thread");
    assert(ShipSignatureName(*GetShipArchetype("nandi_aegis")) == "Living Aegis");
    Player amogha;
    amogha.init(GetShipArchetype("amogha_lancer"));
    const int amogha_base_damage = amogha.bullet_damage;
    std::vector<Bullet> amogha_shots;
    for (int shot = 0; shot < 10; ++shot) {
        amogha.shoot_timer = 0.0f;
        amogha.try_shoot(amogha_shots);
    }
    assert(amogha_shots.size() == 10);
    for (const size_t needle_index : { 4u, 9u }) {
        assert(amogha_shots[needle_index].damage == static_cast<int>(std::round(amogha_base_damage * 1.25f)));
        assert(amogha_shots[needle_index].pierce_remaining == 8);
    }
    Player nandi;
    nandi.init(GetShipArchetype("nandi_aegis"));
    nandi.update(10.0f);
    assert(nandi.has_kavach_shield && nandi.kavach_timer > 1.9f);
    std::unordered_set<std::string> ship_ids;
    for (const auto& ship : SHIP_FLEET) {
        assert(!ship.id.empty());
        assert(!ship.name.empty());
        assert(ship.max_hp > 0);
        assert(ship.speed > 0.0f);
        assert(ship_ids.insert(ship.id).second);
        assert(GetShipArchetype(ship.id) != nullptr);

        Player firing_ship;
        firing_ship.init(&ship);
        std::vector<Bullet> ship_shots;
        firing_ship.try_shoot(ship_shots);
        assert(!ship_shots.empty());
        assert(firing_ship.shots_fired > 0);
        for (const auto& bullet : ship_shots) {
            assert(bullet.is_player_owned);
            assert(std::isfinite(bullet.pos.x) && std::isfinite(bullet.pos.y));
            assert(std::isfinite(bullet.vel.x) && std::isfinite(bullet.vel.y));
        }
    }

    // Difficulty smoke: enemy totals and the same boss archetype's HP scale in
    // the intended direction, while every spawned enemy remains valid.
    constexpr std::array<Difficulty, 4> difficulties = {
        Difficulty::NOVICE, Difficulty::KSHATRIYA,
        Difficulty::ASURA_SLAYER, Difficulty::CHAKRAVYUHA
    };
    int previous_goal = 0;
    int first_goal = 0;
    int previous_boss_hp = 0;
    for (const Difficulty difficulty : difficulties) {
        WaveManager difficulty_waves;
        difficulty_waves.start_campaign(12, difficulty, 1);
        const int goal = difficulty_waves.wave_enemy_goal();
        if (first_goal == 0) first_goal = goal;
        assert(goal >= previous_goal && goal <= 180);
        previous_goal = goal;
        std::vector<Enemy> difficulty_enemies;
        std::vector<Bullet> difficulty_bullets;
        for (int i = 0; i < goal; ++i) {
            difficulty_waves.update(10.0f, difficulty_enemies, difficulty_bullets, { 450.0f, 500.0f });
        }
        assert(static_cast<int>(difficulty_enemies.size()) == goal);
        for (const auto& enemy : difficulty_enemies) {
            assert(enemy.active && enemy.hp > 0 && enemy.max_hp >= enemy.hp);
            assert(std::isfinite(enemy.speed) && enemy.speed > 0.0f);
        }

        difficulty_waves.prepare_wave(30);
        const int boss_hp = difficulty_waves.get_boss().max_hp;
        assert(difficulty_waves.is_boss_wave() && boss_hp > previous_boss_hp);
        previous_boss_hp = boss_hp;
    }
    assert(previous_goal > first_goal);

    // Every boss archetype initializes and remains inside its phase speed ceiling
    // after the strongest act scaling.
    constexpr std::array<BossID, 8> boss_ids = {
        BossID::KUMBHAKARNA, BossID::RAVANA, BossID::MAHISHASURA, BossID::MAKARA,
        BossID::INDRAJIT, BossID::HIRANYAKASHIPU, BossID::MEGHNADA, BossID::VRITRA
    };
    for (const BossID id : boss_ids) {
        for (int phase = 1; phase <= 3; ++phase) {
            Boss boss;
            boss.init(id);
            boss.phase = phase;
            boss.scale_for_act(10, 1.0f, 1.0f);
            const float speed_ceiling = phase == 1 ? 180.0f : phase == 2 ? 200.0f : 220.0f;
            assert(boss.active);
            assert(!boss.name.empty());
            assert(boss.max_hp > 0);
            assert(boss.speed <= speed_ceiling);
        }

        Boss combat_boss;
        combat_boss.init(id);
        combat_boss.pos = { 450.0f, 200.0f };
        combat_boss.attack_timer = 0.5f;
        combat_boss.special_timer = 10.0f;
        const Vector2 target = { 415.0f, 460.0f };
        std::vector<Bullet> boss_bullets;
        combat_boss.update(0.01f, target, boss_bullets);
        assert(combat_boss.is_telegraphing);
        assert(combat_boss.telegraph_target.x == target.x);
        assert(combat_boss.telegraph_target.y == target.y);
        assert(!combat_boss.telegraph_warning.empty());

        combat_boss.attack_timer = 0.001f;
        combat_boss.update(0.01f, target, boss_bullets);
        assert(!combat_boss.is_telegraphing);
        assert(!boss_bullets.empty());
        for (const auto& bullet : boss_bullets) {
            assert(bullet.is_enemy);
            assert(std::string(bullet.damage_source) != "Unknown hostile");
        }
    }

    Boss overlap_telegraph;
    overlap_telegraph.init(BossID::RAVANA);
    overlap_telegraph.pos.y = overlap_telegraph.target_y;
    overlap_telegraph.attack_timer = 0.5f;
    overlap_telegraph.special_timer = 0.8f;
    const std::string special_warning = overlap_telegraph.attack_name;
    std::vector<Bullet> overlapping_bullets;
    overlap_telegraph.update(0.01f, { 400.0f, 460.0f }, overlapping_bullets);
    assert(overlap_telegraph.is_telegraphing);
    assert(overlap_telegraph.telegraph_warning == special_warning);

    Boss damage_test;
    damage_test.init(BossID::RAVANA);
    const int boss_hp_before = damage_test.hp;
    damage_test.is_invincible = true;
    damage_test.invincibility_timer = 0.5f;
    assert(damage_test.take_damage(100) == 0);
    assert(damage_test.hp == boss_hp_before);
    damage_test.is_invincible = false;
    damage_test.invincibility_timer = 0.0f;
    assert(damage_test.take_damage(100) == 100);
    assert(damage_test.hp == boss_hp_before - 100);

    // Authored post-tutorial formations have deterministic multi-enemy queues;
    // Act I wave 10 remains the boss + escort encounter.
    constexpr std::array<int, 4> staged_waves = { 6, 7, 8, 9 };
    constexpr std::array<int, 4> staged_counts = { 15, 15, 15, 18 };
    WaveManager waves;
    std::vector<Enemy> spawned_enemies;
    std::vector<Bullet> spawned_bullets;
    for (size_t i = 0; i < staged_waves.size(); ++i) {
        spawned_enemies.clear();
        spawned_bullets.clear();
        waves.prepare_wave(staged_waves[i]);
        assert(waves.current_wave() == staged_waves[i]);
        assert(!waves.is_boss_wave());
        assert(waves.wave_enemy_goal() == staged_counts[i]);
        assert(static_cast<int>(waves.queued_spawn_count()) == staged_counts[i]);
        assert(!waves.is_wave_cleared());
        for (int spawn = 0; spawn < staged_counts[i]; ++spawn) {
            waves.update(10.0f, spawned_enemies, spawned_bullets, { 450.0f, 500.0f });
        }
        assert(static_cast<int>(spawned_enemies.size()) == staged_counts[i]);
        for (const auto& enemy : spawned_enemies) assert(enemy.active && enemy.hp > 0);
        if (staged_waves[i] == 8) {
            bool found_miniboss = false;
            for (const auto& enemy : spawned_enemies)
                found_miniboss = found_miniboss || (enemy.is_miniboss && enemy.miniboss_name == "RIFT MAULER");
            assert(found_miniboss);
        }
    }

    // Mini-boss roster encounters recur in later acts and use distinct volleys.
    for (const int wave : { 18, 28, 278 }) {
        WaveManager miniboss_wave;
        miniboss_wave.start_campaign(wave, Difficulty::KSHATRIYA, 1);
        std::vector<Enemy> miniboss_enemies;
        std::vector<Bullet> miniboss_bullets;
        const int goal = miniboss_wave.wave_enemy_goal();
        for (int i = 0; i < goal; ++i)
            miniboss_wave.update(10.0f, miniboss_enemies, miniboss_bullets, { SCREEN_WIDTH * 0.5f, SCREEN_HEIGHT * 0.75f });
        bool found_miniboss = false;
        for (const auto& enemy : miniboss_enemies) found_miniboss = found_miniboss || enemy.is_miniboss;
        assert(found_miniboss);
    }
    for (const auto& spec : std::array<std::pair<EnemyType, const char*>, 3>{{
             { EnemyType::ASURA_TANK, "RIFT MAULER" },
             { EnemyType::ASURA_SNIPER, "SILENCE WARDEN" },
             { EnemyType::ASURA_SHOOTER, "EMBER TYRANT" } }}) {
        Enemy miniboss;
        miniboss.init(spec.first, { SCREEN_WIDTH * 0.5f, 150.0f }, 1.0f, 1.0f, true, true);
        miniboss.miniboss_name = spec.second;
        miniboss.shoot_timer = 0.01f;
        std::vector<Bullet> volley;
        std::vector<Enemy> no_allies;
        miniboss.update(0.02f, { SCREEN_WIDTH * 0.5f, 450.0f }, volley, no_allies);
        const size_t expected_volley = spec.first == EnemyType::ASURA_TANK ? 5u : 3u;
        assert(volley.size() == expected_volley);
        assert(std::string(volley.front().damage_source) == miniboss.damage_source_name());
    }
    spawned_enemies.clear();
    waves.prepare_wave(10);
    assert(waves.is_boss_wave());
    assert(waves.get_boss().active);
    assert(waves.wave_enemy_goal() >= 5);
    assert(waves.queued_spawn_count() >= 5);
    assert(!waves.is_wave_cleared());
    const size_t boss_escort_count = waves.queued_spawn_count();
    for (size_t spawn = 0; spawn < boss_escort_count; ++spawn) {
        waves.update(10.0f, spawned_enemies, spawned_bullets, { 450.0f, 500.0f });
    }
    assert(static_cast<int>(spawned_enemies.size()) == waves.wave_enemy_goal());

    std::cout << "Audit smoke passed: campaign lore, all realm modifier hooks, signature ships, SQLite/JSON, networking, "
                 "mini-boss encounters, 62 ship weapons, four difficulty scales, boss combat, waves 6–10.\n";
    return 0;
}
