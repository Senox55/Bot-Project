import pandas as pd
import numpy as np
import tensorflow as tf
import scipy.sparse as sparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.preprocessing import LabelEncoder

# Load the data
comment_data = pd.read_csv(r'C:\Users\very-\Desktop\Bot Project\Bot-Project\cleaned_data.csv', sep=',').sample(n=50000)


X_train = comment_data['comment'].fillna('')

y_train = comment_data['game_id']

tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)


X_train, X_val, y_train, y_val = train_test_split(X_train_tfidf, y_train_encoded, test_size=0.2, random_state=42)


def get_model():
    model = Sequential()

    model.add(Dense(64, activation='relu', input_shape=(X_train_tfidf.shape[1],)))
    model.add(Dropout(0.4, noise_shape=None, seed=None))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(np.unique(y_train_encoded).shape[0], activation='softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


model = get_model()

model.fit(X_train.toarray(), y_train, epochs=10, batch_size=32, validation_data=(X_val.toarray(), y_val))

model.save("model.keras")
loaded_model = tf.keras.saving.load_model("model.keras")

while True:
    user_input = input("Enter your comment: ")
    user_input_vect = tfidf_vectorizer.transform([user_input])
    print(user_input_vect)
    predictions = model.predict(user_input_vect.toarray())
    print(predictions)
    predicted_labels = int(label_encoder.inverse_transform(
        [np.argmax(predictions)])[0])
    print(f'https://store.steampowered.com/app/{predicted_labels}')