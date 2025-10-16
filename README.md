# Translingo
Translates and detects text language.

# STEP BY STEP INSTRUCTIONS ON HOW TO RUN:
(if errors occur, goto the end to step 5 some common issues are listed there)

### 1. Clone the project

Press **Win+R**, type `cmd` and press Enter. In the command prompt run:

```bash
git clone https://github.com/your-username/translator-app.git
cd translator-app
```

## 2. Run the backend (Flask)

### a. Go into backend folder

In the same cmd window:

```bash
cd backend
```

### b. Create a virtual environment 

NOT NECESSARY THO, I RUN THIS PROJECT WITHOUT A VIRTUAL ENVIRONMENT. SO IT WILL WORK EVEN IF YOU DON'T CREATE A VIRTUAL ENVIRONMENT: 

to create virtual environment run

```bash
python -m venv venv
```

### c. Activate the virtual environment (Windows cmd)

```bash
venv\Scripts\activate
```

If they use PowerShell instead, they can run:

```powershell
.\venv\Scripts\Activate.ps1
```

(If PowerShell blocks scripts, they may temporarily need `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` — advanced users only.)

### d. Install backend dependencies

Make sure `requirements.txt` exists in the backend folder. Typical contents:

(required libraries, don't run this one)

```
Flask
Flask-Cors
```

Then run (Run this command inside the backend folder. u can use cd function to get into that folder, if errors occurs goto step 5 and fix your errors):

```bash
pip install -r requirements.txt
```

### e. Run the Flask app

Go to cmd and type: 

```bash
python app.py
```

or

goto IDLE and open app.py, press Ctrl+S and F5 to run or simply go to the run tab in the ribbon and click on run module from dropdown.

You should see something like `Running on http://127.0.0.1:5000` or `http://0.0.0.0:5000`.


## 3. Run the frontend (React)

### a. Open a new command prompt window (don’t kill the backend)

app.py is flask-backend keep it running or else the link is killed between App.js(react-frontend) and app.py(flask-backend)

Press **Win+R**, type `cmd` again, or open a new terminal tab.

### b. Go into frontend folder

```bash
cd path\to\translator-app\frontend
```

(If you’re already in the repo root, `cd ../frontend` from backend.)

if error occurs move to step 5

### c. Install frontend dependencies

```bash
npm install
```

If `npm` isn’t installed, they need to install Node.js (LTS) from nodejs.org.

### d. Start the React dev server

```bash
npm start
```

React will usually start at `http://localhost:3000`.


## 4. Helpful Windows one-click: run_project.bat

Open notepad and type:

```bat
@echo off
title Translator App - Backend
start cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python app.py"
timeout /t 1 >nul
title Translator App - Frontend
start cmd /k "cd /d %~dp0frontend && npm start"
exit
```

save this as run_project.bat or whatever you like but remove .txt extension.

This will open two windows: one for Flask, one for React. (If It Doesn't Work Then Leave It)

## 5. Common issues & fixes 

* **error using cd**
  Ensure that while trying to open a specific folder on cmd write
  

  ```bash
  cd folderpath
  ```

to know the folder path right click on the folder you want to open and click on properties it will show you the file path for example my flask-backend (app.py) is at 'C:\Users\HP\Desktop\translator-app' from properties then you should run 
 ```bash
cd  C:\Users\HP\Desktop\translator-app
 ```

Then run
 ```
python app.py
 ```

this will open app.py on my cmd window

* **Node_modules missing or broken**
  Delete `node_modules` and `package-lock.json`, then:

  ```bash
  npm install
  ```
* **npm error while installing**
  if error occurs when you run this
  
```bash
npm install
```

goto nodejs.org and download Node.js (LTS) complete the installation and then move back to cmd and run. 

```bash
npm install
```
this time it should work

* **Backend crashes on startup**
  Read the Python traceback. Common causes: missing package, wrong Python version, or syntax errors. Install packages, or run `python --version` to confirm.
### a. Go into backend folder
on cmd goto backend folder by running
 
 cd backend

IF ERRORS STILL OCCUR AND THESE STEPS DOESN'T FIX IT I AM REALLY SORRY, 

## Support / Contact
If you run into unresolved issues, contact:
- Email: fauziaiqbal.018@gmail.com  
- WhatsApp: +92 321 4796769
