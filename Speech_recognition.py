# -*- coding: utf-8 -*-
"""PBL3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LSyfsLK-yShiUlAZMrU10ifekLxQwQ6N

Autores:
* Santiago Castro Benavides 			A01799544
* Rodrigo Lira Del Ángel 			A01799277
* Diego Jesús de Lara de la Cruz		A01748449
* Andrés Felipe García Viña                              A01800027

En el presente notebook se muestra el funcionamiento de un modelo de reconocimiento del habla utilizando la librería `speech_recognition` en Python. El objetivo principal es demostrar cómo se puede transcribir el contenido de archivos de audio a texto de manera automática. Para ello, se utiliza la API de Google Speech Recognition, que procesa los archivos de audio y genera transcripciones precisas, acompañadas de un valor de confianza que indica la fiabilidad del resultado. Además, se explora cómo el modelo responde cuando se introduce ruido en los audios, comparando la transcripción de los audios originales con la de los audios alterados. Esta comparación permite analizar cómo el ruido afecta la calidad de la transcripción y la confianza del reconocimiento, proporcionando una visión práctica de los desafíos que pueden enfrentar los sistemas de reconocimiento de voz en condiciones adversas.

# Librerias

1. **`os`**:
   - **Descripción**: La librería `os` en Python proporciona una forma de interactuar con el sistema operativo. Permite realizar operaciones como acceder al sistema de archivos, manipular rutas de directorios, y gestionar procesos del sistema.
   - **Propósito**: En este proyecto, `os` se utiliza para manejar rutas de archivos y directorios, facilitando la carga y almacenamiento de archivos de audio de manera eficiente.

2. **`numpy`**:
   - **Descripción**: `numpy` es una librería fundamental para la computación científica en Python. Ofrece soporte para arrays multidimensionales (matrices) y funciones matemáticas de alto nivel para operar sobre esos arrays.
   - **Propósito**: Se utiliza en este proyecto para manipular los datos de audio como arrays de números. Esto nos permite realizar operaciones matemáticas, como agregar ruido al audio, de una manera eficiente y sencilla.

3. **`pydub`**:
   - **Descripción**: `pydub` es una librería que facilita la manipulación de archivos de audio en Python. Permite cargar, modificar, y exportar archivos de audio en varios formatos como WAV, MP3, etc.
   - **Propósito**: En este proyecto, `pydub` se usa para cargar archivos de audio, agregarles ruido, y luego exportar el resultado. Además, facilita la conversión entre diferentes formatos de audio y la manipulación de las propiedades del audio como el volumen y la tasa de bits.

4. **`speech_recognition`**:
   - **Descripción**: `speech_recognition` es una librería que permite a Python acceder a diferentes servicios de reconocimiento de voz, como Google Web Speech API, IBM Watson, etc., para convertir audio en texto.
   - **Propósito**: En este proyecto, `speech_recognition` se utiliza para transcribir el contenido de los archivos de audio, tanto originales como aquellos con ruido añadido. Esto nos permite analizar cómo el ruido afecta la precisión de la transcripción y la confianza en los resultados generados por el servicio de reconocimiento de voz.
"""

# !pip install pydub

import os
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr

listaAudios = os.listdir()
listaAudios

"""# Transcripcion

Este bloque de código realiza la transcripción de archivos de audio utilizando el servicio de Google Speech Recognition a través de la librería `speech_recognition`. A continuación, se describe el flujo y propósito de cada parte:

Primero se crea una instancia de la clase `Recognizer` de la libreria `speech_recognition`. esta intancia se utiliza para reconocer y transcribir audio a texto
"""

r = sr.Recognizer()

"""se define una funcion llamada `transcribe_audio` que toma como argumento el nombre o la ruta de un archivo de audio. Esta función es la responsable de convertir el audio en texto y devolver tanto la transcripción como la confianza asociada"""

def transcribe_audio(audio):
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)
        result = r.recognize_google(audio_data, language='es-MX',show_all=True)
        transcripcion = result['alternative'][0]['transcript']
        confianza = result['alternative'][0]['confidence']

        return transcripcion, confianza

"""mostramos los resultado de la transcripcion de todos los audios y su respectivo nivel de confianza. para evitar problemas de ejecucion se limita a que solo sean leidos los archivos en formato `.wav` ya que es el requerido por el gestor `r`"""

for i in range(len(listaAudios)):
    if listaAudios[i].endswith('.wav'):
        transcripcion, confianza = transcribe_audio(listaAudios[i])
        print(f'Archivo: {listaAudios[i]}')
        print(f'Transcripción: {transcripcion}')
        print(f'Confianza: {confianza}\n')

"""# Transcripcion con ruido

Esta función, `add_noise`, añade ruido blanco a un segmento de audio. Convierte el audio en un array numérico, genera ruido blanco basado en una distribución normal ajustada por `noise_level`, y lo suma al audio original. Luego, crea un nuevo segmento de audio con el ruido añadido y lo devuelve.
"""

def add_noise(audio_segment,noise_level):
    audio_data = np.array(audio_segment.get_array_of_samples())
    noise = np.random.normal(0, noise_level*np.max(audio_data), audio_data.shape)
    audio_noise = audio_data + noise
    end_audio = audio_segment._spawn(audio_noise.astype(np.int16).tobytes())
    return end_audio

"""Este bloque de código carga un archivo de audio, le añade ruido y compara las transcripciones del audio original y el ruidoso. Primero, se carga el audio original con `AudioSegment.from_file`, se le añade ruido blanco con `add_noise(audio, valor ruido)`, y se guarda como un nuevo archivo. Luego, ambos audios (original y ruidoso) se cargan y se convierten en un formato que puede ser reconocido por el modelo. Finalmente, se transcriben ambos audios utilizando la API de Google Speech Recognition y se imprimen las transcripciones para comparar los resultados."""

audio = AudioSegment.from_file('New-Recording-3.wav')
audio_noise = add_noise(audio,0.4)
audio_noise.export('New-Recording-3-noisy.wav',format='wav')
with sr.AudioFile("New-Recording-3.wav") as source:
    original_audio = r.record(source)

with sr.AudioFile("New-Recording-3-noisy.wav") as source:
    noisy_audio = r.record(source)

print("Original audio:")
print(r.recognize_google(original_audio, language='es-MX'))
print("Noisy audio:")
print(r.recognize_google(noisy_audio, language='es-MX'))

audio = AudioSegment.from_file('New-Recording-5.wav')
audio_noise = add_noise(audio,0.55)
audio_noise.export('New-Recording-5-noisy.wav',format='wav')
with sr.AudioFile("New-Recording-5.wav") as source:
    original_audio = r.record(source)

with sr.AudioFile("New-Recording-5-noisy.wav") as source:
    noisy_audio = r.record(source)

print("Original audio:")
print(r.recognize_google(original_audio, language='es-MX'))
print("Noisy audio:")
print(r.recognize_google(noisy_audio, language='es-MX'))

audio = AudioSegment.from_file('parrafo.wav')
audio_noise = add_noise(audio,0.6)
audio_noise.export('parrafo-noisy.wav',format='wav')
with sr.AudioFile("parrafo.wav") as source:
    original_audio = r.record(source)

with sr.AudioFile("parrafo-noisy.wav") as source:
    noisy_audio = r.record(source)

print("Original audio:")
print(r.recognize_google(original_audio, language='es-MX'))
print("Noisy audio:")
print(r.recognize_google(noisy_audio, language='es-MX'))

transcrip, confianza = transcribe_audio('parrafo-noisy.wav')
print(confianza)

"""El modelo de reconocimiento de voz logró mantener un nivel de confianza relativamente alto (0.9479) a pesar de la adición de un ruido considerable. Esto destaca la capacidad del sistema de Google para manejar y reducir el impacto del ruido en la transcripción. Aunque el ruido añadido con un nivel de 0.6 hizo que el audio fuera casi imperceptible, el modelo aún pudo generar una transcripción con un alto grado de precisión. Sin embargo, se observó que algunas palabras y frases fueron distorsionadas, lo que subraya la importancia de utilizar audios de alta calidad en aplicaciones donde la precisión es esencial. Esto demuestra la robustez del módulo de reducción de ruido de Google, pero también advierte sobre la necesidad de audios claros para obtener transcripciones más fieles.

# Conclusion

El proyecto demostró cómo funciona el reconocimiento de voz utilizando la API de Google en Python, mostrando su precisión y capacidad para manejar ruido. A pesar de añadir un nivel significativo de ruido, el sistema mantuvo una alta confianza en las transcripciones, evidenciando la eficacia de la reducción de ruido de Google. Sin embargo, se observaron algunas distorsiones, lo que subraya la importancia de trabajar con audios de buena calidad para obtener transcripciones más precisas.
"""