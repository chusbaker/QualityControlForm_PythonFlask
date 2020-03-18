from flask import render_template
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

def send_records_email():
    user = os.getenv('username')
    u_mail = user + "@postproduction.team"

    # Query last record received
    records = QCformdb.query.order_by(QCformdb.id.desc()).first()
    rec = asdict(records)
    camera = records.cameras
    sound = records.sounds

    # Assignament of data
    qid = rec['id']
    timestamp = rec['timestamp']
    editor_name = rec['editor_name'],
    producer_name = rec['producer_name'],
    program_name = rec['program_name'],
    source_id = rec['source_id'],
    exported_id = rec['exported_id'],
    comments = rec['comments']

    # Format email delivery
    email_comp = '{} sent a new Quality Form: ' \
                 'ID: {} ' \
                 'TIME: {} ' \
                 'EDITOR: {} ' \
                 'PRODUCER: {} ' \
                 'PROGRAM: {} ' \
                 'SOURCE IDs: {} ' \
                 'EXPORTED ID: {} ' \
                 'COMMENTS: {}. ' \
        .format(user, qid, timestamp, editor_name, producer_name, program_name,
                exported_id, source_id, comments)
    details = 'CAMERA QUALITY CONTROL: {} ' \
              'SOUND QUALITY CONTROL: {}' \
        .format(camera, sound)

    subject_user = user + ' sent a new QCForm'

    msg = Message(subject=subject_user, sender=app.config['ADMINS'][0], recipients=[u_mail])
    msg.body = email_comp + details
    msg.html = render_template('QCFormDelivery.html', user=user,
                               qid=qid, timestamp=timestamp, editor_name=editor_name,
                               producer_name=producer_name, program_name=program_name,
                               exported_id=exported_id, source_id=source_id,
                               camera=camera, sound=sound, comments=comments)

    Thread(target=send_async_email, args=(app, msg)).start()

    return print("Mail sent")
