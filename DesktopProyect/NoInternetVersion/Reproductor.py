import tkinter as tk
from tkinter import ttk, filedialog
import time
from PIL import Image, ImageTk
import requests
from io import BytesIO
import ctypes
import subprocess
import sys
import pygame
import os
from moviepy.editor import AudioFileClip
import tempfile
import threading

# Función para instalar una biblioteca
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Intentar importar la biblioteca keyboard, instalar si no está instalada
try:
    import keyboard  # Nueva biblioteca para capturar eventos de teclado a nivel global
except ImportError:
    install("keyboard")
    import keyboard

# Inicializar pygame
pygame.mixer.init()

class ClockWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Reloj y Reproductor de Música")
        self.geometry("300x600")  # Ajusta el tamaño de la ventana según la imagen y reproductor
        self.resizable(False, False)
        self.overrideredirect(True)
        self.attributes('-transparentcolor', 'purple')
        self.attributes('-topmost', True)  # Asegura que la ventana esté siempre al frente
        self.configure(bg='purple')

        # Cargar la imagen desde la URL
        url = "https://static.wikia.nocookie.net/mamarre-estudios-espanol/images/9/95/PACO.png/revision/latest?cb=20200331204013&path-prefix=es"
        response = requests.get(url)
        image_data = response.content
        self.image = Image.open(BytesIO(image_data))
        self.photo = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self, image=self.photo, bg='purple')
        self.image_label.pack()

        # Crear el reloj
        self.label = ttk.Label(self, font=('calibri', 40, 'bold'), background='purple', foreground='white')
        self.label.pack(anchor='center')

        self.update_clock()
        self.set_as_desktop_widget()

        # Vincular eventos de ratón (ya no oculta al hacer clic)
        self.hidden = False

        # Configurar evento de teclado global
        keyboard.add_hotkey('ctrl+1', self.toggle_visibility)

        # Crear lista de reproducción
        self.playlist = []
        self.current_song_index = 0

        # Botones de control de música
        self.add_music_button = ttk.Button(self, text="Agregar Música/Video", command=self.add_media)
        self.add_music_button.pack()

        self.play_button = ttk.Button(self, text="Reproducir", command=self.play_media)
        self.play_button.pack()

        self.pause_button = ttk.Button(self, text="Pausar/Despausar", command=self.toggle_pause)
        self.pause_button.pack()

        self.next_button = ttk.Button(self, text="Siguiente", command=self.next_media)
        self.next_button.pack()

        self.previous_button = ttk.Button(self, text="Anterior", command=self.previous_media)
        self.previous_button.pack()

        self.is_paused = False

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.label.config(text=current_time)
        self.after(1000, self.update_clock)  # Actualiza cada segundo

    def set_as_desktop_widget(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        # Configura la ventana como siempre encima usando WS_EX_TOPMOST
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, 0x00000008 | 0x00000080)  # WS_EX_TOPMOST
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # HWND_TOPMOST

    def toggle_visibility(self):
        if self.hidden:
            self.deiconify()  # Muestra la ventana
            self.attributes('-topmost', True)  # Pone la ventana al frente
        else:
            self.withdraw()  # Oculta la ventana
        self.hidden = not self.hidden

    def add_media(self):
        files = filedialog.askopenfilenames(filetypes=[("Media Files", "*.mp3 *.mp4")])
        self.playlist.extend(files)

    def load_and_play(self, media_file):
        if media_file.endswith('.mp3'):
            pygame.mixer.music.load(media_file)
            pygame.mixer.music.play()
        elif media_file.endswith('.mp4'):
            temp_audio_path = tempfile.mktemp(suffix=".mp3")
            audio = AudioFileClip(media_file)
            audio.write_audiofile(temp_audio_path)
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()

    def play_media(self):
        if self.playlist:
            media_file = self.playlist[self.current_song_index]
            threading.Thread(target=self.load_and_play, args=(media_file,)).start()

    def toggle_pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.pause_button.config(text="Pausar")
        else:
            pygame.mixer.music.pause()
            self.pause_button.config(text="Despausar")
        self.is_paused = not self.is_paused

    def next_media(self):
        self.current_song_index += 1
        if self.current_song_index >= len(self.playlist):
            self.current_song_index = 0
        self.play_media()

    def previous_media(self):
        self.current_song_index -= 1
        if self.current_song_index < 0:
            self.current_song_index = len(self.playlist) - 1
        self.play_media()

if __name__ == "__main__":
    app = ClockWidget()
    app.mainloop()
