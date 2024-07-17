import os
import json
import subprocess
import requests

# 从环境变量中获取密钥
accounts_json = os.getenv('ACCOUNTS_JSON')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# 解析 JSON 字符串
servers = json.loads(accounts_json)

# 初始化汇总消息
summary_message = "serv00-vless 恢复操作结果：\n"

# 遍历服务器列表并执行恢复操作
for server in servers:
    host = server['host']
    port = server['port']
    username = server['username']
    password = server['password']

    print(f"连接到 {host}...")

    # 执行恢复命令（这里假设使用 SSH 连接和密码认证）
    restore_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -p {port} {username}@{host} 'cd ~/domains/onionbabylove.cloudns.ch/vless && ./check_vless.sh'"
    try:
        output = subprocess.check_output(restore_command, shell=True, stderr=subprocess.STDOUT)
        summary_message += f"\n成功恢复 {host} 上的 vless 服务：\n{output.decode('utf-8')}"
    except subprocess.CalledProcessError as e:
        summary_message += f"\n无法恢复 {host} 上的 vless 服务：\n{e.output.decode('utf-8')}"

# 发送汇总消息到 Telegram
telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
telegram_payload = {
    "chat_id": telegram_chat_id,
    "text": summary_message,
    "reply_markup": '{"inline_keyboard":[[{"text":"问题反馈❓","url":"https://t.me/yxjsjl"}]]}'
}

# 打印请求的详细信息
print(f"Telegram 请求 URL: {telegram_url}")
print(f"Telegram 请求 Payload: {telegram_payload}")

# 发送请求到 Telegram
response = requests.post(telegram_url, json=telegram_payload)

# 打印请求的状态码和返回内容
print(f"Telegram 请求状态码：{response.status_code}")
print(f"Telegram 请求返回内容：{response.text}")

if response.status_code != 200:
    print("发送 Telegram 消息失败")
else:
    print("发送 Telegram 消息成功")
