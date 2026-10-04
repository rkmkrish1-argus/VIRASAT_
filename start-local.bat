@echo off
cd /d "C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar_(3)\ambedkar\.venv\Scripts"
if not exist ".venv\Scripts\python.exe" (
  echo Creating Python environment...
  py -m venv .venv
)
echo Installing or updating project dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
echo.
echo Starting Dr. B.R. Ambedkar Digital Heritage Archive
echo Website: http://127.0.0.1:8000/
echo API docs: http://127.0.0.1:8000/docs
echo Press Ctrl+C in this window to stop the server.
.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
