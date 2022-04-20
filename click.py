import win32api, win32con

def do_click(x,y, click=False):
    win32api.SetCursorPos((x,y))
    
    if click:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

do_click(450,510)