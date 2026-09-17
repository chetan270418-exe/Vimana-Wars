#include <iostream>
#include <memory>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "systems/db_system.hpp"
#include "systems/network_manager.hpp"
#include "ui/debug_overlay.hpp"

#include "views/boot_view.hpp"
#include "views/pilot_setup_view.hpp"
#include "views/menu_view.hpp"
#include "views/campaign_map_view.hpp"
#include "views/loadout_view.hpp"
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
#include "views/settings_view.hpp"
#include "views/game_over_view.hpp"

using namespace Vimana;

int main() {
    // 1. Initialize Raylib Window
    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT);
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE);
    SetTargetFPS(TARGET_FPS);

    // 2. Initialize Engine Systems
    SoundSystem::instance().init();
    AssetManager::instance().init();
    DBSystem::instance().init();
    NetworkManager::instance().init();

    // 3. Render Texture for 900x600 Logical Scaling
    RenderTexture2D target = LoadRenderTexture(SCREEN_WIDTH, SCREEN_HEIGHT);
    SetTextureFilter(target.texture, TEXTURE_FILTER_BILINEAR);

    // 4. Instantiate Views
    auto boot_view = std::make_unique<BootView>();
    auto title_view = std::make_unique<TitleView>();
    auto pilot_setup_view = std::make_unique<PilotSetupView>();
    auto menu_view = std::make_unique<MenuView>();
    auto campaign_map_view = std::make_unique<CampaignMapView>();
    auto loadout_view = std::make_unique<LoadoutView>();
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
    auto settings_view = std::make_unique<SettingsView>();
    auto game_over_view = std::make_unique<GameOverView>(false);

    // Starting screen: BOOT splash
    ViewType current_view_type = ViewType::BOOT;
    IView* current_view = boot_view.get();

    std::cout << "[VimanaWars] C++ Master Engine Initialized. Running at 60 FPS." << std::endl;

    // 5. Master Game Loop
    while (!WindowShouldClose()) {
        float dt = GetFrameTime();
        if (dt > 0.1f) dt = 0.1f; // Cap delta time against hitches

        SoundSystem::instance().update_music();
        DebugOverlay::instance().update();

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

        // Update active view
        if (current_view) {
            current_view->update(dt, virtual_mouse);
            ViewType next = current_view->next_view();

            if (next != current_view_type) {
                current_view->reset_next_view();

                if (next == ViewType::BOOT) {
                    boot_view->init();
                    current_view = boot_view.get();
                } else if (next == ViewType::TITLE) {
                    title_view->init();
                    current_view = title_view.get();
                } else if (next == ViewType::PILOT_SETUP) {
                    pilot_setup_view->init();
                    current_view = pilot_setup_view.get();
                } else if (next == ViewType::MENU) {
                    // If returning from title on a fresh profile, prompt callsign setup
                    if (current_view_type == ViewType::TITLE && DBSystem::instance().player_name() == "Warrior") {
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
                } else if (next == ViewType::LOADOUT) {
                    if (current_view_type == ViewType::CAMPAIGN_MAP) {
                        loadout_view->set_mission_target(campaign_map_view->starting_wave(), &ship_select_view->selected_ship(), ship_select_view->consumables());
                    } else if (current_view_type == ViewType::SHIP_SELECT) {
                        loadout_view->set_mission_target(loadout_view->starting_wave(), &ship_select_view->selected_ship(), ship_select_view->consumables());
                    }
                    loadout_view->init();
                    current_view = loadout_view.get();
                } else if (next == ViewType::SHIP_SELECT) {
                    ship_select_view->set_return_view(current_view_type == ViewType::LOADOUT ? ViewType::LOADOUT : ViewType::MENU);
                    ship_select_view->init();
                    current_view = ship_select_view.get();
                } else if (next == ViewType::CODEX) {
                    codex_view->init();
                    current_view = codex_view.get();
                } else if (next == ViewType::DIFFICULTY_SELECT) {
                    difficulty_view->init();
                    current_view = difficulty_view.get();
                } else if (next == ViewType::GAMEPLAY) {
                    if (current_view_type == ViewType::LOADOUT) {
                        game_view->start_with_ship(&loadout_view->selected_ship(), loadout_view->inventory(), loadout_view->starting_wave());
                    } else if (current_view_type == ViewType::SHIP_SELECT) {
                        game_view->start_with_ship(&ship_select_view->selected_ship(), ship_select_view->consumables(), 1);
                    } else if (current_view_type == ViewType::BOON_SELECT) {
                        game_view->apply_boon_and_resume(boon_view->chosen_boon());
                    } else if (current_view_type == ViewType::MULTIPLAYER_LOBBY) {
                        game_view->start_with_ship(&ship_select_view->selected_ship(), ship_select_view->consumables(), 1);
                    }
                    current_view = game_view.get();
                } else if (next == ViewType::WAVE_CLEAR) {
                    bool is_final = (game_view->current_wave() >= 30);
                    wave_clear_view->set_results(game_view->latest_wave_result(), is_final);
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
                    multiplayer_result_view->init();
                    current_view = multiplayer_result_view.get();
                } else if (next == ViewType::SETTINGS) {
                    settings_view->init();
                    current_view = settings_view.get();
                } else if (next == ViewType::GAME_OVER || next == ViewType::VICTORY) {
                    bool is_vic = (next == ViewType::VICTORY);
                    const auto& p = game_view->player();
                    game_over_view->set_results(is_vic, p.score, game_view->current_wave(), p.kills, p.total_damage_dealt, p.archetype ? p.archetype->name : "Pushpaka");
                    current_view = game_over_view.get();
                }

                current_view_type = next;
            }
        }

        // Render to 900x600 virtual canvas
        BeginTextureMode(target);
        if (current_view) {
            current_view->draw();
        }
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
}
