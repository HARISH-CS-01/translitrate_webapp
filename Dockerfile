FROM python:3.13-slim
RUN apt-get update && apt install -y python3-pip
RUN pip3 install fastapi[standard]>=0.116.1 pydantic>=2.11.7 torch>=2.8.0 numpy
WORKDIR /translit_app
COPY src src/
COPY best_model_95.pt best_model_95.pt
COPY inferencemodel.py inferencemodel.py
COPY Model.py Model.py
COPY Translit_app.py Translit_app.py
CMD ["fastapi","dev","Translit_app.py","--host","0.0.0.0","--port","8000","--reload"]