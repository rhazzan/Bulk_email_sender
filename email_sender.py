from email.message import EmailMessage
import smtplib

def send_email(smtp_server: str, port: int, username: str, password: str, subject: str, body: str, to_email: str, use_tls: bool = True, is_html: bool = False, timeout: int = 30):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = to_email

    if is_html:
        msg.set_content('This email contains HTML. Please view in an HTML-capable client.')
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    with smtplib.SMTP(smtp_server, port, timeout=timeout) as server:
        if use_tls:
            server.starttls()
        server.login(username, password)
        server.send_message(msg)

def sendmail(password,sender_email,host,port,subject,ttls,To,body,is_HTML:bool,timeout: int = 30):
    message = EmailMessage()
    message["To"] = To
    message["From"] = sender_email
    message["Subject"] = subject
    if is_HTML:
        message.set_content('This email contains HTML. Please view in an HTML-capable client.')
        message.add_alternative(body, subtype='html')
    else:
        message.set_content(body)
        with smtplib.SMTP(host,port,timeout=timeout) as server:
            if ttls:
                server.starttls()
            server.login(sender_email, password)
            server.send_message(message)






