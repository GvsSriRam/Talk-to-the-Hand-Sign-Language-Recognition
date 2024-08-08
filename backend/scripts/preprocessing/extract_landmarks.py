import mediapipe as mp
import cv2
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder

from utils import get_relative_positions

# Load the MediaPipe Hands model
mp_hands = mp.solutions.hands.Hands()

global curr_label
curr_label = ""

class ExtractLandmarks:

    def __init__(self) -> None:
        self.files, self.folders = self.scan_files_and_folders("/Users/gvssriram/Desktop/projects-internship/MathNoteX/sign/ASL_Alphabet_Dataset/asl_alphabet_train")

    def get_landmarks(self, file_location):
        # Read the image
        image = cv2.imread(file_location)

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and get the landmarks data
        results = mp_hands.process(image_rgb)

        # Extract the landmarks from the results
        landmarks = results.multi_hand_landmarks
        
        # Convert the landmarks to a numpy array
        if landmarks:
            landmarks_np = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks[0].landmark])
        else:
            return None
        
        return landmarks_np

    # count the number of subfolders and files in the given path
    def scan_files_and_folders(self, path='.'):
        files = []
        folders = []
        
        with os.scandir(path) as entries:    
            for entry in entries:
                # print(entry.path)
                # print(curr_label)
                if entry.is_file():
                    files.append(entry.path)
                elif entry.is_dir():
                    folders.append(entry.path)
                    self.scan_files_and_folders(entry.path)
            
        return files, folders

    def getLandmarksAndLabels(self, path='.'):
        global curr_label
        # Initialize the list to store the landmarks
        landmarks_list = []
        # Initialize the list to store the labels
        labels = []

        with os.scandir(path) as entries:
            
            for entry in entries:
                # print(entry.path)
                # print(curr_label)
                if entry.is_file():
                    landmarks = self.get_landmarks(entry.path)
                    # print(landmarks)
                    if landmarks is not None:
                        landmarks_list.append(landmarks)
                        labels.append(curr_label)
                    # else:
                    #     print("No landmarks found")
                elif entry.is_dir():
                    curr_label = entry.name
                    print(curr_label)
                    self.getLandmarksAndLabels(entry.path)
            
        return landmarks_list, labels

    def __call__(self):
        x_train, y_train = self.getLandmarksAndLabels("/Users/gvssriram/Desktop/projects-internship/MathNoteX/sign/ASL_Alphabet_Dataset/asl_alphabet_train")

        x_train = np.array(x_train)
        y_train = np.array(y_train)

        np.save('../data/ASL_Alphabet_Dataset_Processed/x_train.npy', x_train)
        np.save('../data/ASL_Alphabet_Dataset_Processed/y_train.npy', y_train)

        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
        np.save('../data/ASL_Alphabet_Dataset_Processed/x_train_flat.npy', x_train)

        x_train_relative = np.apply_along_axis(get_relative_positions, 1, x_train)
        np.save('../data/ASL_Alphabet_Dataset_Processed/x_train_relative.npy', x_train_relative)

        x_train_relative = x_train_relative.reshape(x_train_relative.shape[0], x_train_relative.shape[1]*x_train_relative.shape[2])
        np.save('../data/ASL_Alphabet_Dataset_Processed/x_train_relative_flat.npy', x_train_relative)
