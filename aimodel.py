import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

comment_data = pd.read_csv(r'C:\Users\very-\Desktop\Bot Project\Bot-Project\steam_comments.csv', sep=',')

# Комментарии
X_train = comment_data['comment']

# Вектор игр
y_train = comment_data['game_name']

tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train.values.astype('U'))

X_train, X_val, y_train, y_val = train_test_split(X_train_tfidf, y_train, test_size=0.2, random_state=42)

# Обучение модели
rf_clf = KNeighborsClassifier(n_neighbors=1, weights='distance', leaf_size=9)
rf_clf.fit(X_train, y_train)
# parametrs = {'n_neighbors': range(1, 10, 4),
#              'weights': ['uniform', 'distance'],
#              'leaf_size': range(1, 100, 10)}
# grid = GridSearchCV(rf_clf, parametrs, cv=5, verbose=3)
# grid.fit(X_train, y_train)
# print(grid.best_params_)
# print(grid.best_score_)

# Комментарий пользователя
user_comment = tfidf_vectorizer.transform([input()])

# Результат
print(rf_clf.predict(user_comment))
