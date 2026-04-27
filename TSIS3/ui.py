import pygame

WHITE = (245, 245, 245)
BLACK = (20, 20, 25)
DARK = (35, 35, 45)
GRAY = (140, 140, 150)


class Button:
    def __init__(self, x, y, w, h, text, font, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            color = tuple(min(255, c + 30) for c in self.color)
        else:
            color = self.color

        pygame.draw.rect(screen, (0, 0, 0), self.rect.move(4, 4), border_radius=14)
        pygame.draw.rect(screen, color, self.rect, border_radius=14)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=14)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_text(screen, text, font, color, center=None, topleft=None):
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = center

    if topleft:
        text_rect.topleft = topleft

    screen.blit(text_surface, text_rect)


def ask_username(screen, clock, width, height):
    title_font = pygame.font.SysFont("Verdana", 42, bold=True)
    font = pygame.font.SysFont("Verdana", 30)
    small_font = pygame.font.SysFont("Verdana", 18)

    name = ""

    while True:
        screen.fill(BLACK)

        draw_text(screen, "ENTER USERNAME", title_font, WHITE, center=(width // 2, 170))
        draw_text(screen, "Press ENTER to start", small_font, GRAY, center=(width // 2, 225))

        input_rect = pygame.Rect(width // 2 - 170, 290, 340, 60)
        pygame.draw.rect(screen, DARK, input_rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=12)

        shown_name = name if name else "Player"
        draw_text(screen, shown_name, font, WHITE, center=input_rect.center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Player"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name if name else "Player"

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode

        pygame.display.flip()
        clock.tick(60)