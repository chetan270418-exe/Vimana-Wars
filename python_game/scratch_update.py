import os

filepath = 'game/views/loading_screen.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'draw_segmented_bar, draw_scanlines, draw_telemetry_ticks, pulse_alpha,\n)',
    'draw_segmented_bar, draw_scanlines, draw_telemetry_ticks, pulse_alpha,\n    FONT_CEREMONIAL, FONT_TELEMETRY, FONT_INTERFACE\n)'
)
text = text.replace(
    'draw_segmented_bar, draw_scanlines, draw_telemetry_ticks, pulse_alpha,\r\n)',
    'draw_segmented_bar, draw_scanlines, draw_telemetry_ticks, pulse_alpha,\r\n    FONT_CEREMONIAL, FONT_TELEMETRY, FONT_INTERFACE\r\n)'
)

text = text.replace(
    'anchor_x="center", anchor_y="center",\n        )',
    'anchor_x="center", anchor_y="center",\n            font_name=FONT_TELEMETRY[0],\n        )'
)
text = text.replace(
    'anchor_x="center", anchor_y="center",\r\n        )',
    'anchor_x="center", anchor_y="center",\r\n            font_name=FONT_TELEMETRY[0],\r\n        )'
)

text = text.replace(
    'font_name=FONT_TELEMETRY[0],\n        )\n        self._subtitle',
    'font_name=FONT_CEREMONIAL[0],\n        )\n        self._subtitle'
)
text = text.replace(
    'font_name=FONT_TELEMETRY[0],\r\n        )\r\n        self._subtitle',
    'font_name=FONT_CEREMONIAL[0],\r\n        )\r\n        self._subtitle'
)

# And for arcade.draw_text calls in on_draw
text = text.replace(
    'arcade.draw_text(line, WIDTH // 2, HEIGHT // 2 + 15 - idx * 24,',
    'arcade.draw_text(line, WIDTH // 2, HEIGHT // 2 + 15 - idx * 24, font_name=FONT_INTERFACE[0],'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated loading_screen.py")
