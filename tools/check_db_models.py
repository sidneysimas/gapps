import sys
import os
from sqlalchemy import exc
from flask_sqlalchemy import inspect

# improve this hack
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def should_we_create_models():
    """
    checks if the tables are defined in the database
    and if we should create the models
    will return 3 possible values: Yes, No, Error
    """
    with app.app_context():
        try:
            inspector = inspect(db.engine)

            # tables have not been created
            if not inspector.get_table_names():
                return "Yes"
            return "No"
        except exc.SQLAlchemyError as e:
            print(f"[ERROR] Traceback while querying db model: {e}")
            return "Error"
    return "Error"

print(f"[INFO] Checking if we should create the models")
result = should_we_create_models()
if result == "Yes":
    print(f"[WARNING] Unable to query the database models. They need to be created.")
    exit(1)
elif result == "No":
    print(f"[INFO] Successfully queried the database models")
exit(0)
