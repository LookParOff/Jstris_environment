import time
from parser_for_Jstris import Jstris
import numpy as np
import pygame


# реализовать флаг done
class GymJstris:
    def __init__(self, path_to_chrome_driver, mode_of_game,
                 headless=True, enable_to_play=False, grayscale=True):
        self.jstris = Jstris(path_to_chrome_driver, mode_of_game, headless, grayscale)
        self.total_score = 0
        self.previous_time = np.array([[]])
        self.game_loading = True
        display_width = 800
        display_height = 600
        self.game_display = pygame.display.set_mode((display_width, display_height))
        # if human decide to play:
        self.enable_to_play = enable_to_play
        # with this we can recognize digits in get_reward()
        self.characteristic = np.array([87.1529, 78.8265, 83.2353, 83.3853, 84.0206,
                                        85.8324, 86.2794, 79.4059, 89.6441, 86.0971, 60])
        # self.screen, self.queue, self.hold, self.stats = self.jstris.get_frame_of_game()
        self.main_img, self.stats_img = self.jstris.get_frame_of_game()

    def get_stats(self, stats_img):
        score_img = stats_img.crop((0, 20, 96, 40))
        reward = self.get_reward(score_img)
        time_img = stats_img.crop((0, 0, 96, 20))
        done = self.get_done(time_img)
        return reward, done

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
        reward = score - self.total_score
        self.total_score += reward
        return reward

    def get_done(self, time_img):
        # time_img.save(f"time.png")
        width_of_one_digit = 12
        time_arr = np.array(time_img)
        if self.game_loading:
            # this is prevented to return done=True just in beginning of the game
            first_digit = time_arr[:, :width_of_one_digit]
            first_digit = np.sum(first_digit, axis=2) / (255 * first_digit.shape[2])
            digit = np.argmin(np.abs(self.characteristic - first_digit.sum()))
            if 1 <= digit <= 9:
                # on timer we have digit more than 0
                # this is mean, that timer is started and game is on
                self.game_loading = False
            else:
                return False
        if np.array_equal(time_arr, self.previous_time):
            return True
        else:
            self.previous_time = time_arr
            return False

    def step(self, action):
        """
        0, 1: left and right moves of shapes
        2, 3: soft drop, hard drop
        4, 5: rotate left, rotate right
        6: rotate 180
        7: hold
        """
        self.jstris.perform_action(action)
        self.main_img, self.stats_img = self.jstris.get_frame_of_game()
        # self.main_img, self.queue, self.hold, self.stats_img = self.jstris.get_frame_of_game()
        obs = np.array(self.main_img)
        reward, done = self.get_stats(self.stats_img)
        return obs, reward, done, None

    def render(self):
        stats = self.stats_img.crop((0, 0, 96, 40))
        # Convert PIL image to pygame image
        py_screen = pygame.image.fromstring(self.main_img.tobytes(),
                                            self.main_img.size, self.main_img.mode)
        # py_queue = pygame.image.fromstring(queue.tobytes(), queue.size, queue.mode)
        # py_hold = pygame.image.fromstring(hold.tobytes(), hold.size, hold.mode)
        py_stats = pygame.image.fromstring(stats.tobytes(), stats.size, stats.mode)
        # render everything
        self.game_display.blit(py_screen, (0, 0))
        # self.game_display.blit(py_queue, (screen.size[0], 0))
        # self.game_display.blit(py_hold, (screen.size[0] + queue.size[0], 0))
        self.game_display.blit(py_stats, (0, self.main_img.size[1]))
        pygame.display.update()

    def close(self):
        self.jstris.close()
        pygame.quit()

    def reset(self):
        self.jstris.reset()
        self.total_score = 0


if __name__ == "__main__":
    path_to_browser_driver = r"C:\Program Files (x86)\Google\chromedriver.exe"
    game_mode = "Practice"
    gym = GymJstris(path_to_browser_driver, game_mode, enable_to_play=True,
                    grayscale=False)
    available_keys = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1,
                      pygame.K_DOWN: 2, pygame.K_SPACE: 3,
                      pygame.K_z: 4, pygame.K_UP: 5,
                      pygame.K_a: 6,
                      pygame.K_c: 7,
                      "": 8}
    was_action = False
    act = ""
    fps = 0
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in available_keys.keys():
                act = available_keys[event.key]
                was_action = True
            if event.type == pygame.QUIT:
                gym.close()
                break
        if not was_action:
            act = available_keys[""]
        obs_, reward_, done_, info_ = gym.step(act)
        fps += 1
        if time.time() - start_time > 1:
            start_time = time.time()
            print(fps)
            fps = 0
        gym.render()
        was_action = False
