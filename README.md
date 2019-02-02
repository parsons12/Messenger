# Messenger
A messenger program that runs in terminal. Receives and sends emails through a Gmail account. Also connects to local MySQL database to hold contact information of people.

Currently only supports sending messeages to email accounts or AT&T customers.
To send messages to other cell phone carriers change line #165. See https://20somethingfinance.com/how-to-send-text-messages-sms-via-email-for-free/ for cell phone carriers.

To allow your gmail to be connected you must change your gmail setting to allow less secure apps. See https://devanswers.co/allow-less-secure-apps-access-gmail-account/

Additional changes in the code are needed to connect to your Gmail account as well as a local database you create as well as the table name(I recommend naming the table people so you don't have to change the code).
Example of the table and its variables are in table.png and setup.png.


