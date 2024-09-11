from app import create_app

#It fetches create_app from __init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  