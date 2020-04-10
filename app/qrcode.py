import qrcode

from sqlalchemy.orm import class_mapper

# import os
from app.models import QCformdb

# user = os.getenv('username')


def asdict(obj):
    return dict((col.name, getattr(obj, col.name))
                for col in class_mapper(obj.__class__).mapped_table.c)

def makeqr():
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

    id = 'ID: {} '.format(qid)
    t = 'TIME: {} '.format(timestamp)
    e = 'EDITOR: {}: '.format(editor_name)
    p = 'PRODUCER: {} '.format(producer_name)
    pm = 'PROGRAM: {} '.format(program_name)
    sid = 'SOURCE IDs: {} '.format(exported_id)
    ex = 'EXPORTED ID: {} '.format(source_id)
    co = 'COMMENTS: {}'.format(comments)

    c = 'CAMERA QUALITY CONTROL: {} '.format(camera)
    s = 'SOUND QUALITY CONTROL: {}'.format(sound)

    subject_user = '{} sent a new Quality Form: '.format(editor_name)

    data = 'MATMSG: \
            TO:post.booking@alrayyan.tv; \
            SUB:{}; \
            BODY:{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{};;' \
            .format(subject_user, id, t, e, p, pm, sid, ex, co, c, s)


    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_name = 'mysite/app/static/img/qr_{}.png'.format(qid)
    img.save(qr_name)
    return qr_name




