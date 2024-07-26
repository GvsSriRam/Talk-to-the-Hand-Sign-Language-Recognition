import tensorflow as tf
import numpy as np

from utils import get_relative_positions

class ASLModelPrediction:

    def __init__(self, encoder, model = None) -> None:
        if model is None:
            self.model = self.load_model()
            print("loaded model")
        else:
            self.model = model
        
        self.encoder = encoder

    def predict(self, landmarks_np):
        print(landmarks_np)
        # landmarks_np = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks[0].landmark])
        landmarks_relative = get_relative_positions(np.array(landmarks_np))
        landmarks_relative = landmarks_relative.reshape(1, landmarks_relative.shape[0]*landmarks_relative.shape[1])
        prediction = self.model.predict(landmarks_relative)
        prediction = np.argmax(prediction, axis=1)
        char = self.encoder.get_feature_names_out()[prediction[0]]

        return char

    def predict_live(self, landmarks):
        landmarks_np = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks[0].landmark])
        landmarks_relative = get_relative_positions(landmarks_np)
        landmarks_relative = landmarks_relative.reshape(1, landmarks_relative.shape[0]*landmarks_relative.shape[1])
        prediction = self.model.predict(landmarks_relative)
        prediction = np.argmax(prediction, axis=1)
        char = self.encoder.get_feature_names_out()[prediction[0]]

        return char[3:]

    def load_model(self):
        return tf.keras.models.load_model('../models/model/asl_alphabet_model_2.keras')
