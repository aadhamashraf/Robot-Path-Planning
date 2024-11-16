from Basic_Attributes import *


class Button:
    def __init__(self, x, y, width, height, text, subtext=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.subtext = subtext if subtext is not None else ""
        self.action = action

    def draw(self, screen, hover=False):
        color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, 15)
        label = font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

        if self.subtext:
            subtext_label = font.render(self.subtext, True, (255, 255, 255))
            subtext_rect = subtext_label.get_rect(
                center=(self.rect.centerx, self.rect.centery + 20))
            screen.blit(subtext_label, subtext_rect)

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()
