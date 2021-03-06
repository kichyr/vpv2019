from flask import Flask
from flask import render_template
from flask import request
from function_resolver import string2func1D
from schorodinger_eq1D import SchorodingerSolver1D



app = Flask(__name__)
front_host = "127.0.0.1:5000"

def potential_pit(x):
    """U(x,y,z) potential"""
    if  x**2 <= 400:
        return 0
    else:
        return 100

@app.route('/calculate1D',  methods=['GET'])
def hello_world():
    func = request.args.get('potential')
    d = request.args.get('d')
    ss = SchorodingerSolver1D()
    potential = string2func1D(func)
    ss.generateMatrix(string2func1D(func), float(d))
    return ss.get_output_data()

@app.route('/')
def main_page():
    return render_template("front.html", host=front_host)

if __name__ == '__main__':
    app.run(port=5000)
