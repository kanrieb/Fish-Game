import arcade
import random

SCREEN_WIDTH =600
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 4
FOOD_COUNT = 10
LOG_COUNT = 6
SPRITE_SCALING_FOOD = 0.035
SPRITE_SCALING_WATER = 1.5
SPRITE_SCALING_FISH = 0.05
SPRITE_SCALING_LOG = .15

INSTRUCTIONS_PAGE_0 = 0
GAME_RUNNING = 1
GAME_OVER = 2
FINISHED = 3

class Water(arcade.Sprite):
    def reset_pos(self):
        # Reset the water to a random spot above the screen
        self.center_y = SCREEN_HEIGHT + 20
        self.center_x = SCREEN_WIDTH//2

    def update(self):
        # Move the water
        self.center_y -= 1
        # See if the water has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()

class Food(arcade.Sprite):
    def reset_pos(self):
        self.center_x = random.randrange(SCREEN_WIDTH//4, SCREEN_WIDTH*(4/6))
        self.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT+20)

    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.reset_pos()

class Log(arcade.Sprite):
    def reset_pos(self):
        self.center_x = random.randrange(SCREEN_WIDTH//4, SCREEN_WIDTH*(4/6))
        self.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT+20)
    
    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.reset_pos()

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


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        self.current_state = INSTRUCTIONS_PAGE_0
        super().__init__(width, height)
        self.fish_list= None
        self.fish_sprite = None
        self.score_food = 0
        self.score_log = 0
        self.grass = None
        self.log_sprite_list = None
        self.water_sprite_list = None
        self.food_sprite_list = None

        self.instructions = []
        texture = arcade.load_texture("Images/instructions_0.png")
        self.instructions.append(texture)


    def setup(self):
        self.grass = arcade.load_texture("Images/grass.jpg")

        self.fish_list = arcade.SpriteList()
        self.water_sprite_list = arcade.SpriteList()
        self.food_sprite_list = arcade.SpriteList()
        self.log_sprite_list = arcade.SpriteList()

        water = Water("Images/water.jpg", SPRITE_SCALING_WATER)
        water.center_x = SCREEN_WIDTH//2
        water.center_y = SCREEN_HEIGHT
        self.water_sprite_list.append(water)
        water1 = Water("Images/water.jpg", SPRITE_SCALING_WATER)
        water1.center_x = SCREEN_WIDTH//2
        water1.center_y = SCREEN_HEIGHT*(2/3)
        self.water_sprite_list.append(water1)
        water2 = Water("Images/water.jpg", SPRITE_SCALING_WATER)
        water2.center_x = SCREEN_WIDTH//2
        water2.center_y = SCREEN_WIDTH//3
        self.water_sprite_list.append(water2)
        water3 = Water("Images/water.jpg", SPRITE_SCALING_WATER)
        water3.center_x = SCREEN_WIDTH//2
        water3.center_y = 0
        self.water_sprite_list.append(water3)

        for i in range(FOOD_COUNT):
            food = Food("Images/food.jpg", SPRITE_SCALING_FOOD)
            food.center_x = random.randrange(SCREEN_WIDTH//4, SCREEN_WIDTH*(4/6))
            food.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT*2)
            self.food_sprite_list.append(food)

        for i in range(LOG_COUNT):
            log = Log("Images/log.png", SPRITE_SCALING_LOG)
            log.center_x = random.randrange(SCREEN_WIDTH//4, SCREEN_WIDTH*(4/6))
            log.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT*2)
            self.log_sprite_list.append(log)

        self.score = 0
        self.fish_sprite = Player("Images/fish.png", SPRITE_SCALING_FISH)
        self.fish_sprite.center_x = SCREEN_WIDTH /2
        self.fish_sprite.center_y = 50
        self.fish_sprite.angle = -90
        self.fish_sprite.boundary_right = SCREEN_WIDTH *(4/5)
        self.fish_list.append(self.fish_sprite)

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)


    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 110, 300, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 180, 250, arcade.color.WHITE, 24)

    def draw_finished(self):
        """
        Draw "Finished" across the screen.
        """
        output = "Finished!"
        arcade.draw_text(output, 110, 300, arcade.color.WHITE, 54)

    def draw_game(self):
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
        self.water_sprite_list.draw()
        self.food_sprite_list.draw()
        self.log_sprite_list.draw()
        self.fish_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        elif self.current_state == FINISHED:
            self.draw_game()
            self.draw_finished()

        else:
            self.draw_game()
            self.draw_game_over() 

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == FINISHED:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING

    def on_key_press(self, key, modifiers):
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.UP:
                self.fish_sprite.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.fish_sprite.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.fish_sprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.fish_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.fish_sprite.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.fish_sprite.change_x = 0

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.current_state == GAME_RUNNING:
            self.water_sprite_list.update()
            self.fish_list.update()
            self.food_sprite_list.update()
            self.log_sprite_list.update()
            
            hit_list = arcade.check_for_collision_with_list(self.fish_sprite, self.food_sprite_list)
            for food in hit_list:
                food.kill()
                self.score_food += 1

            kill_list = arcade.check_for_collision_with_list(self.fish_sprite,self.log_sprite_list)
            for log in kill_list:
                self.score_log += 1

            if self.score_log > 0:
                self.score_log = 0
                self.current_state = GAME_OVER

            if self.score_food == 10:
                self.current_state = FINISHED


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
