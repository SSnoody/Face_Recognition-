import cv2
import face_recognition
import os
from datetime import datetime
from CorreoElectronico import CorreoElectronico
import numpy

class P1:
    def __init__(self):
        try:
            self.detectorRostro = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.rutaImages = "images"
            self.correoDestinatario = " " #U can delete the part of sending the email.
            self.encodingsRostros = []
            self.nombresRostros = []
            self.intentos = 0
            self.detallesIntentos = []
            print("Iniciando sistema...")
            self.cargarRostros()
            print("Rostros cargados")
        except:
            print(f"Error al inicializar el sistema")

    def cargarRostros(self):
        try:
            rostros = [
                {"nombre": "#Person name", "imagen": "images/name_2.jpeg"},
                {"nombre": "#Person name", "imagen": "images/name2_1.jpeg"},    #U can delete or add more recognition faces
                {"nombre": "#Person name", "imagen": "images/name3_1.jpeg"},
                {"nombre": "#Person name", "imagen": "images/name4_2.jpeg"}
            ]
            for rostro in rostros:
                if os.path.exists(rostro["imagen"]):
                    imagen = face_recognition.load_image_file(rostro["imagen"])
                    encoding = face_recognition.face_encodings(imagen)
                    if encoding:
                        self.encodingsRostros.append(encoding[0])
                        self.nombresRostros.append(rostro["nombre"])
                        print(f"Rostro de {rostro['nombre']} cargado")
                    else:
                        print(f"No se detectó ningún rostro en la imagen {rostro['nombre']}")
                else:
                    print(f"No se encontró el archivo {rostro['imagen']}")
        except:
            print(f"Error al cargar los rostros")

    def reconocerImagen(self, imagen):
        try:
            rgbFrame = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            ubicacionRostros = face_recognition.face_locations(rgbFrame)
            encodingsRostros = face_recognition.face_encodings(rgbFrame, ubicacionRostros)

            nombRostros = []
            for encodingRostro in encodingsRostros:
                if len(self.encodingsRostros) == 0:
                    print("No se han cargado encodings de caras conocidas.")
                    continue

                coincidencias = face_recognition.compare_faces(self.encodingsRostros, encodingRostro)
                nombre = "Desconocido"
                distanciaRostro = face_recognition.face_distance(self.encodingsRostros, encodingRostro)
                mejorCoincidencia = numpy.argmin(distanciaRostro)
                if coincidencias[mejorCoincidencia]:
                    nombre = self.nombresRostros[mejorCoincidencia]
                nombRostros.append(nombre)
                if nombre == "Desconocido":
                    self.intentos += 1
                    self.detallesIntentos.append(f"Intento fallido a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    if self.intentos >= 3:
                        self.enviarCorreo()
            return nombRostros
        except:
            print(f"Error al reconocer la imagen")
            return []

    def reconocerRostro(self):
        try:
            captura = cv2.VideoCapture(0)
            if not captura.isOpened():
                print("No se puede acceder a la cámara")
                return
            while True:
                ret, frame = captura.read()
                if not ret:
                    print("No se pudo capturar la imagen correctamente")
                    break

                nomRostros = self.reconocerImagen(frame)

                for (top, right, bottom, left), nombre in zip(face_recognition.face_locations(frame), nomRostros):
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                    cv2.putText(frame, nombre, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                cv2.imshow('Sistema de reconocimiento facial', frame)
                if cv2.waitKey(1) & 0xFF == ord('x'):
                    break
            captura.release()
            cv2.destroyAllWindows()
        except:
            print(f"Error al realizar el reconocimiento facial")

    def enviarCorreo(self):
        try:
            correo = CorreoElectronico()
            asunto = "Notificación de intentos fallidos de reconocimiento facial"
            mensaje = "Se han detectado 3 intentos fallidos de reconocimiento facial.\n\n"
            mensaje += "Detalles de los intentos fallidos:\n"
            for detalle in self.detallesIntentos:
                mensaje += f"{detalle}\n"
            correo.enviarCorreo(self.correoDestinatario, asunto, mensaje)
            self.intentosFallidos = 0
            self.detallesIntentos.clear()
        except:
            print(f"Error al enviar el correo electrónico")

objReconocer = P1()
objReconocer.reconocerRostro()
