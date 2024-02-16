import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import utils as ut

import time
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf

# Hyperparameters
MAX_SEQUENCE_LENGTH = 128
EMBEDDING_DIM = 512
LSTM_UNITS = 256
DENSE_UNITS = 128
EPOCHS = 25
BATCH_SIZE = 256
TEST_SIZE = 0.3
LEARNING_RATE = 0.01
DROPOUT_RATE = 0.2

def load_tokenizer(tokenizer_file_path='tokenizer.pkl'):
    with open(tokenizer_file_path, 'rb') as tokenizer_file:
        tokenizer = pickle.load(tokenizer_file)
    return tokenizer

def load_label_encoder(label_encoder_file_path='label_encoder.pkl'):
    with open(label_encoder_file_path, 'rb') as label_encoder_file:
        label_encoder = pickle.load(label_encoder_file)
    return label_encoder

def load_data():
    # Load CSV data
    df = pd.read_csv("random_samples.csv")

    # Encode datatypes
    label_encoder = LabelEncoder()
    df['datatype_encoded'] = label_encoder.fit_transform(df['datatype'])

    # Tokenize and pad sequences
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(df['ops_funcs'])
    sequences = tokenizer.texts_to_sequences(df['ops_funcs'])
    padded_sequences = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    return df, tokenizer, padded_sequences, label_encoder

def build_model(df, tokenizer, padded_sequences, label_encoder, learning_rate=LEARNING_RATE):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, df['datatype_encoded'], test_size=TEST_SIZE, random_state=42)

    # Build LSTM model with bidirectional layers
    model = Sequential()
    model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=EMBEDDING_DIM, input_length=padded_sequences.shape[1]))

    model.add(Bidirectional(LSTM(units=LSTM_UNITS, return_sequences=True)))
    model.add(Dropout(rate=DROPOUT_RATE))
    
    model.add(Bidirectional(LSTM(units=LSTM_UNITS//2, return_sequences=True)))
    model.add(Dropout(rate=DROPOUT_RATE))
    
    model.add(Bidirectional(LSTM(units=LSTM_UNITS//4)))
    model.add(Dropout(rate=DROPOUT_RATE))
    
    model.add(Dense(units=len(label_encoder.classes_), activation='softmax'))


    # Compile the model
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Print model architecture
    tf.keras.utils.plot_model(model, to_file='lstm_model.png', show_shapes=True, dpi=64)

    return model, X_train, y_train, X_test, y_test


def fit_model(model, X_train, y_train, X_test, y_test):
    # Train the model
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test, y_test), callbacks=[early_stopping])

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    ut.print_info(f'[TEST] Accuracy: {accuracy * 100:.2f}%')

    return loss, accuracy


def train():
    start = time.time()
    # Load data
    df, tokenizer, padded_sequences, label_encoder = load_data()

    # Save tokenizer
    with open('tokenizer.pkl', 'wb') as tokenizer_file:
        pickle.dump(tokenizer, tokenizer_file)

    # Save label encoder
    with open('label_encoder.pkl', 'wb') as label_encoder_file:
        pickle.dump(label_encoder, label_encoder_file)

    # Build model
    model, X_train, y_train, X_test, y_test = build_model(df, tokenizer, padded_sequences, label_encoder)

    # Train and evaluate model
    loss, accuracy = fit_model(model, X_train, y_train, X_test, y_test)

    # Save model to h5 file
    model.save('classifier.h5')
    
    end = time.time()

    # format in minutes and seconds
    ut.print_info(f'Training time: {int((end - start) / 60)} minutes {int((end - start) % 60)} seconds')

    return loss, accuracy


def predict_datatype(new_data, model_name="classifier.h5"):
    # Load model
    model = load_model(model_name)
    
    tokenizer = load_tokenizer() 
    label_encoder = load_label_encoder() 

    # Tokenize and pad the new data
    new_data_sequences = tokenizer.texts_to_sequences(new_data)
    padded_new_data = pad_sequences(new_data_sequences, maxlen=MAX_SEQUENCE_LENGTH)  # Adjust maxlen based on your training data

    # Make predictions
    predictions = model.predict(padded_new_data)

    # Decode predictions to class labels
    decoded_predictions = label_encoder.inverse_transform(predictions.argmax(axis=1))

    predictions = []
    
    for ops_funcs, prediction in zip(new_data, decoded_predictions):
        predictions.append((ops_funcs, prediction))
    
    return predictions