# 🔒 TaskLock – Parental Control with Object Unlock 🔓

A smart, interactive parental control tool built with Python that locks tasks until the child proves completion — by showing a real-world object through the webcam!  
Perfect for motivating kids to **actually** complete assigned tasks before using the computer.

---

## 🚀 What Is TaskLock?

**TaskLock** is a fun and effective to-do/task manager designed with a twist — tasks can only be unlocked when the user captures a **matching photo** of a specific object (like a textbook, water bottle, or toothbrush).

No more fake “yes I did it” responses — proof is required to proceed!

---

## 🧠 Key Features

✅ **Add Tasks with Object Proof** – Parents can assign a task and set a reference object image via webcam  
🔒 **Lock System UI (Simulated)** – Tasks stay locked until the child proves completion  
📸 **Object Verification** – Uses ORB feature matching in OpenCV to compare live image with reference  
⚙️ **Customizable Sensitivity** – Matching thresholds can be adjusted in `settings.json`  
🖼️ **Visual Feedback** – Captured image shown for confirmation before saving  
🛠️ **Simple, Intuitive Interface** – Built with Tkinter for cross-platform UI  
📁 **Data Persistence** – Tasks and settings saved using local `.json` files

---

## 🧰 Technologies Used

- **Python 3.x**
- **Tkinter** – GUI
- **OpenCV (cv2)** – Image capture and comparison
- **ORB (Oriented FAST and Rotated BRIEF)** – Feature-based image matching
- **JSON** – Task and settings storage

---

## 📷 How It Works

1. Parent adds a task like “Brush your teeth” and captures an object image (e.g., toothpaste).
2. The task is saved in a locked state (`🔒`).
3. The child must complete the task and show the same object to the webcam.
4. If the live image **matches** the reference image → task unlocked (`✅`)  
   If not → task remains locked (`❌`).

---

## 🔧 How to Run

1. **Clone this repository**

```bash
git clone https://github.com/your-username/tasklock.git
cd tasklock

    Install dependencies

pip install opencv-python

    Run the app

python task_lock.py

    ✅ Make sure your webcam is functional before starting.

🛠️ Future Improvements

    🔑 Add secure parent PIN for task modifications

    📱 Android version using device camera + parental lock features

    🔊 Alarm reminder system for task deadlines

    ☁️ Cloud sync for cross-device access

    🎨 Better UI with drag-and-drop task management

🙌 Credits

Developed with ❤️ by Vasuki Naik
Open to feedback and contributions!

📜 License

This project is licensed under the MIT License.
