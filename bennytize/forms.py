"""

"""

from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

class BennyForm(Form):
    """

    """

    youtube_url = StringField('YouTubeURL', 
        validators = [
            DataRequired(message='You gotta gimme a link, pal!'),
            Regexp('(https://)?www\.youtube\.com/watch\?v=[a-zA-Z0-9_]+',
                   message='That ain\'t no YouTube link! Try again!')
        ]
    )