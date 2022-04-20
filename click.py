import win32api, win32con, win32gui

def do_click(x,y, click=False):
    win32api.SetCursorPos((x,y))
    
    if click:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


def callback(hwnd, extra):
    if win32gui.GetWindowText(hwnd) == 'Stop all Regin Programs':
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        
        do_click(x+160,y+230, True)
        

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    main()