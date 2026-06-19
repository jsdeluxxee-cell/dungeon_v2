import pygame
from core.config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, FPS

pygame.init()

screen = pygame.display.set_mode(
    (GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)
)
pygame.display.set_caption("Maui's Cave Adventure")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

floor = pygame.image.load("assets/tiles/floor.png").convert()
wall = pygame.image.load("assets/tiles/wall2.png").convert()
door = pygame.image.load("assets/tiles/open_door.png").convert()

floor = pygame.transform.scale(floor, (TILE_SIZE, TILE_SIZE))
wall = pygame.transform.scale(wall, (TILE_SIZE, TILE_SIZE))
door = pygame.transform.scale(door, (TILE_SIZE, TILE_SIZE))

room = [
    "WWWWWWWWWDWWWWWWWWWW",
    "W..................W",
    "W..................W",
    "W..................W",
    "W..................W",
    "W..................W",
    "W..................W",
    "W..................W",
    "WWWWWWWWWDWWWWWWWWWW",
]

room_width_px = len(room[0]) * TILE_SIZE
room_height_px = len(room) * TILE_SIZE

offset_x = (screen.get_width() - room_width_px) // 2
offset_y = (screen.get_height() - room_height_px) // 2

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((40, 40, 60))

    for row_index, row in enumerate(room):
        for col_index, tile_char in enumerate(row):

            x = offset_x + col_index * TILE_SIZE
            y = offset_y + row_index * TILE_SIZE

            if tile_char == "W":
                screen.blit(wall, (x, y))
            elif tile_char == "D":
                screen.blit(door, (x, y))
            else:
                screen.blit(floor, (x, y))

    text = font.render("Maui's Cave Adventure", True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(screen.get_width() // 2, 50)
    )
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()