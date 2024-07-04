import time
import win32gui
import win32process
import psutil
from datetime import datetime, timedelta
from customtkinter import *
def get_process_filename(hwnd):
    try:
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)
        filename = process.exe()
        return filename
    except psutil.Error:
        return None
def win_for_warn(filename,title):
    toplevel=CTkToplevel()
    CTkLabel(toplevel,text=f"filename : \n{filename}\n\n\n title   :{title}").pack()
def log_window_events():
    open_windows = {}
    close_threshold = timedelta(seconds=5)

    while True:
        current_windows = {}
        active_windows = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                window_filename = get_process_filename(hwnd)
                current_windows[hwnd] = {'title': window_title, 'filename': window_filename}

        win32gui.EnumWindows(callback, None)

        current_time = datetime.now()
        current_window_ids = set(current_windows.keys())
        open_window_ids = set(open_windows.keys())

        # Check for newly opened windows
        for hwnd in current_window_ids - open_window_ids:
            window_title = current_windows[hwnd]['title']
            window_filename = current_windows[hwnd]['filename']
            open_windows[hwnd] = {
                'title': window_title,
                'filename': window_filename,
                'start_time': current_time
            }
            print(f"Window opened: {window_title} - File: {window_filename}")
            with open('log.txt', 'a') as f:
                f.write(f"{current_time} - Window opened: {window_title} - File: {window_filename}\n")

        # Check for closed or inactive windows
        for hwnd in open_window_ids - current_window_ids:
            window_data = open_windows.pop(hwnd)
            window_title = window_data['title']
            window_filename = window_data['filename']
            start_time = window_data['start_time']
            duration = current_time - start_time
            if duration < close_threshold:
                print(f"Window closed quickly: {window_title} - File: {window_filename} ({duration.total_seconds():.2f} seconds)")
                with open('log.txt', 'a') as f:
                    f.write(f"{current_time} - Window closed quickly: {window_title} - File: {window_filename} ({duration.total_seconds():.2f} seconds)\n")
                if "explorer" not in window_filename:
                    win_for_warn(window_filename,window_title)

        # Check for actively open windows
        for hwnd in open_window_ids & current_window_ids:
            window_title = current_windows[hwnd]['title']
            window_filename = current_windows[hwnd]['filename']
            active_windows.append(hwnd)

        """# Prompt message box for short-lived active windows
        for hwnd in active_windows:
            window_data = open_windows[hwnd]
            start_time = window_data['start_time']
            duration = current_time - start_time
            if duration < close_threshold:
                print(f"Short-lived active window: {window_data['title']} - File: {window_data['filename']} ({duration.total_seconds():.2f} seconds)")
                # Example: Replace with code to prompt message box
"""
        time.sleep(0.4)

if __name__ == "__main__":
    log_window_events()
