# data\platformer_game\scenes\menu.py

import pygame
from engine.base_scene import BaseScene

class MenuScene(BaseScene):
    BASE_FONT_SIZE_RATIO = 0.05  # 5% of screen height for font size
    PADDING_RATIO = 0.03         # 3% of screen width for padding
    ACTIONS = ['move_left', 'move_right', 'jump']

    def __init__(self, core):
        super().__init__(core)

        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.font_size = max(16, int(self.screen_h * self.BASE_FONT_SIZE_RATIO))
        self.padding = int(self.screen_w * self.PADDING_RATIO)
        self.line_spacing = self.font_size + 8

        self.font = pygame.font.SysFont(None, self.font_size)
        self.input_manager = core.input_manager
        self.input_manager.clear_local_callbacks()

        self.selected_index = 0
        self.waiting_for_key = False
        self.message = "Use Up/Down to select, Enter to rebind, R to return"

        self.input_manager.bind_key_down(pygame.K_m, self.exit_menu)

        self.blink_timer = 0
        self.blink_visible = True

        self.setup_input()

    """
    Input Methods
        setup_input
    """
    def setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key": pygame.K_m, "callback": self.exit_menu},
                {"key": pygame.K_UP, "callback": self.select_up},
                {"key": pygame.K_DOWN, "callback": self.select_down},
                {"key": pygame.K_RETURN, "callback": self.select_confirm},
                {"key": pygame.K_r, "callback": self.cancel_rebind},
            ]
        }
        self.input_manager.load_config(input_config)

    def exit_menu(self):
        self.game.return_scene()

    def select_up(self):
        if not self.waiting_for_key:
            self.selected_index = (self.selected_index - 1) % len(self.ACTIONS)

    def select_down(self):
        if not self.waiting_for_key:
            self.selected_index = (self.selected_index + 1) % len(self.ACTIONS)

    def select_confirm(self):
        if not self.waiting_for_key:
            self.waiting_for_key = True
            action = self.ACTIONS[self.selected_index]
            self.message = f"Press a new key for '{action}' (Esc to cancel)"

    def cancel_rebind(self):
        self.waiting_for_key = False
        self.message = "Rebinding cancelled. Use Up/Down to select, Enter to rebind, M to return"

    def events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.assign_key(event)

    def assign_key(self, event):
        if not self.waiting_for_key:
            return

        if event.key == pygame.K_ESCAPE:
            self.cancel_rebind()
            return

        if event.key == pygame.K_RETURN:
            return

        new_key = event.key
        action = self.ACTIONS[self.selected_index]
        self.input_manager.map_action_to_key(new_key, action)
        self.message = f"Rebound '{action}' to {pygame.key.name(new_key)}"
        self.waiting_for_key = False

    def update(self, dt=None):
        if self.waiting_for_key:
            self.blink_timer += dt
            if self.blink_timer >= 0.5:
                self.blink_visible = not self.blink_visible
                self.blink_timer = 0
        else:
            self.blink_visible = True

    def render(self, surface=None):
        surface.fill((20, 20, 20))

        # Draw the message (always visible, no blinking)
        msg_surf = self.font.render(self.message, True, (255, 255, 255))
        surface.blit(msg_surf, (self.padding, self.padding))

        # Start y a bit lower to add extra space after message
        y = self.padding + msg_surf.get_height() + (self.font_size // 2)

        for i, action in enumerate(self.ACTIONS):
            key = self.input_manager.action_to_key.get(action)
            key_name = pygame.key.name(key) if key else "Unbound"
            text = f"{action}: {key_name}"

            color = (255, 255, 0) if i == self.selected_index else (180, 180, 180)
            # Blink only the selected key binding when waiting for key
            if self.waiting_for_key and i == self.selected_index and not self.blink_visible:
                # Skip rendering to create blink off effect
                pass
            else:
                action_surf = self.font.render(text, True, color)
                surface.blit(action_surf, (self.padding, y))
            y += self.line_spacing
