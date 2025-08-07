import tkinter as tk
from PIL import Image, ImageTk
import cv2


class Cv2WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Открываем камеру
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Камера не обнаружена")

        # Холст
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Кнопка выхода
        self.btn_exit = tk.Button(window, text="Выход", command=self.close)
        self.btn_exit.pack(pady=10)

        # Запускаем цикл обновления кадров
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            # BGR → RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            # Обновляем холст
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk  # защита от сборщика мусора

        # Повторяем через 50 мс ≈ 20 FPS
        self.window.after(50, self.update)

    def close(self):
        self.cap.release()
        self.window.destroy()


# Запускаем приложение
if __name__ == "__main__":
    root = tk.Tk()
    app = Cv2WebcamApp(root, "Камера через OpenCV")