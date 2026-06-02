#  Pushup Posture Correction Tool

A real-time AI-powered pushup form analyzer using YOLOv8 pose estimation. It scores your posture live across four body segments and gives a detailed rep-by-rep breakdown after every set.

---

## Demo

> Position your camera for a **side view**, complete 5 pushups, and get scored instantly.

---

## Features

- **Real-time posture scoring** across 4 body segments:
  -  Head / Neck alignment
  -  Arms / Elbow position
  -  Body / Core stability
  -  Legs / Base support
- **Live form corrections** displayed on-screen during exercise
- **Detailed results table** after every 5-rep set with rep-by-rep breakdown
- **Action plan & grade** (Excellent / Good / Fair / Needs Work)

---

## Requirements

- Python 3.8+
- Webcam

### Install dependencies

```bash
pip install -r requirements.txt
```

> The `requirements.txt` installs:
> - `opencv-python` - webcam capture and frame rendering
> - `ultralytics` - YOLOv8 pose estimation model
> - `numpy` - angle and keypoint calculations

On first run, the YOLOv8 nano-pose model (`yolov8n-pose.pt`) will be **automatically downloaded** by the `ultralytics` library (~6 MB).

---

## Project Structure

```
.
├── main.py               # Entry point - webcam loop and key controls
├── pushup_analyzer.py    # Core logic - pose analysis, scoring, results display
├── requirements.txt      # Python dependencies
└── README.md
```

---

## How to Run

```bash
python main.py
```

### Controls

| Key     | Action                                      |
|---------|---------------------------------------------|
| `Enter` | Start a new set after results are displayed |
| `R`     | Reset counter mid-set                       |
| `Q`     | Quit the application                        |

---

## Camera Setup

- Use a **side-view** angle (camera level with your body, perpendicular to direction of movement)
- Ensure your **full body is visible** in frame - head to feet
- Good lighting improves detection accuracy

---

## Scoring System

Each body part is scored out of **100%** per rep:

| Score   | Status          |
|---------|-----------------|
| ≥ 90%   |  Excellent     |
| ≥ 75%   |  Good          |
| ≥ 60%   |  Needs Work    |
| < 60%   |  Poor          |

The **overall score** is the average of all four segment scores.

---

## How It Works

1. Each frame is passed through `yolov8n-pose.pt` to extract 17 body keypoints
2. Joint angles (elbow, body alignment, leg) are calculated using vector math
3. Each segment is scored independently and displayed live on the video feed
4. A rep is counted when the elbow angle transitions from `≤ 100°` (down) back to `≥ 160°` (up)
5. After 5 reps, a full results screen is shown with per-rep scores and recommendations

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ERROR: Could not open webcam` | Check that your webcam is connected and not used by another app |
| Low detection accuracy | Improve lighting; ensure full body is in frame from the side |
| Model not found | Let the app run once - it auto-downloads `yolov8n-pose.pt` |
| Slow FPS | Use a machine with a GPU, or switch to a lighter model like `yolov8n-pose` (already the smallest) |

---

## License

MIT License - free to use.
