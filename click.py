import win32api, win32con, win32gui, time, environ

env = environ.Env()
environ.Env.read_env()

debug = env.int('DEBUG')


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


def callback(hwnd, extra):
    if win32gui.GetWindowText(hwnd) == 'Stop all Regin Programs':
        #win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        
        do_click(x+160,y+230)
    
    time.sleep(30)


def main():
    win32gui.EnumWindows(callback, None)


if __name__ == '__main__':
    main()