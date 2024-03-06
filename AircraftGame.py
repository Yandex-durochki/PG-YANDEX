
"""
Copyright (c) 2024 Yandex-durochki

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from sys import exit
from pygame.locals import *
from StrategyGame import *
import random 

class AircraftGame(object):
    def __init__(self):
        pygame.init()
        
        self.screen                   = None
        self.BULLETSHOT_SOUNDTEST     = None
        self.OPPONENT1_DOWN_SOUNDTEST = None
        self.GAMEOVER_SOUNDTEST       = None
        self.GAME_BACKGROUND          = None
        self.GAME_OVER                = None
        self.AIRCRAFT_IMAGES          = None
        self.hover                    = None
        
        self.play_button_image        = None
        self.how_to_play_button_image = None
        self.how_to_play_info         = None
        self.logo                     = None
        
        self.init_display()
        self.load_images()
        self.load_sounds()
        self.set_sounds_volume()
        
        self.SCORE = 0
        
    def init_display(self, title = 'Звёздный бой'):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # From StrategyGame.py
        pygame.display.set_caption(title)

    def load_sounds(self):
        self.BULLETSHOT_SOUNDTEST = pygame.mixer.Sound('image/sound/bullet.wav')
        self.OPPONENT1_DOWN_SOUNDTEST = pygame.mixer.Sound('image/sound/opponent1_down.wav')
        self.GAMEOVER_SOUNDTEST = pygame.mixer.Sound('image/sound/game_over.wav')
        self.hover = pygame.mixer.Sound('image/sound/hover.mp3')
        
    def set_sounds_volume(self, new_volume = 0.3):
        self.BULLETSHOT_SOUNDTEST.set_volume(new_volume)
        self.OPPONENT1_DOWN_SOUNDTEST.set_volume(new_volume)
        self.GAMEOVER_SOUNDTEST.set_volume(new_volume)
        
    def play_music_core(self, filename, volume):
        if (pygame.mixer.music.get_busy()):
            pygame.mixer.music.unload()
        pygame.mixer.music.load('image/sound/' + filename)
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(volume)

    def start_main_theme(self, volume = 0.25):
        self.play_music_core('game_music.mp3', volume)

    def start_game_over_theme(self, volume = 0.5):
        self.play_music_core('gameover.mp3', volume)
        
    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def load_images(self):
        self.GAME_BACKGROUND = pygame.image.load('image/image/background.png').convert()
        self.GAME_OVER = pygame.image.load('image/image/gameover.png')
        self.AIRCRAFT_IMAGES = pygame.image.load('image/image/aircraft_shooter.png')
        
        self.play_button_image = pygame.image.load('image/image/play_button.png').convert_alpha()
        self.how_to_play_button_image = pygame.image.load('image/image/how_to_play_button.png').convert_alpha()
        self.how_to_play_info = pygame.image.load('image/image/how_to_play_info.png').convert_alpha()
        self.logo = pygame.image.load('image/image/logo.png').convert_alpha()
        
    def main_menu(self):
        
        self.start_main_theme()
        
        on_main_menu = True
        
        play_button_rect = pygame.Rect(0, 0, 0, 0)
        how_to_play_button_rect = pygame.Rect(0, 0, 0, 0)
        mouse_rect = pygame.Rect(0, 0, 0, 0)
        
        while (on_main_menu):
            for ev in pygame.event.get():
            
                LKM_OK = (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1)
                
                if (ev.type == pygame.QUIT):
                    pygame.quit()
                    exit(0)
                
                if (mouse_rect.colliderect(play_button_rect)):
                    if (LKM_OK):
                        self.hover.play()
                        self.clear_screen()
                        self.game_process()
                elif (mouse_rect.colliderect(how_to_play_button_rect)):
                    if (LKM_OK):
                        self.hover.play()
                        self.clear_screen()
                        self.how_to_play_menu()
                        
                    
            self.clear_screen()
            
            pbx = self.play_button_image.get_size()[0]
            pby = self.play_button_image.get_size()[1]
            
            htpbx = self.how_to_play_button_image.get_size()[0]
            htpby = self.how_to_play_button_image.get_size()[1]
            
            lx = self.logo.get_size()[0]
            ly = self.logo.get_size()[1]
            
            play_button_xpos = (SCREEN_WIDTH / 2) - (pbx * 0.5)
            play_button_ypos = 500
           
            how_to_play_xpos = (SCREEN_WIDTH / 2) - (htpbx * 0.5)
            how_to_play_ypos = 600
            
            logo_xpos = (SCREEN_WIDTH / 2) - (lx * 0.5)
            logo_ypos = 100
            
            mx = pygame.mouse.get_pos()[0]
            my = pygame.mouse.get_pos()[1]
               
            self.screen.blit(self.GAME_BACKGROUND, (0, 0))
            self.screen.blit(self.logo, (logo_xpos, logo_ypos))
            self.screen.blit(self.play_button_image, [play_button_xpos, play_button_ypos])
            self.screen.blit(self.how_to_play_button_image, [how_to_play_xpos, how_to_play_ypos])
            
            play_button_rect = pygame.Rect((play_button_xpos, play_button_ypos), (pbx, pby))
            how_to_play_button_rect = pygame.Rect((how_to_play_xpos, how_to_play_ypos), (htpbx, htpby))
            mouse_rect = pygame.Rect((mx, my), (1, 1))

            pygame.display.update()
            
    def how_to_play_menu(self):
        
        while (True):
            
            for ev in pygame.event.get():
                if (ev.type == pygame.QUIT):
                    pygame.quit()
                    exit(1)
                if (ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN):
                    self.hover.play()
                    self.clear_screen()
                    self.main_menu()
                
            self.clear_screen()
            
            self.screen.blit(self.GAME_BACKGROUND, (0, 0))
            self.screen.blit(self.how_to_play_info, (0, 0))
            
            pygame.display.update()

    def game_process(self):
    
        if (self.SCORE != 0):
            self.SCORE = 0
    
        AIRCRAFT_PLAYER = []
        AIRCRAFT_PLAYER.append(pygame.Rect(0, 99, 102, 126))
        AIRCRAFT_PLAYER.append(pygame.Rect(165, 360, 102, 126))
        AIRCRAFT_PLAYER.append(pygame.Rect(165, 234, 102, 126))
        AIRCRAFT_PLAYER.append(pygame.Rect(330, 624, 102, 126))
        AIRCRAFT_PLAYER.append(pygame.Rect(330, 498, 102, 126))
        AIRCRAFT_PLAYER.append(pygame.Rect(432, 624, 102, 126))
        AIRCRAFT_PLAYER_POSITION = [200, 600]
        OPPONENT = Opponent(self.AIRCRAFT_IMAGES, AIRCRAFT_PLAYER, AIRCRAFT_PLAYER_POSITION)

        AIRCRAFT_BULLET = pygame.Rect(1004, 987, 9, 21)
        BULLET_IMAGES = self.AIRCRAFT_IMAGES.subsurface(AIRCRAFT_BULLET)

        OPPONENT1 = pygame.Rect(534, 612, 57, 43)
        OPPONENT1_IMAGES = self.AIRCRAFT_IMAGES.subsurface(OPPONENT1)
        OPPONENT1_DOWN_IMAGES = []
        OPPONENT1_DOWN_IMAGES.append(self.AIRCRAFT_IMAGES.subsurface(pygame.Rect(267, 347, 57, 43)))
        OPPONENT1_DOWN_IMAGES.append(self.AIRCRAFT_IMAGES.subsurface(pygame.Rect(873, 697, 57, 43)))
        OPPONENT1_DOWN_IMAGES.append(self.AIRCRAFT_IMAGES.subsurface(pygame.Rect(267, 296, 57, 43)))
        OPPONENT1_DOWN_IMAGES.append(self.AIRCRAFT_IMAGES.subsurface(pygame.Rect(930, 697, 57, 43)))

        CHALLENGER1 = pygame.sprite.Group()

        CHALLENGER_DOWN = pygame.sprite.Group()

        SHOOT_DISTANCE = 0
    
        CHALLENGER_DISTANCE = 0

        OPPONENT_DOWN_INDEX = 16
        
        CLOCK = pygame.time.Clock()
    
        while (True):
        
            CLOCK.tick(60)

            if not OPPONENT.is_hit:
                if SHOOT_DISTANCE % 15 == 0:
                    self.BULLETSHOT_SOUNDTEST.play()
                    OPPONENT.shoot(BULLET_IMAGES)
                SHOOT_DISTANCE += 1
                if SHOOT_DISTANCE >= 15:
                    SHOOT_DISTANCE = 0

            if SHOOT_DISTANCE % 50 == 0:
                CHALLENGER1_POSITION = [random.randint(0, SCREEN_WIDTH - OPPONENT1.width), 0]
                CHALLENGERS1 = Challenger(OPPONENT1_IMAGES, OPPONENT1_DOWN_IMAGES, CHALLENGER1_POSITION)
                CHALLENGER1.add(CHALLENGERS1)
            CHALLENGER_DISTANCE += 1
            if CHALLENGER_DISTANCE >= 100:
                CHALLENGER_DISTANCE = 0

            for bullet in OPPONENT.bullets:
                bullet.move()
                if bullet.rect.bottom < 0:
                    OPPONENT.bullets.remove(bullet)

            for CHALLENGER in CHALLENGER1:
                CHALLENGER.move()
                if pygame.sprite.collide_circle(CHALLENGER, OPPONENT):
                    CHALLENGER_DOWN.add(CHALLENGER)
                    CHALLENGER1.remove(CHALLENGER)
                    OPPONENT.is_hit = True
                    self.GAMEOVER_SOUNDTEST.play()
                    self.game_over()
                if CHALLENGER.rect.top > SCREEN_HEIGHT:
                    CHALLENGER1.remove(CHALLENGER)

            CHALLENGER1_DOWN = pygame.sprite.groupcollide(CHALLENGER1, OPPONENT.bullets, 1, 1)
            for CHALLENGERS_DOWN in CHALLENGER1_DOWN:
                CHALLENGER_DOWN.add(CHALLENGERS_DOWN)

            self.screen.fill(0)
            self.screen.blit(self.GAME_BACKGROUND, (0, 0))

            if not OPPONENT.is_hit:
                self.screen.blit(OPPONENT.image[OPPONENT.img_index], OPPONENT.rect)
                OPPONENT.img_index = SHOOT_DISTANCE // 8
            else:
                OPPONENT.img_index = OPPONENT_DOWN_INDEX // 8
                self.screen.blit(OPPONENT.image[OPPONENT.img_index], OPPONENT.rect)
                OPPONENT_DOWN_INDEX += 1
                if OPPONENT_DOWN_INDEX > 47:
                    self.game_over()

            for CHALLENGERS_DOWN in CHALLENGER_DOWN:
                if CHALLENGERS_DOWN.down_index == 0:
                    self.OPPONENT1_DOWN_SOUNDTEST.play()
                if CHALLENGERS_DOWN.down_index > 7:
                    CHALLENGER_DOWN.remove(CHALLENGERS_DOWN)
                    self.SCORE += 1000
                    continue
            
                self.screen.blit(CHALLENGERS_DOWN.down_imgs[CHALLENGERS_DOWN.down_index // 2], CHALLENGERS_DOWN.rect)
                CHALLENGERS_DOWN.down_index += 1

            OPPONENT.bullets.draw(self.screen)
            CHALLENGER1.draw(self.screen)

            SCORE_FONT = pygame.font.Font(None, 36)
            SCORE_TXT = SCORE_FONT.render(str(self.SCORE), True, (255, 255, 0))
            TXT_AIRCRAFT = SCORE_TXT.get_rect()
            TXT_AIRCRAFT.topleft = [10, 10]
            self.screen.blit(SCORE_TXT, TXT_AIRCRAFT)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        self.hover.play()
                        self.clear_screen()
                        self.main_menu()

            KEY_PRESSED_ENTER = pygame.key.get_pressed()
            if not OPPONENT.is_hit:
                if KEY_PRESSED_ENTER[K_r] or KEY_PRESSED_ENTER[K_UP]:
                    OPPONENT.moveUp()
                if KEY_PRESSED_ENTER[K_f] or KEY_PRESSED_ENTER[K_DOWN]:
                    OPPONENT.moveDown()
                if KEY_PRESSED_ENTER[K_d] or KEY_PRESSED_ENTER[K_LEFT]:
                    OPPONENT.moveLeft()
                if KEY_PRESSED_ENTER[K_g] or KEY_PRESSED_ENTER[K_RIGHT]:
                    OPPONENT.moveRight()

    def game_over(self):
    
        self.start_game_over_theme()
    
        FONT = pygame.font.Font(None, 60)
        TXT = FONT.render('Score: ' + str(self.SCORE), True, (255, 255, 0))
        TXT_AIRCRAFT = TXT.get_rect()
        TXT_AIRCRAFT.centerx = self.screen.get_rect().centerx
        TXT_AIRCRAFT.centery = self.screen.get_rect().centery + (24 * 5)
        self.screen.blit(self.GAME_OVER, (0, 0))
        self.screen.blit(TXT, TXT_AIRCRAFT)

        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.clear_screen()
                    self.hover.play()
                    self.start_main_theme()
                    self.game_process()
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.clear_screen()
                    self.hover.play()
                    self.start_main_theme()
                    self.main_menu()
            
            
            pygame.display.update()
    
if (__name__ == '__main__'):
    main = AircraftGame()
    main.main_menu()
else:
    AircraftGame = None
