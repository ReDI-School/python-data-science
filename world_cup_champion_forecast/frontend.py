from flask import Flask, render_template
from flask import request
values1 = [{'value':i, 'selected': False}  for i in range(0, 20)]
values2 = [{'value':i, 'selected': False}  for i in range(0, 20)]

app = Flask(__name__)

@app.route("/")
def template_test():
    global values1
    global values2
    value1 = request.args.get('value1', default = 1, type = int)
    value2 = request.args.get('value2', default = 2, type = int)
    result = calculate(value1, value2)
    values1 = update_values(values1, value1)
    values2 = update_values(values2, value2)
    return render_template(
        'template.html', value1=value1, value2=value2, values1=values1, values2=values2, 
        result=result)

def update_values(values, value):
    return [{'value':val['value'], 'selected': val['value'] == value} for val in values]


def calculate(val1, val2):
    return val1 + val2

if __name__ == '__main__':
    app.run(debug=True)