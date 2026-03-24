FROM python:3.10-slim

# Working folder root
WORKDIR /app

# Copy Requirements and setup
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files.
COPY . .

# FastAPI port
EXPOSE 8000

# CMD: run main.py in the app folder.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]