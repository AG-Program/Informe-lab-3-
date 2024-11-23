import random

# Registrar usuario
def registerUser(name, password):
    try:
        # Lee los usuarios del archivo y verifica si el nombre de usuario ya está registrado
        with open("usuarios.txt", "r") as file:
            users = [line.strip().split(":") for line in file]

        for user in users:
            if user[0] == name:
                return "El usuario ya está registrado"

        # Si el usuario no está registrado, se agrega al archivo
        with open("usuarios.txt", "a") as file:
            file.write(f"{name}:{password}:0:False\n")
        return "Usuario registrado"

    except FileNotFoundError:
        # Si el archivo no existe, lo crea y registra al usuario
        with open("usuarios.txt", "w") as file:
            file.write(f"{name}:{password}:0:False\n")
        return "Usuario registrado"


# Abrir o cerrar sesión
def openCloseSession(name, password, flag):
    try:
        with open("usuarios.txt", "r") as file:
            users = [line.strip().split(":") for line in file]

        updated_users = []
        session_message = "Error"
        for user in users:
            if len(user) < 4:
                continue
            if user[0] == name and user[1] == password:
                user[3] = "True" if flag else "False"
                session_message = "Sesion iniciada" if flag else "Sesion cerrada"
            updated_users.append(":".join(user))

        with open("usuarios.txt", "w") as file:
            file.write("\n".join(updated_users) + "\n")
        
        return session_message
    except FileNotFoundError:
        return "Error: archivo no encontrado"


# Actualizar el puntaje del usuario
def updateScore(name, password, score):
    try:
        with open("usuarios.txt", "r") as file:
            users = [line.strip().split(":") for line in file]

        updated_users = []
        score_message = "Error"
        for user in users:
            if len(user) < 4:
                continue
            if user[0] == name and user[1] == password and user[3] == "True":
                user[2] = str(score)
                score_message = "Puntaje actualizado"
            updated_users.append(":".join(user))

        with open("usuarios.txt", "w") as file:
            file.write("\n".join(updated_users) + "\n")

        return score_message
    except FileNotFoundError:
        return "Error: archivo no encontrado"


# Leer el puntaje del usuario
def getScore(name, password):
    try:
        with open("usuarios.txt", "r") as file:
            users = [line.strip().split(":") for line in file]

        for user in users:
            if len(user) < 4:
                continue
            if user[0] == name and user[1] == password and user[3] == "True":
                return int(user[2])

        return "Error: no se encontró el usuario o la sesión no está activa"
    except FileNotFoundError:
        return "Error: archivo no encontrado"


def usersList(name, password):
    try:
        with open("usuarios.txt", "r") as file:
            users = [line.strip().split(":") for line in file]

        # Verifica que el usuario esté conectado
        for user in users:
            if len(user) < 5:  # Asegúrate de que cada línea tiene al menos 5 elementos
                continue
            if user[0] == name and user[1] == password and user[3] == "True":
                connected_users = {}
                # Recorre la lista de usuarios para obtener los conectados y su puntaje
                for u in users:
                    if len(u) >= 5 and u[3] == "True":  # Verifica que el usuario esté conectado
                        connected_users[u[0]] = u[4]  # Diccionario con nombre de usuario y puntaje
                return connected_users

        return "Error: no se encuentra el usuario o la sesión no está activa"
    except FileNotFoundError:
        return "Error: archivo no encontrado"

def question(password, cat):
    try:
        cat = int(cat)
    except ValueError:
        return "Error: categoría inválida"

    if cat == 1:
        selected_file = "preguntas_categoria_1.txt"
    elif cat == 2:
        selected_file = "preguntas_categoria_2.txt"
    else:
        return "Error: categoría no válida"

    try:
        with open(selected_file, "r", encoding="utf-8") as file:
            question_list = []
            question_buffer = []
            for line in file:
                line = line.strip()
                if line:
                    question_buffer.append(line)
                else:
                    # Al encontrar una línea vacía, procesamos la pregunta
                    if question_buffer:
                        # La primera línea es la pregunta
                        question_text = question_buffer[0].split(". ", 1)[1].strip()  # Eliminamos el número de la pregunta
                        
                        # Las siguientes 4 líneas son las opciones
                        options = [question_buffer[i].strip() for i in range(1, 5)]
                        
                        # La última línea contiene la respuesta correcta
                        correct_answer = question_buffer[5].split(":")[1].strip()
                        
                        # Almacenamos la pregunta, las opciones y la respuesta correcta
                        question_list.append((question_text, options, correct_answer))
                    
                    # Limpiamos el buffer para la siguiente pregunta
                    question_buffer = []

        if not question_list:
            return "Error: no hay preguntas disponibles"

    except FileNotFoundError:
        return "Error: archivo no encontrado"

    # Selecciona una pregunta aleatoria
    return random.choice(question_list)
