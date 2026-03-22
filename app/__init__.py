from flask import Flask
import os
from pathlib import Path

def create_app(): 
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #load configuration
    app.config.from_pyfile("config.py", silent=True)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    # default DB lives in instance/ unless DATABASE_URL is explicitly set
    if "DATABASE_URL" not in os.environ:
        db_path = Path(app.instance_path) / "database.db"
        app.config["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"
 
    #initialize the database
    with app.app_context():
        from app.database import Database
        Database.init_db()

    #import bluePrint
    from .blueprints.auth import auth
    import app.blueprints.manager.routes as manager_route 
    import app.blueprints.professor.routes as prof_route 
    import app.blueprints.student.routes as student_route 

    app.register_blueprint(auth.bp)
    app.register_blueprint(manager_route.bp)
    app.register_blueprint(prof_route.bp)
    app.register_blueprint(student_route.bp)

    return app
