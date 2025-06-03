import pygame
import os
import subprocess
import sys

GAMES_FOLDER = "games"

class Launcher:
    def __init__(self, debug=False):
        pygame.init()
        self.width, self.height = 400, 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Launcher")

        self.font = pygame.font.SysFont(None, 28)
        self.bg_color = (40, 40, 40)
        self.text_color = (220, 220, 220)
        self.highlight_color = (70, 130, 180)

        self.games = self.list_games()
        self.selected_index = 0
        self.running = True

        self.launched_games = {}  # game_name -> subprocess.Popen
        self.debug = debug

    def list_games(self):
        return [name for name in os.listdir(GAMES_FOLDER) if os.path.isdir(os.path.join(GAMES_FOLDER, name))]

    def draw_menu(self):
        self.screen.fill(self.bg_color)
        title_surf = self.font.render("Select a game to launch:", True, self.text_color)
        self.screen.blit(title_surf, (20, 10))

        start_y = 50
        for i, game in enumerate(self.games):
            color = self.highlight_color if i == self.selected_index else self.text_color
            text_surf = self.font.render(game, True, color)
            self.screen.blit(text_surf, (40, start_y + i * 30))

        quit_color = self.highlight_color if self.selected_index == len(self.games) else self.text_color
        quit_surf = self.font.render("Quit", True, quit_color)
        self.screen.blit(quit_surf, (40, start_y + len(self.games) * 30))

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % (len(self.games) + 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % (len(self.games) + 1)
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == len(self.games):
                        self.running = False
                    else:
                        self.try_launch_game(self.games[self.selected_index])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                start_y = 50
                for i, game in enumerate(self.games):
                    rect = pygame.Rect(40, start_y + i * 30, 200, 28)
                    if rect.collidepoint(mx, my):
                        self.try_launch_game(game)
                        break
                quit_rect = pygame.Rect(40, start_y + len(self.games) * 30, 100, 28)
                if quit_rect.collidepoint(mx, my):
                    self.running = False

    def try_launch_game(self, game_name):
        # Check if game is already running
        if not self.debug:
            if self.launched_games:
                print("A game is already running. Close it before launching another.")
                return

        proc = self.launched_games.get(game_name)
        if proc:
            if proc.poll() is None:
                print(f"Game '{game_name}' is already running.")
                return
            else:
                self.launched_games.pop(game_name)

        print(f"Launching game '{game_name}'...")
        proc = subprocess.Popen([sys.executable, "run_game.py", game_name])
        self.launched_games[game_name] = proc

        if not self.debug:
            pygame.display.iconify()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.handle_input()
            self.draw_menu()

            # Check launched games; if any ended, remove them and restore window
            ended_games = []
            for game, proc in self.launched_games.items():
                if proc.poll() is not None:  # process ended
                    print(f"Game '{game}' closed.")
                    ended_games.append(game)

            for game in ended_games:
                self.launched_games.pop(game)

            if ended_games and not self.debug:
                # Restore launcher window only if any game ended and not in debug mode
                pygame.display.set_mode((self.width, self.height))

            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    # Use debug=True for development/testing to allow multiple games and keep launcher visible
    launcher = Launcher(debug=False)
    launcher.run()
