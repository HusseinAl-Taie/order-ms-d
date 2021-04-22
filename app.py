from flask import Flask

app = Flask(__name__)


@app.route('/')
def health():
    return 'root from app.py flask - orderMS-01'


if __name__ == '__main__':
    app.run()
