import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement1(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
     
        self.mouse_over = False  # indicates if the mouse over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__()

        self.action = action

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

#Button UI SET UP (colors)
CLEAR = (0,0,0,0)
WHITE = (255, 255, 255)
PURPLE = (150,111,214)
DARK_ORANGE = (229, 103, 23)
LIGHT_ORANGE = (255,132,0)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2

class Players():
    pass
class PlayerStats:
    """ Stores information about a player """

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level
    

def main():
    #ini pygame lib
    pygame.init()
    #creates screen
    screen = pygame.display.set_mode((800,600))
    game_state = GameState.TITLE

    #background set ups
    home_setting = pygame.image.load("homebackground.png")

    running = True

    #Exe Bar set up
    pygame.display.set_caption("The Three Bears")
    icon = pygame.image.load("paw.png")
    pygame.display.set_icon(icon)

    #Angy Bear ini
    AngyBrIcon = pygame.image.load("Angy.png")
    AngyBrIconX = 260
    AngyBrIconY = 480

    #Shy Bear ini
    ShyBrIcon = pygame.image.load("Shy.png")
    ShyBrIconX= 360
    ShyBrIconY = 480

    #Baby Bear ini
    BabyBrIcon = pygame.image.load("Baby.png")
    BabyBrIconX = 460
    BabyBrIconY = 480

    def playerIcons():
        screen.blit(AngyBrIcon,(AngyBrIconX, AngyBrIconY))
        screen.blit(ShyBrIcon,(ShyBrIconX, ShyBrIconY))
        screen.blit(BabyBrIcon,(BabyBrIconX, BabyBrIconY))

    #Title Screen buttons
    def title_screen(screen):
       
        Title = UIElement1(
                center_position=(395, 100),
                font_size= 53,
                bg_rgb=CLEAR,
                text_rgb=WHITE,
                text="The Three Bears",
            )   

        New_Game = UIElement1(
                center_position=(400, 200),
                font_size=30,
                bg_rgb=CLEAR,
                text_rgb=WHITE,
                text="New Game",
                action=GameState.NEWGAME,
            )   
        Load_Game = UIElement1(
                center_position=(400, 260),
                font_size=30,
                bg_rgb=CLEAR,
                text_rgb=WHITE,
                text="Load Game",
                action=GameState.NEXT_LEVEL,
            )     
        Settings = UIElement1(
                center_position=(400, 330),
                font_size=30,
                bg_rgb=CLEAR,
                text_rgb=WHITE,
                text="Settings",
            )     
        quit_btn = UIElement1(
                center_position=(400, 400),
                font_size=30,
                bg_rgb=CLEAR,
                text_rgb=WHITE,
                text="Quit",
                action=GameState.QUIT,
            )   
        buttons = RenderUpdates(Title, New_Game, Load_Game, Settings, quit_btn)
        

        return game_loop(screen, buttons, playerIcons)

    #In Game Start buttons
    def play_level(screen):
        return_btn = UIElement1(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=CLEAR,
            text_rgb=WHITE,
            text="Return to main menu",
            action=GameState.TITLE,
        )
        choose_character = UIElement1(
            center_position=(395, 100),
            font_size= 40,
            bg_rgb = CLEAR,
            text_rgb= DARK_ORANGE,
            text = "Choose Your Character",

        )
      
        buttons = RenderUpdates(return_btn, choose_character)

        return game_loop(screen, buttons, playerIcons)
    
    

    #Game Config
    def game_loop(screen, buttons, playerIcons):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            screen.blit(home_setting,(0, 0))

            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action

            buttons.draw(screen)
            playerIcons()
            pygame.display.flip()

    while running:
        #background color (pastel pink)
        #screen.fill((255,192,203))

        screen.blit(home_setting,(0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            if game_state == GameState.TITLE:
                game_state = title_screen(screen)

            if game_state == GameState.NEWGAME:
                game_state = play_level(screen)

            # new level
            if game_state == GameState.NEXT_LEVEL:
                pass

            if game_state == GameState.QUIT:
                pygame.quit()
            return

 
if __name__ == "__main__":
    main()
