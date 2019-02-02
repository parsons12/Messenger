import smtplib
import imaplib
import email
import mysql.connector

#add a contact to the database
def add_contact(person, num):
    #connect to contacts database
    conn = mysql.connector.connect(host='localhost',
                                            user='<EnterUsername>',
                                            password='<EnterPassword>',
                                            database = '<EnterDBName>')

    mycursor = conn.cursor()
    #create sql command
    sql = "INSERT INTO people (name, number) VALUES (%s, %s)"
    val = (person, num)
    #add the contact to database and commit
    mycursor.execute(sql, val)
    conn.commit()

def delete_contact(person):
    #connect
    conn = mysql.connector.connect(host='localhost',
                                            user='<EnterUsername>',
                                            password='<EnterPassword>',
                                            database = '<EnterDBNAME>')

    mycursor = conn.cursor()
    #create sql delete command
    sql = "DELETE FROM people WHERE name = '%s'" % person
    #delete and commit
    mycursor.execute(sql)
    conn.commit()

def show_contacts():
    #connect
    conn = mysql.connector.connect(host='localhost',
                                            user='<EnterUsername>',
                                            password='<EnterPassword>',
                                            database = '<EnterDBNAME>')
    mycursor = conn.cursor()
    #Create sql command to select all contacts
    sql = ("SELECT * from people")
    mycursor.execute(sql)
    record = mycursor.fetchall()
    #show each person
    for person in record:
        print(person)

#
def check_contacts(number):
    #connect
    conn = mysql.connector.connect(host='localhost',
                                            user='<EnterUsername>',
                                            password='<EnterPassword>',
                                            database = '<EnterDBNAME>')
    mycursor = conn.cursor()
    #try to select person with info of sender
    sql = "SELECT name from people where number = '%s'" % number
    sender = ''
    try:
        mycursor.execute(sql)
        sender = mycursor.fetchall()
    except:
        pass
    word = ''
    #if person is not in contacts
    if(sender == [] or sender == ''):
        return number
    #if person is in contacts
    else:
        try:
            sender = sender[0]
            sender = sender[0]
        except:
            for letter in sender:
                word = word + letter
            return word
        return sender

def readmail():
    SMTP_SERVER = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(SMTP_SERVER, 993)
    #login to email and check inbox
    mail.login('<EnterGMAIL','<EnterPassword>')
    mail.select('inbox');
    #find unread mail
    result, data = mail.search(None, 'ALL', 'UNSEEN')
    mail_ids = data[0]
    id_list = mail_ids.split()
    #check if any new mail was retrieved
    if(id_list == []):
        m = "NO NEW MESSAGES"
        return m
    #find the newest email id
    latest_email_id = int(id_list[-1])
    #feth the newest email wtih id
    result, data = mail.fetch(str(latest_email_id), '(RFC822)' )
    #get all email information
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    msg.as_string()
    #retrieve who mail is from
    sender = msg['from']
    #if sent from a mobile phone (this only works for at&t)
    if '@mms.att.net' in sender:
        sender = sender.replace("@mms.att.net",'')#change this to send to other cell carriers
        #check if person is in contacts
        sender = check_contacts(sender)
    #if sent from an email
    else:
        #retrieve sender name and check contact info
        try:
            sender = sender.split('<')
            sender = sender[1]
            sender = sender.replace(">", '')
            sender = check_contacts(sender)
        except:
            sender = sender[0]
            sender = str(sender)
            sender.replace("[", '')
            sender.replace("'", '')
            sender.replace("]", '')
            sender = check_contacts(sender)
    #show who email is from
    print("\nFROM: " + sender + "\n")
    #show subject if there is one
    if(msg['Subject'] != None):
        print("Subject: " + msg['Subject'] + "\n")
    #check if the message is multipart
    if msg.is_multipart():
        out = ''
        for part in msg.walk():
                #if txt message
                if part.get_content_type() == 'text/html':
                    for i in range(352, len(part.get_payload())):
                        item = part.get_payload()
                        if(item[i] != '<' or item[i+1] != '/' or item[i+2] != 't'):
                            out = out + (part.get_payload()[i])
                        else:
                            break
                #if email
                if part.get_content_type() == 'text/plain' :
                    for i in range(0, len(part.get_payload())):
                        item = part.get_payload()
                        if(item[i] != '<' or item[i+1] != '/' or item[i+2] != 't'):
                            out = out + (part.get_payload()[i])
                        else:
                            break
        print(out)
    else:
        print(msg.get_payload())

    return(msg['From'])

def sendmail(send_to, message):
    #setup connection
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    #login to gmail account
    server.login('<EnterGMAIL>', '<EnterPassword>')
    try:
        if(isinstance(send_to, int)):
            send_to = str(send_to) + "@mms.att.net"
        server.sendmail('<EnterGMAIL>', send_to, message)
    except:
            print("\nUnable to send mail to this address\n",send_to)

def check_for_message():
    unread_from = readmail()
    if(unread_from == 'NO NEW MESSAGES'):
        print('\n'+unread_from)
    else:
        print("Message back?")
        answer = str(input())
        if(answer == 'yes' or answer == 'y'):
            send_to = unread_from
            print("What would you like to say?")
            message = str(input())
            sendmail(send_to, message)

def write_a_message():
    print("Who would you like to message?")
    send_to = input()
    #connect to contacts database and check for contact
    try:
        conn = mysql.connector.connect(host='localhost',
                                                user='<EnterUsername>',
                                                password='<EnterPassword>',
                                                database = '<EnterDBNAME>')

        mycursor = conn.cursor()
        sql = ("SELECT number from people WHERE name = '" + send_to + "'")
        mycursor.execute(sql)
        record = mycursor.fetchall()
        record = record[0]
        num = record[0]
        try:
            #if contact information is a phone number
            num = int(num)
        except:
            #if contact information is an email address
            pass
        print("What would you like to say?")
        message = str(input())
        sendmail(num, message)
    #when no contact is found in database
    except:
        print("NOT A CONTACT")


#Driver class to select commands
def main():
    reply = ''
    while(reply != 'exit'):
        print("\nCommands to type:")
        print("(checkInbox), (Compose), (addContact), (deleteContact), (showContacts), (exit)")
        reply = input()

        if(reply == 'checkInbox' or reply == 'checkinbox'):
            check_for_message()
        elif(reply == 'Compose' or reply == 'compose'):
            print("\nWrite a message? (yes or no)")
            reply = input()
            if(reply == 'yes' or reply == 'y'):
                write_a_message()
        elif(reply == 'exit' or reply == 'Exit'):
            reply = 'exit'
        elif(reply == 'addContact' or reply == 'addcontact'):
            print("Name of person:")
            person = input()
            print("Number or email address of person:")
            num = input()
            add_contact(person, num)
        elif(reply == 'deleteContact' or reply == 'deletecontact'):
            print("Name of contact to delete:")
            person = input()
            delete_contact(person)
        elif(reply == 'showContacts' or reply == 'showcontacts'):
            show_contacts()
        else:
            print("NOT A COMMAND")

main()
