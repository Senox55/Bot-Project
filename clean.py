import re
import enchant
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import pandas as pd
from tqdm import tqdm
import os
import nltk


class CleanData:
    index = 'comment'
    input_csv_file_path = 'steam_comments.csv'
    output_csv_file_path = 'cleaned_data.csv'

    def clean_text(self, text):
        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        text = stemmer.stem(text)
        text = lemmatizer.lemmatize(text)
        language = "en_US"
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
        dictionary = enchant.Dict(language)
        stop_words = set(stopwords.words("english"))
        words = cleaned_text.split()
        clean_words = [word for word in words if
                       len(word) >= 3 and dictionary.check(word) and word.lower() not in stop_words]
        final = ' '.join(clean_words)
        return final

    def black_list(self):
        filter_file_path = 'blacklist.txt'
        words_to_remove = []

        with open(filter_file_path, 'r', encoding='utf-8') as filter_file:
            words_to_remove = filter_file.read().split()
        return words_to_remove

    def filter_text(self, text):
        words_to_remove = self.black_list()
        words = text.split()

        filtered_words = [word for word in words if word.lower() not in words_to_remove]

        filtered_text = ' '.join(filtered_words)

        return filtered_text

    def filter(self, text):
        text = str(text).lower()
        data1 = self.clean_text(text)
        data2 = self.filter_text(data1)
        return data2

    def processor(self):
        input_csv_file_path = self.input_csv_file_path
        tmp_csv_file_path = 'tmp.csv'
        output_csv_file_path = self.output_csv_file_path
        index = self.index
        df = pd.read_csv(input_csv_file_path, sep=';', encoding='latin-1')

        df[index] = tqdm(df[index].progress_apply(self.filter), desc="Cleaning progress")
        df = df.dropna(subset=[index])
        df.to_csv(tmp_csv_file_path, index=False, encoding='utf-8')

        dn = pd.read_csv(tmp_csv_file_path, sep=',')

        dn = dn.dropna(subset=[index])
        dn.to_csv(output_csv_file_path, index=False, encoding='utf-8')
        os.remove(tmp_csv_file_path)

    def main(self):
        nltk.download('stopwords')
        tqdm.pandas()
        tqdm(self.processor(), desc="Cleaning progress")
        return True


instance = CleanData()
instance.main()
