# one hot encode the labels
from sklearn.preprocessing import OneHotEncoder

class Encoder:

    def __init__(self) -> None:
        pass

    def encode_labels(self, y_train):
        encoder = OneHotEncoder()
        y_train_encoded = encoder.fit_transform(y_train.reshape(-1,1)).toarray()
        return y_train_encoded, encoder
