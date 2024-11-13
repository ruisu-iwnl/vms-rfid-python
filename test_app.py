import os
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'app', 'templates'))

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

@app.route('/test')
def test_route():
    return render_template('test.html')

if __name__ == '__main__':
    context = (cert_path, key_path)
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=context)
