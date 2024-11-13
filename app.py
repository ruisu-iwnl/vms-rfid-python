from app import create_app

app = create_app()

# SSL certificate paths
context = (
    '/etc/ssl/certs/selfsigned-cert.pem',  # Full certificate (public)
    '/etc/ssl/private/selfsigned-key.pem'   # Private key
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=context)
