from core.config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, FPS
import pygame

pygame.init()

screen = pygame.display.set_mode(
    (GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)
)
pygame.display.set_caption("Maui's Cave Adventure")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

running = True
while running:

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # DRAW
    screen.fill((40, 40, 60))

    text = font.render("Maui's Cave Adventure", True, (255, 255, 255))

    text_rect = text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 - 50)
    )

    screen.blit(text, text_rect)

    # SHOW FRAME
    pygame.display.flip()

    # LIMIT FPS
    clock.tick(FPS)

pygame.quit()