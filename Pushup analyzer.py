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
 # Live scores for each body part
        self.head_score = 0
        self.arm_score = 0
        self.body_score = 0
        self.leg_score = 0
        
        # Data collection for results table
        self.rep_data = []
        self.current_rep_feedback = []
        
        # Feedback mode
        self.analyzing = True
        self.feedback_mode = False
        
        print("Model loaded successfully!")
        
def calculate_angle(self, a, b, c):
        """Calculate angle between three points (a-b-c), b is vertex"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle
