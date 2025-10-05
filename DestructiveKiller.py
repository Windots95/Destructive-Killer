import win32gui
import win32con
import win32api
import random
import time
import math
import subprocess
import os

STAGES = 200

def get_desktop_dc():
    hwnd = win32gui.GetDesktopWindow()
    return win32gui.GetDC(hwnd)

def random_color():
    return win32api.RGB(random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255))

# ----------- Effects (safe visual only) -----------

def pixelate(hdc, w, h, steps=200):
    for _ in range(steps):
        small_w, small_h = w // 8, h // 8
        win32gui.StretchBlt(hdc, 0, 0, small_w, small_h,
                            hdc, 0, 0, w, h, win32con.SRCCOPY)
        win32gui.StretchBlt(hdc, 0, 0, w, h,
                            hdc, 0, 0, small_w, small_h, win32con.SRCCOPY)
        time.sleep(0.05)

def bouncing_squares(hdc, w, h, steps=200):
    x, y = w//2, h//2
    dx, dy = 15, 12
    for _ in range(steps):
        x += dx; y += dy
        if x < 0 or x > w-60: dx *= -1
        if y < 0 or y > h-60: dy *= -1
        brush = win32gui.CreateSolidBrush(random_color())
        win32gui.Rectangle(hdc, x, y, x+50, y+50)
        win32gui.DeleteObject(brush)
        time.sleep(0.02)

def flashing_lights(hdc, w, h, steps=200):
    for _ in range(steps):
        x1 = random.randint(0, w-100)
        y1 = random.randint(0, h-100)
        x2 = x1 + random.randint(50, 200)
        y2 = y1 + random.randint(50, 200)
        brush = win32gui.CreateSolidBrush(random_color())
        win32gui.FillRect(hdc, (x1, y1, x2, y2), brush)
        win32gui.DeleteObject(brush)
        time.sleep(0.03)

def triangles_and_lights(hdc, w, h, steps=200):
    for _ in range(steps):
        pts = [(random.randint(0, w), random.randint(0, h)),
               (random.randint(0, w), random.randint(0, h)),
               (random.randint(0, w), random.randint(0, h))]
        brush = win32gui.CreateSolidBrush(random_color())
        win32gui.Polygon(hdc, pts)
        win32gui.DeleteObject(brush)
        if random.random() < 0.4:
            bx = random.randint(0, w-150)
            by = random.randint(0, h-150)
            brush2 = win32gui.CreateSolidBrush(random_color())
            win32gui.FillRect(hdc, (bx, by, bx+100, by+100), brush2)
            win32gui.DeleteObject(brush2)
        time.sleep(0.02)

def spin_desktop(hdc, w, h, steps=200):
    for i in range(steps):
        angle = (i % 360) * math.pi/180
        offset_x = int(20 * math.cos(angle))
        offset_y = int(20 * math.sin(angle))
        win32gui.BitBlt(hdc, offset_x, offset_y, w-offset_x, h-offset_y,
                        hdc, 0, 0, win32con.SRCCOPY)
        time.sleep(0.03)

def crazy_mix(hdc, w, h, steps=200):
    for _ in range(steps):
        choice = random.choice(["rect","ellipse","line","blit"])
        if choice == "rect":
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = x1+random.randint(30,150), y1+random.randint(30,150)
            brush = win32gui.CreateSolidBrush(random_color())
            win32gui.Rectangle(hdc, x1, y1, x2, y2)
            win32gui.DeleteObject(brush)
        elif choice == "ellipse":
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = x1+random.randint(30,150), y1+random.randint(30,150)
            brush = win32gui.CreateSolidBrush(random_color())
            win32gui.Ellipse(hdc, x1, y1, x2, y2)
            win32gui.DeleteObject(brush)
        elif choice == "line":
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = random.randint(0, w), random.randint(0, h)
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, random_color())
            old_pen = win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.SelectObject(hdc, old_pen)
            win32gui.DeleteObject(pen)
        elif choice == "blit":
            ox = random.randint(-30, 30)
            oy = random.randint(-30, 30)
            win32gui.BitBlt(hdc, ox, oy, w-abs(ox), h-abs(oy), hdc, 0, 0, win32con.SRCCOPY)
        time.sleep(0.01)

# ----------- Stage manager -----------

def run_stage(stage, hdc, w, h):
    if stage == 1:
        pixelate(hdc, w, h)
    elif stage == 2:
        bouncing_squares(hdc, w, h)
    elif stage == 3:
        flashing_lights(hdc, w, h)
    elif stage == 4:
        triangles_and_lights(hdc, w, h)
    elif stage % 10 == 0:
        spin_desktop(hdc, w, h)
    else:
        crazy_mix(hdc, w, h)

# ----------- Main -----------

def main():
    print("Opening...")

    # First warning
    warning1 = (
        "⚠ WARNING LIST (10-foot long)\n\n"
        "- This program is VISUAL ONLY.\n"
        "- It will NOT delete files.\n"
        "- It will NOT touch System32.\n"
        "- It will NOT touch your documents.\n"
        "- It will ONLY draw shapes, colors, and effects.\n"
        "- You can stop it anytime with Ctrl+C.\n"
        "- It uses GDI functions (BitBlt, Polygon, etc.).\n"
        "- There are 200 stages of effects.\n"
        "- Some effects are bright/flashing.\n"
        "- Do not use if sensitive to flashing lights.\n"
        "- Safe for your data, 100%.\n"
        "- No disk writes, no deletes.\n"
        "- Only visual screen distortions.\n"
        "- Desktop returns to normal when finished.\n"
        "- Your wallpaper is untouched.\n"
        "- Explorer shell is untouched.\n"
        "- No files are modified.\n"
        "- No apps are auto-opened.\n"
        "- This is harmless fun.\n"
        "- Continue only if you accept.\n"
    )
    win32api.MessageBox(0, warning1, "⚠ FIRST WARNING", win32con.MB_ICONEXCLAMATION)

    # Second warning
    warning2 = (
        "⚠ LAST WARNING (3-foot list)\n\n"
        "- This program is safe.\n"
        "- It does NOT delete or change files.\n"
        "- It ONLY shows flashing shapes.\n"
        "- You can quit anytime (Ctrl+C).\n"
        "- By clicking OK, you agree.\n"
    )
    win32api.MessageBox(0, warning2, "⚠ LAST WARNING", win32con.MB_ICONEXCLAMATION)

    # --- Open Notepad with a 124-line message ---
    textfile = "DestructiveKiller_Info.txt"
    with open(textfile, "w", encoding="utf-8") as f:
        f.write("📜 Destructive Killer Information\n\n")
        for i in range(1, 125):
            f.write(f"Line {i}: This is part of the Destructive Killer visual experience.\n")

    # Open real Notepad with the file
    subprocess.Popen(["notepad.exe", os.path.abspath(textfile)])

    # --- Begin visual effects ---
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    hdc = get_desktop_dc()

    try:
        for stage in range(1, STAGES+1):
            run_stage(stage, hdc, w, h)
    except KeyboardInterrupt:
        win32gui.ReleaseDC(win32gui.GetDesktopWindow(), hdc)

if __name__ == "__main__":
    main()
