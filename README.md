# Auto-Smiling-Capture

A learning focused computer vision project using OpenCV and MediaPipe FaceMesh to detect smiles in real time and automatically capture images.

This repository is maintained as a logbook-style project, documenting the final solution alongside major problems, mistakes, and debugging insights encountered during development particularly those related to Python environments on macOS. This miniproject is an exercise in "learning in public", capturing both the technical implementation and the troubleshooting process.

## Project Intent

The purpose of this project was not to build a production-grade smile detector, but rather to achieve the following educational goals:
* Understand the fundamental operations of **OpenCV**.
* Learn how real-time camera streams are handled in **Python**.
* Explore **MediaPipe FaceMesh** landmarks and their coordinate systems.
* Gain hands-on experience with **macOS-specific Python environment issues**.
* Document debugging steps for reuse in future projects.

This repository serves as a learning artifact, a personal reference guide, and a debugging playbook for macOS, Python, and Computer Vision (CV) workflows.

---

## Technical Stack

* **Python 3.11**
* **OpenCV (cv2):** Camera input and image processing.
* **MediaPipe FaceMesh (Apple Silicon compatible build):** Facial landmark extraction.
* **PyAutoGUI:** Automation utilities (planned for future use).
* **macOS afplay:** Native system audio feedback.

---

## Conceptual Reference

This project was inspired by a YouTube tutorial demonstrating smile detection using OpenCV and MediaPipe.

* **Tutorial Reference:** [[YouTube Link](https://youtu.be/INEprZdeSbg?si=_7Hj2AerBnd_b2Wy)]

The tutorial served as a conceptual starting point. All macOS-specific setup, environment debugging, library compatibility handling, and logic refinements were explored and resolved independently.

---

## Final Behavior

1. **Live Stream:** A webcam feed opens via OpenCV.
2. **Detection:** FaceMesh landmarks are detected in real time.
3. **Calculation:** The distance between selected mouth landmarks is computed.
4. **Trigger:** If the distance crosses a predefined threshold:
* A smile is detected.
* An image is automatically saved to the local directory.
* A system sound (Glass.aiff) is played for feedback.



---

## Smile Detection Logic

1. Capture a frame from the webcam using OpenCV.
2. Flip the frame horizontally to create a mirror effect.
3. Convert the color space from BGR to RGB for MediaPipe compatibility.
4. Execute MediaPipe FaceMesh to extract facial landmarks.
5. Select two specific mouth landmarks (ID 43 and ID 287).
6. Convert normalized landmark values to pixel coordinates based on frame dimensions.
7. Compute the **Euclidean distance** between the two points:


8. Apply a threshold to infer a smile based on the horizontal expansion of the mouth.
9. Trigger image capture and audio feedback.

### Landmark Selection

The following MediaPipe FaceMesh landmarks were used:

* **ID 43:** Left corner of the mouth.
* **ID 287:** Right corner of the mouth.

These landmarks were chosen empirically to approximate mouth width expansion during a smile.

---

## Core Implementation

```python
import cv2
import mediapipe as mp
import pyautogui
import os

x1 = y1 = x2 = y2 = 0

# Initial sound check
os.system("afplay /System/Library/Sounds/Glass.aiff")

face_mesh = mp.solutions.face_mesh.FaceMesh()
camera = cv2.VideoCapture(0)

while True:
    _, image = camera.read()
    fh, fw, _ = image.shape

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    output = face_mesh.process(rgb_image)
    landmark_points = output.multi_face_landmarks

    if landmark_points:
        landmarks = landmark_points[0].landmark

        for id, landmark in enumerate(landmarks):
            x = int(landmark.x * fw)
            y = int(landmark.y * fh)

            if id == 43:
                x1, y1 = x, y
            if id == 287:
                x2, y2 = x, y

        dist = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        print(f"Current Distance: {dist}")

        if dist > 140:
            print("Smile detected")
            cv2.imwrite("smile.png", image)
            os.system("afplay /System/Library/Sounds/Glass.aiff")
            # Delay to prevent multiple captures for one smile
            cv2.waitKey(10000)

    cv2.imshow("Smile Detector", image)

    if cv2.waitKey(100) == 27: # ESC key to exit
        break

camera.release()
cv2.destroyAllWindows()

```

---

## Debugging Logbook

### Problem 1: ModuleNotFoundError: No module named 'cv2'

* **Issue:** OpenCV was installed, but imports failed in scripts and Jupyter.
* **Root Cause:** Packages were being installed into the incorrect Python interpreter (base Conda).
* **Fix:** Use the explicit path to the interpreter: `<exact_python_path> -m pip install opencv-python`

### Problem 2: Jupyter Ignoring Virtual Environments

* **Issue:** Activating a venv in the terminal had no effect on Jupyter Notebooks.
* **Diagnosis:** Ran `import sys; print(sys.executable)` to verify the path.
* **Lesson Learned:** Jupyter utilizes its own set of kernels; shell activation does not automatically switch the Jupyter kernel.

### Problem 3: MediaPipe Failing on Apple Silicon

* **Issue:** `mp.solutions` missing or random runtime crashes.
* **Fix:** Reinstall the silicon-specific build:
```bash
pip uninstall mediapipe
pip install mediapipe-silicon

```



### Problem 4: FaceMesh Initializer Argument Error

* **Issue:** `TypeError: unexpected keyword argument 'refine_face_landmarks'`
* **Root Cause:** The `mediapipe-silicon` distribution does not support the `refine_face_landmarks` argument.
* **Fix:** Revert to standard initialization: `face_mesh = mp.solutions.face_mesh.FaceMesh()`

---

## Key Lessons

* Always match `pip` with the exact Python interpreter being used by your IDE or Notebook.
* Jupyter kernels override shell environment activations.
* Apple Silicon (M1/M2/M3) often requires architecture-specific library builds.
* Environment debugging is a core technical skill, not an indication of failure.

---

## Limitations and Future Improvements

### Current Limitations

* Threshold based detection (fixed value of 140) may not work for all users.
* Sensitivity to lighting and head orientation.
* Basic capture logic without advanced "debounce" handling.
* Lack of face alignment normalization.

### Planned Improvements

* Implement a multi-landmark smile ratio (Mouth Width / Face Width) for better accuracy.
* Add sophisticated debounce logic for image capture.
* Implement on-screen landmark visualization (drawing the mesh).
* Explore ML-based smile classification (SVM or CNN).
* Ensure cross-platform compatibility for audio feedback.

---

## Final Note

This repository is intentionally verbose. It exists as a personal learning log and a reminder that real learning often happens after the tutorial ends when the code breaks and requires logical troubleshooting. If this helps clarify a future debugging session, it has served its purpose.

---
