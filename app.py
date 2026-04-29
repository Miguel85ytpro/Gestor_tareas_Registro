from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'steam_secret_key'

MONGO_URI = "mongodb+srv://Miguel85ytpro5_db_user:Carcam010@cluster0.iifnlr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['Gestor_De_Tareas']
usuarios_col = db['usuarios']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario_input = request.form.get('usuario')
        password_input = request.form.get('password')

        usuario_encontrado = usuarios_col.find_one({
            "usuario": usuario_input, 
            "password": password_input
        })

        if usuario_encontrado:
            session['user'] = usuario_input
            return redirect(url_for('index'))
        
        error = "Usuario no registrado o datos incorrectos"
            
    return render_template("iniciar_sesion.html", error=error)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nuevo_usuario = request.form.get('usuario')
        nueva_password = request.form.get('password')
        
        if nuevo_usuario and nueva_password:
            if usuarios_col.find_one({"usuario": nuevo_usuario}):
                return "El usuario ya existe", 400
            
            usuarios_col.insert_one({
                "usuario": nuevo_usuario, 
                "password": nueva_password
            })
            return redirect(url_for('login'))
            
    return render_template("formulario.html")

@app.route("/recuperar", methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template("recuperar_contraseña.html")

@app.route("/tareas")
def tareas():
    return render_template("gestor_tareas.html")

if __name__ == "__main__":
    app.run(debug=True)