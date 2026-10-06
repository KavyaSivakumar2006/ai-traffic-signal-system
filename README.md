# 🚦 AI-Based Real-Time Adaptive Traffic Signal System

## 📌 Overview

This project implements a real-time adaptive traffic signal system using YOLOv8 object detection.

It detects vehicles from webcam input, analyzes vehicle density, and dynamically adjusts traffic signal timing based on the detected traffic conditions.

The project is currently being upgraded from a basic vehicle-count-based system to a more advanced AI-based traffic management system with vehicle tracking, traffic analysis, intelligent signal control, emergency vehicle priority, and a web-based monitoring dashboard.

---

## 🧠 Technologies Used

- Python
- YOLOv8 Nano (Ultralytics)
- OpenCV
- NumPy
- PyTorch

---

## ⚙️ Current Workflow

Webcam
↓
YOLO Detection
↓
Vehicle Classification
↓
Vehicle Counting
↓
Traffic Density Classification
↓
Adaptive Signal Timing
↓
Live Display

---

## 🚦 Current Signal Logic

0–10 vehicles → 20 sec green  
11–20 vehicles → 40 sec green  
21+ vehicles → 60 sec green

Signal cycle:

RED → GREEN → YELLOW → RED

---

## 📂 Project Structure

```text
ai-traffic-signal-system/
│
├── traffic_ai.py
├── requirements.txt
├── README.md
└── .gitignore