# Create a classification model using tensorflow
from typing import Any
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.regularizers import l2
import tensorflow_decision_forests as tfdf
import tf_keras

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from log import logger

class ASLModel:

    def __init__(self):
        pass

    def create_model(self, n_dim):
        model = Sequential()
        model.add(Dense(128, input_shape=(n_dim,), activation='relu', kernel_regularizer=l2(0.01)))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(29, activation='softmax'))

        model.summary()

        opt = tf.keras.optimizers.Adam(learning_rate=0.005)

        loss = tf.keras.losses.CategoricalCrossentropy()

        metrics = []
        metrics.append("categorical_accuracy")

        # callbacks

        early_stopping = EarlyStopping(monitor='val_loss', patience=10)
        model_checkpoint = ModelCheckpoint(filepath='../models/ckpts/asl_alphabet_model.keras', 
                                           monitor='val_loss', 
                                           save_best_only=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', 
                                      factor=0.1, 
                                      patience=3, 
                                      min_lr=0.0001)
        tensorboard = TensorBoard(log_dir='../tflogs')

        callbacks = [early_stopping, model_checkpoint, reduce_lr, tensorboard]

        model.compile(optimizer=opt, loss=loss, metrics=metrics)

        return model, callbacks

    def create_and_train_tf_decision_trees_model(self, x_train_relative, y_train_labels):
        model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.CLASSIFICATION)
        model.compile(metrics=["accuracy"])
        rf_hist = model.fit(x_train_relative, 
                            y_train_labels, 
                            epochs=1, 
                            validation_split=0.2, 
                            verbose=2)
        return model, rf_hist

    def train_model(self, model, x_train_relative, y_train_encoded, callbacks):
        history = model.fit(x_train_relative, 
                            y_train_encoded, 
                            epochs=100, 
                            validation_split=0.2, 
                            verbose=1, 
                            callbacks=callbacks)
        return history

    def evaluate_model(self, x_train_relative, y_train_encoded, model):
        y_pred = model.predict(x_train_relative)
        y_pred = np.argmax(y_pred, axis=1)
        y_train_labels = np.argmax(y_train_encoded, axis=1)
        # print(classification_report(y_train_labels, y_pred))
        acc = accuracy_score(y_train_labels, y_pred)

        return acc

    def model_1(self, x_train_relative, y_train_encoded):
        n_dim = x_train_relative.shape[1]
        model, callbacks = self.create_model(n_dim)
        history = self.train_model(
                                model, 
                                x_train_relative, 
                                y_train_encoded, 
                                callbacks)
        acc = self.evaluate_model(
                                x_train_relative, 
                                y_train_encoded, 
                                model)
        model.save('../models/model/asl_alphabet_model.keras')
        logger.info("Model saved successfully!")
        return model, history, acc

    def model_2(self, x_train_relative, y_train_labels, y_train_encoded):
        model, rf_hist = self.create_and_train_tf_decision_trees_model(x_train_relative, y_train_labels)
        acc = self.evaluate_model(x_train_relative, y_train_encoded, model)
        try:
            model.save('../models/model/asl_alphabet_model_2', save_format="tf")
            logger.info("Model saved successfully!")
        except Exception as e:
            logger.error(str(e))
        return model, rf_hist, acc
