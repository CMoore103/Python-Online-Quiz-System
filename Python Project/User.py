from UserData import *
from rapidfuzz import fuzz

class User:
        def __init__(self, username, password, role, quiz_scores=None):
            """
            Initialize a User object.
            :@param username: The username of the user.
            :@param role: The role of the user ('student' or 'instructor').
            """
            self.username = username
            self.password = password
            self.role = role
            self.quiz_scores =quiz_scores if quiz_scores is not None else []

            if role.lower() not in ['student', 'instructor']:
                raise ValueError("Role must be either 'student' or 'instructor'.")
            self.role = role.lower()

        def is_instructor(self):
            """
            Check if the user is an instructor.
            """
            return self.role == 'instructor'

        def __str__(self):
            """
            String representation of the User.
            """
            return f"User: {self.username}, Role: {self.role.capitalize()}"
        
        @staticmethod
        def register_user(username, password, role):
             """
        Register a new user by saving their credentials to a text file.
        :@param username: Username chosen by the user.
        :@param password: Password chosen by the user.
        :@param role: Role of the user ("student" or "instructor").
        """
             user_data = load_user_data()

             if username in user_data:
                 print(f"Username {username} already exists")
             else:
                 user_data[username] = {
                     "Password" : password ,
                     "Role" : role ,
                     "Quiz Scores" : []
                 }

                 save_user_data(user_data)
                 print("Successfully Registered")
        
        @staticmethod
        def login_user(username, password):
             """
            Log in an existing user by checking credentials against stored data.
            :@param username: Username provided by the user.
            :@param password: Password provided by the user.
            :return: User object if credentials match, otherwise None.
            """
             user_data = load_user_data()

             if username in user_data:
                 stored_password = user_data[username]["Password"]
                 stored_role = user_data[username]["Role"]
                 quiz_scores = user_data[username]["Quiz Scores"]

                 if password == stored_password:
                     print(f"Login successful: Welcome {username}")

                     if stored_role == "instructor":
                         return Instructor(username, password)
                     else:
                         return User(username, stored_password, stored_role, quiz_scores)
        
             print("Invalid username and/or password")
             return None
        
        def logout(user):
            """
            Log out a user and save their data
            @param user : The user to be logged out
            """

            user.save()
            print("Logged out")
        

             
        def take_quiz(self):
            """
            Allow the user to take a quiz
            """
            from QuizManager import QuizManager
            QuizManager.begin_quiz(self)
        
        def add_quiz_score(self, score):
            """
            Add a quiz score to the user's score history, each 
            score history contains no more than the last 10
            quiz attempts

            :param score: The quiz score to be added to the score history
            """

            self.quiz_scores.append(score)
            if len(self.quiz_scores) > 10:
                self.remove_oldest_score()
        
        def remove_oldest_score(self):
            """
            Remove oldest quiz score from the user's score history
            """

            if self.quiz_scores:
                removed_score = self.quiz_scores.pop(0)
                print("Oldest score removed: ")
            else:
                print("No score history present. ")

        def view_quiz_scores(self):
            """
            View the users last 10 score attempts
            """

            if not self.quiz_scores:
                print(f"No scores for {self.username} to report")
            else:
                print(f"{self.username} score history")
                for idx, score in enumerate(self.quiz_scores, start = 1):
                    print(f" Attempt {idx} : {score}")

        def save(self):
            """
            Save the user's updated data back to the JSON file
            """

            user_data = load_user_data()
            user_data[self.username] = {
                "Password" : self.password,
                "Role" : self.role ,
                "Quiz Scores" : self.quiz_scores,
            }

            save_user_data(user_data)

                          
        
class Instructor(User):
    def __init__(self, username, password):
        """
        Initialize an Instructor object.
        :param username: The username of the instructor.
        """
        super().__init__(username, password, "instructor")  # Automatically set role to 'instructor'

    def view_all_questions(self):
        """
        Display all questions in the question bank.
        """

        from QuizManager import QuizManager

        questions = QuizManager.load_questions()
        if not questions:
            print("No questions available in the question bank.")
            return
        for qid, question in questions.items():
            print(f"ID: {qid}, Question: {question['Question']}")

    def add_question(self):
        """
        Add a question to the question bank.
        :@param question: A dictionary containing question details (Question, Options, Answer).
        """

        from QuizManager import QuizManager

        questions = QuizManager.load_questions()
        question = input("\nPlease enter the question you wish to add ")

        for exisitng_question in questions.values():
            existing_text = exisitng_question.get("Question", "").strip()
            similarity = fuzz.ratio(question.lower(), existing_text.lower()) #Calculate a similarity ratio between the question you wish to enter, and the questions on file

            if similarity >= 70:
                print(f"Similar question already exists: Similarity = {similarity}")
                return
        

    
        options = []
        for i in range(4):
            option = input("Enter one of the options: ")
            options.append(option)
        
        #Get the correct answer to the question
        correct_answer = input("From the options entered, which one is the correct answer? ").strip()


        while (correct_answer not in options): #While the user enters an answer not listed in the options, prompt them to re-enter the answer
            print("Please enter a valid option")
            correct_answer = input("From the options entered, which one is the correct answer? ")


        new_question = { #Organize the new question
            "Question" : question ,
            "Options" : options , 
            "Answer" : correct_answer
        }

        question_id = f"{len(questions) + 1}"  # Generate a new unique ID
        questions[question_id] = new_question
        
        QuizManager.save_questions(questions) #Add the new question to the question bank
        print(f"Question added successfully with ID {question_id}. ")

    def remove_question(self):
        """
        Remove a question from the question bank.
        :@param question_id: The ID of the question to remove.
        """
        from QuizManager import QuizManager

        self.view_all_questions() #Display all questions currently in the list

        question_id = input("Please select the question you wish to remove (Enter the ID)\t") #Select the ID of the question you wish to remove

        questions = QuizManager.load_questions()
        if question_id in questions:
            del questions[question_id]
            QuizManager.save_questions(questions)
            print(f"Question with ID {question_id} removed successfully.")
        else:
            print(f"Question with ID {question_id} not found.")

    def modify_question(self):
        """Allow instructor to modify an existing question."""

        from QuizManager import QuizManager

        questions = QuizManager.load_questions()
        if not questions:
            print("No questions available to modify.")
            return

        print("Existing questions:")
        self.view_all_questions()

        question_id = input("Enter the ID of the question to modify: ")
        if question_id in questions:
            new_question = input("Enter the new question: ")
            options = [input(f"Enter option {chr(65 + i)}: ") for i in range(4)]
            correct_answer = input("Enter the correct answer (A/B/C/D): ").strip().upper()

            if correct_answer not in ['A', 'B', 'C', 'D']:
                print("Invalid answer option.")
                return

            questions[question_id] = {
                "Question": new_question,
                "Options": options,
                "Answer": options[ord(correct_answer) - 65]
            }
            QuizManager.save_questions(questions)
            print(f"Question {question_id} modified.")
        else:
            print("Question ID not found.")

   
    