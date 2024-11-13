import os
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'app', 'templates'))

@app.route('/test')
def test_route():
    return render_template('test.html')

if __name__ == '__main__':
    context = (
        '/etc/ssl/certs/selfsigned-cert.pem',
        '/etc/ssl/private/selfsigned-key.pem'
    )
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=context)
