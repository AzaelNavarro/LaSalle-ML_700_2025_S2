import cv2
from picamera2 import picamera2 
import base64
import numpy as np
import requests
import time
from gpiozero import LED, Motor

URL_POST = "https://ef532a86-c48e-4cf5-8792-441a5faeafbd-00-15rwru2eu6u7x.spock.replit.dev/insert/ANJ_ROBOT_TELEMETRIA%22"

IMAGE_WIDTH =640
IMAGE_HEIGHT = 480
IMAGE_FORMAT = "RGB888"


LED_R1 = LED(22)
LED_G1 =LED (23)
LED_B1 =LED (24)
LED_R2 =LED (10)
LED_G2 =LED (9)
LED_B2 =LED (25)

CELEBRATION_MOTOR = Motor(forward=18, backward=27)

def motor_stop():
    CELEBRATION_MOTOR.stop()

def celebrate_success():

    print("exito... Bailando y encendiendo luces !")

    for _ in range(3):

        LED_R1.off(); LED_G1.on(); LED_B1.off()
        LED_R2.off(); LED_G2.on(); LED_B2.off()
        time.sleep(0.15)


        LED_R1.off(); LED_G1.off(); LED_B1.on()
        LED_R2.on(); LED_G2.off(); LED_B2.off()
        time.sleep(0.15)

    LED_R1.off(); LED_G1.off(); LED_B1.off()
    LED_R2.off(); LED_G2.off(); LED_B2.off()

    try:
        speed = 0.9
        CELEBRATION_MOTOR.forward(speed)
        time.sleep(0.9)

        CELEBRATION_MOTOR.backward(speed)
        time.sleep(0.9)

        moto_stop()
    except Exception:
        motor_stop()

def capture_photo_to_base64():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size":(IMAGE_WIDTH, IMAGE_HEIGHT), "format": IMAGE_FORMAT}

    )
    picam2.configure(config)

    try:
        print("Cámara: Capturando imagen...")
        picam2.start()
        time.sleep(0.2)
        frame_array = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame_array)
        if not ret:
            print("Camara:error al codificar la imagen")
            return none

        base64_string=base64.b64encode(buffer).decode('utf-8')
        return base64_string
    except Exception as e:
        print(f"Cámara:Falló la inicialización o captura: {e}")
        return None
    finally:
        try:
            picam2.stop()
        except Exception:
            pass
def send_telemetry(base64_image_data):
        selected_id = 1021

        payload ={
            "ID_LECTURA": selected_id,
            "ROVER_NAME": "Voyager",
            "TEMPERATURA_RUEDA": 30.0,
            "INTENSIDAD_TERRENO":0.5,
            "CARGA_BATERIA":90,
            "IMAGEN_BASE64":base64_image_data
        }
    print("\n POST: intentando enviar datos...")

    try:
        response = requests.post(URL_POST, json=payload, timeout=10)

        print(f"Codigo HTTP recibido:{response.status_code}")
        print(f"Cuerpo de respuesta:{response.text[:100]}...")

        if response.status_code == 200 or response.status_code == 201:
            celebrate_success()
        else:
            print(f"POST: Error en la respuesta del servidor.")

    except resquests.exceptions.RequestException as e:
        print(f"POST: Error de conexión. El servidor no fue alcanzado")


if __name__ == "__main__":
    print("---Iniciando Robot Telemetría---")
    motor_stop()
    foto_base64 = capture_photo_to_base64()

    if foto_base64:
        send_telemetry(foto_base64)
    else:
        print("Proceso detenido: La captura de la imagen falló")

    motor_stop()
    print("---Fin del Programa---")







