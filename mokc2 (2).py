# first pip install transformers

from transformers import BertTokenizer, BertModel
import torch
import sqlite3

# Загрузка предварительно обученной модели BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def embed_text(text):
    # Токенизация текста
    tokens = tokenizer(text, return_tensors='pt')

    # Получение представления текста из последнего слоя в BERT
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

    return embeddings.numpy()


def find_best_match(user_comment, comments):
    user_embedding = embed_text(user_comment)
    comment_embeddings = [embed_text(comment) for comment in comments]

    # Рассчет схожести с использованием внутреннего произведения матриц
    scores = [user_embedding.dot(comment_embedding) for comment_embedding in comment_embeddings]

    # Нахождение наилучшего совпадения
    best_match_index = scores.index(max(scores))
    return comments[best_match_index]


def get_game_recommendation(user_comment):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT comment FROM game_comments")
    comments = [row[0] for row in cursor.fetchall()]

    best_match = find_best_match(user_comment, comments)

    cursor.execute("SELECT game_name FROM game_comments WHERE comment = ?", (best_match,))
    game_recommendation = cursor.fetchone()

    conn.close()

    return game_recommendation[0] if game_recommendation else "Не найдено подходящей игры"


# Пример использования
user_input = "Обожаю игры с потрясающей графикой!"
recommended_game = get_game_recommendation(user_input)
print("Рекомендуемая игра:", recommended_game)
