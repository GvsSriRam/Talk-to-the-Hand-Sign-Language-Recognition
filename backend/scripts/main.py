from preprocessing.encode import Encoder
from model_training.create_model import ASLModel
from model_training.prediction import ASLModelPrediction
from autocorrect.autocorrect import SpacyContextualSpellCheckMethod as Autocorrect
from log import logger
import numpy as np

autocorrect = Autocorrect()

class Pipeline:

    def __init__(self) -> None:
        self.encoder = None
        self.model = None

    def run(self):
        # Extract landmarks
        # logger.info("Extracting landmarks...")
        # extract_landmarks = ExtractLandmarks()
        # extract_landmarks()
        # logger.info("Landmarks extracted successfully!")

        # Load the data
        logger.info("Loading the data...")
        x_train_relative = np.load('../data/ASL_Alphabet_Dataset_Processed/x_train_relative.npy')
        y_train = np.load('../data/ASL_Alphabet_Dataset_Processed/y_train.npy')

        x_train_relative = x_train_relative.reshape(x_train_relative.shape[0], x_train_relative.shape[1]*x_train_relative.shape[2])
        np.save('../data/ASL_Alphabet_Dataset_Processed/x_train_relative_flat.npy', x_train_relative)

        # Encode the labels
        logger.info("Encoding labels...")
        encoder_class = Encoder()
        y_train_encoded, self.encoder = encoder_class.encode_labels(y_train)
        y_train_labels = np.argmax(y_train_encoded, axis=1)
        logger.info("Labels encoded successfully!")

        # Train the model
        logger.info("Training the model...")
        asl_model = ASLModel()
        self.model, _, _ = asl_model.model_2(x_train_relative, y_train_labels, y_train_encoded)
        # self.model, _, _ = asl_model.model_1(x_train_relative, y_train_encoded)
        logger.info("Model trained successfully!")
        return

    def predict(self, landmarks):
        # Predict the labels
        logger.info("Predicting the labels...")
        asl_model_prediction = ASLModelPrediction(self.encoder, self.model)
        prediction = asl_model_prediction.predict(landmarks)
        logger.info("Predicted label: %s", prediction)
        return prediction
    
    def autocorrect(self, input_str: str):
        # Autocorrect the input
        logger.info("Autocorrecting the input...")
        suggestions = autocorrect(input_str)
        logger.info("Autocorrected input: %s", suggestions)
        return suggestions

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
    # pipeline.predict(landmarks)
