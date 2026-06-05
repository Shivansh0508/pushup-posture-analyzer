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
    
def calculate_body_alignment(self, shoulder, hip, ankle):
        """Check if body is in a straight line (plank position)"""
        alignment_angle = self.calculate_angle(shoulder, hip, ankle)
        return alignment_angle
    
    def analyze_head_posture(self, nose, shoulder, hip):
        """Analyze head/neck alignment"""
        feedback = []
        score = 100
        
        # Check if head is too far forward or back
        head_shoulder_x_diff = abs(nose[0] - shoulder[0])
        shoulder_hip_x_diff = abs(shoulder[0] - hip[0])

if head_shoulder_x_diff > shoulder_hip_x_diff * 1.5:
            feedback.append("Head too far forward")
            score -= 30
        elif nose[1] < shoulder[1] - 50:  # Head dropped down
            feedback.append("Head dropped - Look forward")
            score -= 25
        elif nose[1] > shoulder[1]:  # Head up too much
            feedback.append("Head too high - Neutral neck")
            score -= 20
        if not feedback:
            feedback.append("✓ Head aligned")
        return score, feedback

def analyze_arm_posture(self, shoulder, elbow, wrist, elbow_angle):
        """Analyze arm form and elbow position"""
        feedback = []
        score = 100
        
        # Check elbow angle for depth
        if elbow_angle > 160:
            feedback.append("✓ Arms extended")
        elif 90 <= elbow_angle <= 110:
            feedback.append("✓ Perfect depth")
        elif elbow_angle < 70:
            feedback.append("Too deep - Control!")
            score -= 15
        elif elbow_angle > 120:
            feedback.append("Go lower")
            score -= 25
