from flask import Flask, render_template, request, url_for
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = Path(app.static_folder) / 'uploads'
OUTPUT_FOLDER = Path(app.static_folder) / 'generated'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

DATAGEN = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='reflect'
)


def augment_image(image_path: Path, batch_count: int = 9):
    img = load_img(str(image_path))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    run_id = uuid.uuid4().hex
    output_dir = OUTPUT_FOLDER / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, _ in enumerate(DATAGEN.flow(x, batch_size=1, save_to_dir=str(output_dir), save_prefix='aug', save_format='jpeg')):
        if i >= batch_count - 1:
            break

    images = sorted(output_dir.iterdir())
    return [url_for('static', filename=f'generated/{run_id}/{img.name}') for img in images]


@app.route('/', methods=['GET', 'POST'])
def index():
    generated_images = []
    uploaded_image_url = None
    error = None

    if request.method == 'POST':
        image_file = request.files.get('image')

        if not image_file or image_file.filename == '':
            error = 'Please choose an image to augment.'
        else:
            filename = secure_filename(image_file.filename)
            upload_path = UPLOAD_FOLDER / f"{uuid.uuid4().hex}_{filename}"
            image_file.save(upload_path)
            uploaded_image_url = url_for('static', filename=f'uploads/{upload_path.name}')
            generated_images = augment_image(upload_path, batch_count=9)

    return render_template(
        'index.html',
        generated_images=generated_images,
        uploaded_image_url=uploaded_image_url,
        error=error
    )


if __name__ == '__main__':
    app.run(debug=True)
