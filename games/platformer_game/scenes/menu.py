import pygame
from engine.scene import Scene

class MenuScene(Scene):
    FONT_SIZE = 24
    PADDING = 10
    ACTIONS = ['move_left', 'move_right', 'jump']  # actions to rebind

    def __init__(self, game):
        super().__init__(game)
        self.input_manager = game.input_manager
        self.input_manager.clear_callbacks()
        self.selected_index = 0
        self.waiting_for_key = False
        self.message = "Use Up/Down to select, Enter to rebind, R to return"

        self.input_manager.bind_key(pygame.K_r, self.exit_menu)

        # Preload font
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)

    def exit_menu(self):
        self.game.return_to_previous_scene()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.waiting_for_key:
                    # Assign new key for selected action
                    new_key = event.key
                    action = self.ACTIONS[self.selected_index]
                    self.input_manager.map_action(action, new_key)
                    self.message = f"Rebound '{action}' to {pygame.key.name(new_key)}"
                    self.waiting_for_key = False
                else:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.ACTIONS)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.ACTIONS)
                    elif event.key == pygame.K_RETURN:
                        self.waiting_for_key = True
                        self.message = f"Press a new key for '{self.ACTIONS[self.selected_index]}'"

    def update(self, dt):
        pass  # no special update logic needed

    def render(self, surface):
        surface.fill((20, 20, 20))  # dark background

        # Draw instructions / message
        msg_surf = self.font.render(self.message, True, (255, 255, 255))
        surface.blit(msg_surf, (self.PADDING, self.PADDING))

        # List actions with current bindings
        y = self.PADDING + self.FONT_SIZE + 10
        for i, action in enumerate(self.ACTIONS):
            key = self.input_manager.key_bindings.get(action)
            key_name = pygame.key.name(key) if key else "Unbound"
            text = f"{action}: {key_name}"

            color = (255, 255, 0) if i == self.selected_index else (180, 180, 180)
            action_surf = self.font.render(text, True, color)
            surface.blit(action_surf, (self.PADDING, y))
            y += self.FONT_SIZE + 5
