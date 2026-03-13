from flask import Flask
import os

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #load configuration
    with app.app_context():
        pass

    from .config import Config
    app.config.from_object(Config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
 
    #initialize the database
    with app.app_context():
        from app.database import Database
        Database.init_db()

    #import bluePrint
    from .blueprints.auth import auth
    from .blueprints.manager import prof
    import app.blueprints.manager.routes as manager_route 
    import app.blueprints.professor.routes as prof_route 
    import app.blueprints.student.routes as student_route 

    app.register_blueprint(auth.bp)
    app.register_blueprint(prof.bp)
    app.register_blueprint(manager_route.bp)
    app.register_blueprint(prof_route.bp)
    app.register_blueprint(student_route.bp)

    return app
