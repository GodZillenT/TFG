FROM python:3.9.4

WORKDIR /TFG/evaluation_api

# Install requirements, including from Gemfury
ADD ./evaluation_api /TFG/evaluation_api

RUN pip install --upgrade pip
RUN pip install --upgrade -r /TFG/evaluation_api/requirements.txt


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]