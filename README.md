# 🔡 Transliteration WebApp (Seq2Seq LSTM + Attention)

An end-to-end **Transliteration Web Application** built from scratch using:  
- **Seq2Seq Encoder–Decoder model with LSTM + Attention**  
- ~**5.55M parameters**, trained for transliteration  
- **FastAPI backend** serving the model  
- **Frontend built with HTML, CSS, JavaScript**  
- Packaged with a **Dockerfile** for containerized deployment  

---

## 🚀 Features
- Encoder–Decoder **LSTM with Attention mechanism**  
- Class-based modular structure:  
  - `Model.py` → defines the neural network architecture  
  - `inferencemodel.py` → loads `best_model_95.pt` and handles inference  
  - `Translit_app.py` → main FastAPI app, serves frontend & handles requests  
- Frontend built with HTML/CSS/JavaScript for interactive input/output  
- Deployment-ready using **Docker** or **FastAPI** directly  

---

## 📂 Project Structure

transliterate_webapp/
│── Translit_app.py # Main FastAPI entrypoint (serves HTML + API)
│── Model.py # Neural network architecture (Seq2Seq + Attention)
│── inferencemodel.py # Loads trained model 'best_model_95.pt' & runs inference
│── best_model_95.pt # Trained model weights (~5.55M parameters)
│── requirements.txt # Python dependencies
│── Dockerfile # Docker build file
│── README.md # Documentation
│
└── src/
└── frontend/ # Web UI
├── index.html
├── style.css
└── script.js


---

## ⚡ Quickstart

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/transliterate_webapp.git
cd transliterate_webapp

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Run FastAPI app

fastapi dev Translit_app.py

4️⃣ Run with Docker

docker build -t transliterate-app .
docker run -p 8000:8000 transliterate-app

---

```
---
## 🌐 Web Interface
Open http://127.0.0.1:8000 in browser
Enter text in the input field → get transliterated output instantly
Simple UI powered by HTML, CSS, and JavaScript

