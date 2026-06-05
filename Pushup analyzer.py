import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
class PushupAnalyzer:
    def __init__(self):
        print("Loading YOLO pose model for pushup analysis...")
        self.model = YOLO('yolov8n-pose.pt')
        
        # Counters
        self.pushup_count = 0
        self.position = "up"
        self.set_target = 5
