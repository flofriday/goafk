# goafk Server
The server that powers the goafk service.

## Run the server (virtual env)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run the server (docker)
TODO
