FROM python:3.9

COPY . .

RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]