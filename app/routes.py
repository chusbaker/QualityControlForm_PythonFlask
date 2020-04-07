import os

from flask import render_template, flash, request, redirect, url_for

from app import app, db
from app.emails import send_records_email
from app.forms import Qcform
from app.models import QCformdb, Camera, Sound
from datetime import datetime, timedelta


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Qcform()

    camera_query = Camera.query.all()
    sound_query = Sound.query.all()

    form.cameras.choices = [(c.id, c.camera_name) for c in camera_query]
    form.sounds.choices = [(s.id, s.sound_name) for s in sound_query]

    if request.method == 'POST':
        ## Convert time now to local time now
        record = QCformdb(timestamp=datetime.utcnow() + timedelta(hours=+3),
                          editor_name=form.editor_name.data,
                          producer_name=form.producer_name.data,
                          program_name=form.program_name.data,
                          source_id=form.source_id.data,
                          exported_id=form.exported_id.data,
                          comments=form.comments.data)

        db.session.add(record)

        cs = form.cameras.data
        ss = form.sounds.data

        for c in cs:
            cam = Camera.query.filter_by(id=c).one_or_none()
            record.cameras.append(cam)
        for s in ss:
            sou = Sound.query.filter_by(id=s).one_or_none()
            record.sounds.append(sou)

        db.session.commit()

        flash('Your Quality Control Report has been sent!', 'done')
        send_records_email()
        return redirect('index')
    else:

        return render_template('index.html', form=form)


@app.route('/records')
def records():
    u = os.getenv('username')
    page = request.args.get('page', 1, type=int)
    records_list = QCformdb.query.order_by(QCformdb.id.asc()).paginate(
        page, app.config['RECORDS_PER_PAGE'], False)

    next_url = url_for('records', page=records_list.next_num)\
        if records_list.has_next else None
    prev_url = url_for('records', page=records_list.prev_num)\
        if records_list.has_prev else None

    return render_template('records.html', title='Records', user=u,
                           records_list=records_list.items,
                           next_url=next_url, prev_url=prev_url)
def data():
    rec = QCformdb.query.order_by(QCformdb.id.asc()).one_or_none()
    print(rec)

    return rec
