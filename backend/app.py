# import os
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from PIL import Image
# import uuid
# import json

# app = Flask(__name__)
# CORS(app, resources={
#     r"/*": {
#         "origins": [
#             "http://localhost:5173",
#             "http://127.0.0.1:5173",
#         ],
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Content-Type"],
#         "supports_credentials": True
#     }
# })

# @app.route('/api/upload', methods=['POST'])
# def upload_image():
#     try:
#         print("Starting upload process")  # Debug log
#         if 'image' not in request.files:
#             print("No image in request files:", request.files)  # Debug log
#             return jsonify({'error': 'No image part'}), 400
        
#         file = request.files['image']
#         print(f"Received file: {file.filename}")  # Debug log
        
#         if not file.filename:
#             return jsonify({'error': 'No selected file'}), 400
        
#         settings = json.loads(request.form.get('settings', '{}'))
#         print(f"Received settings: {settings}")  # Debug log
        
#         filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
#         upload_path = os.path.join(UPLOAD_FOLDER, filename)
#         processed_path = os.path.join(PROCESSED_FOLDER, filename)
        
#         print(f"Saving file to: {upload_path}")  # Debug log
#         file.save(upload_path)
        
#         with Image.open(file) as img:
#             if settings.get('cropArea'):
#                 img = crop_image(img, settings['cropArea'])
            
#             # Save the cropped image
#             img.save(upload_path)
        
#         return jsonify({
#             'message': 'Image processed successfully',
#             'image_url': f'/api/images/{filename}'
#         })
#     except Exception as e:
#         import traceback
#         print("Error during upload:")
#         print(traceback.format_exc())  # Detailed error traceback
#         return jsonify({'error': str(e)}), 500


# # @app.route('/api/images/<filename>')
# # def get_image(filename):
# #     return send_from_directory(PROCESSED_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)