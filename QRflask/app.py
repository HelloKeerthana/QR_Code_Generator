from flask import Flask, render_template, request
import qrcode
from PIL import Image
import qrcode.constants
import os

app = Flask(__name__)


def generate_qr_codes(input_url, qrcode_size, qrcode_border, outputfile_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qrcode_size,
        border=qrcode_border
    )
    qr.add_data(input_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    
    img.save(outputfile_path)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    # Get the form data
    input_url = request.form.get("input_url")
    qrcode_size = int(request.form.get("qrcode_size", 10))
    qrcode_border = int(request.form.get("qrcode_border", 3))
    outputfile_path = request.form.get("outputfile_path")  

    
    static_folder = os.path.join(app.root_path, 'static')
    outputfile_og_path = os.path.join(static_folder, outputfile_path)

    
    generate_qr_codes(input_url, qrcode_size, qrcode_border, outputfile_og_path)

    
    return render_template("index.html", qr_code_url=outputfile_path)


if __name__ == "__main__":
    app.run(debug=True)
