# Student Score Management System

This is a simple Python student score management system built with:

- `PyQt6` for the desktop UI
- `socket` for client/server communication
- `sqlite3` for local data storage

## Features

- Add a new student with multiple subjects and scores
- Show all students and their scores
- Modify an existing student's subject score
- Add a new subject for an existing student
- Delete a student

## Project Structure

```text
.
|- Main.py
|- README.md
|- requirements.txt
|- WorkWidgets/
|- SocketClient/
|- server/
   |- MainServer.py
   |- Command/
   |- DBController/
   |- SocketServer/
```

## Requirements

- Python 3.9 or newer
- `PyQt6`

Install dependencies:

```powershell
pip install -r requirements.txt
```

## How to Run

Open two terminals.

Terminal 1: start the server

```powershell
python server\MainServer.py
```

Terminal 2: start the client UI

```powershell
python Main.py
```

To stop the server, type:

```text
finish
```

## Demo Flow

1. Open the server first.
2. Open the client window.
3. In `Add Student`, enter a new name, click `Query`, add one or more subjects, then click `Send`.
4. In `Show Student`, check the saved data.
5. In `Modify Subject`, change a score or add a new subject.
6. In `Delete Student`, remove a student record.

## Notes

- Student names are treated as unique in this project.
- The database file is stored at `server/student_dict.db`.
- If the server is not running, the client will show a connection error message.
