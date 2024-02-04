import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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

# Hyperparameters
MAX_SEQUENCE_LENGTH = 100
EMBEDDING_DIM = 200
LSTM_UNITS = 100
DENSE_UNITS = 50
EPOCHS = 20
BATCH_SIZE = 200
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

    return model, X_train, y_train, X_test, y_test


def fit_model(model, X_train, y_train, X_test, y_test):
    # Train the model
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test, y_test), callbacks=[early_stopping])

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Accuracy: {accuracy * 100:.2f}%')

    return loss, accuracy


def execute():
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

    return loss, accuracy


def iterate_model(threshold=0.9, max_iterations=100):
    acc = []
    i = 1
    while True:
        print(f'\n\n[INFO] Iteration {i}')
        loss, accuracy = execute()
        acc.append((loss, accuracy))
        if accuracy > threshold or i >= max_iterations:
            break
        i += 1

    print(f'Average Accuracy: {sum([a[1] for a in acc]) / len(acc) * 100:.2f}%')
    print(f'Average Loss: {sum([a[0] for a in acc]) / len(acc):.4f}')

 
def predict_datatype(new_data, model_name="classifier.h5", ):
    # Load model
    model = load_model(model_name)
    
    tokenizer = load_tokenizer()  # Load your tokenizer (you need to implement this based on how you saved it during training)
    label_encoder = load_label_encoder()  # Load your label encoder (you need to implement this based on how you saved it during training)

    # Tokenize and pad the new data
    new_data_sequences = tokenizer.texts_to_sequences(new_data)
    padded_new_data = pad_sequences(new_data_sequences, maxlen=MAX_SEQUENCE_LENGTH)  # Adjust maxlen based on your training data

    # Make predictions
    predictions = model.predict(padded_new_data)

    # Decode predictions to class labels
    decoded_predictions = label_encoder.inverse_transform(predictions.argmax(axis=1))

    # Print the final predictions
    for ops_funcs, prediction in zip(new_data, decoded_predictions):
        print(f"Predicted Datatype: {prediction} <== ops/funcs: {ops_funcs}")


# execute()
iterate_model(threshold=0.92, max_iterations=50)

# New data: List of operations/functions
new_data = [
    "['add']",
    "['sin', 'gt', 'gt']",
    "['add', 'range', 'add']",
    "['round', 'cosh', 'div', 'pow', 'ne', 'gt']",
    "['round', 'trunc', 'floor', 'pow', 'tanh', 'exp', 'div', 'le', 'ceil', 'add', 'mul']",
    "['mod', 'lt', 'sub', 'trunc', 'floor', 'gt', 'div', 'sinh', 'fabs', 'add', 'pow', 'sqrt']",
    "['sinh', 'mul', 'add', 'abs', 'gt', 'log', 'ceil', 'pow', 'fabs', 'le', 'trunc', 'sub']",
    "['fabs', 'floor', 'lt', 'tanh', 'ceil', 'ne', 'mul', 'div', 'sinh', 'abs', 'eq', 'le']",
    "['rstrip', 'center', 'strip', 'rfind', 'concat', 'isdigit', 'replace', 'find', 'expandtabs', 'ljust', 'title', 'rindex']",
    "['isupper', 'capitalize', 'rstrip', 'isprintable', 'index', 'concat', 'isdecimal', 'strip']",
    "['isalnum', 'split', 'lstrip', 'count', 'isprintable', 'format', 'replace', 'rstrip', 'isidentifier', 'isdigit', 'concat', 'rpartition']",
    "['istitle', 'ljust', 'concat', 'center', 'find', 'lower', 'startswith', 'isprintable', 'isalpha', 'isspace', 'rjust', 'rindex']"
]  

# predict_datatype(new_data=new_data)