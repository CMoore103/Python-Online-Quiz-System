from QuizManager import QuizManager
from User import User, Instructor
import sys

def menu():
    print("Welcome to the Online Quiz System!")
    print("----------------------------------")

    while True:
        print("1.) Register")
        print("2.) Login")
        print("3.) Exit")

        choice = int(input("Please select one of the three options: "))

        if choice == 1:
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            role = input("Are you a student or a instructor?").strip().lower()
            if role not in ["student", "instructor"]:
                print("Invalid role, please enter Student or Instructor")
                continue
            User.register_user(username, password, role)
        elif choice == 2:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            user = User.login_user(username, password)

            if user:
                if user.role == "student":
                    student_menu(user)
                elif user.role == "instructor":
                    instructor_menu(user)

        elif choice == 3:
            print("Thank you for using the Online Quiz System! ")
            sys.exit(0)

def student_menu(user):
    """
    Menu for students, allowing them to take a quiz and view their scores 

    """

    while True:
        print("\n--- Student Menu ---")
        print("1. Take Quiz")
        print("2. View Quiz Scores")
        print("3. Log Out")
        choice = input("Please select an option: ")

        if choice == "1":
            # Start the quiz for the student
            user.take_quiz()

        elif choice == "2":
            # Display quiz scores
            print(f"Quiz Scores for {user.username}: {user.quiz_scores}")

        elif choice == "3":
            # Log out
            user.save()  # Save any data if needed before logging out
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")

def instructor_menu(user):
     """
     Menu for instructors, allowing them to add, remove, or modify existing questions
     """
     while True:
        print("\n--- Instructor Menu ---")
        print("1. Add Question")
        print("2. Modify Question")
        print("3. Remove Question")
        print("4. View All Questions")
        print("5. Log Out")
        choice = input("Please select an option: ")

        if choice == "1":
            # Add a question to the question bank
            print("\n",user.add_question())

        elif choice == "2":
            # Modify an existing question
            user.modify_question()

        elif choice == "3":
            # Remove a question from the question bank
            user.remove_question()

        elif choice == "4":
            # View all questions in the question bank
            user.view_all_questions()

        elif choice == "5":
            # Log out
            user.save()  # Save any data if needed before logging out
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


                            



                    
                    


            
            


