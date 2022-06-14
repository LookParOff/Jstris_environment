import time
from parser_for_Jstris import Jstris
import numpy as np
import pygame


class GymJstris:
    def __init__(self, path_to_chrome_driver, mode_of_game,
                 headless=True, enable_to_play=False, grayscale=True):
        self.jstris = Jstris(path_to_chrome_driver, mode_of_game, headless, grayscale)
        self.previous_score = 0
        display_width = 800
        display_height = 600
        self.game_display = pygame.display.set_mode((display_width, display_height))
        # if human decide to play:
        self.enable_to_play = enable_to_play
        self.available_keys = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1,
                               pygame.K_DOWN: 2, pygame.K_SPACE: 3,
                               pygame.K_z: 4, pygame.K_UP: 5,
                               pygame.K_a: 6,
                               pygame.K_c: 7}
        # with this we can recognize digits in get_reward()
        self.characteristic = np.array([87.1529, 78.8265, 83.2353, 83.3853, 84.0206,
                                        85.8324, 86.2794, 79.4059, 89.6441, 86.0971, 60])

    def get_stats(self, stats_img):
        score_img = stats_img.crop((0, 20, 96, 40))
        reward = self.get_reward(score_img)
        return reward

    def get_reward(self, score_img):
        score = ""
        width_of_one_digit = 12
        width = score_img.size[0]
        for pixel_ind in range(0, width, width_of_one_digit):
            digit_img = score_img.crop((pixel_ind, 0, pixel_ind + width_of_one_digit, 20))
            digit_arr = np.array(digit_img)
            # make image gray and normalized
            digit_arr = np.sum(digit_arr, axis=2) / (255 * digit_arr.shape[2])
            digit = np.argmin(np.abs(self.characteristic - digit_arr.sum()))
            if digit == 10:
                # only when digit_img is a black image without digit
                break
            score += str(digit)
        score = int(score)
        return score

    def step(self, action):
        """
        0, 1: left and right moves of shapes
        2, 3: soft drop, hard drop
        4, 5: rotate left, rotate right
        6: rotate 180
        7: hold
        """
        self.jstris.perform_action(action)
        main_img, queue_img, hold_img, stats_img = self.jstris.get_frame_of_game()
        obs = np.array(main_img)
        reward = self.get_stats(stats_img)
        done = False  # somewhere need to subtract time and previous_time
        return obs, reward, done, None

    def render(self):
        if self.enable_to_play:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in self.available_keys.keys():
                    action = self.available_keys[event.key]
                    _, reward, _, _ = self.step(action)
                    print(reward, "\r", end="")
                if event.type == pygame.QUIT:
                    self.close()
                    return False
        screen, queue, hold, stats = self.jstris.get_frame_of_game()
        stats = stats.crop((0, 0, 96, 40))
        # Convert PIL image to pygame image
        py_screen = pygame.image.fromstring(screen.tobytes(), screen.size, screen.mode)
        py_queue = pygame.image.fromstring(queue.tobytes(), queue.size, queue.mode)
        py_hold = pygame.image.fromstring(hold.tobytes(), hold.size, hold.mode)
        py_stats = pygame.image.fromstring(stats.tobytes(), stats.size, stats.mode)
        # render everything
        self.game_display.blit(py_screen, (0, 0))
        self.game_display.blit(py_queue, (screen.size[0], 0))
        self.game_display.blit(py_hold, (screen.size[0] + queue.size[0], 0))
        self.game_display.blit(py_stats, (0, screen.size[1]))
        pygame.display.update()
        return True

    def close(self):
        self.jstris.close()
        pygame.quit()

    def reset(self):
        self.jstris.reset()
        self.previous_score = 0


if __name__ == "__main__":
    path_to_browser_driver = r"C:\Program Files (x86)\Google\chromedriver.exe"
    game_mode = "Practice"
    gym = GymJstris(path_to_browser_driver, game_mode, enable_to_play=True)
    running = True
    while running:
        running = gym.render()
