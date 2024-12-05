import os
from flask_socketio import SocketIO, emit
from app import create_app  

app = create_app()  

#kept this, so i can add real-time notifications in the future?
socketio = SocketIO(app)  

if __name__ == '__main__':
    linux_cert_path = '/etc/ssl/certs/selfsigned-cert.pem'
    linux_key_path = '/etc/ssl/private/selfsigned-key.pem'
    windows_cert_path = r'C:\certs\selfsigned-cert.pem'
    windows_key_path = r'C:\certs\selfsigned-key.pem'

    cert_path = windows_cert_path if os.name == 'nt' else linux_cert_path
    key_path = windows_key_path if os.name == 'nt' else linux_key_path

    context = (cert_path, key_path)

    socketio.run(app, debug=True, host='0.0.0.0', port=8443, ssl_context=context)
