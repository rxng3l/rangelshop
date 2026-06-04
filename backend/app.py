from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/remove-background', methods=['POST'])
def remove_background():

    if 'image' not in request.files:
        return {'error': 'No se recibió ninguna imagen'}, 400

    file = request.files['image']

    r_target = int(request.form.get('r', 0))
    g_target = int(request.form.get('g', 0))
    b_target = int(request.form.get('b', 0))

    tolerance = int(request.form.get('tolerance', 120))

    print("Color seleccionado:", r_target, g_target, b_target)
    print("Tolerancia:", tolerance)

    img = Image.open(file.stream).convert("RGBA")

    data = img.getdata()

    new_data = []

    for item in data:

        r, g, b, a = item

        distance = (
            abs(r - r_target) +
            abs(g - g_target) +
            abs(b - b_target)
        )

        if distance <= tolerance:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)

    img_io = BytesIO()

    img.save(img_io, format="PNG")

    img_io.seek(0)

    return send_file(
        img_io,
        mimetype='image/png'
    )

if __name__ == '__main__':
    app.run(debug=True)