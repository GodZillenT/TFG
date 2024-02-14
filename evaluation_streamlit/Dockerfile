# Imagen base para Streamlit
FROM python:3.9.4

WORKDIR /TFG/evaluation_streamlit

# Instalar dependencias de Streamlit
ADD ./evaluation_streamlit /TFG/evaluation_streamlit
RUN pip install --upgrade pip
RUN pip install --upgrade -r /TFG/evaluation_streamlit/requirements.txt


# Puerto en el que se ejecuta Streamlit
EXPOSE 8501

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "app.py"]
