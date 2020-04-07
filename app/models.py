# User database model

from app import db

cameras = db.Table('cameras',
                   db.Column('camera_id', db.Integer, db.ForeignKey('camera.id'), primary_key=True),
                   db.Column('qcformdb_id', db.Integer, db.ForeignKey('qcformdb.id'), primary_key=True)
                   )
sounds = db.Table('sounds',
                  db.Column('sound_id', db.Integer, db.ForeignKey('sound.id'), primary_key=True),
                  db.Column('qcformdb_id', db.Integer, db.ForeignKey('qcformdb.id'), primary_key=True)
                  )

class QCformdb(db.Model):
    """QCForm_db"""
    __tablename__ = 'qcformdb'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    editor_name = db.Column(db.String(64), index=True, unique=False)
    producer_name = db.Column(db.String(64), index=True, unique=False)
    program_name = db.Column(db.String(64), index=True, unique=False)
    source_id = db.Column(db.String(120), index=True, unique=False)
    exported_id = db.Column(db.String(120), index=True, unique=False)
    cameras = db.relationship('Camera',
                              secondary=cameras, lazy='subquery',
                              backref=db.backref("qcformdbs", lazy=True))
    sounds = db.relationship('Sound',
                             secondary=sounds, lazy='subquery',
                             backref=db.backref("qcformdbs", lazy=True))
    comments = db.Column(db.String(512), index=True, unique=False)

    def __repr__(self):
        return '[ || <QCForm> ' \
               '{}, {}, {}, {}, {}, {}, {}, {}|| ]'.format(self.id,
                                                           self.timestamp, self.editor_name,
                                                           self.producer_name, self.program_name,
                                                           self.exported_id, self.source_id,
                                                           self.cameras, self.sounds,
                                                           self.comments)

class Camera(db.Model):
    """Camera"""
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(64))

    def __repr__(self):
        return '{}'.format(self.camera_name)


class Sound(db.Model):
    """Sound"""
    __tablename__ = 'sound'
    id = db.Column(db.Integer, primary_key=True)
    sound_name = db.Column(db.String(64))

    def __repr__(self):
        return '{}'.format(self.sound_name)
