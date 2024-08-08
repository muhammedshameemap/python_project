#!/usr/bin/env python3

import os
import random


class Flashcard:
    """
    A class representing a flashcard with a question and an answer.

    Attributes:
        question (str): The question displayed on the flashcard.
        answer (str): The answer to the question on the flashcard.
    """

    def __init__(self, question, answer):
        """
        Initializes a new Flashcard object.

        Args:
            question (str): The question to be displayed on the flashcard.
            answer (str): The answer to the question on the flashcard.
        """
        self.question = question
        self.answer = answer


class FlashcardDeck:
    """
    A class that represents a deck of flashcards.

    Attributes:
        __ques_file (str): The file path for the questions.
        __ans_file (str): The file path for the answers.
        questions (list): A list of questions.
        answers (list): A list of answers.
        flashcards (list): A list of Flashcard objects.
    """

    def __init__(self, question_file, answer_file):
        """
        Initializes a FlashcardDeck object.

        Args:
            question_file (str): The file path for the questions.
            answer_file (str): The file path for the answers.
        """
        self.__ques_file = question_file
        self.__ans_file = answer_file
        self.questions = self.read_file(question_file)
        self.answers = self.read_file(answer_file)
        if len(self.questions) != len(self.answers):
            raise ValueError(
                "Number of questions and answers must be the same"
                )
        # Create a list of Flashcard objects
        self.flashcards = [Flashcard(q, a)
                           for q, a in zip(self.questions, self.answers)]

    @staticmethod
    def read_file(filename):
        """
        Read the contents of a file and return them as a list of lines.

        Args:
            filename (str): The name of the file to read.

        Returns:
            list: A list containing the lines read from the file.

        If the file is not found, an empty list is returned.
        """
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    @staticmethod
    def write_file(filename, data):
        """
        Write data to a file.

        Args:
            filename (str): The name of the file to write to.
            data (list): The data to write to the file.

        If an error occurs while writing to the file,
         an error message is printed.
        """
        try:
            with open(filename, 'w') as f:
                for line in data:
                    f.write(line + "\n")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def shuffle(self):
        random.shuffle(self.flashcards)

    def ask_questions(self):
        """
        Presents flashcards to the user and tracks their score.

        This method iterates through the flashcards in the
         `self.flashcards` list, asking the user the question
          for each flashcard. The user's answer is compared to the
           correct answer, and the score is updated accordingly.
        The user can quit the test at any time by typing 'q'.

        Args:
            Takes no args

        Returns:
            None
        """
        score = 0
        for flashcard in self.flashcards:
            # Ask the user the question and get their answer
            user_answer = input(f"{flashcard.question} (type 'q' to quit) ")
            # Check if the user wants to quit
            if user_answer.lower() == 'q':
                # Calculate the number of questions attempted
                attempted_questions = (
                        len(self.flashcards) -
                        (len(self.flashcards) -
                         self.flashcards.index(flashcard) - 1)
                    )
                # Print the final score and exit the function
                print(
                    f"Quitting the test. Your final score is {score}"
                    f" out of {attempted_questions}."
                    )
                return
            # Check if the user's answer is correct
            if user_answer.lower() == flashcard.answer.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is {flashcard.answer}.")
        # Print the final score after all flashcards have been presented
        print(f"Your final score is {score} out of {len(self.flashcards)}.")

    def add_question(self, question, answer):
        """
        Add a new question and answer to the deck.
        Args:
            question:
            answer:

        Returns:

        """
        self.questions.append(question)
        self.answers.append(answer)
        self.flashcards.append(Flashcard(question, answer))
        self.write_file(self.__ques_file, self.questions)
        self.write_file(self.__ans_file, self.answers)

    def delete_question(self, question):
        """
        Delete a question and answer from the deck.
        Args:
            question:

        Returns:

        """
        if question in self.questions:
            index = self.questions.index(question)
            del self.questions[index]
            del self.answers[index]
            self.flashcards = [Flashcard(q, a) for q, a in zip(
                self.questions, self.answers
                )]
            self.write_file(self.__ques_file, self.questions)
            self.write_file(self.__ans_file, self.answers)
        else:
            print("Question not found.")


def flashcard_app():
    try:
        question_file = input("Enter the question file: ")
        answer_file = input("Enter the answer file: ")

        # Check if both question and answer files are provided
        if question_file == "" or answer_file == "":
            # raise ValueError("Both question and answer files are required.")
            print("Both question and answer files are required.")

        # Check if both question and answer files exist
        if (not os.path.exists(question_file)
                or not os.path.exists(answer_file)):
            # if not, create new question and answer files (empty files)
            print(
                "No existing question and answer files found."
                "\n...Creating new question and answer files..."
                )
            question_file = "questions"
            answer_file = "answers"
            with open(question_file, 'w') as f:
                f.write("")
            with open(answer_file, 'w') as f:
                f.write("")

        while True:
            print("Options Available:")

            # Check if question file is empty
            is_question_file_empty = open(question_file).read() == ""
            if not is_question_file_empty:
                # if not empty, option 1 is available
                print("1. Take the test")
            print("2. Add a question")
            print("3. Delete a question")
            print("4. Quit")
            option = input("Choose an option: ")
            if option == "1" and not is_question_file_empty:
                deck = FlashcardDeck(question_file, answer_file)
                deck.shuffle()
                deck.ask_questions()
            elif option == "2":
                question = input("Enter the question: ")
                answer = input("Enter the answer: ")
                deck = FlashcardDeck(question_file, answer_file)
                deck.add_question(question, answer)
            elif option == "3":
                question = input("Enter the question to delete: ")
                deck = FlashcardDeck(question_file, answer_file)
                deck.delete_question(question)
            elif option == "4":
                print("Thank you!")
                break
            else:
                # if not, invalid option is provided
                print("Invalid option. Please try again.")
    except Exception as e:
        # if any error occurs, an error message is printed, and exits
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    flashcard_app()
