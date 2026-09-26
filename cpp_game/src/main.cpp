#include <memory>
#include <algorithm>
#include <exception>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "systems/db_system.hpp"
#include "systems/network_manager.hpp"
#include "systems/account_system.hpp"
#include "systems/achievement_system.hpp"
#include "systems/transition_manager.hpp"
#include "ui/debug_overlay.hpp"
#include "views/boot_view.hpp"
#include "views/pilot_setup_view.hpp"
#include "views/auth_view.hpp"
#include "views/menu_view.hpp"
#include "views/campaign_map_view.hpp"
#include "views/loadout_view.hpp"
#include "views/mission_briefing_view.hpp"
#include "views/ship_select_view.hpp"
#include "views/difficulty_view.hpp"
#include "views/game_view.hpp"
#include "views/wave_clear_view.hpp"
#include "views/codex_view.hpp"
#include "views/duel_view.hpp"
#include "views/boon_select_view.hpp"
#include "views/leaderboard_view.hpp"
#include "views/multiplayer_view.hpp"
#include "views/multiplayer_result_view.hpp"
#include "views/profile_view.hpp"
#include "views/achievements_view.hpp"
#include "views/settings_view.hpp"
#include "views/game_over_view.hpp"

using namespace Vimana;

int main() {
    try {
    // 1. Initialize Raylib Window
    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT);
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE);
    SetTargetFPS(TARGET_FPS);

    // Raylib's default exit key is ESC — which would steal our pause toggle.
    // Disable it so ESC can drive the in-game pause menu instead.
    SetExitKey(KEY_NULL);

    // 2. Initialize Engine Systems
    SoundSystem::instance().init();
    AssetManager::instance().init();
    DBSystem::instance().init();
    if (g_fullscreen_enabled && !IsWindowFullscreen()) ToggleFullscreen();
    NetworkManager::instance().init();
    AccountSystem::instance().init();
    AchievementSystem::instance().init();

    // 3. Render Texture for 900x600 Logical Scaling
    RenderTexture2D target = LoadRenderTexture(SCREEN_WIDTH, SCREEN_HEIGHT);
    SetTextureFilter(target.texture, TEXTURE_FILTER_BILINEAR);

    // 4. Instantiate Views
    auto boot_view = std::make_unique<BootView>();
    auto title_view = std::make_unique<TitleView>();
    auto pilot_setup_view = std::make_unique<PilotSetupView>();
    auto auth_view = std::make_unique<AuthView>();
    auto menu_view = std::make_unique<MenuView>();
    auto campaign_map_view = std::make_unique<CampaignMapView>();
    auto loadout_view = std::make_unique<LoadoutView>();
    auto mission_briefing_view = std::make_unique<MissionBriefingView>();
    auto ship_select_view = std::make_unique<ShipSelectView>();
    auto difficulty_view = std::make_unique<DifficultyView>();
    auto game_view = std::make_unique<GameView>();
    auto wave_clear_view = std::make_unique<WaveClearView>();
    auto codex_view = std::make_unique<CodexView>();
    auto duel_view = std::make_unique<DuelView>();
    auto boon_view = std::make_unique<BoonSelectView>();
    auto leaderboard_view = std::make_unique<LeaderboardView>();
    auto multiplayer_view = std::make_unique<MultiplayerView>();
    auto multiplayer_result_view = std::make_unique<MultiplayerResultView>();
    auto profile_view = std::make_unique<ProfileView>();
    auto achievements_view = std::make_unique<AchievementsView>();
    auto settings_view = std::make_unique<SettingsView>();
    auto game_over_view = std::make_unique<GameOverView>(false);

    // Starting screen: BOOT splash
    ViewType current_view_type = ViewType::BOOT;
    IView* current_view = boot_view.get();

    // 5. Master Game Loop (QUIT breaks for safe teardown in section 6)
    bool quit_requested = false;
    while (!WindowShouldClose() && !quit_requested) {
        const float frame_dt = GetFrameTime();
        float dt = frame_dt;
        if (dt > 0.1f) dt = 0.1f; // Cap delta time against hitches

        if (IsKeyPressed(KEY_F11)) {
            ToggleFullscreen();
            g_fullscreen_enabled = IsWindowFullscreen();
            DBSystem::instance().save_game();
        }

        SoundSystem::instance().update_music();
        DebugOverlay::instance().update(frame_dt);
        AccountSystem::instance().update();
        AchievementSystem::instance().update(dt);

        // Calculate aspect ratio scaling
        float scale = std::min(static_cast<float>(GetScreenWidth()) / SCREEN_WIDTH,
                               static_cast<float>(GetScreenHeight()) / SCREEN_HEIGHT);
        float offset_x = (GetScreenWidth() - (SCREEN_WIDTH * scale)) * 0.5f;
        float offset_y = (GetScreenHeight() - (SCREEN_HEIGHT * scale)) * 0.5f;

        // Virtual mouse position inside 900x600 logical canvas
        Vector2 mouse = GetMousePosition();
        Vector2 virtual_mouse = {
            (mouse.x - offset_x) / scale,
            (mouse.y - offset_y) / scale
        };

        // Lambda to perform view initialization and pointer switch
        auto switch_to_view = [&](ViewType next) {
            if (next == ViewType::BOOT) {
                boot_view->init();
                current_view = boot_view.get();
            } else if (next == ViewType::TITLE) {
                title_view->init();
                current_view = title_view.get();
            } else if (next == ViewType::PILOT_SETUP) {
                pilot_setup_view->init();
                current_view = pilot_setup_view.get();
            } else if (next == ViewType::AUTH) {
                auth_view->init();
                current_view = auth_view.get();
            } else if (next == ViewType::MENU) {
                // If returning from title on a fresh profile, prompt callsign setup
                if (current_view_type == ViewType::TITLE && DBSystem::instance().player_name() == "Warrior" && !AccountSystem::instance().is_logged_in()) {
                    pilot_setup_view->init();
                    current_view = pilot_setup_view.get();
                    next = ViewType::PILOT_SETUP;
                } else {
                    menu_view->init();
                    current_view = menu_view.get();
                }
            } else if (next == ViewType::CAMPAIGN_MAP) {
                campaign_map_view->init();
                current_view = campaign_map_view.get();
            } else if (next == ViewType::PROFILE) {
                profile_view->init();
                current_view = profile_view.get();
            } else if (next == ViewType::ACHIEVEMENTS) {
                achievements_view->init();
                current_view = achievements_view.get();
            } else if (next == ViewType::LOADOUT) {
                if (current_view_type == ViewType::CAMPAIGN_MAP) {
                    loadout_view->set_mission_target(campaign_map_view->starting_wave(), &ship_select_view->selected_ship(), ship_select_view->consumables());
                } else if (current_view_type == ViewType::DIFFICULTY_SELECT) {
                    loadout_view->set_mission_target(difficulty_view->starting_wave(), &ship_select_view->selected_ship(), ship_select_view->consumables());
                } else if (current_view_type == ViewType::SHIP_SELECT) {
                    loadout_view->set_mission_target(loadout_view->starting_wave(), &ship_select_view->selected_ship(), ship_select_view->consumables());
                }
                loadout_view->init();
                current_view = loadout_view.get();
            } else if (next == ViewType::MISSION_BRIEFING) {
                mission_briefing_view->set_mission(loadout_view->starting_wave(),
                                                   &loadout_view->selected_ship(),
                                                   difficulty_view->selected_difficulty());
                mission_briefing_view->init();
                current_view = mission_briefing_view.get();
            } else if (next == ViewType::SHIP_SELECT) {
                const bool from_campaign_flow = current_view_type == ViewType::CAMPAIGN_MAP ||
                    current_view_type == ViewType::DIFFICULTY_SELECT || current_view_type == ViewType::LOADOUT;
                ship_select_view->set_return_view(from_campaign_flow ? ViewType::LOADOUT : ViewType::MENU);
                ship_select_view->init();
                current_view = ship_select_view.get();
            } else if (next == ViewType::CODEX) {
                codex_view->init();
                current_view = codex_view.get();
            } else if (next == ViewType::DIFFICULTY_SELECT) {
                if (current_view_type == ViewType::CAMPAIGN_MAP) {
                    difficulty_view->set_starting_wave(campaign_map_view->starting_wave());
                }
                difficulty_view->init();
                // preserve pending wave across init (init must not reset it)
                if (current_view_type == ViewType::CAMPAIGN_MAP) {
                    // re-apply after init in case init clears state
                    difficulty_view->set_starting_wave(campaign_map_view->starting_wave());
                }
                current_view = difficulty_view.get();
            } else if (next == ViewType::GAMEPLAY) {
                if (current_view_type == ViewType::LOADOUT || current_view_type == ViewType::MISSION_BRIEFING) {
                    game_view->start_with_ship(&loadout_view->selected_ship(), loadout_view->inventory(), loadout_view->starting_wave(), difficulty_view->selected_difficulty(), 1);
                } else if (current_view_type == ViewType::SHIP_SELECT) {
                    game_view->start_with_ship(&ship_select_view->selected_ship(), ship_select_view->consumables(), 1, difficulty_view->selected_difficulty(), 1);
                } else if (current_view_type == ViewType::BOON_SELECT) {
                    game_view->apply_boon_and_resume(boon_view->chosen_boon());
                } else if (current_view_type == ViewType::MULTIPLAYER_LOBBY) {
                    int num_squad = NetworkManager::instance().players().empty() ? 2 : static_cast<int>(NetworkManager::instance().players().size());
                    game_view->start_with_ship(&ship_select_view->selected_ship(), ship_select_view->consumables(), 1,
                                               difficulty_view->selected_difficulty(), num_squad, DBSystem::instance().coop_rule());
                }
                current_view = game_view.get();
            } else if (next == ViewType::WAVE_CLEAR) {
                bool act_cleared = (CampaignWaveWithinAct(game_view->current_wave()) == WAVES_PER_ACT);
                bool campaign_complete = act_cleared && CampaignActForWave(game_view->current_wave()) >= static_cast<int>(CAMPAIGN_REALMS.size());
                if (act_cleared && game_view->difficulty() == Difficulty::CHAKRAVYUHA) {
                    AchievementSystem::instance().check_and_award("IRON_MODE");
                }
                if (campaign_complete) {
                    game_view->record_ship_mastery();
                    AccountSystem::instance().sync_profile();
                }
                wave_clear_view->set_results(game_view->latest_wave_result(), act_cleared, campaign_complete);
                wave_clear_view->init();
                current_view = wave_clear_view.get();
            } else if (next == ViewType::BOON_SELECT) {
                boon_view->set_player_boons(game_view->player().boons);
                boon_view->init();
                current_view = boon_view.get();
            } else if (next == ViewType::DUEL) {
                duel_view->init();
                current_view = duel_view.get();
            } else if (next == ViewType::LEADERBOARD) {
                leaderboard_view->init();
                current_view = leaderboard_view.get();
            } else if (next == ViewType::MULTIPLAYER_LOBBY) {
                multiplayer_view->init();
                current_view = multiplayer_view.get();
            } else if (next == ViewType::MULTIPLAYER_RESULT) {
                multiplayer_result_view->set_results(
                    game_view->current_wave() >= WAVES_PER_ACT * static_cast<int>(CAMPAIGN_REALMS.size()),
                    game_view->total_team_score(),
                    game_view->squad()
                );
                multiplayer_result_view->init();
                current_view = multiplayer_result_view.get();
            } else if (next == ViewType::SETTINGS) {
                settings_view->init();
                current_view = settings_view.get();
            } else if (next == ViewType::GAME_OVER || next == ViewType::VICTORY) {
                bool is_vic = (next == ViewType::VICTORY);
                const auto& p = game_view->player();
                int pilot_xp_reward = 0;
                const int prana_reward = game_view->grant_run_completion_reward(is_vic, pilot_xp_reward);
                game_over_view->set_results(is_vic, p.score, game_view->current_wave(), p.kills, p.total_damage_dealt,
                                            p.archetype ? p.archetype->name : "Pushpaka",
                                            game_view->run_duration(), game_view->difficulty_string(),
                                            is_vic ? "" : game_view->death_cause(), prana_reward, pilot_xp_reward);
                game_over_view->set_killed_by(is_vic ? "" : game_view->death_cause());
                if (DBSystem::instance().fetch_match_history(10).size() >= 10) {
                    AchievementSystem::instance().check_and_award("PLAY_10");
                }
                current_view = game_over_view.get();
            }

            current_view_type = next;
        };

        // Update active view
        if (current_view) {
            current_view->update(dt, virtual_mouse);
            ViewType next = current_view->next_view();

            if (next == ViewType::QUIT) {
                quit_requested = true;
                continue;
            }

            if (next != current_view_type) {
                current_view->reset_next_view();

                // Instant switch for Boon Selection within combat
                if (next == ViewType::BOON_SELECT || (current_view_type == ViewType::BOON_SELECT && next == ViewType::GAMEPLAY)) {
                    switch_to_view(next);
                } else {
                    TransitionManager::instance().start_transition(next, 0.22f);
                }
            }
        }

        // Check if transition manager has reached midpoint to trigger switch
        ViewType target_to_switch;
        if (TransitionManager::instance().update(dt, target_to_switch)) {
            switch_to_view(target_to_switch);
        }

        // Render to 900x600 virtual canvas
        BeginTextureMode(target);
        if (current_view) {
            current_view->draw();
        }
        AchievementSystem::instance().draw_toast(AssetManager::instance().title_font(), AssetManager::instance().body_font());
        TransitionManager::instance().draw();
        DebugOverlay::instance().draw();
        EndTextureMode();

        // Render virtual canvas scaled to physical display with letterboxing
        BeginDrawing();
        ClearBackground(BLACK);
        Rectangle src_rec = { 0.0f, 0.0f, static_cast<float>(target.texture.width), -static_cast<float>(target.texture.height) };
        Rectangle dest_rec = { offset_x, offset_y, SCREEN_WIDTH * scale, SCREEN_HEIGHT * scale };
        DrawTexturePro(target.texture, src_rec, dest_rec, { 0, 0 }, 0.0f, WHITE);
        EndDrawing();
    }

    // 6. Cleanup Engine Systems
    UnloadRenderTexture(target);
    AssetManager::instance().cleanup();
    SoundSystem::instance().cleanup();
    DBSystem::instance().cleanup();
    CloseWindow();

    return 0;
    } catch (const std::exception& ex) {
        TraceLog(LOG_ERROR, "[Fatal] Vimana Wars stopped: %s", ex.what());
        if (IsAudioDeviceReady()) SoundSystem::instance().cleanup();
        if (IsWindowReady()) {
            AssetManager::instance().cleanup();
            CloseWindow();
        }
        return 1;
    } catch (...) {
        TraceLog(LOG_ERROR, "[Fatal] Vimana Wars stopped by an unknown error.");
        if (IsAudioDeviceReady()) SoundSystem::instance().cleanup();
        if (IsWindowReady()) {
            AssetManager::instance().cleanup();
            CloseWindow();
        }
        return 1;
    }
}
