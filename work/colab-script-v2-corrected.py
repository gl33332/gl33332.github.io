# ==========================================
# 🚀 语音转文字监控脚本 V2.1 - 单线程稳定版
# ==========================================

import os
import time
import requests
import threading
from queue import Queue
from google.colab import drive

# --- 核心配置区 ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
MONITOR_PATH = os.getenv("MONITOR_PATH", "/content/drive/MyDrive/音频")
HISTORY_LOG = os.getenv("HISTORY_LOG", "/content/drive/MyDrive/音频/processed_log.txt")

# --- 队列机制（不是并发，而是解耦）---
new_file_queue = Queue()
queue_lock = threading.Lock()
processing = False

# --- 功能函数区 ---

def load_history():
    """加载历史记录"""
    if os.path.exists(HISTORY_LOG):
        with open(HISTORY_LOG, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_to_history(filename):
    """追加记录"""
    with open(HISTORY_LOG, 'a', encoding='utf-8') as f:
        f.write(filename + "\n")

def transcribe_file(filepath):
    """单文件转写（带断点续传）"""
    base_name = os.path.splitext(filepath)[0]
    txt_file = f"{base_name}.txt"
    
    # 检查是否已有部分结果
    if os.path.exists(txt_file):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content) > 100:  # 至少100字才算有效
            return content
    
    # 重新转写
    print(f"🧠 正在转写: {os.path.basename(filepath)}")
    
    os.system(f"whisper-ctranslate2 \"{filepath}\" --model large-v3 --language zh --output_dir .")
    
    if os.path.exists(txt_file):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    return None

def send_to_a_brain(text, filename):
    """推送结果"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = (
        "🤖 【三脑情报站】\n"
        "A 脑，检测到新通话转写，请开始博弈分析：\n"
        "--------------------------------\n"
        f"📂 文件: {filename}\n"
        f"📝 内容: \n{text}"
    )
    
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": payload}, timeout=30)
        print(f"📡 推送成功")
    except Exception as e:
        print(f"❌ 推送失败: {e}")

def monitor_thread():
    """监控线程：只负责发现新文件，放入队列"""
    global processing
    
    while True:
        try:
            if not os.path.exists(MONITOR_PATH):
                time.sleep(10)
                continue
            
            processed_files = load_history()
            all_files = [f for f in os.listdir(MONITOR_PATH) 
                        if f.endswith(('.mp3', '.m4a', '.wav', '.ogg', '.flac'))]
            
            with queue_lock:
                for file in all_files:
                    if file not in processed_files and not new_file_queue.full():
                        new_file_queue.put(file)
                        print(f"📥 发现新文件: {file}")
            
            time.sleep(30)  # 每30秒扫描一次
            
        except Exception as e:
            print(f"⚠️ 监控波动: {e}")
            time.sleep(30)

def worker_thread():
    """工作线程：从队列取出文件单线程处理"""
    global processing
    
    while True:
        try:
            filename = new_file_queue.get()
            processing = True
            
            filepath = os.path.join(MONITOR_PATH, filename)
            print(f"\n▶️ 开始处理: {filename}")
            
            content = transcribe_file(filepath)
            
            if content:
                send_to_a_brain(content, filename)
                save_to_history(filename)
                print(f"✅ 处理完成并记录: {filename}")
            
            new_file_queue.task_done()
            processing = False
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            new_file_queue.task_done()
            processing = False
            time.sleep(5)

# --- 主程序 ---

def start_monitor():
    print(f"🚀 启动监控: {MONITOR_PATH}")
    print("💡 单线程模式 + 队列解耦")
    
    # 启动监控线程
    monitor = threading.Thread(target=monitor_thread, daemon=True)
    monitor.start()
    
    # 启动工作线程
    worker = threading.Thread(target=worker_thread, daemon=True)
    worker.start()
    
    # 主线程等待（保持后台运行）
    while True:
        time.sleep(60)
        status = "🟢 处理中" if processing else "⚪ 等待中"
        print(f"⏱️  运行中 {status}")

if __name__ == "__main__":
    init_environment()
    start_monitor()
