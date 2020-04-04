import ezgmail

# The EZGmail module requires enabling the Google API:
# https://developers.google.com/gmail/api/quickstart/python
# The tutorial above will only enable read-only access.
# To actually send email, you need r/w access.
# You can grant these perms by manually importing the EZGmail module
# in a Python interpreter (command-line) and it will automatically 
# redirect you to the Google API site again and request r/w perms.

def send_email(email, body, subject=""):
    ezgmail.send(email, subject, body)