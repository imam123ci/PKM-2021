import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        # choose between production or development config
        if app.config["ENV"] == "production":
            app.config.from_object("config.ProductionConfig")
        else:
            app.config.from_object("config.DevelopmentConfig")

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # import other file

    # import db file
    from . import db
    db.init_app(app)

    # import mongodb model file
    from . import mongodb
    mongodb.init_app(app)

    # import crawler file
    from .controller import crawler
    crawler.init_app(app)

    # import clasifier file
    from .controller import classifier
    classifier.init_app(app)

    #from .controller import classifier
    #classifier.init_app(app)

    # IMPORT BLUEPRINT #

    # import blueprint auth
    from . import auth
    app.register_blueprint(auth.bp)

    # import blueprint api 
    from . import apis
    app.register_blueprint(apis.bp)

    # import blueprint frontend
    from . import fe
    app.register_blueprint(fe.bp)
    

    return app