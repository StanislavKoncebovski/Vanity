import pickle
import random


class Vanitizer:
    """
    Creates sentences of a given structure (rule-based).
    """
    def __init__(self):
        self.pos = {}
        self._vowels = "aeiou"
        self.plural_noun_frequency = 0.5    # Probability with which to create plural nouns vs singular.
        self.determinant_frequency = 0.5    # Probability with which nouns get determinants
        self.adjective_frequency = 0.5      # Probability with which nouns get adjectives
        self.verb_third_person_frequency = 0.1  # Probability with which the verb will be in 3rd person
        self.verb_past_frequency  = 0.5         # Probability with which the verb will be in past tence
        self.adverb_frequency   = 0.5           # Probability with which the verb will be supplied by an adverb

    def load_pos(self, file_name: str):
        '''
        Loads pickled POS from a file.
        :param: file_name: Name of the file to load from.
        :return: None
        '''
        with open(file_name, "rb") as file:
            self.pos = pickle.load(file)


    def create_sentence(self) -> str:
        '''
        Creates a random sentence of given structure.
        :return: Sentence created.
        '''
        result = self._create_noun_group()
        result += " " + self._create_verbal_group()
        result += ", "
        result += random.choice(self.pos["conjunctions"])
        result += " "
        result += self._create_noun_group()
        result += " " + self._create_verbal_group()
        result += " " + self._create_noun_group()

        return result

    def create_sentences(self, number_of_sentences: int) -> str:
        '''
        Creates a number of random sentences.
        :param: number_of_sentences: Number of sentences to create.
        :return: The sentences created.
        '''
        result = ""

        for i in range(number_of_sentences):
            result += f"{self.create_sentence()}\n"

        return result

    #region Private Auxiliary
    def _create_det_noun(self):
        noun = random.choice(self.pos["nouns"])
        is_plural = random.random() > self.plural_noun_frequency

        if is_plural:
            noun = self._get_plural_noun(noun)

        if random.random() > self.determinant_frequency:
            det = random.choice(self.pos["determinants"])
        else:
            det = ""

        if is_plural and (det == 'a' or det == 'an'):
            det = ""

        if det == 'a' and noun[0] in self._vowels:
            det = 'an'

        if is_plural and det == 'this':
            det = 'these'

        if is_plural and det == 'that':
            det = 'those'

        return (noun, det)

    def _get_plural_noun(self, noun: str):
        if noun == "child":
            return "children"
        elif noun == "sheep":
            return "sheep"
        elif noun == "fish":
            return "fish"
        elif noun == "aircraft":
            return "aircraft"

        if noun.endswith("y"):
            return noun[-1:] + "ies"

        if noun.endswith("ch") or noun.endswith("sh"):
            return noun + "es"

        else:
            return noun + "s"

    def _create_noun_group(self):
        noun, det = self._create_det_noun()

        if random.random() > self.adjective_frequency:
            adjective = random.choice(self.pos["adjectives"])
        else:
            adjective = ""

        return f"{det} {adjective} {noun}".strip().replace("  ", " ")

    def _create_verbal_group(self):
        result = ""

        if random.random() > 0.25:
            result += f"{random.choice(self.pos['adverbs'])}"

        is_third_person = random.random() > self.verb_third_person_frequency
        is_past_tense = random.random() > self.verb_past_frequency

        verb = random.choice(self.pos["verb_forms"])

        if is_third_person:
            result += f" {verb[3]}"
        elif is_past_tense:
            result += f" {verb[1]}"
        else:
            result += f" {verb[0]}"

        return result.strip()
    #endregion

if __name__ == '__main__':
    vanitizer = Vanitizer()

    vanitizer.load_pos("pos_lite.pkl")

    for i in range(20):
        sentence = vanitizer.create_sentence()
        print(sentence)