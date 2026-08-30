import math
import arcade

HEIGHT = 600
WIDTH = 900
SCREEN_TITLE = "Space Shooting"

PLAYER_SCALE = 0.3
PLAYER_SPEED = 5
PLAYER_TURN_SPEED = 0.2  
PLAYER_SHOOT_COOLDOWN = 0.2
BULLET_SPEED = 10
BULLET_SCALE = 0.8


class bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.radius = 5 * BULLET_SCALE
    def update(self):  
        
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.YELLOW)
    def is_off_screen(self):
        return not (0 < self.x < WIDTH and 0 < self.y < HEIGHT)

class GameWindowScreen(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = WIDTH // 2
        self.player_y = HEIGHT // 2
        self.player_angle = 0
        self.player_radius = 150 * PLAYER_SCALE

        self.keys_pressed = set()
        self.bullets = []  
        self.last_shot_time = 0

    def on_draw(self):
        self.clear()

        angle_rad = math.radians(self.player_angle)

        tip_x = self.player_x + math.cos(angle_rad) * self.player_radius * 1.5
        tip_y = self.player_y + math.sin(angle_rad) * self.player_radius * 1.5

        left_rad = math.radians(self.player_angle + 150)
        left_x = self.player_x + math.cos(left_rad) * self.player_radius
        left_y = self.player_y + math.sin(left_rad) * self.player_radius

        right_rad = math.radians(self.player_angle - 150)
        right_x = self.player_x + math.cos(right_rad) * self.player_radius
        right_y = self.player_y + math.sin(right_rad) * self.player_radius

        arcade.draw_triangle_filled(
            tip_x, tip_y,
            left_x, left_y,
            right_x, right_y,
            arcade.color.WHITE
        )

        # Draw bullets
        for bullet in self.bullets:
            bx, by, _ = bullet
            arcade.draw_circle_filled(bx, by, 5, arcade.color.YELLOW)

    def on_update(self, delta_time):
        # Movement
        if arcade.key.W in self.keys_pressed or arcade.key.UP in self.keys_pressed:
            self.player_y += PLAYER_SPEED
        if arcade.key.S in self.keys_pressed or arcade.key.DOWN in self.keys_pressed:
            self.player_y -= PLAYER_SPEED
        if arcade.key.A in self.keys_pressed or arcade.key.LEFT in self.keys_pressed:
            self.player_x -= PLAYER_SPEED
        if arcade.key.D in self.keys_pressed or arcade.key.RIGHT in self.keys_pressed:
            self.player_x += PLAYER_SPEED

        # Keep player on screen
        self.player_x = max(self.player_radius, min(WIDTH - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius, min(HEIGHT - self.player_radius, self.player_y))

        # Update bullets
        for bullet in self.bullets[:]:
            bx, by, angle = bullet
            rad = math.radians(angle)
            bx += math.cos(rad) * BULLET_SPEED
            by += math.sin(rad) * BULLET_SPEED
            bullet[0] = bx
            bullet[1] = by

            # Remove bullets that go off-screen
            if not (0 < bx < WIDTH and 0 < by < HEIGHT):
                self.bullets.remove(bullet)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):
        dx = x - self.player_x
        dy = y - self.player_y
        self.player_angle = math.degrees(math.atan2(dy, dx))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            current_time = arcade.get_running_time()
            if current_time - self.last_shot_time > PLAYER_SHOOT_COOLDOWN:
                self.bullets.append([self.player_x, self.player_y, self.player_angle])
                self.last_shot_time = current_time


def main():
    game = GameWindowScreen()
    arcade.run()


if __name__ == "__main__":
    main()