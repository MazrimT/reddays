from app.main import app

if __name__ == '__main__':
    app.run(debug=True, port=80)
    app.config['TEMPLATES_AUTO_RELOAD'] = True