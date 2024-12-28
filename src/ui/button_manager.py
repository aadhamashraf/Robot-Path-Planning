import pygame
from src.ui.button import Button


class ButtonManager:
    def __init__(self, button_x, button_y, button_width, button_height, button_gap):
        self.buttons = []
        self.button_x = button_x
        self.button_y = button_y
        self.button_width = button_width
        self.button_height = button_height
        self.button_gap = button_gap

    def add_button(
        self, text, y_offset, width_offset=0, action=None, subtext=None, btn_width=0
    ):
        x = self.button_x + width_offset
        y = self.button_y + y_offset * (self.button_height + self.button_gap)
        width = self.button_width - width_offset
        if btn_width > 0:
            width = btn_width
        button = Button(x, y, width, self.button_height, text, subtext, action)
        self.buttons.append(button)
        return button

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_hover(pos):
                button.click()
                break

    def draw_all(self, screen):
        for button in self.buttons:
            button.draw(screen, button.is_hover(pygame.mouse.get_pos()))
