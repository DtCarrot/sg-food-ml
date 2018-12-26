from flask import Blueprint, jsonify, request
from predict import predict_image

predict_api = Blueprint('predict', __name__)

@predict_api.route('/predict', methods=['POST'])
def predict():
    content = request.json
    image_data = content['imageData']
    payload = predict_image(base64_data=image_data)
    for result in payload:
        class_name = result.display_name
        score = result.classification.score
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))
        return jsonify({'class_name': class_name, 'score': score})
