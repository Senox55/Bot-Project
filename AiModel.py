import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

comment_data = pd.read_csv(r'C:\Users\very-\Desktop\Bot Project\Bot-Project\steam_comments.csv', sep=';')

# Комментарии
X_train = comment_data['comment']

# Вектор игр
y_train = comment_data['game_name']

# Обучение модели
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train.values.astype('U'))
rf_clf = KNeighborsClassifier()
rf_clf.fit(X_train_tfidf, y_train)

# Комментарий пользователя
user_comment = tfidf_vectorizer.transform([input()])

#Результат
print(rf_clf.predict(user_comment))
