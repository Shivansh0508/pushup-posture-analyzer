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
        # Check elbow flare (width)
        shoulder_elbow_y = abs(shoulder[1] - elbow[1])
        shoulder_elbow_x = abs(shoulder[0] - elbow[0])
        if shoulder_elbow_x > shoulder_elbow_y * 0.8:
            feedback.append("Elbows flaring wide")
            score -= 30
        return score, feedback
    
    def analyze_body_posture(self, shoulder, hip, knee, body_alignment):
        """Analyze core/body alignment"""
        feedback = []
        score = 100
        # Check body straight line
        if body_alignment < 160:
            feedback.append("⚠ Hips sagging")
            score -= 40
        elif body_alignment < 170:
            feedback.append("Slight hip sag")
            score -= 20
        elif body_alignment > 190:
            feedback.append("⚠ Hips too high")
            score -= 35
        elif body_alignment > 185:
            feedback.append("Hips slightly high")
            score -= 15
        else:
            feedback.append("✓ Body straight")
        return score, feedback

def analyze_leg_posture(self, hip, knee, ankle):
        """Analyze leg position and stability"""
        feedback = []
        score = 100
        # Check leg alignment
        leg_angle = self.calculate_angle(hip, knee, ankle)
        if leg_angle < 165:
            feedback.append("Knees bent - Straighten")
            score -= 25
        elif leg_angle < 175:
            feedback.append("Slight knee bend")
            score -= 10
        else:
            feedback.append("✓ Legs straight")
        # Check if feet are stable (not lifting)
        knee_ankle_y = abs(knee[1] - ankle[1])
        if knee_ankle_y < 100:  # Too close, feet might be lifting
            feedback.append("Keep feet grounded")
            score -= 15
        return score, feedback
    
    def generate_results_table(self):
        """Generate detailed results table after 5 pushups"""
        results = []
        results.append("\n" + "="*90)
        results.append(" " * 25 + "PUSHUP ANALYSIS - DETAILED RESULTS")
        results.append("="*90)
        results.append("")
        results.append(f"Total Pushups Completed: {self.pushup_count}")
        results.append("")
        # Calculate averages
        avg_head = sum([r['head_score'] for r in self.rep_data]) / len(self.rep_data)
        avg_arm = sum([r['arm_score'] for r in self.rep_data]) / len(self.rep_data)
        avg_body = sum([r['body_score'] for r in self.rep_data]) / len(self.rep_data)
        avg_leg = sum([r['leg_score'] for r in self.rep_data]) / len(self.rep_data)
        avg_overall = (avg_head + avg_arm + avg_body + avg_leg) / 4
        # Overall assessment
        results.append("-"*90)
        results.append("OVERALL PERFORMANCE SUMMARY")
        results.append("-"*90)
        results.append(f"{'Body Part':<20} {'Average Score':<15} {'Status':<20}")
        results.append("-"*90)

        def get_status(score):
            if score >= 90: return "✓ EXCELLENT"
            elif score >= 75: return "✓ GOOD"
            elif score >= 60: return "⚠ NEEDS WORK"
            else: return "✗ POOR"
                
        results.append(f"{'Head/Neck':<20} {avg_head:>6.1f}%{'':>8} {get_status(avg_head):<20}")
        results.append(f"{'Arms/Elbows':<20} {avg_arm:>6.1f}%{'':>8} {get_status(avg_arm):<20}")
        results.append(f"{'Body/Core':<20} {avg_body:>6.1f}%{'':>8} {get_status(avg_body):<20}")
        results.append(f"{'Legs/Stability':<20} {avg_leg:>6.1f}%{'':>8} {get_status(avg_leg):<20}")
        results.append("-"*90)
        results.append(f"{'OVERALL SCORE':<20} {avg_overall:>6.1f}%{'':>8} {get_status(avg_overall):<20}")
        results.append("="*90)
        results.append("")
        
        # Rep by rep breakdown
        results.append("-"*90)
        results.append("REP-BY-REP BREAKDOWN")
        results.append("-"*90)
        results.append(f"{'Rep':<6} {'Head':<10} {'Arms':<10} {'Body':<10} {'Legs':<10} {'Overall':<10} {'Issues':<30}")
        results.append("-"*90)
        
        for i, rep in enumerate(self.rep_data, 1):
            rep_avg = (rep['head_score'] + rep['arm_score'] + rep['body_score'] + rep['leg_score']) / 4
            issues = ", ".join(rep['issues'][:2]) if rep['issues'] else "None"
            results.append(
                f"{i:<6} {rep['head_score']:>5.0f}%{'':>3} {rep['arm_score']:>5.0f}%{'':>3} "
                f"{rep['body_score']:>5.0f}%{'':>3} {rep['leg_score']:>5.0f}%{'':>3} "
                f"{rep_avg:>5.0f}%{'':>3} {issues:<30}"
            )
            
        results.append("="*90)
        results.append("")
        
         # Specific feedback and recommendations
        results.append("-"*90)
        results.append("DETAILED FEEDBACK & RECOMMENDATIONS")
        results.append("-"*90)
        results.append("")
        
        # Collect all issues
        all_issues = []
        for rep in self.rep_data:
            all_issues.extend(rep['issues'])
        
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

        if avg_head < 80:
            results.append("🔴 HEAD/NECK POSTURE:")
            if "Head too far forward" in issue_counts:
                results.append("   • Keep head in neutral position aligned with spine")
                results.append("   • Look at floor 3-4 feet in front of you")
            if "Head dropped" in issue_counts:
                results.append("   • Don't let head drop down")
                results.append("   • Maintain cervical spine alignment")
            results.append("")
        
        if avg_arm < 80:
            results.append("🔴 ARM/ELBOW FORM:")
            if "Elbows flaring" in issue_counts:
                results.append("   • Keep elbows at 45° angle from body, not 90°")
                results.append("   • Imagine squeezing something in your armpits")
            if "Go lower" in issue_counts:
                results.append("   • Lower chest until elbows reach 90 degrees")
                results.append("   • Full range of motion is important")
            if "Too deep" in issue_counts:
                results.append("   • Control your descent - don't collapse")
                results.append("   • Stop when elbows reach 90 degrees")
            results.append("")
             
        if avg_body < 80:
            results.append("🔴 BODY/CORE ALIGNMENT:")
            if "Hips sagging" in issue_counts:
                results.append("   • CRITICAL: Engage your core throughout movement")
                results.append("   • Squeeze glutes and pull belly button to spine")
                results.append("   • Practice plank holds: 3 sets x 30-60 seconds")
            if "Hips too high" in issue_counts:
                results.append("   • Lower hips to create straight line from head to heels")
                results.append("   • Don't pike up into downward dog position")
            results.append("")
        
        if avg_leg < 80:
            results.append("🔴 LEG POSITION:")
            if "Knees bent" in issue_counts:
                results.append("   • Keep legs fully extended and locked")
                results.append("   • Squeeze quads to maintain tension")
            if "Keep feet grounded" in issue_counts:
                results.append("   • Keep toes firmly planted throughout")
                results.append("   • Don't lift feet or lose base of support")
            results.append("")
             # Overall grade and action plan
        results.append("-"*90)
        results.append("FINAL GRADE & ACTION PLAN")
        results.append("-"*90)
        results.append("")
        
        if avg_overall >= 90:
            results.append("⭐⭐⭐ EXCELLENT - Your form is outstanding!")
            results.append("Action: Try progressions like diamond pushups or tempo variations")
        elif avg_overall >= 75:
            results.append("⭐⭐ GOOD - Solid performance with room for refinement")
            results.append("Action: Focus on weak points identified above")
        elif avg_overall >= 60:
            results.append("⭐ FAIR - You need consistent practice")
            results.append("Action: Do 3 sets of 5 pushups daily, focusing on form")
        else:
            results.append("⚠ NEEDS SIGNIFICANT WORK")
            results.append("Action: Start with incline pushups and build strength")
            results.append("")
        results.append("="*90)
        results.append(" " * 30 + "Press ENTER to try again | Press Q to quit")
        results.append("="*90)
        
        return "\n".join(results)
    
    def analyze_pushup(self, image):
        """Analyze pushup form with live posture scores"""
        if self.feedback_mode:
            return self.show_results_table(image)
        
        feedback = "Position yourself in frame (side view)"
        form_issues = []
          elbow_angle = 0
        shoulder_angle = 0
        body_alignment = 0
        color = (255, 165, 0)
        
        # Reset live scores
        self.head_score = 0
        self.arm_score = 0
        self.body_score = 0
        self.leg_score = 0
        
        results = self.model(image, verbose=False)
        
        if results and len(results[0].keypoints) > 0:
            keypoints = results[0].keypoints.xy[0].cpu().numpy()
             if len(keypoints) >= 16:
                # Extract keypoints
                nose = keypoints[0]
                shoulder = keypoints[5]
                elbow = keypoints[7]
                wrist = keypoints[9]
                hip = keypoints[11]
                knee = keypoints[13]
                ankle = keypoints[15]
                
                if all(shoulder) and all(elbow) and all(wrist) and all(hip) and all(ankle):
                    
                    # Calculate angles
                    elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
                    shoulder_angle = self.calculate_angle(elbow, shoulder, hip)
                    body_alignment = self.calculate_body_alignment(shoulder, hip, ankle)
                    
                     # Analyze each body part
                    self.head_score, head_feedback = self.analyze_head_posture(nose, shoulder, hip)
                    self.arm_score, arm_feedback = self.analyze_arm_posture(shoulder, elbow, wrist, elbow_angle)
                    self.body_score, body_feedback = self.analyze_body_posture(shoulder, hip, knee, body_alignment)
                    self.leg_score, leg_feedback = self.analyze_leg_posture(hip, knee, ankle)
                    
                    # Collect issues
                    for fb in head_feedback + arm_feedback + body_feedback + leg_feedback:
                        if not fb.startswith("✓"):
                            form_issues.append(fb)
                    
                    # Overall form score
                    form_score = (self.head_score + self.arm_score + self.body_score + self.leg_score) / 4
                    
                    # Position tracking
                    if elbow_angle > 160:
                        position = "UP"
                        if self.position == "down":
                            # Count rep and store data
                            self.pushup_count += 1
                            
                            self.rep_data.append({
                                'rep_num': self.pushup_count,
                                'head_score': self.head_score,
                                'arm_score': self.arm_score,
                                'body_score': self.body_score,
                                'leg_score': self.leg_score,
                                'issues': self.current_rep_feedback.copy()
                                
                            })
                            
                            # Check if set complete
                            if self.pushup_count >= self.set_target:
                                self.feedback_mode = True
                            
                            self.position = "up"
                            self.current_rep_feedback = []
                        feedback = "Ready position"
                        color = (255, 255, 0)
                        
                    elif 70 <= elbow_angle <= 100:
                        position = "DOWN"
                        self.position = "down"
                        self.current_rep_feedback = form_issues.copy()
                        
                        if form_score >= 85:
                            feedback = "Perfect depth & form!"
                            color = (0, 255, 0)
                        else:
                            feedback = "Depth OK - Fix: " + (form_issues[0] if form_issues else "")
                            color = (0, 165, 255)
                            elif elbow_angle > 100:
                        position = "GOING DOWN"
                        feedback = "Go lower for full pushup"
                        color = (255, 200, 0)
                    else:
                        position = "TOO LOW"
                        feedback = "Too deep - Maintain control"
                        color = (0, 165, 255)
                    
                    # Render frame
                    annotated_frame = results[0].plot()
                    h, w = annotated_frame.shape[:2]
                    
                    # Top info panel
                    overlay = annotated_frame.copy()
                    cv2.rectangle(overlay, (0, 0), (w, 280), (0, 0, 0), -1)
                    cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0, annotated_frame)
                    
                    # Counter
                    cv2.putText(annotated_frame, f'PUSHUPS: {self.pushup_count}/{self.set_target}', 
                               (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 
                               1.3, (0, 255, 255), 3, cv2.LINE_AA)
                    # Live Posture Scores
                    y_pos = 95
                    cv2.putText(annotated_frame, "LIVE POSTURE SCORES:", 
                               (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.7, (200, 200, 200), 2, cv2.LINE_AA)
                    
                    y_pos += 35
                    
                    # Head score
                    head_color = (0, 255, 0) if self.head_score >= 80 else (0, 165, 255) if self.head_score >= 60 else (0, 0, 255)
                    cv2.putText(annotated_frame, f'Head/Neck: {int(self.head_score)}%', 
                               (30, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.65, head_color, 2, cv2.LINE_AA)
                    
                    y_pos += 30

                     # Arm score
                    arm_color = (0, 255, 0) if self.arm_score >= 80 else (0, 165, 255) if self.arm_score >= 60 else (0, 0, 255)
                    cv2.putText(annotated_frame, f'Arms/Elbows: {int(self.arm_score)}%', 
                               (30, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.65, arm_color, 2, cv2.LINE_AA)
                    
                    y_pos += 30
                    
                    # Body score
                    body_color = (0, 255, 0) if self.body_score >= 80 else (0, 165, 255) if self.body_score >= 60 else (0, 0, 255)
                    cv2.putText(annotated_frame, f'Body/Core: {int(self.body_score)}%', 
                               (30, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.65, body_color, 2, cv2.LINE_AA)
                    
                    y_pos += 30
                    # Leg score
                    leg_color = (0, 255, 0) if self.leg_score >= 80 else (0, 165, 255) if self.leg_score >= 60 else (0, 0, 255)
                    cv2.putText(annotated_frame, f'Legs/Stability: {int(self.leg_score)}%', 
                               (30, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.65, leg_color, 2, cv2.LINE_AA)
                    
                    # Overall score on right
                    score_color = (0, 255, 0) if form_score >= 80 else (0, 165, 255) if form_score >= 60 else (0, 0, 255)
                    cv2.putText(annotated_frame, f'Overall: {int(form_score)}%', 
                               (w - 250, 45), cv2.FONT_HERSHEY_SIMPLEX, 
                               1.0, score_color, 2, cv2.LINE_AA)
                    
                    # Current issues display
                    if form_issues:
                        issue_y = h - 140
                        cv2.rectangle(annotated_frame, (0, issue_y), (w, h-60), (40, 0, 0), -1)
                        cv2.putText(annotated_frame, "FORM CORRECTIONS:", 
                                   (20, issue_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 
                                   0.7, (255, 255, 255), 2, cv2.LINE_AA)
                         for i, issue in enumerate(form_issues[:2]):
                            cv2.putText(annotated_frame, f"• {issue}", 
                                       (30, issue_y + 65 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 
                                       0.6, (255, 150, 100), 1, cv2.LINE_AA)
                    
                    # Main feedback
                    cv2.rectangle(annotated_frame, (0, h-60), (w, h), (0, 0, 0), -1)
                    cv2.putText(annotated_frame, feedback, 
                               (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.85, color, 2, cv2.LINE_AA)
                    
                    return annotated_frame, feedback, elbow_angle, body_alignment
        
        return image, feedback, elbow_angle, body_alignment

def show_results_table(self, image):
        """Display results table"""
        h, w = image.shape[:2]
        results_screen = np.zeros((h, w, 3), dtype=np.uint8)
        
        results_text = self.generate_results_table()
        lines = results_text.split('\n')
        
        y_position = 15

 for line in lines:
            # Color coding
            if '=' in line:
                color, thickness, font_scale = (100, 100, 100), 1, 0.45
            elif 'DETAILED RESULTS' in line or 'SUMMARY' in line or 'BREAKDOWN' in line:
                color, thickness, font_scale = (0, 255, 255), 2, 0.55
            elif '✓ EXCELLENT' in line or '⭐⭐⭐' in line:
                color, thickness, font_scale = (0, 255, 0), 1, 0.5
            elif '✓ GOOD' in line or '⭐⭐' in line:
                color, thickness, font_scale = (100, 255, 100), 1, 0.5
            elif '⚠' in line or '⭐' in line or 'FAIR' in line:
                color, thickness, font_scale = (0, 165, 255), 1, 0.5
            elif '✗' in line or 'POOR' in line or '🔴' in line:
                color, thickness, font_scale = (0, 0, 255), 1, 0.5
            elif line.startswith('   •') or line.startswith('      '):
                color, thickness, font_scale = (180, 180, 180), 1, 0.43
            elif '-' in line:
                color, thickness, font_scale = (80, 80, 80), 1, 0.42
            else:
                color, thickness, font_scale = (255, 255, 255), 1, 0.48

             cv2.putText(results_screen, line, 
                       (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, 
                       font_scale, color, thickness, cv2.LINE_AA)
            y_position += 19
            
            if y_position > h - 20:
                break
        
        return results_screen, "Results Table", 0, 0

 def reset_counter(self):
        """Reset for new set"""
        self.pushup_count = 0
        self.position = "up"
        self.rep_data = []
        self.current_rep_feedback = []
        self.analyzing = True
        self.feedback_mode = False
 
