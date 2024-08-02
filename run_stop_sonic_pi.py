import pygetwindow as gw
import pyautogui
import time

def bring_sonic_pi_to_foreground():
    # List all windows
    windows = gw.getAllTitles()
    
    # Look for a window with 'Sonic Pi' in the title
    sonic_pi_window = None
    for window in windows:
        if 'Sonic Pi' in window:
            sonic_pi_window = gw.getWindowsWithTitle(window)[0]
            break

    if sonic_pi_window:
        # Bring the Sonic Pi window to the foreground
        sonic_pi_window.activate()
        print("Sonic Pi window brought to foreground.")
        return True
    else:
        print("Sonic Pi window not found.")
        return False

def trigger_alt_s():
    # Wait a moment to ensure the window is active
    time.sleep(1)
    
    # Press Alt+S
    pyautogui.hotkey('alt', 's')
    print("Triggered Alt+S shortcut.")

def trigger_alt_r():
    # Wait a moment to ensure the window is active
    time.sleep(1)
    
    # Press Alt+S
    pyautogui.hotkey('alt', 'r')
    print("Triggered Alt+S shortcut.")

def stop_sonic_pi():
    if bring_sonic_pi_to_foreground():
        trigger_alt_s()

def run_sonic_pi():
    if bring_sonic_pi_to_foreground():
        trigger_alt_r()

