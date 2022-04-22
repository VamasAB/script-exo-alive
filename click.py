import win32api, win32con, win32gui, time, environ

env = environ.Env()
environ.Env.read_env()

debug = env.int('DEBUG')
delayed_start = env.int('DELAYED_START')
program = env.str('PROGRAM')

but_offset_x = env.int('BUTTON_OFFSET_X')
but_offset_y = env.int('BUTTON_OFFSET_Y')

ico_offset_x = env.int('ICON_OFFSET_X')
ico_offset_y = env.int('ICON_OFFSET_Y')

def minimize():
    win32api.keybd_event(0x5B,0,0,0)
    time.sleep(.1)
    win32api.keybd_event(0x44,0,0,0)
    time.sleep(.1)
    win32api.keybd_event(0x44,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(.1)
    win32api.keybd_event(0x5B,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(.1)


def do_click(x,y, double=False):
    def left_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    win32api.SetCursorPos((x,y))
    
    if debug:
        left_click()
        if double:
            time.sleep(0.2)
            left_click()


def main():
    handle = win32gui.FindWindow(0, program)
    win32gui.SetForegroundWindow(handle)
    time.sleep(2)
    rect = win32gui.GetWindowRect(handle)
    x = rect[0] + but_offset_x
    y = rect[1] + but_offset_y

    do_click(x,y)

    time.sleep(delayed_start)
    minimize()
    time.sleep(2)
    do_click(ico_offset_x,ico_offset_y,True)


if __name__ == '__main__':
    main()