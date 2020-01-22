from pancake.app import create_app
from pancake.config import Config

application = create_app(Config())

if __name__ == '__main__':
    application.run(port=5000)
