from flask_mail import Message

from threading import Thread
import os

from sqlalchemy.orm import class_mapper

from app import app, mail
from app.models import QCformdb


def asdict(obj):
    return dict((col.name, getattr(obj, col.name))
                for col in class_mapper(obj.__class__).mapped_table.c)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    Thread(target=send_async_email, args=(app, msg)).start()


def send_records_email():
    user = os.getenv('username')
    u_mail = user + "@postproduction.team"

    # Query last record received
    records = QCformdb.query.order_by(QCformdb.id.desc()).first()
    rec = asdict(records)
    camera = records.cameras
    sound = records.sounds

    # Assignament of data
    id = rec['id']
    timestamp = rec['timestamp']
    editor_name = rec['editor_name'],
    producer_name = rec['producer_name'],
    program_name = rec['program_name'],
    source_id = rec['source_id'],
    exported_id = rec['exported_id'],
    comments = rec['comments']

    # Format email delivery
    email_comp = 'A new Quality Form has been received: ' \
                 'ID: {} ' \
                 'TIME: {} ' \
                 'EDITOR: {} ' \
                 'PRODUCER: {} ' \
                 'PROGRAM: {} ' \
                 'SOURCE IDs: {} ' \
                 'EXPORTED ID: {} ' \
                 'COMMENTS: {}. ' \
        .format(id, timestamp, editor_name, producer_name, program_name,
                exported_id, source_id, comments)
    details = 'CAMERA QUALITY CONTROL: {} ' \
              'SOUND QUALITY CONTROL: {}' \
        .format(camera, sound)

    send_email('A new [QCForm] has been received',
               sender=app.config['ADMINS'][0],
               recipients=[u_mail],
               text_body=email_comp + details,
               html_body=email_comp + details)
    return print("Mail sent")
