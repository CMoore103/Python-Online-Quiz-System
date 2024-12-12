import json
import random
from User import User
from UserData import *

class QuizManager:
    """A static class for managing quiz questions."""
    
    @staticmethod
    def load_questions(filename="QuestionBank.json"):
        """
        Load questions from a JSON file.
        :param filename: The JSON file containing questions.
        :return: A dictionary of questions.
        """
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"The file {filename} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file {filename}.")
            return {}

    @staticmethod
    def save_questions(questions, filename="QuestionBank.json"):
        """
        Save questions to a JSON file.
        :param questions: A dictionary of questions.
        :param filename: The JSON file to save questions to.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(questions, f, indent=4)
                print(f"Questions saved successfully to {filename}.")
        except Exception as e:
            print(f"Error saving questions: {e}")

    @staticmethod
    def get_questions(questions, num_questions=10):
        """
        Randomize and retrieve a set number of questions.
        :param questions: The dictionary of all questions.
        :param num_questions: Number of questions to retrieve.
        :return: A subset of questions.
        """
        question_ids = list(questions.keys())
        random.shuffle(question_ids)
        selected_ids = question_ids[:num_questions]
        return {qid: questions[qid] for qid in selected_ids}

    @staticmethod
    def begin_quiz(user):
        """
        Start a new quiz session.
        """
        correct = 0
        incorrect = 0

        questions = QuizManager.load_questions()
        if not questions:
            print("No questions available to start the quiz.")
            return

        randomized_questions = QuizManager.get_questions(questions)

        for question in randomized_questions.values():
            if QuizManager.ask_question(question):
                correct += 1
            else:
                incorrect += 1

        print("\n===== Quiz Results =====")
        print(f"Correct answers: {correct}")
        print(f"Incorrect answers: {incorrect}")
        total = correct + incorrect
        score = (correct / total) * 100
        print(f"Score: {score:.2f}")
        user.add_quiz_score(score)
        user.save()
        

    @staticmethod
    def ask_question(question):
        """
        Ask a single question to the user.
        :param question: The question data as a dictionary.
        :return: True if the answer is correct, False otherwise.
        """
        print(question["Question"])
        options = question["Options"].copy()
        random.shuffle(options)
        letters = ['A', 'B', 'C', 'D']
        option_map = {letters[i]: options[i] for i in range(len(options))}

        for letter, option in option_map.items():
            print(f"{letter}: {option}")

        user_choice = input("Your answer: ").strip().upper()

        if user_choice not in option_map:
            print("Invalid choice. Try again.")
            return QuizManager.ask_question(question)

        if option_map[user_choice] == question["Answer"]:
            print("Correct!\n")
            return True
        else:
            print(f"Incorrect! The correct answer was: {question['Answer']}\n")
            return False