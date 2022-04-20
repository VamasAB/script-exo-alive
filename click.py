import win32api, win32con, win32gui

# def do_click(x,y, click=False):
#     win32api.SetCursorPos((x,y))
    
#     if click:
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

# do_click(250,330)

def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]

    print(win32gui.GetWindowText(hwnd))

    # print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    main()