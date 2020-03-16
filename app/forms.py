import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, widgets
from wtforms.fields import SelectMultipleField
from wtforms.validators import Length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Qcform(FlaskForm):
    editor_name = StringField('Editor Name', default=os.getenv('username'))
    producer_name = StringField('Producer Name', validators=[Length(min=0, max=140)])
    program_name = StringField('Program Name', validators=[Length(min=0, max=140)])
    source_id = StringField('Source ID')
    exported_id = StringField('Exported ID')
    cameras = SelectMultipleField('Camera Quality (Check all that apply)',
                                  coerce=int,
                                  option_widget=widgets.CheckboxInput(),
                                  widget=widgets.ListWidget(prefix_label=False))

    sounds = SelectMultipleField('Sound Quality (Check all that apply)',
                                 coerce=int,
                                 option_widget=widgets.CheckboxInput(),
                                 widget=widgets.ListWidget(prefix_label=False))

    comments = TextAreaField('Comments')
    submit = SubmitField('Send >>')
