from app import app, db
from app.models import QCformdb, Camera, Sound

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'QCformdb': QCformdb, 'Camera': Camera, 'Sound': Sound}