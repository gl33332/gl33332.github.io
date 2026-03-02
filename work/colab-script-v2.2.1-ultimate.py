# ==========================================
# 🚀 语音转文字监控脚本 V2.2.1 - 堡垒终极版
# 核心升级：三维特征码防重 / 纯文本防崩 / 超时防卡死 / 精准历史比对
# ==========================================

import os
import time
import subprocess
import requests
from google.colab import drive
from google.colab import userdata

# --- 1. 核心与安全配置区 ---
try:
    TELEGRAM_TOKEN = userdata.get('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = userdata.get('TELEGRAM_CHAT_ID')
except Exception as e:
    print("❌ 严重错误：未配置 Secrets (TELEGRAM_TOKEN / TELEGRAM_CHAT_ID)")
    raise e

# 目录划分更清晰，避免文件污染
BASE_DIR = '/content/drive/MyDrive/音频'
MONITOR_PATH = BASE_DIR
TRANSCRIPT_DIR = os.path.join(BASE_DIR, '转写结果')
HISTORY_LOG = os.path.join(BASE_DIR, 'processed_log.txt')
FAILED_LOG = os.path.join(BASE_DIR, 'failed_log.txt')

PROMPT_WORDS = "哈密物流、建材生意、运费博弈、回程车安排、石材矿项目、走流水、国央企对接。"

# --- 2. 核心功能函数 ---

def init_environment():
    """初始化云端环境与网盘挂载"""
    print("🛠 [1/3] 正在挂载 Google Drive...")
    drive.mount('/content/drive', force_remount=True)
    print("📦 [2/3] 检查并安装底层转写引擎...")
    subprocess.run(["pip", "install", "-q", "whisper-ctranslate2"], check=True)
    print("📂 [3/3] 正在构建军械库目录...")
    os.makedirs(MONITOR_PATH, exist_ok=True)
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    print("📡 环境阵地部署完毕！\n")

def get_file_signature(filepath):
    """【A脑建议】三维特征码：文件名|大小|修改时间"""
    if not os.path.exists(filepath):
        return None
    try:
        size = os.path.getsize(filepath)
        mtime = int(os.path.getmtime(filepath))
        return f"{os.path.basename(filepath)}|{size}|{mtime}"
    except Exception:
        return None

def load_history():
    """读取已处理特征码库"""
    if os.path.exists(HISTORY_LOG):
        with open(HISTORY_LOG, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def append_history(signature):
    """【A脑修正】纯净历史记录，不带时间戳，确保精准比对"""
    with open(HISTORY_LOG, "a", encoding="utf-8") as f:
        f.write(signature + "\n")

def save_to_log(log_path, content):
    """通用错误日志追加写入（带时间戳）"""
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {content}\n")

def wait_for_file_sync(filepath, timeout=300):
    """【防抖神器】等待文件完全落盘，带异常保护"""
    print(f"⏳ 正在校验文件完整性: {os.path.basename(filepath)}")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            size1 = os.path.getsize(filepath)
            time.sleep(5)
            size2 = os.path.getsize(filepath)
            if size1 == size2 and size1 > 0:
                return True
            else:
                print(f"🔄 仍在传输中，当前: {size2 / 1024 / 1024:.2f} MB...")
                time.sleep(5)
        except Exception as e:
            print(f"⚠️ 同步校验异常: {e}")
            return False
    print("❌ 文件同步超时，已跳过。")
    return False

def split_and_send_telegram(text, filename):
    """【长文本分发】A脑建议：彻底移除 parse_mode，发送最稳纯文本"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    chunk_size = 3500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    for idx, chunk in enumerate(chunks):
        title = f"🤖 【三脑情报站】(第 {idx+1}/{len(chunks)} 部分)\n📂 录音: {filename}\n--------------------------------\n"
        payload = title + chunk
        try:
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": payload}
            response = requests.post(url, data=data, timeout=15)
            if response.status_code == 200:
                print(f"📡 分片 [{idx+1}/{len(chunks)}] 推送成功。")
            else:
                print(f"⚠️ 推送分片 [{idx+1}] 被拒，状态码: {response.status_code}")
                save_to_log(FAILED_LOG, f"Telegram推送失败: {filename} - 分片{idx+1}")
                time.sleep(1.5)
        except Exception as e:
            print(f"❌ 推送分片 [{idx+1}] 崩溃: {e}")
            save_to_log(FAILED_LOG, f"Telegram推送异常: {filename} - {str(e)}")
            time.sleep(1.5)

def transcribe_audio(input_file):
    """稳定单轨转写，输出至独立文件夹，带超时防卡死"""
    filename = os.path.basename(input_file)
    base_name = os.path.splitext(filename)[0]
    txt_file_path = os.path.join(TRANSCRIPT_DIR, f"{base_name}.txt")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"🧠 [GPU 启动 {attempt+1}/{max_retries}] 正在深度解析语音...")

            cmd = [
                "whisper-ctranslate2", input_file,
                "--model", "large-v3",
                "--language", "zh",
                "--initial_prompt", PROMPT_WORDS,
                "--output_dir", TRANSCRIPT_DIR
            ]

            # A脑建议：增加 timeout=3600 (1小时)，防止极其损坏的音频导致死锁
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

            if result.returncode == 0 and os.path.exists(txt_file_path):
                with open(txt_file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f"⚠️ 引擎返回异常: {result.stderr[-200:]}")

        except subprocess.TimeoutExpired:
            print(f"❌ 转写进程严重超时 (超 1 小时)，强制终止当前尝试。")
        except Exception as e:
            print(f"❌ 转写进程硬核崩溃: {e}")

        time.sleep(5)

    return None

# --- 3. 铁壁防御主循环 ---

def start_monitor():
    print(f"🚀 [雷达启动] 全天候监控中...")
    print(f"📂 监听目录: {MONITOR_PATH}")
    print(f"📝 存档目录: {TRANSCRIPT_DIR}\n")

    while True:
        try:
            if not os.path.exists(MONITOR_PATH):
                time.sleep(10)
                continue

            processed_signatures = load_history()
            all_files = [f for f in os.listdir(MONITOR_PATH) if f.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg', '.flac'))]

            for file in all_files:
                input_file = os.path.join(MONITOR_PATH, file)
                file_sig = get_file_signature(input_file)

                # 特征码匹配
                if file_sig and file_sig not in processed_signatures:
                    print(f"\n🎯 锁定新目标: {file}")

                    if not wait_for_file_sync(input_file):
                        continue

                    # 重新获取三维特征码
                    final_sig = get_file_signature(input_file)

                    content = transcribe_audio(input_file)

                    if content:
                        split_and_send_telegram(content, file)
                        # 【修正】使用纯净的 append_history 写入，杜绝死循环
                        append_history(final_sig)
                        print(f"✅ 战利品回收完毕，[{file}] 已存入历史档案。")
                    else:
                        print(f"❌ 目标解析彻底失败，已登记至错题本。")
                        save_to_log(FAILED_LOG, f"彻底转写失败: {file}")

            time.sleep(30)

        except KeyboardInterrupt:
            print("\n👋 接收到 Boss 手动挂起指令，雷达休眠。")
            break
        except Exception as e:
            print(f"⚠️ 雷达阵列受干扰，30秒后重启: {e}")
            time.sleep(30)

if __name__ == "__main__":
    init_environment()
    start_monitor()
