import re
import yagmail
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


def validate_email(email):
    """Check if the provided string is a valid email format"""
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None


class EmailApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Sender email input
        self.sender_email = TextInput(hint_text='Your Email', multiline=False)
        layout.add_widget(self.sender_email)

        # Receiver email input with default value
        self.receiver_email = TextInput(hint_text='Receiver Email', multiline=False, text='default_receiver@example.com')
        layout.add_widget(self.receiver_email)

        # Subject input
        self.subject = TextInput(hint_text='Subject', multiline=False)
        layout.add_widget(self.subject)

        # Message input
        self.message = TextInput(hint_text='Message', size_hint_y=None, height=90)
        layout.add_widget(self.message)

        # Button to send email
        send_button = Button(text='Send Email')
        send_button.bind(on_press=self.send_email)
        layout.add_widget(send_button)

        # Status label
        self.status_label = Label(size_hint_y=None, height=44)
        layout.add_widget(self.status_label)

        return layout

    def send_email(self, instance):
        # Email format validation
        if not validate_email(self.sender_email.text) or not validate_email(self.receiver_email.text):
            self.status_label.text = 'Please provide valid email addresses.'
            return

        # Basic input validation
        if not (self.sender_email.text and self.receiver_email.text and self.subject.text):
            self.status_label.text = 'Please fill in the email, receiver, and subject fields.'
            return

        try:
            yag = yagmail.SMTP(os.environ.get("EMAIL_ID"), os.environ.get("APP_PASSWORD"))
            yag.send(
                to=self.receiver_email.text,
                subject=self.subject.text,
                contents=self.message.text
            )
            self.status_label.text = 'Email sent successfully!'
        except Exception as e:
            self.status_label.text = f'Error: {e}'


if __name__ == "__main__":
    EmailApp().run()
