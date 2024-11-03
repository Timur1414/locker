import hashlib
import sys
import pygame
import os

import win32con
import win32gui


def update_size(screen):
    return screen.get_width(), screen.get_height()


def check_input(input_text):
    input_salt = f'{input_text}{len(input_text)}'
    sha224 = hashlib.sha224()
    sha224.update(input_salt.encode())
    return sha224.hexdigest() == '9f17cd624f25b28374a58a6c107d3d0df4299ddccfe390eeba373d12'


def main():
    pygame.init()
    pygame.font.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.NOFRAME | pygame.WINDOWFOCUSGAINED)
    size = width, height = update_size(screen)
    flag = False


    # hwnd = win32gui.GetForegroundWindow()
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)

    BLACK = pygame.color.Color('black')
    RED = pygame.color.Color('red')
    WHITE = pygame.color.Color('white')

    font = pygame.font.Font(None, 74)
    input_text = ''
    attempts_count = 3
    end = False
    while not end:
        if not pygame.display.get_active() and not flag:
            print(1)
            print(os.system('python.exe .\main.py'))
            # print(os.system('python.exe .\main.py'))
            flag = True
            # print(hwnd)
            # hwnd = pygame.display.get_wm_info()["window"]
            # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if check_input(input_text):
                        end = True
                    input_text = ''
                    attempts_count -= 1
                else:
                    input_text += event.unicode

        header_surface = font.render('Lock', True, RED)
        attempts_surface = font.render(f'Attempts: {attempts_count}', True, RED)
        input_surface = font.render(input_text, True, WHITE)

        screen.fill(BLACK)
        screen.blit(header_surface, (width // 2 - header_surface.get_width() / 2, 250))
        screen.blit(attempts_surface, (width // 2 - attempts_surface.get_width() / 2, 350))
        screen.blit(input_surface, (width // 2 - input_surface.get_width() / 2, 500))
        pygame.display.flip()
        pygame.time.wait(5)
    sys.exit(0)


if __name__ == '__main__':
    main()
