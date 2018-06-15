import asyncio
import random
import numpy as np
import pickle
import bz2
import cv2

cap = cv2.VideoCapture(0)
last_message = None
# This function has driving code
async def drive(loop):
    global last_message
    while True:
        await asyncio.sleep(1.0, loop)
        # last_message should contain result of processed camera frames. do something with it
        print("last_message", last_message)

# This function sends camera frames to server
async def send_frames(message, loop):
    global last_message
    global writer
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)
    while True:
        try:
            await asyncio.sleep(3.0, loop)
            ret, frame = cap.read()
            gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (64, 64))
            message = bz2.compress(pickle.dumps(np.resize(gray, (64, 64, 1))))
            print("Sending", len(message), "bytes")
            writer.write(message)
            data = await reader.read(100)
            last_message = data.decode()
        except Exception as e:
            print(e)


loop = asyncio.get_event_loop()
message = 'Hello World {}'.format(random.randint(1, 10))
# Create coroutines for each simultaneous task
sender_coro = send_frames(message, loop)
drive_coro = drive(loop)
# Create a simultaneous task
task = loop.create_task(asyncio.gather(sender_coro, drive_coro))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

writer.close()
loop.close()
cap.release()
