# 🎮 Juego 3 en Raya - Guía Completa para Principiantes

¡Bienvenida! Esta es una guía paso a paso para instalar y ejecutar el juego de 3 en raya. No te preocupes si no tienes experiencia, seguiremos cada paso juntos. 😊

---

## 📋 ¿Qué vamos a instalar?

- **Python** (el lenguaje de programación)
- **MySQL** (base de datos para guardar jugadores y partidas)
- **UV** (herramienta para manejar el proyecto)
- **El juego** (los archivos del proyecto)

---

## 🚀 PASO 1: Instalar Python

### Windows:
1. Ve a: https://www.python.org/downloads/
2. Descarga "Python 3.12" (el botón amarillo grande)
3. **MUY IMPORTANTE:** Al instalar, marca la casilla "Add Python to PATH"
4. Haz clic en "Install Now"
5. Espera a que termine

### Linux (Ubuntu/Debian):
Abre la terminal y ejecuta:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### macOS:
Abre la terminal y ejecuta:
```bash
brew install python@3.12
```
(Si no tienes Homebrew, instálalo desde: https://brew.sh)

### ✅ Verificar que Python se instaló:
Abre una **terminal nueva** (CMD en Windows, Terminal en Mac/Linux) y escribe:
```bash
python --version
```
Debería decir algo como: `Python 3.12.x`

Si no funciona, intenta:
```bash
python3 --version
```

---

## 🗄️ PASO 2: Instalar MySQL

### Windows:
1. Ve a: https://dev.mysql.com/downloads/installer/
2. Descarga "MySQL Installer" (el archivo más grande)
3. Ejecuta el instalador
4. Selecciona "Developer Default"
5. **IMPORTANTE:** Cuando te pida una contraseña para root, escribe algo que recuerdes (ejemplo: `Root@123`)
6. Anota esta contraseña, la necesitarás después
7. Continúa dando "Next" hasta terminar

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo mysql_secure_installation
```

Cuando te pregunte por la contraseña, usa: `Root@123` (o la que prefieras)

### macOS:
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### ✅ Verificar que MySQL se instaló:
```bash
mysql --version
```
Debería mostrar algo como: `mysql  Ver 8.x.x`

---

## 🛠️ PASO 3: Instalar UV

UV es una herramienta moderna para manejar proyectos Python de forma más rápida.

### Windows (PowerShell como Administrador):
1. Haz clic derecho en el botón de Windows
2. Selecciona "Windows PowerShell (Administrador)"
3. Copia y pega esto:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
4. **Cierra y vuelve a abrir** PowerShell

### Linux/macOS:
Abre la terminal y ejecuta:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Luego ejecuta:
```bash
source $HOME/.cargo/env
```

### ✅ Verificar que UV se instaló:
Cierra y abre una **terminal nueva**, luego escribe:
```bash
uv --version
```
Debería mostrar algo como: `uv 0.x.x`

---

## 📁 PASO 4: Descargar el Proyecto

### Opción A: Si tienes los archivos en una carpeta
Ya tienes todo listo, salta al PASO 5.

### Opción B: Si te enviaron el proyecto por correo/USB
1. Descomprime el archivo ZIP
2. Deberías tener una carpeta llamada `en_raya` con estos archivos:
   ```
   en_raya/
   ├── database.py
   ├── game.py
   ├── server.py
   ├── requirements.txt
   ├── templates/
   │   └── index.html
   └── README.md
   ```

---

## ⚙️ PASO 5: Configurar el Proyecto

### 1️⃣ Abrir terminal en la carpeta del proyecto

**Windows:**
- Abre la carpeta `en_raya`
- Mantén presionada la tecla `Shift` y haz clic derecho dentro de la carpeta
- Selecciona "Abrir ventana de PowerShell aquí" o "Abrir en Terminal"

**Mac/Linux:**
- Abre Terminal
- Escribe `cd ` (con espacio al final)
- Arrastra la carpeta `en_raya` a la terminal
- Presiona Enter

### 2️⃣ Configurar la contraseña de MySQL

**📄 Lee primero el archivo `CONFIGURACION.txt` que viene en el proyecto**

Abre el archivo `database.py` con un editor de texto (Bloc de notas, VSCode, etc.)

Busca las líneas 6-11 (aproximadamente):
```python
def __init__(
    self,
    host="localhost",
    user="root",
    password="Root@Pass123",    # 👈 CAMBIA ESTA LÍNEA si no esta asi 
    database="tictactoe",
):
```

Cambia `password="Root@Pass123"` por TU contraseña de MySQL:
```python
    password="TU_CONTRASEÑA_AQUI",
```

**⚠️ IMPORTANTE:** Usa la contraseña que elegiste cuando instalaste MySQL.

**🔍 Para verificar tu contraseña:**
```bash
mysql -u root -p
# Ingresa tu contraseña. Si entras a MySQL, esa es la correcta.
```

Guarda el archivo.

### 3️⃣ Crear el entorno virtual

En la terminal (dentro de la carpeta `en_raya`), ejecuta:
```bash
uv venv
```

Deberías ver un mensaje como:
```
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

### 4️⃣ Activar el entorno virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

✅ **Sabrás que funcionó** cuando veas `(.venv)` al inicio de la línea:
```
(.venv) C:\Users\TuNombre\en_raya>
```

### 5️⃣ Instalar las dependencias

```bash
uv pip install -r requirements.txt
```

Esto instalará Flask y mysql-connector-python. Tomará unos segundos.

---

## 🎮 PASO 6: ¡Ejecutar el Juego!

### 1️⃣ Asegúrate de que MySQL esté corriendo

**Windows:**
- Abre "Servicios" (busca en el menú de inicio)
- Busca "MySQL80" (o similar)
- Si no dice "En ejecución", haz clic derecho → "Iniciar"

**Mac/Linux:**
```bash
sudo systemctl start mysql    # Linux
brew services start mysql      # Mac
```

### 2️⃣ Ejecutar el servidor

En la terminal (con el entorno virtual activado):
```bash
python server.py
```

Deberías ver:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

✅ **¡Perfecto!** El servidor está funcionando.

⚠️ **Si ves un error de MySQL**, verifica que:
- MySQL esté corriendo
- La contraseña en `database.py` sea correcta

### 3️⃣ Abrir el juego en el navegador

Abre tu navegador favorito (Chrome, Firefox, Edge) y ve a:

**http://localhost:5000**

¡Deberías ver el juego! 🎉

---

## 🎯 Cómo Usar el Juego

### 1. Crear Jugadores
- Ve a la pestaña **"Nuevo Jugador"**
- Escribe un nombre (ejemplo: "Ana")
- Haz clic en **"Crear Jugador"**
- Crea al menos 2 jugadores

### 2. Iniciar una Partida
- Ve a la pestaña **"Nueva Partida"**
- Selecciona el Jugador 1 (jugará con X)
- Selecciona el Jugador 2 (jugará con O)
- Haz clic en **"Iniciar Partida"**

### 3. Jugar
- Haz clic en las casillas vacías para hacer tu jugada
- El juego alterna automáticamente entre X y O
- El juego detecta automáticamente al ganador o empates

### 4. Ver Estadísticas
- Ve a la pestaña **"Estadísticas"**
- Verás cuántas partidas ha ganado cada jugador

### 5. Continuar una Partida Guardada
- Ve a **"Partidas Activas"**
- Haz clic en **"Continuar"** en cualquier partida

---

## 🛑 Cómo Detener el Servidor

Cuando termines de jugar:
1. Ve a la terminal donde está corriendo `python server.py`
2. Presiona `Ctrl + C`
3. El servidor se detendrá

Para volver a jugar después:
1. Abre la terminal en la carpeta `en_raya`
2. Activa el entorno virtual:
   - Windows: `.venv\Scripts\Activate.ps1`
   - Mac/Linux: `source .venv/bin/activate`
3. Ejecuta: `python server.py`
4. Abre el navegador en http://localhost:5000

---

## 🆘 Solución de Problemas Comunes

### ❌ "python: command not found"
**Solución:** Asegúrate de que Python se instaló correctamente. Intenta con `python3` en lugar de `python`.

### ❌ "uv: command not found"
**Solución:** 
1. Cierra y vuelve a abrir la terminal
2. Si sigue sin funcionar, reinstala UV siguiendo el PASO 3

### ❌ "Error conectando a MySQL"
**Soluciones:**
1. Verifica que MySQL esté corriendo (ve al PASO 6, punto 1)
2. Verifica que la contraseña en `database.py` sea correcta
3. Si olvidaste tu contraseña de MySQL, busca en Google "reset mysql root password"

### ❌ "Port 5000 already in use"
**Solución:** Otro programa está usando ese puerto. 

Edita `server.py`, busca la última línea:
```python
app.run(debug=True, port=5000)
```
Cámbiala a:
```python
app.run(debug=True, port=5001)
```
Y abre el navegador en: http://localhost:5001

### ❌ "Cannot import name 'Database'"
**Solución:** Asegúrate de que todos los archivos estén en la carpeta correcta:
- `database.py`, `game.py`, `server.py` en la raíz
- `index.html` dentro de la carpeta `templates`

### ❌ El tablero no aparece al iniciar partida
**Solución:** 
1. Presiona `F12` en el navegador para abrir las herramientas de desarrollo
2. Ve a la pestaña "Console"
3. Si ves errores en rojo, presiona `Ctrl+Shift+R` para recargar la página forzosamente

---

## 📞 ¿Necesitas Más Ayuda?

Si algo no funciona:

1. **Lee el mensaje de error completo** (aunque no lo entiendas, cópialo)
2. Busca en Google: "python [tu error aquí]"
3. Verifica que seguiste TODOS los pasos en orden
4. Asegúrate de que el entorno virtual esté activado (debes ver `(.venv)`)

---

## 🎓 ¿Qué Aprendiste?

Al completar este proyecto, aprendiste a:
- ✅ Instalar Python y gestionar paquetes
- ✅ Configurar una base de datos MySQL
- ✅ Usar entornos virtuales con UV
- ✅ Ejecutar un servidor web con Flask
- ✅ Conectar una aplicación web con una base de datos

¡Felicidades! 🎉 Esto es programación real en el mundo profesional.

---

## 📚 Archivos del Proyecto

- `database.py` - Maneja la conexión con MySQL y todas las operaciones de la base de datos
- `game.py` - Contiene la lógica del juego (reglas, ganador, empates)
- `server.py` - El servidor web que conecta todo (Flask)
- `templates/index.html` - La interfaz visual del juego
- `requirements.txt` - Lista de dependencias necesarias

---

## 💡 Consejos Finales

- **No borres la carpeta `.venv`** - contiene todas las dependencias instaladas
- **Siempre activa el entorno virtual** antes de ejecutar `python server.py`
- **La contraseña de MySQL** debe coincidir en `database.py`
- **MySQL debe estar corriendo** antes de iniciar el servidor

---

¡Disfruta jugando! 🎮✨