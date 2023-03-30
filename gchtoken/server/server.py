from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/token', methods=['GET', 'POST']):
    if request.method == 'POST':
        print('POST')

    return render_template('index.html')
