import  sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ Overall class to manage game assets and behavior """

    def __init__(self) -> None:
        """ Initialize the game, and create game resources """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """ Respond to keypresses and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event.key, True)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event.key, False)

    def _check_keyup_events(self, event_key, moving_flag):
        if event_key == pygame.K_RIGHT:
            self.ship.moving_right = moving_flag
        elif event_key == pygame.K_LEFT:
            self.ship.moving_left = moving_flag

    def _check_keydown_events(self, event_key, moving_flag):
        if event_key == pygame.K_RIGHT:
            self.ship.moving_right = moving_flag
        elif event_key == pygame.K_LEFT:
            self.ship.moving_left = moving_flag
        elif event_key == pygame.K_q:
            sys.exit()
        elif event_key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullet group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """ Create the fleet of aliens """
        # Create an alien and keep adding aliens until there's no room left 
        # Spacing between aliens is one alien's width and one alien's height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """ Create an alien and place it in the fleet """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets """
        # Update bullet position
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """ Update images on the screen, and flip to the new screen """
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()
        

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()

