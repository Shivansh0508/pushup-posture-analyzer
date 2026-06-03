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

    print("\n" + "=" * 75)
    print("FEATURES:")
    print("✓ Real-time posture scoring for:")
    print("  • Head/Neck alignment")
    print("  • Arms/Elbows position")
    print("  • Body/Core stability")
    print("  • Legs/Base support")
    print("✓ Live form corrections during exercise")
    print("✓ Detailed results table after 5 pushups")
    print("\nINSTRUCTIONS:")
    print("• Position camera for SIDE VIEW")
    print("• Complete 5 pushups")
    print("• Get detailed analysis with scores")
    print("\nCONTROLS:")
    print("- ENTER: New set after results")
    print("- Q: Quit")
    print("=" * 75 + "\n")
    
