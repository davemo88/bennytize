


from flask import render_template, flash, redirect, session, url_for, request, jsonify, g

import requests

from bennytize import app, utils
from bennytize.forms import BennyForm

@app.route('/', methods=['GET', 'POST'])
def index():

    form = BennyForm()

    if form.validate_on_submit():

        bennylink = utils.get_bennylink(form.youtube_url.data)

        return render_template('index.jinja2',
                               form=form,
                               msg=bennylink)

    elif form.errors:

        return render_template('index.jinja2',
                               form=form,
                               msg=form.errors['youtube_url'][0])

    return render_template('index.jinja2',
                           form=form,
                           msg=None)


@app.route('/<string:video_id>')
def bennytized(video_id):

    source = utils.bennytize(video_id)

    return source

