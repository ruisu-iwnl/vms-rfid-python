from flask import Flask, render_template

app = Flask(__name__)

context = (
    '/etc/ssl/certs/selfsigned-cert.pem',  # Full certificate (public)
    '/etc/ssl/private/selfsigned-key.pem'  # Private key
)

@app.route('/test')
def test_route():
    return render_template('test.html')  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=context)
