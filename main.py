import threading
import queue
import pyautogui
import pytesseract
from googletrans import Translator
import tkinter as tk

class GUI:
    def __init__(self):
        # Cria a janela da interface gráfica
        self.window = tk.Tk()
        self.window.title("Captura e Tradução")
        self.window.geometry("500x300")

        # Cria um frame para os botões
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Cria um botão na janela para capturar e traduzir
        self.capture_button = tk.Button(self.button_frame, text="Capturar e Traduzir", command=self.start_capture_and_translate)
        self.capture_button.pack(side="left", padx=5)

        # Cria um botão na janela para apagar o texto
        self.clear_button = tk.Button(self.button_frame, text="Apagar texto", command=self.clear_text)
        self.clear_button.pack(side="left", padx=5)

        # Cria um widget Text com barra de rolagem na janela
        self.text = tk.Text(self.window, wrap='word')
        self.scrollbar = tk.Scrollbar(self.window, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.text.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Cria uma fila para comunicar entre threads
        self.queue = queue.Queue()

    def start_capture_and_translate(self):
        # Inicia um thread para capturar a tela e processar o OCR
        threading.Thread(target=self.capture_and_translate).start()

    def capture_and_translate(self):
        # Esconde a janela
        self.window.iconify()

        # Captura a tela inteira do computador
        screenshot = pyautogui.screenshot()

        # Reconhece letras na captura de tela usando Tesseract OCR
        text = pytesseract.image_to_string(screenshot)

        # Traduz o texto reconhecido usando o Googletrans
        translator = Translator()
        translated_text = translator.translate(text, dest='pt').text

        # Insere o texto traduzido na fila para atualização da interface gráfica
        self.queue.put(translated_text)

        # Mostra a janela novamente
        self.window.deiconify()

    def update_text(self):
        # Se houver textos traduzidos na fila, atualiza o widget Text com o último
        # texto traduzido
        while not self.queue.empty():
            translated_text = self.queue.get()
            self.text.delete('1.0', 'end')
            self.text.insert('end', translated_text)

        # Agenda a atualização do widget Text novamente em 100ms
        self.window.after(100, self.update_text)

    def clear_text(self):
        # Apaga todo o texto no widget Text
        self.text.delete('1.0', 'end')

    def run(self):
        # Inicia a atualização do widget Text
        self.update_text()

        # Inicia o loop da interface gráfica
        self.window.mainloop()

# Cria uma instância da GUI e executa o loop da interface gráfica
gui = GUI()
gui.run()
