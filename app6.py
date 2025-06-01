from flask import Flask, render_template, request
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Hide INFO and WARNING from TensorFlow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from io import BytesIO
import base64
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Ini log debug")


app = Flask(__name__)

# Load model
model = load_model('model/v7_custom13_2.h5', compile=False)
IMG_SIZE = (224, 224)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("DEBUG: POST request diterima", flush=True)
        if 'image' not in request.files:
            return render_template('index.html', error="Tidak ada file yang diupload")

        file = request.files['image']
        if file.filename == '':
            print("DEBUG: Filename kosong", flush=True)
            return render_template('index.html', error="Tidak ada file yang dipilih")

        print("DEBUG: File berhasil diterima:", file.filename, flush=True)
        
        if not allowed_file(file.filename):
            return render_template('index.html', error="Format file tidak didukung")

        try:
            image_bytes = file.read()
            image = Image.open(BytesIO(image_bytes)).convert('RGB')
            image = image.resize(IMG_SIZE)
            image_array = img_to_array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)

            prediction = model.predict(image_array)[0][0]
            # label = 'Cacar Monyet' if prediction[0] > 0.5 else 'Bukan Cacar Monyet'
            # confidence = f"{float(prediction[0]) * 100:.2f}%" if label == 'Cacar Monyet' else f"{(1 - float(prediction[0])) * 100:.2f}%"
            # Prediksi
            # prediction = model.predict(img_array)[0][0]
            confidence = round(prediction * 100, 2)
            pureconfidence = round(prediction * 100, 2)
            if (prediction <= 0.2) : 
                confidence = (100 - confidence)
                label = 'Monkeypox'
            else :
                label = 'Bukan Monkeypox'
            
            # Ubah gambar ke base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            mime_type = file.mimetype  # contoh: 'image/jpeg', 'image/png'
            image_data_url = f"data:{mime_type};base64,{encoded_image}"
            
            print(f"ini image url: {image_data_url}", flush=True)
            return render_template('index.html', label=label, confidence=confidence, image_url=image_data_url)

        except Exception as e:
            return render_template('index.html', error=f"Terjadi kesalahan: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)