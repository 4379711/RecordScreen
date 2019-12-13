import os
import win32gui
import win32con
import time
from RecordVideo import RecordVideo
from threading import Thread


class TestTaskbarIcon:
    def __init__(self):
        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonRecordScreen"
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy}
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "PythonRecordScreen", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)

        icon = os.path.join(os.path.abspath(os.path.dirname(__file__)) + 'ico.ico')
        if os.path.isfile(icon):

            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:

            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "PythonRecordScreen")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def showMsg(self, title, msg):
        nid = (self.hwnd,  # 句柄
               0,  # 托盘图标ID
               win32gui.NIF_INFO,  # 标识
               0,  # 回调消息ID
               0,  # 托盘图标句柄
               "TestMessage",  # 图标字符串
               msg,  # 气球提示字符串
               0,  # 提示的显示时间
               title,  # 提示标题
               win32gui.NIIF_INFO  # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.


if __name__ == '__main__':
    t = TestTaskbarIcon()
    t.showMsg("出来吧!", "皮卡丘!")
    ####################################
    rv = RecordVideo()
    print(rv.cmd)
    if rv.cmd:
        record_thread = Thread(target=rv.ffmpeg, args=(rv.cmd,), daemon=True)
        rv.start(record_thread)
        time.sleep(150)
        rv.stop()
        ###################################
        win32gui.DestroyWindow(t.hwnd)
