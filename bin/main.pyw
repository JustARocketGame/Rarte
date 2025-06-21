import requests
from tkinter import *
import time
import threading
import os
import subprocess

def read_file_content(file_path):
  try:
    with open(file_path, 'r') as file:
      content = file.read()
      return content
  except FileNotFoundError:
    print(f"Ошибка: Файл не найден по пути {file_path}")
    return None
  except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    return None


# Пример использования:
version_path = os.path.join(os.getcwd(), "version.txt") # Замените на реальный путь к файлу
version = read_file_content(version_path)

version_url = "https://raw.githubusercontent.com/JustARocketGame/RarteData/main/version.txt"
program_url = "https://raw.githubusercontent.com/JustARocketGame/RarteData/main/program.pyw"

response = requests.get(version_url, timeout=5)
response.raise_for_status()
latest_version = response.text.strip()
has_update = latest_version > version

class CheckForUpdates():
    def __init__(self, root):

        self.root = root
        self.root.title("Обновление")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        # Задаём размеры окна
        self.window_width = 400
        self.window_height = 200

        # Получаем размеры экрана
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Вычисляем координаты для центрирования
        self.x = int((self.screen_width - self.window_width) / 2)
        self.y = int((self.screen_height - self.window_height) / 2)

        # Устанавливаем геометрию окна
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")

        self.label = Label(root, text="Подождите...", font='"Comic Sans MS" 35 bold')
        self.label.place(x=30, y=60)

        threading.Thread(target=self.step_1, daemon=True).start()

    def step_1(self):

        time.sleep(1)
        if has_update:

            print("Updating...")

            with open(version_path, "w") as file:
                file.write(latest_version)
            response = requests.get(program_url, timeout=10)
            response.raise_for_status()
            with open("program.pyw", "wb") as f:
                f.write(response.content)
            
            time.sleep(1)
            RunMainProgram()
            self.root.destroy()

        else:
            print("No update!")
            RunMainProgram()
            self.root.destroy()


class RunMainProgram:
    def __init__(self):
       print("Running...")
       subprocess.Popen(["pythonw", "program.pyw"])

if __name__ == "__main__":
    root = Tk()
    CheckForUpdates(root)
    root.mainloop()