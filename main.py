import tkinter as tk
from tkinter import messagebox, Toplevel
import speech_recognition as sr
from datetime import datetime

class InterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interview App")

        self.interviewee_info = {}
        self.session_start_time = None

        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root, width=50)
        self.name_entry.pack()

        self.email_label = tk.Label(root, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(root, width=50)
        self.email_entry.pack()

        self.questions = [
            "Tell me about yourself.",
            "What is your greatest strength?",
            "What is your greatest weakness?",
            "Why do you want to work here?",
        ]

        self.current_question_index = 0

        self.question_label = tk.Label(root, text=self.questions[self.current_question_index])
        self.question_label.pack()

        self.answer_entry = tk.Entry(root, width=50)
        self.answer_entry.pack()

        self.next_question_button = tk.Button(root, text="Next Question", command=self.next_question)
        self.next_question_button.pack()

        self.speech_to_text_button = tk.Button(root, text="Speech to Text", command=self.speech_to_text)
        self.speech_to_text_button.pack()

        self.show_database_button = tk.Button(root, text="Show Database", command=self.show_database)
        self.show_database_button.pack()

        self.clear_database_button = tk.Button(root, text="Clear Database", command=self.clear_database)
        self.clear_database_button.pack()

        self.answer_entry.bind('<Return>', lambda event=None: self.next_question())

        self.recognizer = sr.Recognizer()

    def next_question(self):
        answer = self.answer_entry.get()
        if not answer:
            messagebox.showerror("Error", "Please provide an answer.")
            return

        if self.current_question_index == 0:
            name = self.name_entry.get()
            email = self.email_entry.get()
            self.interviewee_info["Name"] = name
            self.interviewee_info["Email"] = email
            self.session_start_time = datetime.now()
            self.save_interviewee_info(name, email)

        self.save_answer(self.questions[self.current_question_index], answer)

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question_index])
            self.answer_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Interview Complete", "Thank you for completing the interview.")
            self.save_session_end_time()

    def save_interviewee_info(self, name, email):
        with open("interview_data.txt", "a") as file:
            file.write(f"Session started at: {self.session_start_time}\n")
            file.write(f"Name: {name}\n")
            file.write(f"Email: {email}\n")
            file.write("\n")

    def save_session_end_time(self):
        with open("interview_data.txt", "a") as file:
            file.write(f"Session ended at: {datetime.now()}\n")
            file.write("-" * 40 + "\n\n")

    def save_answer(self, question, answer):
        with open("interview_data.txt", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Question: {question}\n")
            file.write(f"Answer: {answer}\n")
            file.write("\n")

    def show_database(self):
        database_window = Toplevel(self.root)
        database_window.title("Database")

        with open("interview_data.txt", "r") as file:
            data = file.read()

        text_widget = tk.Text(database_window)
        text_widget.insert(tk.END, data)
        text_widget.pack()

    def clear_database(self):
        with open("interview_data.txt", "w") as file:
            file.truncate(0)
        messagebox.showinfo("Database Cleared", "The database has been cleared.")

    def speech_to_text(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, "Listening...")

            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.insert(0, text)
            except sr.UnknownValueError:
                messagebox.showerror("Speech Recognition Error", "Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                messagebox.showerror("Speech Recognition Error", f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewApp(root)
    root.mainloop()
