import keyboard

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

    print(linear_x)
    print(angular_z)