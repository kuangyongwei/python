from apps import create_api_app
from flask_script import Manager

app = create_api_app()
manager = Manager(app)

if __name__ == '__main__':
    print(app.url_map)
    manager.run()
