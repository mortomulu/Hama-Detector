import cv2
import torch
import numpy as np
import pygame
import telepot
import io
import threading
import serial
import mysql.connector
from datetime import datetime
from telepot.exception import TooManyRequestsError
import time
from mysql.connector import pooling

# Initialize MySQL connection pool
db_connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    user="root",
    password="",
    database="pysql"
)

# Function to get a connection from the pool
def get_db_connection():
    return db_connection_pool.get_connection()

# Arduino port
arduino_port = serial.Serial('COM6', 9600)

# Telegram bot token
telegram_bot_token = '6786434209:AAH8evnaYbeRsi9wRNmonygEn68JknT7F4s'

# Telegram chat ID
telegram_chat_id = 1079574772  # to check id = https://api.telegram.org/bot<TOKEN>/getUpdates

# Create a Telegram bot
bot = telepot.Bot(telegram_bot_token)

# Path to the alarm sound
path_alarm = "Alarm/alarm.wav"

# Initializing pygame
pygame.init()
pygame.mixer.music.load(path_alarm)

# Loading the model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Using video file
cap = cv2.VideoCapture("Test Videos/bird.mp4")

target_classes = ['bird']
count = 0
bird_detected = False  # Flag to track if a bird is detected
telegram_message_sent = False  # Flag to track if Telegram message has been sent

number_of_photos = 3

def preprocess(img):
    height, width = img.shape[:2]
    ratio = height / width
    img = cv2.resize(img, (640, int(640 * ratio)))
    return img

# Function to send message and photo to Telegram
def send_telegram_message():
    global count
    global frame_detected
    global telegram_message_sent

    if not telegram_message_sent:
        try:
            # Send a message to Telegram.
            bot.sendMessage(telegram_chat_id, "Bird detected!")
            telegram_message_sent = True  # Set the flag to indicate the message has been sent

            # Simpan data ke MySQL ketika burung terdeteksi
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Modify this query to insert real-time data
            insert_query = "INSERT INTO `detect` (`date_added`, `time_added`, `timestamp_added`, `data_column`) VALUES (%s, %s, %s, %s)"
            with get_db_connection() as db_conn:
                with db_conn.cursor() as db_cursor:
                    db_cursor.execute(insert_query, (current_date, current_time, current_timestamp, 'burung terdeteksi'))
                db_conn.commit()

        except TooManyRequestsError:
            print("Too Many Requests. Waiting for a while.")
            time.sleep(5)  # You can adjust the waiting time here
            send_telegram_message()  # Retry the function

while True:
    ret, frame = cap.read()
    frame_detected = frame.copy()
    frame = preprocess(frame)
    results = model(frame)

    bird_detected = False  # Reset the flag for each frame

    for index, row in results.pandas().xyxy[0].iterrows():
        center_x = None
        center_y = None

        if row['name'] in target_classes:
            name = str(row['name'])
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)
            # write name
            cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            # draw center
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            if name == 'bird':
                bird_detected = True  # if a bird is detected

    # Play or stop the alarm based on the bird detection
    if bird_detected:
        if not pygame.mixer.music.get_busy():  # Check if the mixer is not already playing
            pygame.mixer.music.play()
        # Send a signal to Arduino
        signal_to_arduino = "BIRD_DETECTED\n"  
        arduino_port.write(signal_to_arduino.encode())
        # Send a message to Telegram
        alarm_thread = threading.Thread(target=send_telegram_message)
        alarm_thread.start()
        count += 1

        # Add warning text on the screen
        warning_text = "Bird Detected!"
        cv2.putText(frame, warning_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        pygame.mixer.music.stop()
        telegram_message_sent = False  # Reset the flag if no bird is detected

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Menutup koneksi ke MySQL saat program berakhir
db_connection_pool.close()
cv2.destroyAllWindows()
