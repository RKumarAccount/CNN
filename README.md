# Image Augmentation Frontend

A simple Flask frontend for the existing augmentation notebook.

## Files added
- `app.py` - Flask backend to upload an image and generate augmented outputs
- `templates/index.html` - frontend form and preview layout
- `requirements.txt` - required Python packages

## Run
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000/` in your browser.

## Notes
- Uploaded images are stored under `static/uploads`
- Generated augmentations are stored under `static/generated`
- The app uses the same ImageDataGenerator settings as your notebook
