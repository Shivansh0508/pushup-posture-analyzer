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
