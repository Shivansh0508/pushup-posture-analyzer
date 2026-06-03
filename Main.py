import cv2
from pushup_analyzer import PushupAnalyzer

def main():
    print("=" * 75)
    print(" PUSHUP POSTURE CORRECTION TOOL - Live Score Analysis")
    print("=" * 75)
    print("\nInitializing AI posture analyzer...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return
     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    analyzer = PushupAnalyzer()
    
