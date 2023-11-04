from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at X: {x}, Y: {y}")


with Listener(on_click=on_click) as listener:
    listener.join()
