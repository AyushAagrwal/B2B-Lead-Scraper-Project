import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import os
from datetime import datetime

class EmailService:
    """
    Email service that works with local SMTP (MailHog) for testing
    or production SMTP services (SendGrid, Mailgun, etc.)
    """
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        self.from_email = os.getenv("FROM_EMAIL", "demo@leadscaper.local")
        
    def send_email(self, to_email: str, subject: str, html_body: str) -> dict:
        """Send a single email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            # Attach HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                # For production SMTP (SendGrid, Mailgun)
                if self.smtp_user and self.smtp_pass:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_pass)
                
                server.send_message(msg)
            
            return {
                "status": "sent",
                "to": to_email,
                "subject": subject,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "to": to_email,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def send_campaign(self, recipients: List[dict], template: str) -> dict:
        """Send emails to multiple recipients"""
        results = {
            "total": len(recipients),
            "sent": 0,
            "failed": 0,
            "details": []
        }
        
        for recipient in recipients:
            # Get email template
            html_body = self.get_template(template, recipient)
            subject = self.get_subject(template, recipient)
            
            # Send email
            result = self.send_email(
                to_email=recipient.get("email"),
                subject=subject,
                html_body=html_body
            )
            
            if result["status"] == "sent":
                results["sent"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append(result)
        
        return results
    
    def get_template(self, template_type: str, lead: dict) -> str:
        """Get HTML email template"""
        templates = {
            "intro": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #6366f1;">Hello {lead.get('owner_name', 'there')}!</h2>
                    <p>I noticed your business, <strong>{lead.get('business_name')}</strong>, and wanted to reach out.</p>
                    <p>We specialize in providing cutting-edge solutions for roofing contractors like yourself.</p>
                    <p>Would you be interested in a quick 15-minute call to discuss how we can help grow your business?</p>
                    <br>
                    <p>Best regards,<br>Your Name<br>Company Name</p>
                    <hr style="border: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 12px; color: #888;">
                        You received this email because your business is listed on Google Maps.
                        <a href="#">Unsubscribe</a>
                    </p>
                </body>
                </html>
            """,
            "partnership": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #6366f1;">Partnership Opportunity for {lead.get('business_name')}</h2>
                    <p>Hi {lead.get('owner_name')},</p>
                    <p>We're looking for top-rated roofing contractors to partner with in {lead.get('city')}, {lead.get('state')}.</p>
                    <p>Your {lead.get('rating', 5.0)}⭐ rating caught our attention!</p>
                    <p><strong>What we offer:</strong></p>
                    <ul>
                        <li>Exclusive lead generation</li>
                        <li>Marketing support</li>
                        <li>Technology solutions</li>
                    </ul>
                    <p>Interested? Let's schedule a call.</p>
                    <br>
                    <p>Best regards,<br>Partnership Team</p>
                </body>
                </html>
            """,
            "demo": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #6366f1;">Free Demo for {lead.get('business_name')}</h2>
                    <p>Hi {lead.get('owner_name')},</p>
                    <p>We have a powerful tool that's helping roofing contractors increase efficiency by 40%.</p>
                    <p>I'd love to show you a quick demo - no commitment required.</p>
                    <p><a href="#" style="background: #6366f1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Book Your Demo</a></p>
                    <br>
                    <p>Looking forward to connecting,<br>Sales Team</p>
                </body>
                </html>
            """,
            "followup": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #6366f1;">Following Up</h2>
                    <p>Hi {lead.get('owner_name')},</p>
                    <p>I wanted to follow up on my previous message about helping {lead.get('business_name')} grow.</p>
                    <p>Quick question: What's your biggest challenge right now in growing your roofing business?</p>
                    <p>Happy to share some insights that might help.</p>
                    <br>
                    <p>Best,<br>Your Name</p>
                </body>
                </html>
            """
        }
        
        return templates.get(template_type, templates["intro"])
    
    def get_subject(self, template_type: str, lead: dict) -> str:
        """Get email subject line"""
        subjects = {
            "intro": f"Quick question about {lead.get('business_name')}",
            "partnership": f"Partnership opportunity in {lead.get('city')}",
            "demo": "Free demo - 40% efficiency boost for your roofing business",
            "followup": "Following up on our conversation"
        }
        return subjects.get(template_type, "Reaching out")


# For testing
if __name__ == "__main__":
    service = EmailService()
    
    test_lead = {
        "business_name": "Elite Roofing Solutions",
        "owner_name": "John Smith",
        "email": "test@example.com",
        "city": "Houston",
        "state": "TX",
        "rating": 4.8
    }
    
    result = service.send_email(
        to_email="test@example.com",
        subject="Test Email",
        html_body=service.get_template("intro", test_lead)
    )
    
    print(result)
