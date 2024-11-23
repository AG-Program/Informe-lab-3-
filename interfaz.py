import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import trivia_client

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer


class TriviaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia")
        self.root.geometry("800x800")
        self.server_url = "http://localhost:80"  
        self.current_user = {"name": "", "password": "", "score": 0}
        self.questions = []  # Lista de preguntas
        self.question_number = 0
        self.correct_answers = 0  # Contador de respuestas correctas
        self.incorrect_answers = 0  # Contador de respuestas incorrectas

        # Configurar la interfaz
        self.setup_background()
        self.fill_progress_bar()

    def setup_background(self):
        img = Image.open(r"c:\Users\PERSONAL\Downloads\preguntas.jpg.jpg")
        img = self.resize_image(img, 800, 800)
        self.bg_image = ImageTk.PhotoImage(img)
        self.label_bg = tk.Label(self.root, image=self.bg_image)
        self.label_bg.place(relwidth=1, relheight=1)

    def resize_image(self, image, width, height):
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def fill_progress_bar(self):
        self.clear_window()
        tk.Label(self.root, text="Cargando...", font=("Arial", 12), bg="lightblue").pack(pady=20)

        progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        progress_bar.pack(pady=20)

        for i in range(101):
            progress_bar["value"] = i
            self.root.update()
            time.sleep(0.03)

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.label_bg:
                widget.destroy()

    def update_info(self, message):
        self.clear_window()
        tk.Label(self.root, text=message, font=("Arial", 14), bg="lightblue").pack(pady=20)

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Menú Principal", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)
        tk.Button(self.root, text="Iniciar Sesión", font=("Arial", 14), command=self.show_login_form).pack(pady=10)
        tk.Button(self.root, text="Registrar", font=("Arial", 14), command=self.show_register_form).pack(pady=10)

    def show_login_form(self):
        def login_action():
            name = entry_name.get()
            password = entry_password.get()
            response = trivia_client.openSession(self.server_url, name, password)

            if response.lower().strip() == "sesion iniciada":
                self.current_user["name"], self.current_user["password"] = name, password
                self.update_info("Sesión iniciada exitosamente.")
                self.show_user_menu()
            else:
                self.update_info("Error al iniciar sesión. Verifique su nombre o contraseña.")

        self.clear_window()
        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.root, text="Nombre:", font=("Arial", 12), bg="lightblue").pack(pady=5)
        entry_name = tk.Entry(self.root, font=("Arial", 12))
        entry_name.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 12), bg="lightblue").pack(pady=5)
        entry_password = tk.Entry(self.root, font=("Arial", 12), show="*")
        entry_password.pack(pady=5)

        tk.Button(self.root, text="Iniciar Sesión", font=("Arial", 12), command=login_action).pack(pady=10)
        tk.Button(self.root, text="Volver", font=("Arial", 12), command=self.show_main_menu).pack(pady=10)

    def show_register_form(self):
        def register_action():
            name = entry_name.get()
            password = entry_password.get()
            response = trivia_client.registerUser(self.server_url, name, password)
            self.update_info(f"Registro: {response}")
            self.show_main_menu()

        self.clear_window()
        tk.Label(self.root, text="Registrar Usuario", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.root, text="Nombre:", font=("Arial", 12), bg="lightblue").pack(pady=5)
        entry_name = tk.Entry(self.root, font=("Arial", 12))
        entry_name.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 12), bg="lightblue").pack(pady=5)
        entry_password = tk.Entry(self.root, font=("Arial", 12), show="*")
        entry_password.pack(pady=5)

        tk.Button(self.root, text="Registrar", font=("Arial", 12), command=register_action).pack(pady=10)
        tk.Button(self.root, text="Volver", font=("Arial", 12), command=self.show_main_menu).pack(pady=10)

    def show_user_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"Bienvenido, {self.current_user['name']}!", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)
        tk.Button(self.root, text="Ver Puntaje", font=("Arial", 14), command=self.view_score).pack(pady=10)
        tk.Button(self.root, text="Obtener Preguntas", font=("Arial", 14), command=self.choose_category).pack(pady=10)
        tk.Button(self.root, text="Ver Usuarios Conectados", font=("Arial", 14), command=self.get_connected_users).pack(pady=10)
        tk.Button(self.root, text="Cerrar Sesión", font=("Arial", 14), command=self.logout).pack(pady=10)

    def view_score(self):
        def update_score():
            new_score = entry_score.get()
            if new_score.isdigit():
                trivia_client.updateScore(self.server_url, self.current_user["name"], self.current_user["password"], int(new_score))
                score_label.config(text=f"Puntaje actualizado a: {new_score}")
            else:
                error_label.config(text="Por favor, ingrese un puntaje válido.")

        self.clear_window()
        tk.Label(self.root, text="Puntaje", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)

        current_score = trivia_client.getScore(self.server_url, self.current_user["name"], self.current_user["password"])
        score_label = tk.Label(self.root, text=f"Puntaje actual: {current_score}", font=("Arial", 14), bg="lightblue")
        score_label.pack(pady=20)

        tk.Label(self.root, text="Nuevo puntaje:", font=("Arial", 12), bg="lightblue").pack(pady=5)
        entry_score = tk.Entry(self.root, font=("Arial", 12))
        entry_score.pack(pady=5)

        tk.Button(self.root, text="Actualizar Puntaje", font=("Arial", 12), command=update_score).pack(pady=10)

        error_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red", bg="lightblue")
        error_label.pack(pady=5)

        tk.Button(self.root, text="Volver al Menú", font=("Arial", 12), command=self.show_user_menu).pack(pady=10)

    def choose_category(self):
        self.clear_window()
        tk.Label(self.root, text="Elige una categoría:", font=("Arial", 16, "bold"), bg="lightblue").pack(pady=20)
        tk.Button(self.root, text="Categoría 1", font=("Arial", 14), command=lambda: self.start_quiz(1)).pack(pady=10)
        tk.Button(self.root, text="Categoría 2", font=("Arial", 14), command=lambda: self.start_quiz(2)).pack(pady=10)

    def start_quiz(self, category):
        self.questions = self.load_questions(category)
        self.question_number = 0
        self.correct_answers = 0
        self.incorrect_answers = 0

        if not self.questions:
            self.update_info("No se encontraron preguntas en la categoría seleccionada.")
        else:
            self.ask_question()

    def load_questions(self, cat):
        file_map = {1: "preguntas_categoria_1.txt", 2: "preguntas_categoria_2.txt"}
        selected_file = file_map.get(cat)

        if not selected_file:
            return []

        questions = []
        try:
            with open(selected_file, "r", encoding="utf-8") as file:
                question_buffer = []
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    question_buffer.append(line)
                    if len(question_buffer) == 6:  # Una pregunta completa
                        text, *options, correct = question_buffer
                        questions.append(Question(text, options, correct))
                        question_buffer.clear()
        except FileNotFoundError:
            return []
        return questions

    def ask_question(self):
        if self.question_number >= len(self.questions):
            self.finish_quiz()
            return

        current_question = self.questions[self.question_number]
        self.clear_window()

        tk.Label(self.root, text=f"Pregunta {self.question_number + 1}", font=("Arial", 16, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.root, text=current_question.text, font=("Arial", 14), wraplength=600, bg="lightblue").pack(pady=10)

        def answer_action(selected_option):
            if selected_option == current_question.correct_answer:
                self.correct_answers += 1
            else:
                self.incorrect_answers += 1

            self.question_number += 1
            self.ask_question()

        for option in current_question.options:
            tk.Button(self.root, text=option, font=("Arial", 12), wraplength=300,
                      command=lambda opt=option: answer_action(opt)).pack(pady=5)

    def finish_quiz(self):
        self.clear_window()
        tk.Label(self.root, text="juego terminado", font=("Arial", 16, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.root, text=f"Respuestas Correctas: {self.correct_answers}", font=("Arial", 14), bg="lightblue").pack(pady=10)
        tk.Label(self.root, text=f"Respuestas Incorrectas: {self.incorrect_answers}", font=("Arial", 14), bg="lightblue").pack(pady=10)
        tk.Button(self.root, text="Volver al Menú", font=("Arial", 14), command=self.show_user_menu).pack(pady=10)

    def get_connected_users(self):
        self.clear_window()
        tk.Label(self.root, text="Usuarios Conectados", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)
        users = trivia_client.getConnectedUsers(self.server_url)
        for user in users:
            tk.Label(self.root, text=user, font=("Arial", 14), bg="lightblue").pack(pady=5)
        tk.Button(self.root, text="Volver al Menú", font=("Arial", 14), command=self.show_user_menu).pack(pady=10)

    def logout(self):
        response = trivia_client.closeSession(self.server_url, self.current_user["name"], self.current_user["password"])
        self.update_info(response)
        self.show_main_menu()


if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaApp(root)
    root.mainloop()
