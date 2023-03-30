from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/token', methods=['GET', 'POST'])
def redeem_token():
    if request.method == 'POST':
        print(f"Token: {request.form['token']}")
        print(f"Password: {request.form['password']}")

    return render_template('index.html')

if __name__ == "__main__":
    app.run()
