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
     print("Ready to analyze your form! \n")
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)

        analyzed_frame, feedback, elbow_angle, body_alignment = analyzer.analyze_pushup(frame)
        cv2.imshow('Pushup Posture Correction Tool - Live Analysis', analyzed_frame)
        key = cv2.waitKey(10) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == 13:  # Enter
            if analyzer.feedback_mode:
                print("\n Starting new analysis session...\n")
                analyzer.reset_counter()
        elif key == ord('r') or key == ord('R'):
            if not analyzer.feedback_mode:
                print("\n Counter reset!\n")
                analyzer.reset_counter()

 cap.release()
    cv2.destroyAllWindows()
    print("\n" + "=" * 75)
    print("Analysis complete! Keep improving your form! ")
    print("=" * 75)
