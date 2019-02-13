import smtplib
import imaplib
import email
import mysql.connector

def checkMail():
    SMTP_SERVER = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(SMTP_SERVER, 993)
    #login to email and check inbox
    mail.login('<GMAIL ACCOUNT','GMAIL PASSWORD')
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
        sender = sender.replace("@mms.att.net",'')
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
    else:
        out = msg.get_payload()

    if(msg['Subject'] != None):
            return(sender + "\n" + msg['Subject'] + "\n" + out)
    else:
        return(sender + "\n" + out)

def check_contacts(number):
    #connect
    conn = mysql.connector.connect(host='localhost',
                                            user='<MySQLUSERNAME',
                                            password='<MySQLPASSWORD>',
                                            database = '<DATABASE NAME>')
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

def show_contacts():
    #connect
    conn = mysql.connector.connect(host='localhost',
                                            user='<MySQLUSERNAME',
                                            password='<MySQLPASSWORD>',
                                            database = '<DATABASE NAME>')
    mycursor = conn.cursor()
    #Create sql command to select all contacts
    sql = ("SELECT * from people")
    mycursor.execute(sql)
    record = mycursor.fetchall()
    #show each person
    return record

def sendmail(send_to, message):
    #setup connection
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    #login to gmail account
    server.login('<GMAIL ACCOUNT>', '<GMAIL PASSWORD>')
    try:
        if(isinstance(send_to, int)):
            send_to = str(send_to) + "@mms.att.net"
        server.sendmail('<SEND_FROM>', send_to, message)
    except:
            print("\nUnable to send mail to this address\n")

def write_a_message(send_to, message):
    #connect to contacts database and check for contact
    try:
        conn = mysql.connector.connect(host='localhost',
                                                user='<MySQLUSERNAME',
                                            password='<MySQLPASSWORD>',
                                            database = '<DATABASE NAME>')

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

        sendmail(num, message)
    #when no contact is found in database
    except:
        sendmail(send_to, message)

#add a contact to the database
def addContact(person, num):
    #connect to contacts database
    conn = mysql.connector.connect(host='localhost',
                                            user='<MySQLUSERNAME',
                                            password='<MySQLPASSWORD>',
                                            database = '<DATABASE NAME>')

    mycursor = conn.cursor()
    #create sql command
    sql = "INSERT INTO people (name, number) VALUES (%s, %s)"
    val = (person, num)
    #add the contact to database and commit
    mycursor.execute(sql, val)
    conn.commit()

def deleteContact(person):
    #connect
    conn = mysql.connector.connect(host='localhost',
                                            user='<MySQLUSERNAME',
                                            password='<MySQLPASSWORD>',
                                            database = '<DATABASE NAME>')

    mycursor = conn.cursor()
    #create sql delete command
    sql = "DELETE FROM people WHERE name = '%s'" % person
    #delete and commit
    mycursor.execute(sql)
    conn.commit()
