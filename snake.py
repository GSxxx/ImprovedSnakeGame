import arcade
import random
import os.path
import re

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

LEFT_LIMIT = 40
RIGHT_LIMIT = 1240
TOP_LIMIT = 600
BOTTOM_LIMIT = 50


class Head(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename)
        self.center_x = 595
        self.center_y = 325
        self.change_x = 10
        self.change_y = 0
        self.last_x = self.center_x
        self.last_y = self.center_y

    def update(self):
        self.last_x = self.center_x
        self.last_y = self.center_y

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x - 5 < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT - 5
        elif self.center_x + 5 > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT + 5
        elif self.center_y + 5 > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT + 5
        elif self.center_y - 5 < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT - 5


class Food(arcade.Sprite):
    pass


class Tail(arcade.Sprite):
    pass


class Wall(arcade.Sprite):
    pass


class Enemy(arcade.Sprite):
    def __init__(self, filename, time):
        super().__init__(filename)
        self.change_x = 2
        self.change_y = 0
        self.start_time = time
        self.center_x = random.randint(5, 122) * 10 + 5
        self.center_y = random.randint(6, 58) * 10 + 5

    def update(self, time):
        self.delta = time - self.start_time

        if self.delta >= 1:
            self.random = random.randint(1, 8)
            self.start_time = time
            if self.random == 1:
                self.angle = 0
                self.change_x = 2
                self.change_y = 0
            elif self.random == 2:
                self.angle = 180
                self.change_x = -2
                self.change_y = 0
            elif self.random == 3:
                self.angle = 90
                self.change_x = 0
                self.change_y = 2
            elif self.random == 4:
                self.angle = 270
                self.change_x = 0
                self.change_y = -2

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x - 5 < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT - 5
        elif self.center_x + 5 > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT + 5
        elif self.center_y + 5 > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT + 5
        elif self.center_y - 5 < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT - 5


class Button(object):
    def __init__(self, list, text, text_x, text_y, color):
        self.co_list = list
        self.text = text
        self.text_x = text_x
        self.text_y = text_y
        self.button_color = color

    def draw(self):
        arcade.draw_polygon_filled(self.co_list, self.button_color)
        arcade.draw_text(self.text, self.text_x, self.text_y, arcade.color.WHITE, 25)


class Stamina_bar(object):
    def __init__(self):
        self.point_list = ((150, 640), (250, 640), (250, 660), (150, 660))
        self.point_list_stamina = ((153, 643), (247, 643), (247, 657), (153, 657))

    def update(self, stamina):
        self.point_list_stamina = (
        (153, 643), (153 + int(stamina / 100 * 94), 643), (153 + int(stamina / 100 * 94), 657), (153, 657))

    def draw(self):
        arcade.draw_polygon_filled(self.point_list, arcade.color.BLACK)
        arcade.draw_polygon_filled(self.point_list_stamina, arcade.color.BLUE)


class Vanishing_text(object):
    def __init__(self, pleyer_position_x, player_position_y, text_to_draw, time, r=20, o=10):
        self.vanish_start_time = time
        self.vanish_x = pleyer_position_x
        self.vanish_y = player_position_y
        self.vanish_text = text_to_draw
        self.vanish_delta = 0
        self.text = text_to_draw
        self.font = r
        self.speed = o

    def draw(self, time, objects):

        self.vanish_delta = time - self.vanish_start_time

        if self.vanish_x < LEFT_LIMIT:
            self.vanish_x = 40
        elif self.vanish_x > RIGHT_LIMIT - 100:
            self.vanish_x = 1135

        alpha = int((4 - self.vanish_delta) * 60)
        if alpha > 230:
            arcade.draw_text(self.text, self.vanish_x, self.vanish_y + 50 + self.vanish_delta * self.speed,
                             (255, 255, 255, 255), self.font)
        else:
            arcade.draw_text(self.text, self.vanish_x, self.vanish_y + 50 + self.vanish_delta * self.speed,
                             (255, 255, 255, alpha), self.font)
        # print (alpha)
        if 15 > alpha:
            self.delete(objects)

    def delete(self, objects):

        objects.pop(0)


class Tongue(arcade.Sprite):
    def __init__(self, filename, direction, time):
        super().__init__(filename)
        self.dire = direction
        self.start_time = time

    def update(self, player_x, player_y, time):
        self.delta = time - self.start_time
        if self.delta > 0.2:
            return 0
        else:
            self.width = 150 * (self.delta / 0.2)
            if self.dire == "RIGHT":
                self.angle = 0
                self.center_x = player_x + 5 + self.width / 2
                self.center_y = player_y
            elif self.dire == "LEFT":
                self.angle = 180
                self.center_x = player_x - 5 - self.width / 2
                self.center_y = player_y
            elif self.dire == "UP":
                self.angle = 90
                self.center_x = player_x
                self.center_y = player_y + 5 + self.width / 2
            elif self.dire == "DOWN":
                self.angle = 270
                self.center_x = player_x
                self.center_y = player_y - 5 - self.width / 2
            return 1


class MyApp(arcade.Window):
    def start(self):
        arcade.set_background_color(arcade.color.GRAY)

        # Sprite lists
        self.button_list = []
        self.instructions = []

        texture = arcade.load_texture("pics/instruction1.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("pics/instruction2.png")
        self.instructions.append(texture)

        self.no_button = 0
        self.game_is_running = 0
        self.instruction = -1

        self.hightlight_button1 = ((395, 395), (885, 395), (885, 455), (395, 455))
        self.hightlight_button2 = ((395, 325), (885, 325), (885, 385), (395, 385))
        self.hightlight_button3 = ((395, 255), (885, 255), (885, 315), (395, 315))

        self.pos_list = [self.hightlight_button1, self.hightlight_button2, self.hightlight_button3]

        self.new_button = Button(self.pos_list[0], "", 565, 412, arcade.color.YELLOW)
        self.button_list.append(self.new_button)

        self.start_game_button = ((400, 400), (880, 400), (880, 450), (400, 450))
        self.new_button = Button(self.start_game_button, "NEW GAME", 565, 412, arcade.color.BLACK)
        self.button_list.append(self.new_button)

        self.instruction_button = ((400, 330), (880, 330), (880, 380), (400, 380))
        self.new_button = Button(self.instruction_button, "INSTRUCTION", 550, 342, arcade.color.BLACK)
        self.button_list.append(self.new_button)

        self.exit_button = ((400, 260), (880, 260), (880, 310), (400, 310))
        self.new_button = Button(self.exit_button, "EXIT", 610, 272, arcade.color.BLACK)
        self.button_list.append(self.new_button)

    def start_new_game(self):

        self.game_is_running = 1

        arcade.set_background_color(arcade.color.GRAY)
        # Main sprite
        self.player_sprite = Head("pics/snake_part.png")
        print("snake...head")
        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.tail_sprites_list = arcade.SpriteList()
        self.food_sprites_list = arcade.SpriteList()
        self.wall_sprites_list = arcade.SpriteList()
        self.enemy_sprites_list = arcade.SpriteList()

        self.list_of_objectcs = []
        self.enemy_ver = ["pics/enemy1.png", "pics/enemy2.png", "pics/enemy3.png"]
        # Player - head
        self.all_sprites_list.append(self.player_sprite)

        self.deathtexture = arcade.load_texture("pics/rip.png")
        self.pausetexture = arcade.load_texture("pics/pause.png")
        self.abilitytexture = arcade.load_texture("pics/abilityicon.png")

        # variables
        self.stage = 1
        self.score = 0
        self.DIRECTION = "RIGHT"
        self.info = 0
        self.total_time = 0.0
        self.snake_size = 3
        self.food_on_the_ground = 0
        self.food_collected = 0
        self.refresh_time = 0
        self.refresh_time2 = 0
        self.snake_speed = 1
        self.game_over = 0
        self.draw = 1
        self.move = 1
        self.pause = 0
        self.ability_count = 3
        self.ability_on = 0
        self.tongue = None
        # turn on stuff
        self.turn_on_game_over_screen = 0
        self.can_change_direction = 1
        # sprint feature
        self.stamina = 100
        self.stamina_on = 0

        # stamina bar
        self.stamina_bar = Stamina_bar()
        # sound
        self.food_sound = arcade.sound.load_sound("sounds/food.wav")

        # create snake
        for new_snake_pos in range(10, self.snake_size * 10 + 10, 10):
            print("snake...tail")
            self.tail_sprite = Tail("pics/tail.png")
            self.tail_sprite.center_x = 595 - new_snake_pos
            self.tail_sprite.center_y = 325
            self.tail_sprites_list.append(self.tail_sprite)

        # best score
        self.bestscore = 0
        if os.path.exists('config.txt'):
            inputdata = open('config.txt', 'r')
            line = inputdata.readline()
            tmp = ""
            for i in line:
                if re.match("[0-9]", i):
                    tmp += i
            self.bestscore = int(tmp)
            inputdata.close()
        else:
            inputdata = open('config.txt', 'w')
            inputdata.write("BestScore: 0\n")
            inputdata.close()

            # self.set_mouse_visible(False)

    def on_key_press(self, symbol, modifiers):

        if self.game_is_running == 0:
            if symbol == arcade.key.UP:
                self.no_button -= 1
                self.no_button = self.no_button % 3
            elif symbol == arcade.key.DOWN:
                self.no_button += 1
                self.no_button = self.no_button % 3

            if symbol == arcade.key.ENTER and self.no_button == 0:
                print("starting the game")
                self.start_new_game()
            elif symbol == arcade.key.ENTER and self.no_button == 2:
                print("closing")
                window.close()
            elif symbol == arcade.key.ENTER and self.no_button == 1:
                print("instruction")
                self.instruction += 1
                if self.instruction > 1:
                    self.instruction = -1
        else:

            if self.game_over == 0:
                if self.pause == 1:
                    if symbol == arcade.key.LEFT:
                        self.no_button -= 1
                        self.no_button = self.no_button % 2
                    elif symbol == arcade.key.RIGHT:
                        self.no_button += 1
                        self.no_button = self.no_button % 2
                    elif symbol == arcade.key.ENTER and self.no_button == 0:
                        self.start()
                        print("menu")
                    elif symbol == arcade.key.ENTER and self.no_button == 1:
                        self.pause = 0
                        print("unpausing")
                elif symbol == arcade.key.UP and self.DIRECTION is not "DOWN" and self.can_change_direction == 1:
                    self.player_sprite.change_x = 0
                    self.player_sprite.change_y = 10
                    self.DIRECTION = "UP"
                    self.can_change_direction = 0
                elif symbol == arcade.key.DOWN and self.DIRECTION is not "UP" and self.can_change_direction == 1:
                    self.player_sprite.change_x = 0
                    self.player_sprite.change_y = -10
                    self.DIRECTION = "DOWN"
                    self.can_change_direction = 0
                elif symbol == arcade.key.RIGHT and self.DIRECTION is not "LEFT" and self.can_change_direction == 1:
                    self.player_sprite.change_x = 10
                    self.player_sprite.change_y = 0
                    self.DIRECTION = "RIGHT"
                    self.can_change_direction = 0
                elif symbol == arcade.key.LEFT and self.DIRECTION is not "RIGHT" and self.can_change_direction == 1:
                    self.player_sprite.change_x = -10
                    self.player_sprite.change_y = 0
                    self.DIRECTION = "LEFT"
                    self.can_change_direction = 0
                elif symbol == arcade.key.ESCAPE:
                    print("pausing")
                    self.set_pause()
                elif symbol == arcade.key.SPACE and self.ability_count > 0 and self.ability_on == 0:
                    self.special_skill()
                elif symbol == arcade.key.I:
                    if self.info == 0:
                        self.info = 1
                    else:
                        self.info = 0

            if symbol == arcade.key.SPACE and self.game_over == 1:
                self.start_new_game()
            elif symbol == arcade.key.ESCAPE and self.game_over == 1:
                self.start()

            # stamina feature
            if symbol == arcade.key.LALT and self.stamina > 0 and self.game_over == 0:
                self.stamina_on = 1
                self.snake_speed = 0
            else:
                self.snake_speed = 1
                self.stamina_on = 0

    def on_key_release(self, symbol, modifiers):

        if self.game_is_running == 0:
            pass
        else:

            if symbol == arcade.key.LALT:
                self.snake_speed = 1
                self.stamina_on = 0
                print("out of stamina")

    def set_pause(self):
        self.pause = 1

        self.button_list = []
        self.no_button = 0

        self.hightlight_button1 = ((320, 295), (555, 295), (555, 365), (320, 365))
        self.hightlight_button2 = ((720, 295), (955, 295), (955, 365), (720, 365))

        self.pos_list = [self.hightlight_button1, self.hightlight_button2]

        self.new_button = Button(self.pos_list[0], "", 565, 412, arcade.color.YELLOW)
        self.button_list.append(self.new_button)

        self.yes_button = ((325, 300), (550, 300), (550, 360), (325, 360))
        self.new_button = Button(self.yes_button, "YES", 410, 320, arcade.color.BLACK)
        self.button_list.append(self.new_button)

        self.n_button = ((725, 300), (950, 300), (950, 360), (725, 360))
        self.new_button = Button(self.n_button, "NO", 815, 320, arcade.color.BLACK)
        self.button_list.append(self.new_button)

    def draw_pause(self):

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.pausetexture.width,
                                      self.pausetexture.height, self.pausetexture, 0)

    def create_food(self):
        self.new_food = Food("pics/food2.png")
        self.new_food.center_x = random.randint(5, 122) * 10 + 5
        self.new_food.center_y = random.randint(6, 58) * 10 + 5
        self.food_sprites_list.append(self.new_food)
        self.food_on_the_ground += 1
        self.food_time = 0
        print("creating food")

    def create_enemy(self):
        self.random = random.randint(0, 2)
        self.enemy = Enemy(self.enemy_ver[self.random], self.total_time)
        self.enemy_sprites_list.append(self.enemy)
        print("creating enemy")

    def add_tail(self):
        self.snake_size += 1
        self.tail_sprite = Tail("pics/tail.png")
        self.tail_sprites_list.append(self.tail_sprite)
        print("snake is growing")

    def special_skill(self):
        print("using special skill")
        self.ability_on = 1
        self.ability_count -= 1

        self.tongue = Tongue("pics/tongue.png", self.DIRECTION, self.total_time)

    def death(self):
        self.move = 0
        self.game_over = 1
        self.restart_time = 0

        # save score
        if self.score > self.bestscore:
            self.bestscore = self.score

        outputdata = open('config.txt', 'w')
        output = "BestScore: {}\n".format(self.bestscore)
        outputdata.write(output)
        outputdata.close()

        print("snake is dead")

    def stage2(self):
        self.text = "STAGE 2"
        self.new_text = Vanishing_text(SCREEN_WIDTH // 2 - 100, 400, self.text, self.total_time, 60, 0)
        self.list_of_objectcs.append(self.new_text)

        for i in range(5, 124):
            self.new_element = Wall("pics/wall.png")
            self.new_element.center_x = i * 10 + 5
            self.new_element.center_y = 55
            self.wall_sprites_list.append(self.new_element)
        for i in range(5, 124):
            self.new_element = Wall("pics/wall.png")
            self.new_element.center_x = i * 10 + 5
            self.new_element.center_y = 595
            self.wall_sprites_list.append(self.new_element)
        for i in range(5, 60):
            self.new_element = Wall("pics/wall.png")
            self.new_element.center_x = 45
            self.new_element.center_y = i * 10 + 5
            self.wall_sprites_list.append(self.new_element)
        for i in range(5, 60):
            self.new_element = Wall("pics/wall.png")
            self.new_element.center_x = 1235
            self.new_element.center_y = i * 10 + 5
            self.wall_sprites_list.append(self.new_element)

    def draw_instructions_page(self, page_number):

        page_texture = self.instructions[page_number]

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, page_texture.width, page_texture.height,
                                      page_texture, 0)

    def game_over_screen(self):

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 900, 600, self.deathtexture)

        output = "Game Over"
        arcade.draw_text(output, SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 200, arcade.color.BLACK, 72)

        output = "Click SPACE key to restart"
        arcade.draw_text(output, SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 210, arcade.color.BLACK, 32)

        output = "Your SCORE: {}".format(self.score)
        arcade.draw_text(output, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, arcade.color.BLACK, 24)

        output = "YOUR BEST SCORE: {}".format(self.bestscore)
        arcade.draw_text(output, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 80, arcade.color.BLACK, 24)

    def draw_game(self):
        # draw everything
        if self.draw == 1:

            if self.ability_on == 1:
                self.tongue.draw()
            self.tail_sprites_list.draw()
            self.all_sprites_list.draw()

        self.enemy_sprites_list.draw()
        self.food_sprites_list.draw()
        if self.stage == 2:
            self.wall_sprites_list.draw()

        # playgoround
        arcade.draw_line(LEFT_LIMIT, BOTTOM_LIMIT, LEFT_LIMIT, TOP_LIMIT, arcade.color.BLACK, 2)
        arcade.draw_line(RIGHT_LIMIT, BOTTOM_LIMIT, RIGHT_LIMIT, TOP_LIMIT, arcade.color.BLACK, 2)
        arcade.draw_line(LEFT_LIMIT, BOTTOM_LIMIT, RIGHT_LIMIT, BOTTOM_LIMIT, arcade.color.BLACK, 2)
        arcade.draw_line(LEFT_LIMIT, TOP_LIMIT, RIGHT_LIMIT, TOP_LIMIT, arcade.color.BLACK, 2)

        # player information
        output = "SCORE: {}".format(self.score)
        arcade.draw_text(output, 50, 640, arcade.color.BLACK, 14)

        for i in range(0, self.ability_count * 35, 35):
            arcade.draw_texture_rectangle(i + 300, 660,
                                          self.abilitytexture.width, self.abilitytexture.height,
                                          self.abilitytexture)

        self.stamina_bar.draw()

        # vanishing text as a object
        for i in self.list_of_objectcs:
            i.draw(self.total_time, self.list_of_objectcs)

    def draw_additional_game_information(self):

        info_x = "center_x: {}".format(self.player_sprite.center_x)
        info_y = "center_y: {}".format(self.player_sprite.center_y)
        arcade.draw_text(info_x, 1050, 660, arcade.color.BLACK, 14)
        arcade.draw_text(info_y, 1050, 630, arcade.color.BLACK, 14)

        info_direction = "direction: {}".format(self.DIRECTION)
        arcade.draw_text(info_direction, 900, 660, arcade.color.BLACK, 14)

        if self.snake_speed == 1:
            real_snake_speed = "NORMAL"
        elif self.snake_speed == 0:
            real_snake_speed = "SPRINT"
        info_SNAKE_SPEED = "speed: {}".format(real_snake_speed)
        arcade.draw_text(info_SNAKE_SPEED, 900, 630, arcade.color.BLACK, 14)

        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        info_time = "time: {:02d}:{:02d}".format(minutes, seconds)
        arcade.draw_text(info_time, 750, 660, arcade.color.BLACK, 14)

        info_food_collected = "food collected: {}".format(self.food_collected)
        arcade.draw_text(info_food_collected, 750, 630, arcade.color.BLACK, 14)

        minutes = int(self.food_time) // 60
        seconds = int(self.food_time) % 60
        info_food_time = "food time: {:02d}:{:02d}".format(minutes, seconds)
        arcade.draw_text(info_food_time, 550, 660, arcade.color.BLACK, 14)

        stamina = "Stamina: {0:.0f}".format(self.stamina)
        arcade.draw_text(stamina, 550, 630, arcade.color.BLACK, 14)

    def on_draw(self):

        # render everything
        arcade.start_render()

        # check if game is on
        if self.game_is_running == 0:

            for i in self.button_list:
                i.draw()

            if self.instruction > -1:
                self.draw_instructions_page(self.instruction)
        else:

            self.draw_game()

            if self.turn_on_game_over_screen == 1:
                self.game_over_screen()

            if self.pause == 1:
                self.draw_pause()
                for i in self.button_list:
                    i.draw()
            # additional game information
            if self.info == 1:
                self.draw_additional_game_information()

    def animate(self, delta_time):

        # check if game is on
        if self.game_is_running == 0:
            # update highlight button
            self.button_list[0].co_list = self.pos_list[self.no_button]

        elif self.pause == 0:
            # time stuff
            self.refresh_time += delta_time
            self.total_time += delta_time
            self.refresh_time2 += delta_time

            # restarting the game
            if self.game_over == 1:
                self.restart_time += delta_time

            # enemy move and spawn
            for i in self.enemy_sprites_list:
                i.update(self.total_time)
            if self.refresh_time2 >= 1:
                self.refresh_time2 = 0
                self.random = random.randint(0, 9)
                if self.random == 5:
                    self.create_enemy()

            # tongue stuff
            if self.ability_on == 1:
                self.ability_on = self.tongue.update(self.player_sprite.center_x, self.player_sprite.center_y,
                                                     self.total_time)
            # food stuff
            if self.food_on_the_ground == 0:
                self.create_food()
            else:
                self.food_time += delta_time

            # points for consumption

            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_sprites_list)
            if len(hit_list) == 0 and self.ability_on == 1:
                hit_list = arcade.check_for_collision_with_list(self.tongue, self.enemy_sprites_list)
            for enemy in hit_list:
                self.add_tail()

                # there is a little chance to get additional part of trunk
                fortune = random.randint(0, 15)
                if fortune == 7:
                    self.add_tail()
                    self.add_tail()
                    self.add_tail()
                    print("it is not your lucky day :(")
                enemy.kill()
                # game balance
                if self.food_time <= 2:
                    self.score_to_add = 100
                elif self.food_time <= 8:
                    self.score_to_add = int((10 - self.food_time) / 10 * 100)
                else:
                    self.score_to_add = 20

                arcade.sound.play_sound(self.food_sound)

                self.score += self.score_to_add
                # vanishing object
                self.text = "Score +{}".format(self.score_to_add)
                self.new_text = Vanishing_text(self.player_sprite.center_x, self.player_sprite.center_y, self.text,
                                               self.total_time)
                self.list_of_objectcs.append(self.new_text)

                # normal food
            if self.food_on_the_ground == 1:
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.food_sprites_list)
                if len(hit_list) == 0 and self.ability_on == 1:
                    hit_list = arcade.check_for_collision_with_list(self.tongue, self.food_sprites_list)
                for food in hit_list:
                    self.food_collected += 1
                    self.add_tail()

                    # there is a little chance to get additional part of trunk
                    fortune = random.randint(1, 11)
                    if fortune == 7:
                        self.add_tail()
                        self.add_tail()
                        self.add_tail()
                        print("it is not your lucky day :(")
                    food.kill()
                    self.food_on_the_ground -= 1

                    # sound
                    arcade.sound.play_sound(self.food_sound)

                    # game balance
                    if self.food_time <= 2:
                        self.score_to_add = 50
                    elif self.food_time <= 8:
                        self.score_to_add = int((10 - self.food_time) / 10 * 50)
                    else:
                        self.score_to_add = 5

                    # vanishing object
                    self.text = "Score +{}".format(self.score_to_add)
                    self.new_text = Vanishing_text(self.player_sprite.center_x, self.player_sprite.center_y, self.text,
                                                   self.total_time)
                    self.list_of_objectcs.append(self.new_text)

                    if self.score_to_add > 35:
                        self.text = "+Ability Point"
                        self.new_text = Vanishing_text(self.player_sprite.center_x - 50,
                                                       self.player_sprite.center_y + 50, self.text, self.total_time)
                        self.list_of_objectcs.append(self.new_text)
                        self.ability_count += 1
                    # score increment
                    self.score += self.score_to_add

                    # stages

                    if self.score > 100 and self.stage == 1:
                        self.stage = 2
                        self.stage2()

            # refresh rate
            if self.refresh_time > 0.05 * self.snake_speed:
                self.refresh_time = 0

                # stamina feature
                if self.stamina < 100:
                    self.stamina += 2.5

                if self.stamina <= 5:
                    self.snake_speed = 1
                    self.stamina_on = 0
                    print("out of stamina")

                if self.stamina_on == 1:
                    self.stamina -= 5

                if self.stamina > 100:
                    self.stamina = 100

                # movement
                if self.move == 1:

                    self.all_sprites_list.update()

                    i = 1
                    for sprite in self.tail_sprites_list:
                        if i == 1:
                            center_x_tmp = sprite.center_x
                            center_y_tmp = sprite.center_y
                            sprite.center_x = self.player_sprite.last_x
                            sprite.center_y = self.player_sprite.last_y

                        else:
                            x = sprite.center_x
                            y = sprite.center_y
                            sprite.center_x = center_x_tmp
                            sprite.center_y = center_y_tmp
                            center_x_tmp = x
                            center_y_tmp = y
                        i += 1

                    self.can_change_direction = 1


                    # snake death
                death_list = arcade.check_for_collision_with_list(self.player_sprite, self.tail_sprites_list)
                if len(death_list) == 0:
                    death_list = arcade.check_for_collision_with_list(self.player_sprite, self.wall_sprites_list)
                if len(death_list) > 0 and self.game_over == 0:
                    self.death()

                # blink after death
                if self.game_over == 1:
                    if (self.restart_time > 0 and self.restart_time < 0.5) or \
                            (self.restart_time > 1 and self.restart_time < 1.5) or \
                            (self.restart_time > 2 and self.restart_time < 2.5):
                        self.draw = 0
                    elif self.restart_time <= 3:
                        self.draw = 1
                    else:
                        self.turn_on_game_over_screen = 1

                # stamina bar
                self.stamina_bar.update(self.stamina)
        # pause screen
        elif self.pause == 1:
            self.button_list[0].co_list = self.pos_list[self.no_button]


window = MyApp(SCREEN_WIDTH, SCREEN_HEIGHT)

window.start()
# window.start_new_game()

arcade.run()
