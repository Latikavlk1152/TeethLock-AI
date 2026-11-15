# 🦷 TeethLock – AI-Based Laptop Authentication using Teeth Recognition

![Python](https://img.shields.io/badge/Python-3.12-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Overview

TeethLock is an AI-powered authentication system that verifies a user's identity using **teeth biometrics** captured through a webcam.

Unlike traditional face recognition systems, TeethLock authenticates users based on the unique characteristics of their teeth, making it an additional biometric security mechanism.

The project was developed as a **Bachelor of Engineering Final Year Project**.

---

## ✨ Features

- User registration through webcam
- Automatic teeth dataset collection
- Facial landmark detection using dlib
- Teeth region extraction
- CNN-based teeth recognition
- Model training using transfer learning
- Real-time authentication
- Automatically locks Windows if authentication fails
- Simple Tkinter GUI

---

## 🏗 Project Architecture

```
Camera
   │
   ▼
Face Detection (OpenCV)
   │
   ▼
68 Facial Landmarks (dlib)
   │
   ▼
Teeth Region Extraction
   │
   ▼
CNN Model (TensorFlow/Keras)
   │
   ▼
Authentication
        │
        ├── Verified ✅
        └── Stranger ❌ → Lock Computer
```

---

## 📂 Project Structure

```
TeethLock/
│
├── assets/
│   └── screenshots/
│
├── dataset/
│
├── docs/
│
├── models/
│   ├── base_model.h5
│   ├── haarcascade_frontalface_default.xml
│   └── shape_predictor_68_face_landmarks.dat
│
├── src/
│   ├── app_gui.py
│   ├── create_face_datasets.py
│   ├── training_model.py
│   └── lock_unlock_face_recognition.py
│
├── trainer/
│   └── trained_model.h5
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙ Technologies Used

- Python
- TensorFlow
- Keras
- OpenCV
- dlib
- NumPy
- Tkinter
- PyAutoGUI

---

## 🚀 Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/TeethLock.git
```

Move into the project.

```bash
cd TeethLock
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## ▶ Running the Project

Start the application.

```bash
python src/app_gui.py
```

---

## 📷 Workflow

### 1. Register User

Capture 100 images of the user's teeth.

### 2. Train Model

Train the CNN model using the captured dataset.

### 3. Authenticate

Run the authentication module to verify the user.

---

## 📸 Screenshots

### Home Screen

*(Add screenshot here)*

### Dataset Collection

*(Add screenshot here)*

### Training

*(Add screenshot here)*

### Authentication

*(Add screenshot here)*



## 👩‍💻 Author

This repository is maintained by **Latika Kumare**.

Originally developed as a Bachelor of Engineering Final Year Group Project.

### Team Members
- Latika Kumare
- Sushil Mhetre
- Sanket Lipne
- Sumit Koli

## 👩‍💻 Maintainer

This repository is maintained and enhanced by **Latika Kumare**.

The original system was developed as a Bachelor of Engineering Final Year Group Project.

## 📄 License

This project is licensed under the MIT License.