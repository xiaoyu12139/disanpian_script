import pyautogui
import time

print("Move your mouse to the desired position and press Ctrl+C to stop.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})", end="\r")  # 打印当前鼠标位置
        time.sleep(1)  # 稍微延迟以减少CPU使用率
except KeyboardInterrupt:
    print("\nStopped.")