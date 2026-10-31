import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)


def draw_snake(snake):
    """Draw all parts of the snake."""
    for segment in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)
        )


def draw_text(text, font_type, color, x, y):
    """Display text on the screen."""
    message = font_type.render(text, True, color)
    screen.blit(message, (x, y))


def main():
    # Starting snake position
    snake = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

    # Starting direction
    direction = "RIGHT"

    # Create the first apple
    apple = [
        random.randrange(0, SCREEN_WIDTH, SNAKE_SIZE),
        random.randrange(0, SCREEN_HEIGHT, SNAKE_SIZE)
    ]

    score = 0
    running = True
    game_over = False

    while running:

        # Handle keyboard and window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

                # Restart or quit after game over
                if game_over:
                    if event.key == pygame.K_r:
                        main()
                        return
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        if not game_over:
            # Get current head position
            head_x, head_y = snake[0]

            # Move the snake
            if direction == "UP":
                head_y -= SNAKE_SIZE
            elif direction == "DOWN":
                head_y += SNAKE_SIZE
            elif direction == "LEFT":
                head_x -= SNAKE_SIZE
            elif direction == "RIGHT":
                head_x += SNAKE_SIZE

            new_head = [head_x, head_y]

            # Check wall collision
            if (
                head_x < 0 or
                head_x >= SCREEN_WIDTH or
                head_y < 0 or
                head_y >= SCREEN_HEIGHT
            ):
                game_over = True

            # Check collision with itself
            if new_head in snake:
                game_over = True

            # Add new head
            snake.insert(0, new_head)

            # Check if snake eats the apple
            if new_head == apple:
                score += 1

                # Create a new apple
                apple = [
                    random.randrange(0, SCREEN_WIDTH, SNAKE_SIZE),
                    random.randrange(0, SCREEN_HEIGHT, SNAKE_SIZE)
                ]
            else:
                # Remove the tail to keep the same length
                snake.pop()

        # Draw background
        screen.fill(BLACK)

        if not game_over:
            # Draw apple
            pygame.draw.rect(
                screen,
                RED,
                (apple[0], apple[1], SNAKE_SIZE, SNAKE_SIZE)
            )

            # Draw snake
            draw_snake(snake)

            # Draw score
            draw_text(f"Score: {score}", font, WHITE, 20, 20)

        else:
            # Game over screen
            draw_text(
                "GAME OVER",
                big_font,
                RED,
                SCREEN_WIDTH // 2 - 170,
                SCREEN_HEIGHT // 2 - 80
            )
            draw_text(
                f"Final Score: {score}",
                font,
                WHITE,
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT // 2
            )
            draw_text(
                "Press R to Restart or ESC to Quit",
                font,
                WHITE,
                SCREEN_WIDTH // 2 - 220,
                SCREEN_HEIGHT // 2 + 60
            )

        # Update display
        pygame.display.flip()

        # Control game speed
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# Start the game
if __name__ == "__main__":
    main()