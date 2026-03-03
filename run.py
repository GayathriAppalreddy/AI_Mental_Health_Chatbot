from app import create_app

app = create_app()

if __name__ == '__main__':
    # setting debug to True for development, set to False in production
    app.run(debug=True)
