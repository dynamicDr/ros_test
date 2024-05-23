import websocket
import json


def on_message(ws, message):
    # print("Received: " + message)
    data = json.loads(message)
    if data.get("op") == "publish" and data.get("topic") == "/odom":
        msg = data.get("msg", {})
        pose = msg.get("pose", {}).get("pose", {})
        position = pose.get("position", {})
        x = position.get("x", 0)
        y = position.get("y", 0)
        z = position.get("z", 0)
        print()
        print(f"Robot Position - x: {x}, y: {y}, z: {z}")
        print()

def on_error(ws, error):
    print("error")
    # print("Error: " + str(error))

def on_close(ws):
    print("### Closed ###")

def on_open(ws):
    topic = "/odom"
    subscribe_msg = json.dumps({
        "op": "subscribe",
        "topic": topic
    })
    ws.send(subscribe_msg)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.50.101:9090",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()