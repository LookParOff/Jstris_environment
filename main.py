from parser_for_Jstris import Jstris
# import parser
import pygame


if __name__ == "__main__":
    path_to_chrome_driver = r"C:\Program Files (x86)\Google\chromedriver.exe"
    jstris = Jstris(path_to_chrome_driver, "Practice", False)
    display_width = 800
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    running = True
    while running:
        try:
            screen, queue, stats = jstris.get_frame_of_game()
            stats = stats.crop((0, 0, 96, 40))
        except Exception as e:
            print("I catch exception while getting screen of game:")
            print(e)
            break

        # Convert PIL image to pygame image
        py_screen = pygame.image.fromstring(screen.tobytes(), screen.size, screen.mode)
        py_queue = pygame.image.fromstring(queue.tobytes(), queue.size, queue.mode)
        py_stats = pygame.image.fromstring(stats.tobytes(), stats.size, stats.mode)
        gameDisplay.blit(py_screen, (0, 0))
        gameDisplay.blit(py_queue, (screen.size[0], 0))
        gameDisplay.blit(py_stats, (0, screen.size[1]))

        pygame.display.update()
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    jstris.close()
    pygame.quit()
