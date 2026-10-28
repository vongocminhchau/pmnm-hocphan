from flask import Flask, render_template, request

app = Flask(__name__)


def parse_number(val):
    """Hàm bổ trợ thay dấu phẩy thập phân và ép kiểu float."""
    if not val:
        return None, "Vui lòng nhập một số."

    try:
        return float(val.strip().replace(',', '.')), None
    except ValueError:
        return None, "Vui lòng nhập một số."


@app.route('/', methods=['GET', 'POST'])
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    values = {'a': '', 'b': '', 'op': '+'}
    errors = {'a': None, 'b': None, 'op': None}
    result = None

    if request.method == 'POST':
        values['a'] = request.form.get('a', '')
        values['b'] = request.form.get('b', '')
        values['op'] = request.form.get('op', '+')

        num_a, errors['a'] = parse_number(values['a'])
        num_b, errors['b'] = parse_number(values['b'])
        op = values['op']

        valid_ops = ['+', '-', '*', '/']
        if op not in valid_ops:
            errors['op'] = "Phép toán không hợp lệ."

        if op == '/' and num_b == 0:
            errors['b'] = "Không thể chia cho 0."

        if not errors['a'] and not errors['b'] and not errors['op']:
            if op == '+':
                res_val = num_a + num_b
            elif op == '-':
                res_val = num_a - num_b
            elif op == '*':
                res_val = num_a * num_b
            else:
                res_val = num_a / num_b

            res_str = f"{res_val:.6g}"
            result = f"{values['a']} {op} {values['b']} = {res_str}"

    return render_template('calc.html', values=values, errors=errors, result=result)


@app.route('/grades', methods=['GET', 'POST'])
def grade_calculator():
    values = {'cc': '', 'gk': '', 'ck': ''}
    errors = {'cc': None, 'gk': None, 'ck': None}
    result = None
    letter = None

    if request.method == 'POST':
        for field in values:
            values[field] = request.form.get(field, '').strip().replace(',', '.')

            if not values[field]:
                errors[field] = 'Vui lòng nhập một số.'
                continue

            try:
                score = float(values[field])
                if score < 0 or score > 10:
                    errors[field] = 'Điểm phải từ 0 đến 10.'
            except ValueError:
                errors[field] = 'Vui lòng nhập một số.'

        if not any(errors.values()):
            cc = float(values['cc'])
            gk = float(values['gk'])
            ck = float(values['ck'])
            result = cc * 0.10 + gk * 0.30 + ck * 0.60

            if result >= 8.5:
                letter = 'A'
            elif result >= 7.0:
                letter = 'B'
            elif result >= 5.5:
                letter = 'C'
            elif result >= 4.0:
                letter = 'D'
            else:
                letter = 'F'

    return render_template(
        'grades.html', values=values, errors=errors,
        result=result, letter=letter
    )


if __name__ == '__main__':
    app.run(debug=True)
