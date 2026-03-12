# 🚦 AI-Based Real-Time Adaptive Traffic Signal System

## 📌 Overview
This project implements a real-time adaptive traffic signal system using YOLOv8 object detection.

It detects vehicles from webcam input and dynamically adjusts signal timing based on vehicle density.

---

## 🧠 Model Used
- YOLOv8 Nano (Ultralytics)
- Pretrained on COCO Dataset
- Python
- OpenCV
- NumPy

---

## ⚙ Workflow

Webcam  
↓  
YOLO Detection  
↓  
Vehicle Counting  
↓  
Traffic Density Classification  
↓  
Adaptive Signal Timing  
↓  
Live Display  

---

## 🚦 Signal Logic
0–10 vehicles → 20 sec green  
11–20 vehicles → 40 sec green  
21+ vehicles → 60 sec green  

Signal cycle: RED → GREEN → YELLOW → RED  

---

## 📂 Project Structure

```
ai-traffic-signal-system

- traffic_ai.py
- requirements.txt
- README.md
- .gitignore

```

## Installation Instructions
```
git clone https://github.com/KavyaSivakumar2006/ai-traffic-signal-system.git
cd ai-traffic-signal-system
```
## ▶ How to Run

```
pip install -r requirements.txt
python traffic_ai.py
```

---

## 🚀 Future Scope
- Multi-camera integration
- Web dashboard
- Emergency priority system


