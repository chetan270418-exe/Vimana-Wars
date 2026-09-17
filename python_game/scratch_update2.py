import os

filepath = 'game/views/loading_screen.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'anchor_x="center", anchor_y="center"\n                )',
    'anchor_x="center", anchor_y="center",\n                    font_name=FONT_INTERFACE[0]\n                )'
)
text = text.replace(
    'anchor_x="center", anchor_y="center"\r\n                )',
    'anchor_x="center", anchor_y="center",\r\n                    font_name=FONT_INTERFACE[0]\r\n                )'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated loading_screen.py again")
