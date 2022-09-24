import spacy

class DataCreator:
    def __init__(self):
        self.nouns = []
        self.adjectives = []
        self.adverbs = []
        self.verbs = []
        self.proper_names = []
        self.determinants = []
        self.conjunctions = []
        self.verb_forms = []
        self.pos = {}
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
        doc = self.nlp(source)

        for token in doc:
            if token.pos_ == "NOUN":
                self.nouns.append(token.lemma_.lower())
            elif token.pos_ == "ADJ":
                self.adjectives.append(token.text.lower())
            elif token.pos_ == "ADV":
                self.adverbs.append(token.text.lower())
            elif token.pos_ == "VERB":
                self.verbs.append(token.lemma_.lower())
            elif token.pos_ == "PROPN":
                self.proper_names.append(token.text.lower())
            elif token.pos_ == "DET":
                self.determinants.append(token.text.lower())
            elif token.pos_ == "CCONJ":
                self.conjunctions.append(token.text.lower())

            # self._process_word_list(self.nouns)
            # self._process_word_list(self.adjectives)
            # self._process_word_list(self.adverbs)
            # self._process_word_list(self.proper_names)
            # self._process_word_list(self.determinants)
            # self._process_word_list(self.conjunctions)

            self.pos["nouns"] = self._process_word_list(self.nouns)
            self.pos["adjectives"] = self._process_word_list(self.adjectives)
            self.pos["adverbs"] = self._process_word_list(self.adverbs)
            self.pos["proper_names"] = self._process_word_list(self.proper_names)
            self.pos["determinants"] = self._process_word_list(self.determinants)
            self.pos["conjunctions"] = self._process_word_list(self.conjunctions)

    def create_verb_forms(self, url) -> list[list[str]]:
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
        pass

    def pickle_pos(self, file_name: str):
        '''
        Saves the POS and the verb forms data as a single pickle file.
        :param file_name: The name of the pickle file
        :return: None
        '''
        pass

    #region Private Auxiliary
    def _process_word_list(self, words: list[str], min_word_length: int = 2) -> list[str]:
        words = set(words)
        words = [word for word in words if len(word) >= min_word_length]

        return  words

    #endregion