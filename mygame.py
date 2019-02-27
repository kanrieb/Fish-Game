import arcade
import random

SCREEN_WIDTH =600
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 4


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < SCREEN_WIDTH*(1/5):
            self.left = SCREEN_WIDTH*(1/5)
        elif self.right > SCREEN_WIDTH*(4/5):
            self.right = SCREEN_WIDTH*(4/5)

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 2:
            self.top = SCREEN_HEIGHT - 2

class Water(arcade.Sprite):
    def update(self):
        self.center_y -= 1


"""
class Grass(arcade.load_texture):
    def reset_pos(self):
        self.center_y = SCREEN_HEIGHT
        self.center_x = SCREEN_WIDTH*(1/10)
"""
class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.fish_list= None
        self.fish_sprite = None
        self.score = 0
        self.grass = None
        self.water = None

    def setup(self):
        self.grass = arcade.load_texture("Images/grass.jpg")
        self.water = arcade.load_texture("Images/water.jpg")
        self.fish_list = arcade.SpriteList()
        self.score = 0
        SPRITE_SCALING_FISH = 0.05
        self.fish_sprite = Player("Images/fish.png", SPRITE_SCALING_FISH)
        self.fish_sprite.center_x = SCREEN_WIDTH /2
        self.fish_sprite.center_y = 50
        self.fish_sprite.angle = -90
        self.fish_sprite.boundary_right = SCREEN_WIDTH *(4/5)
        self.fish_list.append(self.fish_sprite)

    def on_draw(self):
        arcade.start_render()
        #drawBackground()
        #drawGrass()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//10,
                                      SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH*(1/5),
                                      SCREEN_HEIGHT,
                                      self.grass)
        arcade.draw_texture_rectangle(SCREEN_WIDTH*(9/10),
                                      SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH*(1/5),
                                      SCREEN_HEIGHT,
                                      self.grass)
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2,
                                      SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH*(3/5),
                                      SCREEN_HEIGHT,
                                      self.water)
        self.fish_list.draw()



    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.fish_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.fish_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.fish_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.fish_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.fish_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.fish_sprite.change_x = 0


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.fish_list.update()

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
