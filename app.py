from app import create_app

# It fetches create_app from __init__.py
app = create_app()

# SSL certificate paths
context = (
    '/etc/ssl/certs/selfsigned-cert.pem',  
    '/etc/ssl/private/selfsigned-key.pem'
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=context)
