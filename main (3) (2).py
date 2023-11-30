# pip install textblob
import csv
from textblob import TextBlob
import nltk

nltk.download('wordnet')


def clean_text(comment):
    comment_blob = TextBlob(comment)
    cleaned_words = [word.lemmatize().lower() for word in comment_blob.words if word.isalpha()]
    cleaned_comment = ' '.join(cleaned_words)
    return cleaned_comment


with open('input_data.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    with open('cleaned_data.csv', 'w', newline='', encoding='utf-8') as clean_csv_file:
        fieldnames = header + ['cleaned_comment']
        csv_writer = csv.DictWriter(clean_csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in csv_reader:
            comment_id, game_name, original_comment = row
            cleaned_comment = clean_text(original_comment)
            csv_writer.writerow({'comment_id': comment_id, 'game_name': game_name, 'original_comment': original_comment,
                                 'cleaned_comment': cleaned_comment})

print("Data has been cleaned and saved to a new CSV file.")
