

from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ifuhackmegoodjob'
app.config['BITLY_API_TOKEN'] = '4108de02178b34ed1c1f0fc207c020dc06b8aeed'

import views