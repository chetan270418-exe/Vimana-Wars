#include <iostream>
#include <memory>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "systems/db_system.hpp"
#include "views/menu_view.hpp"
#include "views/ship_select_view.hpp"
#include "views/difficulty_view.hpp"
#include "views/game_view.hpp"
#include "views/duel_view.hpp"
#include "views/boon_select_view.hpp"
#include "views/leaderboard_view.hpp"
#include "views/multiplayer_view.hpp"
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

    // 3. Render Texture for 900x600 Logical Scaling
    RenderTexture2D target = LoadRenderTexture(SCREEN_WIDTH, SCREEN_HEIGHT);
    SetTextureFilter(target.texture, TEXTURE_FILTER_BILINEAR);

    // 4. Instantiate Views
    auto menu_view = std::make_unique<MenuView>();
    auto ship_select_view = std::make_unique<ShipSelectView>();
    auto difficulty_view = std::make_unique<DifficultyView>();
    auto game_view = std::make_unique<GameView>();
    auto duel_view = std::make_unique<DuelView>();
    auto boon_view = std::make_unique<BoonSelectView>();
    auto leaderboard_view = std::make_unique<LeaderboardView>();
    auto multiplayer_view = std::make_unique<MultiplayerView>();
    auto settings_view = std::make_unique<SettingsView>();
    auto game_over_view = std::make_unique<GameOverView>(false);

    ViewType current_view_type = ViewType::MENU;
    IView* current_view = menu_view.get();

    std::cout << "[VimanaWars] C++ Engine Running at 60 FPS." << std::endl;

    // 5. Main Game Loop
    while (!WindowShouldClose()) {
        float dt = GetFrameTime();
        if (dt > 0.1f) dt = 0.1f; // Cap delta time against hitches

        SoundSystem::instance().update_music();

        // Calculate aspect ratio scaling
        float scale = std::min(static_cast<float>(GetScreenWidth()) / SCREEN_WIDTH,
                               static_cast<float>(GetScreenHeight()) / SCREEN_HEIGHT);
        float offset_x = (GetScreenWidth() - (SCREEN_WIDTH * scale)) * 0.5f;
        float offset_y = (GetScreenHeight() - (SCREEN_HEIGHT * scale)) * 0.5f;

        // Virtual mouse position inside 900x600 canvas
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

                if (next == ViewType::MENU) {
                    menu_view->init();
                    current_view = menu_view.get();
                } else if (next == ViewType::SHIP_SELECT) {
                    ship_select_view->init();
                    current_view = ship_select_view.get();
                } else if (next == ViewType::DIFFICULTY_SELECT) {
                    difficulty_view->init();
                    current_view = difficulty_view.get();
                } else if (next == ViewType::GAMEPLAY) {
                    if (current_view_type == ViewType::SHIP_SELECT) {
                        game_view->start_with_ship(&ship_select_view->selected_ship(), ship_select_view->consumables());
                    } else if (current_view_type == ViewType::BOON_SELECT) {
                        game_view->apply_boon_and_resume(boon_view->chosen_boon());
                    }
                    current_view = game_view.get();
                } else if (next == ViewType::DUEL) {
                    duel_view->init();
                    current_view = duel_view.get();
                } else if (next == ViewType::BOON_SELECT) {
                    boon_view->init();
                    current_view = boon_view.get();
                } else if (next == ViewType::LEADERBOARD) {
                    leaderboard_view->init();
                    current_view = leaderboard_view.get();
                } else if (next == ViewType::MULTIPLAYER_LOBBY) {
                    multiplayer_view->init();
                    current_view = multiplayer_view.get();
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

        // Render to virtual canvas
        BeginTextureMode(target);
        if (current_view) {
            current_view->draw();
        }
        EndTextureMode();

        // Render virtual canvas scaled to physical window
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
