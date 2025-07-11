import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os
import json

# ----------- Config -----------
TASKS_FILE = "tasks.json"
REF_IMAGE_DIR = "ref_images"
TEMP_IMAGE = "current.jpg"
MATCH_THRESHOLD = 70
MATCH_RATIO_MIN = 0.35

# ----------- Helper Functions -----------

def take_photo(filename):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Camera not working!")
        return False

    print("📷 Show the object. Press 's' to save.")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename, frame)
            print(f"✅ Saved as {filename}")
            break
        elif key == 27:
            print("❌ Cancelled.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return True

def compare_images(ref_path, current_path):
    img1 = cv2.imread(ref_path, 0)
    img2 = cv2.imread(current_path, 0)

    if img1 is None or img2 is None:
        return 0, 0, 0

    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0, len(kp1), len(kp2)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
    return len(good_matches), len(kp1), len(kp2)

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
    print("💾 Tasks saved.")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

# ----------- App State -----------
if not os.path.exists(REF_IMAGE_DIR):
    os.makedirs(REF_IMAGE_DIR)

tasks = load_tasks()
task_widgets = []

# ----------- GUI Setup -----------
root = tk.Tk()
root.title("🔐 Object-Based To-Do Tracker")
root.geometry("420x600")
root.resizable(False, False)

title_label = tk.Label(root, text="To-Do Tracker", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# ----------- UI: Clear Button Logic -----------
def update_clear_button():
    if all(not task["locked"] for task in tasks) or len(tasks) == 0:
        clear_btn.pack(pady=5)
    else:
        clear_btn.pack_forget()

# ----------- Task Functions -----------

def add_task():
    task_name = simpledialog.askstring("New Task", "Enter task name:")
    if not task_name:
        return
    filename = os.path.join(REF_IMAGE_DIR, f"{task_name}_ref.jpg")
    print(f"📸 Capture object for task '{task_name}'")
    if not take_photo(filename):
        return
    new_task = {
        "name": task_name,
        "locked": True,
        "ref_img": filename
    }
    tasks.append(new_task)
    save_tasks()
    add_task_widget(new_task, len(tasks) - 1)
    update_clear_button()

def unlock_task(index):
    task = tasks[index]
    if not task["locked"]:
        return

    print(f"🔓 Trying to unlock: {task['name']}")
    if not take_photo(TEMP_IMAGE):
        return

    matches, kp1, kp2 = compare_images(task["ref_img"], TEMP_IMAGE)
    ratio = matches / min(kp1, kp2) if min(kp1, kp2) > 0 else 0
    print(f"📊 Matches: {matches}, Match Ratio: {ratio:.2f}")

    if matches > MATCH_THRESHOLD and ratio > MATCH_RATIO_MIN:
        task["locked"] = False
        task_widgets[index]["text"].set(f"{task['name']} - ✅ Done")
        task_widgets[index]["unlock"]["state"] = "disabled"
        task_widgets[index]["reset"]["state"] = "normal"
        save_tasks()
        print("✅ Task unlocked!")
        update_clear_button()
    else:
        print("❌ Object did not match.")

    if os.path.exists(TEMP_IMAGE):
        os.remove(TEMP_IMAGE)

def reset_task(index):
    confirm = messagebox.askyesno("Reset Task", f"Are you sure you want to lock '{tasks[index]['name']}' again?")
    if not confirm:
        return

    tasks[index]["locked"] = True
    task_widgets[index]["text"].set(f"{tasks[index]['name']} - 🔒 Locked")
    task_widgets[index]["unlock"]["state"] = "normal"
    task_widgets[index]["reset"]["state"] = "disabled"
    save_tasks()
    print(f"🔁 Task '{tasks[index]['name']}' has been reset.")
    update_clear_button()

def clear_all_tasks():
    confirm = simpledialog.askstring("Clear All", "Type DELETE to clear all tasks:")
    if confirm != "DELETE":
        print("❌ Cancelled.")
        return

    global tasks
    tasks = []
    save_tasks()

    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

    for file in os.listdir(REF_IMAGE_DIR):
        os.remove(os.path.join(REF_IMAGE_DIR, file))

    for widget in task_frame.winfo_children():
        widget.destroy()
    task_widgets.clear()
    update_clear_button()
    print("🧹 All tasks cleared!")

# ----------- UI: Task Widgets -----------

def add_task_widget(task, index):
    row = tk.Frame(task_frame)
    row.pack(anchor="w", pady=5)

    label_var = tk.StringVar()
    status = "🔒 Locked" if task["locked"] else "✅ Done"
    label_var.set(f"{task['name']} - {status}")

    label = tk.Label(row, textvariable=label_var, font=("Arial", 14))
    label.pack(side="left", padx=5)

    unlock_btn = tk.Button(row, text="Unlock", command=lambda i=index: unlock_task(i))
    unlock_btn.pack(side="right", padx=2)

    reset_btn = tk.Button(row, text="Reset", command=lambda i=index: reset_task(i), state="normal" if not task["locked"] else "disabled")
    reset_btn.pack(side="right", padx=2)

    if not task["locked"]:
        unlock_btn["state"] = "disabled"

    task_widgets.append({"text": label_var, "unlock": unlock_btn, "reset": reset_btn})

# ----------- UI: Buttons -----------

add_btn = tk.Button(root, text="➕ Add Task (Parent)", font=("Arial", 12), command=add_task)
add_btn.pack(pady=5)

clear_btn = tk.Button(root, text="🗑 Clear All Tasks", font=("Arial", 12), fg="red", command=clear_all_tasks)

task_frame = tk.Frame(root)
task_frame.pack(pady=10)

# ----------- Load Previous Tasks -----------
for idx, task in enumerate(tasks):
    add_task_widget(task, idx)
update_clear_button()

# ----------- Launch App -----------
root.mainloop()