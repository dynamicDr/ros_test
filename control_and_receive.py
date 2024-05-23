import websocket
import json
import keyboard
import threading

# 连接回调函数
def on_open(ws):
    print("Connected to rosbridge")
    # 订阅 /odom 主题
    topic = "/odom"
    subscribe_msg = json.dumps({
        "op": "subscribe",
        "topic": topic
    })
    ws.send(subscribe_msg)

# 接收消息回调函数
def on_message(ws, message):
    data = json.loads(message)
    if data.get("op") == "publish" and data.get("topic") == "/odom":
        msg = data.get("msg", {})
        pose = msg.get("pose", {}).get("pose", {})
        position = pose.get("position", {})
        x = position.get("x", 0)
        y = position.get("y", 0)
        z = position.get("z", 0)
        print(f"Robot Position - x: {x}, y: {y}, z: {z}")

# 错误回调函数
def on_error(ws, error):
    print(f"Error: {error}")

# 关闭连接回调函数
def on_close(ws):
    print("Connection closed")

# 发布控制命令的函数
def send_cmd_vel(ws, linear_x, angular_z):
    cmd_vel_msg = {
        "op": "publish",
        "topic": "/cmd_vel",
        "msg": {
            "linear": {
                "x": linear_x,  # 线速度
                "y": 0.0,
                "z": 0.0
            },
            "angular": {
                "x": 0.0,
                "y": 0.0,
                "z": angular_z  # 角速度
            }
        }
    }
    ws.send(json.dumps(cmd_vel_msg))
    # print(f"Sent: {cmd_vel_msg}")

# 键盘控制函数
def keyboard_control(ws):
    linear_x = 0.0
    angular_z = 0.0

    while True:
        if keyboard.is_pressed('w'):
            linear_x = 0.5
        elif keyboard.is_pressed('s'):
            linear_x = -0.5
        else:
            linear_x = 0.0

        if keyboard.is_pressed('a'):
            angular_z = 0.5
        elif keyboard.is_pressed('d'):
            angular_z = -0.5
        else:
            angular_z = 0.0

        if keyboard.is_pressed(' '):  # 空格键紧急停止
            linear_x = 0.0
            angular_z = 0.0

        send_cmd_vel(ws, linear_x, angular_z)

if __name__ == "__main__":
    # WebSocket服务器地址
    websocket_url = "ws://192.168.50.101:9090"

    # 创建WebSocket应用
    ws = websocket.WebSocketApp(websocket_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # 启动一个线程来处理WebSocket连接
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

    # 等待WebSocket连接建立
    while not ws.sock.connected:
        pass

    # 启动键盘控制
    keyboard_control(ws)
