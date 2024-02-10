import json
import sys
import re


class Quiz:
    def __init__(self, quiz, quizzee=None):
        self.quiz = json.load(open(quiz))
        self.quizzee = quizzee
    
    # All questions and entering answers occur here
    def do_quiz(self):
        for i, question in enumerate(self.quiz):
            # Ask 1 question at a time
            self._ask_question(i, question["question"])

            # Show choices for question
            self._show_choices(question["choices_and_traits"])

            # Loop until user enters elgible answer
            while True:
                total_choices = len(question["choices_and_traits"])
                ans = self._get_ans()
                if self._validate_ans(ans, total_choices) == True:
                    trait_arr = question["choices_and_traits"][int(ans) - 1][1:]
                    self.quizzee._add_trait_pts(*trait_arr)
                    break

    # NONPRIVATE METHODS
    # Get max total of each trait
    def get_max_traits_total(self):
        traits = {}
        for _, question in enumerate(self.quiz):
            for _, choice_trait in enumerate(question["choices_and_traits"]):
                # [1:] b/c some choice linked with > 1 traits
                for trait in choice_trait[1:]:
                    trait_formatted = trait.strip().lower()
                    if trait_formatted not in traits:
                        traits[trait_formatted] = 1
                    else:
                        traits[trait_formatted] += 1

        return dict(sorted(traits.items()))
    
    def show_max_traits_total(self):
        print(self.get_max_traits_total())

    def get_all_traits(self):
        return [trait for trait in self.get_max_traits_total()]
    
    def show_all_traits(self):
        print(self.get_all_traits())
    
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


class Quizzee():
    def __init__(self):
        pass
    
    # Create properties dynamatically based on traits in the quiz given
    def traits_to_track(self, test_traits):
        for trait in test_traits:
            setattr(self, f"_{re.sub(r'[ -]', '_', trait).lower()}", 0)
    
    # UNDER EDIT
    def _add_trait_pts(self, *traits):
        print("add trait pts working")
        

# Testing Purposes
if __name__ == "__main__":
    user = Quizzee()
    quiz = Quiz("questions.json", user)
    user.traits_to_track(quiz.get_all_traits())

    # quiz.do_quiz()
    # print(vars(user))