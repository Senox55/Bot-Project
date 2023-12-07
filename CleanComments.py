import pandas as pd
import re

comment_data = pd.read_csv(r'C:\Users\very-\Desktop\Bot Project\Bot-Project\steam_comments.csv', sep=';')
X_train = comment_data['comment']


def clean_comments(text):
    cleaned_data = pd.Series(columns=['cleaned_comment'])
    for text in X_train:
        text = str(text)
        text = text.replace("\\", " ").replace(u"╚", " ").replace(u"╩", " ")
        text = text.lower()
        text = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', text)  # deleting newlines and line-breaks
        text = re.sub('[.,:;_%©?*,!@#$%^&()\d]|[+=]|[[]|[]]|[/]|"|\s{2,}|-', ' ', text)  # deleting symbols
        # text = " ".join(ma.parse(unicode(word))[0].normal_form for word in text.split())
        text = ' '.join(word for word in text.split() if len(word) > 3)
        text = text.encode("utf-8")

        cleaned_data.loc['cleaned_comment'] = text
    return cleaned_data


print(clean_comments(X_train))
