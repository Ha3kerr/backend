from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
import base64
import hashlib

app = Flask(__name__)
CORS(app)  # Allow React frontend to connect

# Track submitted applications to prevent duplicates
submitted_applications = set()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "alexandervoss43@gmail.com"
EMAIL_PASSWORD = "raha essk rjlg srsq"  # Your app password

@app.route('/api/send-application', methods=['POST'])
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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Backend is running!'})

# For Vercel
if __name__ == '__main__':
    app.run(debug=True, port=5000)

