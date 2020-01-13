from flask import Flask, render_template, jsonify, send_file, redirect
from datetime import date, timedelta
from io import BytesIO
import pdfmd as p
import apod
import os

app = Flask(__name__)


@app.route('/')
@app.route('/today')
def root():
    data = apod.get_apod(date.today())
    while data is None:
        data = apod.get_apod(date.today() - timedelta(1))
    return render_template('main.html',
                           title=data['title'],
                           img_url=data['image_url'],
                           credits=data['credits'],
                           summary=data['summary'])


@app.route('/api/pdf/today')
@app.route('/pdf/today')
@app.route('/pdf/')
def root_pdf():
    data = apod.get_apod(date.today())
    while data is None:
        data = apod.get_apod(date.today() - timedelta(1))
    file = p.pdf(data)
    file_data = BytesIO()
    with open(file, 'rb') as f:
        file_data.write(f.read())
    file_data.seek(0)
    os.remove(file)
    return send_file(file_data, mimetype='application/pdf')


@app.route('/<year>/<month>/<day>')
def image(year, month, day):
    try:
        d = date(int(year), int(month), int(day))
    except ValueError:
        return render_template('invalid.html', date=f'{year}-{month}-{day}'), 404
    data = apod.get_apod(d)
    if data is None:
        if d > date.today():
            return render_template('future.html', date=str(d)), 404
        elif d < date(1995, 6, 20):
            return render_template('past.html'), 404
        else:
            return render_template('dunno.html'), 404
    return render_template('image.html',
                           title=data['title'],
                           img_url=data['image_url'],
                           credits=data['credits'],
                           summary=data['summary'],
                           date=data['date'])


@app.route('/pdf/<year>/<month>/<day>')
def pdf(year, month, day):
    try:
        d = date(int(year), int(month), int(day))
    except ValueError:
        return render_template('invalid.html', date=f'{year}-{month}-{day}'), 404
    data = apod.get_apod(d)
    if data is None:
        if d > date.today():
            return render_template('future.html', date=str(d)), 404
        elif d < date(1995, 6, 20):
            return render_template('past.html'), 404
        else:
            return render_template('dunno.html'), 404
    return redirect(f'/api/pdf/{year}/{month}/{day}')


@app.route('/api/pdf/<year>/<month>/<day>')
def api_pdf(year, month, day):
    try:
        d = date(int(year), int(month), int(day))
    except ValueError:
        return jsonify({'status': 'INVALID DATE'})
    data = apod.get_apod(d)
    if data is None:
        return jsonify({'status': 'APOD NOT FOUND'})
    file = p.pdf(data)
    file_data = BytesIO()
    with open(file, 'rb') as f:
        file_data.write(f.read())
    file_data.seek(0)
    os.remove(file)
    return send_file(file_data, mimetype='application/pdf')


@app.route('/api/<year>/<month>/<day>')
def api(year, month, day):
    try:
        d = date(int(year), int(month), int(day))
    except ValueError:
        return jsonify({'status': 'INVALID DATE'})
    data = apod.get_apod(d)
    if data is None:
        return jsonify({'status': 'APOD NOT FOUND'})
    data.update({'status': 'ok'})
    return jsonify(data)


@app.errorhandler(404)
def four04(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
