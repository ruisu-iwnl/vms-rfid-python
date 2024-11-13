import os
from app import create_app

app = create_app()

linux_cert_path = '/etc/ssl/certs/selfsigned-cert.pem'
linux_key_path = '/etc/ssl/private/selfsigned-key.pem'

windows_cert_path = r'C:\certs\selfsigned-cert.pem'
windows_key_path = r'C:\certs\selfsigned-key.pem'

if os.name == 'nt':  
    cert_path = windows_cert_path
    key_path = windows_key_path
else: 
    cert_path = linux_cert_path
    key_path = linux_key_path

context = (cert_path, key_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=context)
