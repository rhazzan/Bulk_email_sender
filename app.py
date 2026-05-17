import streamlit as st
import pandas as pd
import smtplib as smtp
from email_sender import send_email

## Set up Streamlit page 
st.set_page_config(page_title = "Bulk Email Sender")
# Set up sidebar
st.sidebar.header("SMTP Settings")
server = st.sidebar.text_input("SMTP server","smtp.gmail.com")
port = st.sidebar.number_input("Port",value=587)
sender_email = st.sidebar.text_input("Sender email")
password = st.sidebar.text_input("Password",type='password')
starttls = st.sidebar.checkbox("Use TLS (STARTTLS)",value=True)

## set up main Page
st.title("Send Bulk Email")
file = st.file_uploader("Upload CSV or Excel file with contacts",accept_multiple_files=False,type=["csv","xlsx"])
if file:
    if file.type == "text/csv":
        df = pd.read_csv(file)
        st.text("Preview of uploaded data")
        st.dataframe(df.head(),hide_index=True,height=200)
    else:
        df = pd.read_excel(file)
        st.text("Preview of uploaded data")
        st.dataframe(df.head(),hide_index=True,height=230)
    st.space("xxsmall")
    email_column = st.selectbox("Select the column containing the email",df.columns,placeholder="Non selected")
    subject = st.text_input("Email Subject")
    send_as_html = st.checkbox("Send as HTML")
    email_body = st.text_area("Email Body (can be HTML if selected)",height=320)
    Preview_recepient = st.text_input("Preview recepient(optional). When set, only this address will receive the message")
    sendemail = st.button("Send Email",False)

    if sendemail:
        if not server:
            st.error("Please input a Server")
            st.stop()
        if not password:
            st.error("Please input a Password")
            st.stop()
        if not sender_email:
            st.error("Please input a sender_email")
            st.stop()
        if not email_body:
            st.error("Please input an email_body")
            st.stop()

        if not subject:
            st.error("Please input an email_subject")
            st.stop()
        
        if not Preview_recepient:
            send_to = [str(r).strip() for r in df[email_column].dropna().unique()]
        else:
            send_to = [str(Preview_recepient)]
            if not str(Preview_recepient).strip().__contains__("@" and "."):
                st.error("Please input a Valid email address")
                st.stop()

        status_area = st.empty()
        progress = st.progress(0)
        success = 0
        failure = []


        for i,r in enumerate(send_to,start = 1):
            if not str(r).strip().__contains__("@" or "."):
                st.error("Please input a Valid email address")
                st.stop()
            progress.progress(int((i/len(df))*100))
            status_area.text(f"Sending to {r} ({i}/{len(df)})...")
            try:
                send_email(server,port,sender_email,password,subject,email_body,r,use_tls=starttls,is_html=send_as_html)
                success += 1
            except Exception as e:
                if str(e) == "[Errno 11001] getaddrinfo failed":
                    failure.append(((r,"No Internet Connections")))
                else:
                    failure.append(((r,str(e))))
                    if len(failure) == len(df):
                        st.write(f"All email failed. Error: {failure[0][1]}")
                    else:
                        st.write("Failures(recepient,error):")
                        st.write(failure)
                        st.stop()
        st.success(f"Done. Success: {success}. Failed: {len(failure)}")
 
            
