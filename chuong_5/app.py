from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    values = {'a': '', 'b': '', 'op': '+'}
    errors = {'a': None, 'b': None, 'op': None}
    result = None

    if request.method == 'POST':
        values['a'] = request.form.get('a', '').strip()
        values['b'] = request.form.get('b', '').strip()
        values['op'] = request.form.get('op', '+')

        try:
            num_a = float(values['a'].replace(',', '.'))
        except ValueError:
            errors['a'] = "Vui lòng nhập một số."
            num_a = None

        try:
            num_b = float(values['b'].replace(',', '.'))
        except ValueError:
            errors['b'] = "Vui lòng nhập một số."
            num_b = None

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


@app.route('/bmi', methods=['GET', 'POST'])
def bmi_calculator():
    values = {'height': '', 'weight': ''}
    errors = {'height': None, 'weight': None}
    bmi = None
    category = None
    color = None

    if request.method == 'POST':
        values['height'] = request.form.get('height', '').strip()
        values['weight'] = request.form.get('weight', '').strip()

        for field, value, minimum, maximum, label in (
            ('height', values['height'], 50, 250, 'chiều cao'),
            ('weight', values['weight'], 10, 300, 'cân nặng'),
        ):
            if not value:
                errors[field] = "Vui lòng nhập một số."
                continue

            try:
                number = float(value.replace(',', '.'))
                if number < minimum or number > maximum:
                    errors[field] = f"Giá trị phải từ {minimum} đến {maximum}."
            except ValueError:
                errors[field] = "Vui lòng nhập một số."

        if not any(errors.values()):
            height_m = float(values['height'].replace(',', '.')) / 100
            weight = float(values['weight'].replace(',', '.'))
            bmi = weight / (height_m * height_m)

            if bmi < 18.5:
                category = 'Thiếu cân (vàng)'
                color = 'warning'
            elif bmi < 25:
                category = 'Bình thường'
                color = 'success'
            elif bmi < 30:
                category = 'Thừa cân (vàng)'
                color = 'warning'
            else:
                category = 'Béo phì'
                color = 'danger'

    return render_template(
        'bmi.html', values=values, errors=errors,
        bmi=bmi, category=category, color=color
    )


@app.route('/grades', methods=['GET', 'POST'])
def grade_calculator():
    values = {'cc': '', 'gk': '', 'ck': ''}
    errors = {'cc': None, 'gk': None, 'ck': None}
    result = None
    letter = None

    if request.method == 'POST':
        for field in values:
            values[field] = request.form.get(field, '').strip()

            if not values[field]:
                errors[field] = 'Vui lòng nhập một số.'
                continue

            try:
                score = float(values[field].replace(',', '.'))
                if score < 0 or score > 10:
                    errors[field] = 'Điểm phải từ 0 đến 10.'
            except ValueError:
                errors[field] = 'Vui lòng nhập một số.'

        if not any(errors.values()):
            cc = float(values['cc'].replace(',', '.'))
            gk = float(values['gk'].replace(',', '.'))
            ck = float(values['ck'].replace(',', '.'))
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
