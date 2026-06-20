import pygame
from core.config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, FPS

pygame.init()

screen = pygame.display.set_mode(
    (GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)
)
pygame.display.set_caption("Maui's Cave Adventure")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

# --------------------
# LOAD SPRITES
# --------------------
player_img = pygame.image.load(
    "assets/tiles/sprites/player.png"
).convert_alpha()

player_img = pygame.transform.scale(
    player_img, (TILE_SIZE, TILE_SIZE)
)

floor = pygame.image.load("assets/tiles/floor.png").convert()
wall = pygame.image.load("assets/tiles/wall2.png").convert()
door = pygame.image.load("assets/tiles/open_door.png").convert()

floor = pygame.transform.scale(floor, (TILE_SIZE, TILE_SIZE))
wall = pygame.transform.scale(wall, (TILE_SIZE, TILE_SIZE))
door = pygame.transform.scale(door, (TILE_SIZE, TILE_SIZE))

# --------------------
# PLAYER (GRID POSITION ONLY)
# --------------------
player_col = 5
player_row = 4

# --------------------
# ROOM
# --------------------
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

# --------------------
# GAME LOOP
# --------------------
running = True

while running:

    # -------- EVENTS --------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            target_row = player_row
            target_col = player_col

            if event.key == pygame.K_UP:
                target_row -= 1
            elif event.key == pygame.K_DOWN:
                target_row += 1
            elif event.key == pygame.K_LEFT:
                target_col -= 1
            elif event.key == pygame.K_RIGHT:
                target_col += 1

            # COLLISION CHECK
            if 0 <= target_row < len(room) and 0 <= target_col < len(room[0]):
                if room[target_row][target_col] != "W":
                    player_row = target_row
                    player_col = target_col

    # -------- DRAW --------
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

    # draw player
    player_x = offset_x + player_col * TILE_SIZE
    player_y = offset_y + player_row * TILE_SIZE
    screen.blit(player_img, (player_x, player_y))

    # title
    text = font.render("Maui's Cave Adventure", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()