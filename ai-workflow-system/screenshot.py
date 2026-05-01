"""截图ai-workflow-system项目"""
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from PIL import ImageGrab
import time

work_dir = r"C:\Users\吴嘉辉\.openclaw\workspace\ai-workflow-system"
save_path = r"C:\Users\吴嘉辉\.openclaw\workspace\ai-workflow-system-screenshot.png"

# 先打开目录资源管理器
os.startfile(work_dir)
print("打开目录中，请稍等...")
time.sleep(2)

# 截图当前屏幕（全屏）
screenshot = ImageGrab.grab()
screenshot.save(save_path, "PNG")
print(f"截图保存到: {save_path}")
print(f"尺寸: {screenshot.size[0]}x{screenshot.size[1]}")
