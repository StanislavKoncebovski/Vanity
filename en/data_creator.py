import bs4.element
import spacy
import requests
from bs4 import BeautifulSoup
import pickle

class DataCreator:
    def __init__(self):
        self.pos = {}

        self.pos["nouns"] = []
        self.pos["adjectives"] = []
        self.pos["adverbs"] = []
        self.pos["verbs"] = []
        self.pos["proper_names"] = []
        self.pos["determinants"] = []
        self.pos["conjunctions"] = []
        self.pos["verb_forms"] = []

        self.nlp = spacy.load("en_core_web_lg")

    """
    Creates lists of English parts of speech (POS) using a large text corpus.
    Saves this data for the use of client classes.
    """
    def create_pos(self, source: str) -> dict[str, list[str]]:
        '''
        Creates lists of POS by extracting them from an enough large text corpus.
        :param source: The text corpus to extract the POS.
        :return: Dictionary of POS. Contains POS names as keys and lists of POS of the kind as values.
                 The keys are as follows: "nouns", "adjectives", "adverbs",
                                          "verbs", "proper_names", "determinants", "conjunctions".
        '''
        self.nlp.max_length = len(source) + 1
        doc = self.nlp(source)

        count = 1
        for token in doc:
            if token.pos_ == "NOUN":
                self.pos["nouns"].append(token.lemma_.lower())
            elif token.pos_ == "ADJ":
                self.pos["adjectives"].append(token.text.lower())
            elif token.pos_ == "ADV":
                self.pos["adverbs"].append(token.text.lower())
            elif token.pos_ == "VERB":
                self.pos["verbs"].append(token.lemma_.lower())
            elif token.pos_ == "PROPN":
                self.pos["proper_names"].append(token.text.lower())
            elif token.pos_ == "DET":
                self.pos["determinants"].append(token.text.lower())
            elif token.pos_ == "CCONJ":
                self.pos["conjunctions"].append(token.text.lower())

            print(f"Processed token {count} of {len(doc)}")
            count += 1

        for key in self.pos:
            min_word_length = 2
            if key == "determinants":
                min_word_length = 1
            self._process_word_list(key, min_word_length)

    def create_verb_forms(self, url):
        '''
        Creates a list of 1000 English verbs with their verb forms.
        :param url: The URL from which to load the original table
                    (https://www.worldclasslearning.com/english/five-verb-forms.html)
        :return: List of lists of verb forms for each verb, in the following order:
                 [0]: Present
                 [1]: Past
                 [2]: Parst Participle
                 [3]: Third person sing.
                 [4]: The ing-form
        '''
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all('table')

        self.pos["verb_forms"] += self._make_verb_form_table(tables[1])
        self.pos["verb_forms"] += self._make_verb_form_table(tables[2])


    def pickle_pos(self, file_name: str):
        '''
        Saves the POS and the verb forms data as a single pickle file.
        :param file_name: The name of the pickle file
        :return: None
        '''
        with open(file_name, 'wb') as file:
            pickle.dump(self.pos, file)

    #region Private Auxiliary
    def _process_word_list(self, key: str, min_word_length: int = 2):
        '''
        Simplifies a word list for a POS.
        :param key: The name of the POS in the dictionary.
        :param min_word_length: The minimum word length.
        :return: None
        '''
        self.pos[key] = set(self.pos[key])
        self.pos[key] = [word for word in self.pos[key] if len(word) >= min_word_length]
        self.pos[key] = [word for word in self.pos[key] if word.isalpha()]

    def _make_verb_form_table(self, table: bs4.element.Tag):
        '''
        Extracts the verb forms from the HTML table
        :return: List of string verb form tuples.
        '''
        verbs = []
        forms = []
        row_index = 0
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all("td")

            if row_index == 0:
                row_index += 1
                continue

            for cell in cells:
                if cell.text.isdigit():
                    if len(forms) > 0:
                        verbs.append(forms)
                    forms = []
                else:
                    forms.append(cell.text)

        return verbs
    #endregion


if __name__ == '__main__':
    data_creator = DataCreator()

    with open("../Data/abstracts_lite.txt", "r", encoding="utf-8") as file:
        source = file.read()

    data_creator.create_pos(source)

    print("POS dictionary ready")

    url = 'https://www.worldclasslearning.com/english/five-verb-forms.html'

    data_creator.create_verb_forms(url)

    print("verb forms ready")

    file_name = "pos.pkl"

    data_creator.pickle_pos(file_name)