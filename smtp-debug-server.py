"""
Simple email logger that prints emails to console
Works without any external dependencies - uses only Python standard library
"""
import socket
import threading
from email import message_from_bytes
from email.policy import default
from datetime import datetime

class SimpleEmailLogger:
    def __init__(self, host='localhost', port=1025):
        self.host = host
        self.port = port
        self.running = False
        
    def handle_client(self, client_socket, address):
        """Handle individual email connection"""
        try:
            # Send SMTP greeting
            client_socket.send(b"220 localhost SMTP\r\n")
            
            data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                    
                data += chunk
                lines = data.decode('utf-8', errors='ignore').split('\r\n')
                
                for line in lines[:-1]:
                    if line.upper().startswith('HELO') or line.upper().startswith('EHLO'):
                        client_socket.send(b"250 Hello\r\n")
                    elif line.upper().startswith('MAIL FROM:'):
                        self.mail_from = line.split(':', 1)[1].strip()
                        client_socket.send(b"250 OK\r\n")
                    elif line.upper().startswith('RCPT TO:'):
                        self.rcpt_to = line.split(':', 1)[1].strip()
                        client_socket.send(b"250 OK\r\n")
                    elif line.upper().startswith('DATA'):
                        client_socket.send(b"354 Send message, end with CRLF.CRLF\r\n")
                    elif line == '.':
                        # Email received
                        self.print_email(data)
                        client_socket.send(b"250 OK\r\n")
                    elif line.upper().startswith('QUIT'):
                        client_socket.send(b"221 Bye\r\n")
                        break
                
                data = lines[-1].encode()
                
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def print_email(self, raw_data):
        """Print email details"""
        print("\n" + "="*80)
        print(f"📧 EMAIL RECEIVED - {datetime.now().strftime('%H:%M:%S')}")
        print("="*80)
        print(f"From: {getattr(self, 'mail_from', 'Unknown')}")
        print(f"To: {getattr(self, 'rcpt_to', 'Unknown')}")
        print("-"*80)
        
        # Extract subject from raw data
        data_str = raw_data.decode('utf-8', errors='ignore')
        for line in data_str.split('\n'):
            if line.lower().startswith('subject:'):
                print(line.strip())
            if '<strong>' in line and '</strong>' in line:
                # Extract business name from email content
                try:
                    business = line.split('<strong>')[1].split('</strong>')[0]
                    print(f"Business: {business}")
                except:
                    pass
        
        print("="*80)
        print("✅ Email logged successfully!\n")
    
    def start(self):
        """Start the SMTP server"""
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            print("🚀 Simple SMTP Email Logger")
            print("="*80)
            print(f"📧 Listening on {self.host}:{self.port}")
            print("💡 All emails will be printed below")
            print("🔧 Press Ctrl+C to stop")
            print("="*80)
            print("\n✅ Ready! Waiting for emails...\n")
            
            while self.running:
                try:
                    server_socket.settimeout(1.0)
                    client_socket, address = server_socket.accept()
                    
                    # Handle in separate thread
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    thread.daemon = True
                    thread.start()
                    
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
                    
        except OSError as e:
            if 'address already in use' in str(e).lower():
                print(f"❌ Error: Port {self.port} is already in use!")
                print("   Try a different port or close the other program.")
            else:
                print(f"❌ Error: {e}")
        finally:
            self.running = False
            server_socket.close()
            print("\n\n👋 SMTP server stopped")

if __name__ == "__main__":
    logger = SimpleEmailLogger()
    try:
        logger.start()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
