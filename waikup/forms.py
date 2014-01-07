# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import url


class NewLinkForm(Form):
    url = URLField(validators=[url()])
    title = TextField()
    description = TextAreaField()
