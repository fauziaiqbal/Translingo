# Translingo
**Translingo** is an AI-powered language translation web app developed for the **WAICY 2025** competition. It uses a **Flask (Python)** backend and a **React (JavaScript)** frontend to detect the language of any given text and translate it into a user-selected language in real time. The system demonstrates how artificial intelligence can bridge global communication barriers by applying natural language processing (NLP) techniques for language detection and translation. When a user inputs text, the frontend sends it to the backend API, which processes it using AI-based language models and returns both the detected source language and its accurate translation. Designed for accessibility, speed, and cross-platform compatibility, Translingo showcases the practical use of AI in breaking linguistic boundaries and promoting inclusive communication across diverse communities.

Folder structure
```bash
translator-app/
      ├── backend/
      │      ├── app.py
      │      └── requirements.txt
      └── translator-ui(or frontend)/ 
             ├── src/App.js    
             ├── build    
             ├── public    
             ├── .env.development    
             ├── .gitignore    
             ├── package.json    
             ├── README.md    
             ├── package-lock.json    
             └── yarn.lock
```
# STEP BY STEP INSTRUCTIONS ON HOW TO RUN:
(if errors occur, goto the end to step 5 some common issues are listed there)

## Simple Steps Break down:
### How to Run
1. Clone repo
2. cd backend && pip install -r requirements.txt && python app.py
3. cd frontend && yarn install && yarn start

## Explaination
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
* **git error**
  run Run:
```bash
git --version
```
  If you get “git is not recognized as an internal or external command”, Git isn’t actually installed on you computer. 
Go to the official site — [https://git-scm.com/download/win](https://git-scm.com/download/win)
   (Don’t grab it from shady “software download” sites unless you *enjoy* malware.)
2. The installer will download automatically. Run the `.exe` file.
3. Follow the setup wizard:
   * **Choose editor:** pick *Visual Studio Code* if you have it, otherwise *Vim* or *Notepad++*.
   * **Adjust PATH:** pick *“Git from the command line and also from 3rd-party software.”* This makes `git` work in CMD, PowerShell, and everywhere else.
   * **Line endings:** choose *“Checkout Windows-style, commit Unix-style.”*
   * Leave other options as defaults.
4. Finish and reboot.

Now test it:

```bash
git --version
```

If you see something like `git version 2.47.0`, this means that git is successfully installed on your computer.
* **Backend crashes on startup**
  Read the Python traceback. Common causes: missing package, wrong Python version, or syntax errors. Install packages, or run `python --version` to confirm.
### a. Go into backend folder
on cmd goto backend folder by running
 
 cd backend

IF ERRORS STILL OCCUR AND THESE STEPS DOESN'T FIX IT I AM REALLY SORRY, 

## Support / Contact
If you run into unresolved issues, and For inquiries related to the project, you can reach me via email:
   📧 **fauziaiqbal.018@gmail.com**
