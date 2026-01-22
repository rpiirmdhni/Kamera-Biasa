# 📸 Kamera Biasa

**Kamera Biasa** is a simple desktop camera application built with **Python**, **OpenCV**, and **CustomTkinter**. The app provides a real-time camera preview, photo capture with optional flash, automatic date & time watermarking, and toast notifications after a photo is saved.

This project focuses on a **clean UI**, **clear logic separation**, and **safe camera handling** to avoid freezes, double triggers, or UI glitches.

---

## ✨ Features

* 🎥 Real-time camera preview
* 📷 Photo capture
* ⚡ Flash mode (on / off)
* 🕒 Automatic date & time watermark
* 🔔 Toast notification after capture
* 📁 Open capture folder directly from the app
* ⬅️ Navigation between Start Screen and Camera Screen
* 🌙 Dark mode user interface

---

## 🛠️ Tech Stack

* **Python 3.12.x**
* **OpenCV (cv2)** – camera access
* **CustomTkinter** – modern UI framework for Tkinter
* **Pillow (PIL)** – image processing and watermarking

---

## 📂 Project Structure

```
Kamera-Biasa/
│
├── main.py            # Main application file
├── camera_captures/   # Captured photos (auto-generated)
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Install dependencies

Make sure Python is installed, then run:

```bash
pip install opencv-python pillow customtkinter
```

### 2️⃣ Run the application

```bash
python main.py
```

---

## 🧠 Application Flow

1. **Start Screen**

   * Click *Start Camera*

2. **Camera Screen**

   * Camera starts and shows live preview
   * Capture button to take a photo
   * Flash button to enable / disable flash

3. **Photo Capture**

   * If flash is enabled → screen flashes once
   * Photo is saved to the `camera_captures` folder
   * Toast notification appears

4. **Back to Start**

   * Camera is safely released
   * Camera loop is stopped properly

---

## ⚠️ Technical Notes

* Flash is triggered **only from the capture logic**, not from the toast
* Toast notifications are **UI-only** and do not trigger side effects
* Camera loop is controlled using a running flag to prevent freezes
* `cv2.VideoCapture()` is started with a small delay to keep the UI responsive

---

## 🧪 Known Limitations

* No camera device selection
* No shutter sound
* Resolution depends on the default camera settings

---

## 🚀 Possible Improvements

* Fade / slide animations between screens
* Animated toast (fade / slide)
* Loading indicator ("Opening Camera...")
* Camera resolution settings
* Keyboard shortcuts for capture

---

## 👤 Author

Developed by **Rafie Restu Ramadhani (a.k.a rpiirmdhni)**
2026

---

> "Simple, functional, and just enough — Kamera Biasa."

