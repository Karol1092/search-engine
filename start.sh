#!/bin/bash

source .venv/bin/activate

uvicorn app.main:app --reload --port 8000 &
python -m http.server 5500 --directory frontend