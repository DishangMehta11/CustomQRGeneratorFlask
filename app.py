import os
from flask import Flask, render_template, request, url_for, redirect

import qrcode

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=["POST"])
def create():
    dataValue = request.form.get('dataValue')
    errorValue = request.form['errorValue']
    boxsizeValue = request.form['boxsizeValue']
    borderValue = request.form['borderValue']
    qrcolorValue = request.form['qrcolorValue']
    bgcolorValue = request.form['bgcolorValue']

    def rgb_to_hex(color):
        if color.__contains__('(') and color.__contains__(')'):
            colorArray = color.lstrip('(').rstrip(')').split(',')
            hexColor = '#{:02x}{:02x}{:02x}'.format(int(colorArray[0]), int(colorArray[1]), int(colorArray[2]))
            return hexColor
        else:
            return color

    qr = qrcode.QRCode(version=1, error_correction=errorValue, box_size=boxsizeValue, border=borderValue)
    qr.add_data(dataValue)
    qr.make(fit=True)

    qrHex = rgb_to_hex(qrcolorValue)
    bgHex = rgb_to_hex(bgcolorValue)

    img = qr.make_image(fill_color=qrHex, back_color=bgHex)
    img.save("./static/qrcode.png")
    return redirect(url_for('qrpng'))


@app.route('/qrpng')
def qrpng():
    path = os.path.join(os.path.dirname(__file__), 'static', 'qrcode.png')
    return render_template('create.html', filename=path)


if __name__ == '__main__':
    app.run(debug=True)
