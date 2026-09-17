import ast, os, sys

print("=== SYNTAX SCAN ===")
errors = []
root = 'game'
for dirpath, _, files in os.walk(root):
    for f in files:
        if not f.endswith('.py'):
            continue
        path = os.path.join(dirpath, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                src = fh.read()
            ast.parse(src, filename=path)
        except SyntaxError as e:
            errors.append(f'SYNTAX ERROR in {path}: {e}')

if errors:
    for e in errors:
        print(e)
else:
    print('No syntax errors found in game/ directory.')

print("\n=== IMPORT SCAN ===")
views_to_check = [
    'game.views.menu_view',
    'game.views.codex_view',
    'game.views.achievements_view',
    'game.views.leaderboard_view',
    'game.views.settings_view',
    'game.views.realm_map_view',
    'game.views.ship_select_view',
    'game.views.multiplayer_view',
    'game.views.difficulty_view',
    'game.views.loading_screen',
    'game.views.victory_view',
    'game.views.game_over_view',
    'game.views.boon_select_view',
    'game.views.story_briefing_view',
    'game.views.account_view',
]

import importlib
for v in views_to_check:
    try:
        importlib.import_module(v)
        print(f'OK  {v}')
    except Exception as e:
        print(f'ERR {v}: {e}')
