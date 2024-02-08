import json
import sys
import re


class Quiz:
    with open("questions.json") as file:
        data = json.load(file)
    
    # All questions and entering answers occur here
    @classmethod
    def do_quiz(cls):
        for i, question in enumerate(cls.data):
            # Ask 1 question at a time
            cls._ask_question(i, question["question"])

            # Show choices for question
            cls._show_choices(question["choices_and_traits"])

            # Loop until user enters elgible answer
            while True:
                total_choices = len(question["choices_and_traits"])
                ans = cls._get_ans()
                if cls._validate_ans(ans, total_choices) == True:
                    break

    # NONPRIVATE METHODS
    # Get max total of each trait
    @classmethod
    def get_max_traits_total(cls):
        traits = {}
        for _, question in enumerate(cls.data):
            for _, choice_trait in enumerate(question["choices_and_traits"]):
                # [1:] b/c some choice linked with > 1 traits
                for trait in choice_trait[1:]:
                    trait_striped = trait.strip()
                    if trait_striped not in traits:
                        traits[trait_striped] = 1
                    else:
                        traits[trait_striped] += 1

        return dict(sorted(traits.items()))
    
    @classmethod
    def show_max_traits_total(cls):
        print(cls.get_max_traits_total())

    @classmethod
    def get_all_traits(cls):
        return [trait for trait in cls.get_max_traits_total()]
    
    @classmethod
    def show_all_traits(cls):
        print(cls.get_all_traits())
    
    # PRIVATE METHODS
    @staticmethod
    def _ask_question(num, question):
        print(f"Q{num + 1}) {question.strip()}")
    
    @staticmethod
    def _show_choices(choices_arr):
        for i, choice_trait in enumerate(choices_arr):
            choice = choice_trait[0]
            print(f"{i + 1} - {choice.strip()}")
    
    @staticmethod
    def _get_ans():
        return input("Enter a number that corresponds with the choices: ")
    
    @staticmethod
    def _validate_ans(ans, total_choices):
        try:
            if int(ans) not in range(1, total_choices + 1):
                return False
        except ValueError:
            return False
        
        return True


class Quizzee:
    tested_traits = Quiz().get_all_traits()

    def __init__(self):
        # Create properties dynamatically based on traits in the quiz given
        self._create_properties()
        pass
    
    # PRIVATE METHODS
    def _create_properties(self):
        for trait in self.tested_traits:
            setattr(self, f"_{re.sub(r'[ -]', '_', trait).lower()}", 0)
        

# Testing Purposes
if __name__ == "__main__":
    q = Quiz()
    # Quiz.do_quiz()
    # q.show_all_traits()
    user = Quizzee()
    print(vars(user))