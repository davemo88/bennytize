


from flask import render_template, flash, redirect, session, url_for, request, jsonify, g

import requests

from bennytize import app, utils
from bennytize.forms import BennyForm

@app.route('/', methods=['GET', 'POST'])
def index():

    form = BennyForm()

    if form.validate_on_submit():

        requests.get(form.youtube_url.data)

        bennylink = utils.get_bennylink()

        return redirect(url_for('bennylink', bennylink=bennylink))

    elif form.errors:

        msg = form.errors[0]

    return render_template('index.jinja2',
                           form=form)

@app.route('/', methods=['POST'])
def bennylink():
    pass

@app.route('/<string:video_id>')
def bennytized(video_id):
    print video_id

    source = utils.bennytize(video_id)

    return source

