from tkinter import *
from tkinter import messagebox as mb
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

root = Tk()
root.iconbitmap("icon.ico")
root.title('Sistema de envio de correos Redsalud')

sender_email = 'cmn.kkckdbb@gmail.com'

def check_password():
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, password_input.get())
        mb.showinfo(title='Loggeado correctamente', message='Contraseña correcta')
    except:
        mb.askretrycancel(title='Contraseña incorrecta', message='Reingrese la contraseña')


password_label = Label(root, text='Contraseña: ')
password_input = Entry(root, show='*')
password_label.grid(row=0, column=0)
password_input.grid(row=0, column=1)
password = password_input.get()

blank_label = Label(root, text="")
blank_label.grid(row=1)
b1 = Button(root, text='Verificar contraseña', command=check_password)
b1.grid(row=1, column=1)

email_label = Label(root, text='E-mail: ')
email_input = Entry(root)
email_label.grid(row=2, column=0)
email_input.grid(row=2, column=1)
receiver_email = email_input.get()

message = MIMEMultipart('alternative')
message["To"] = receiver_email
message["Subject"] = 'Comprobante cita, Clinica Redsalud Providencia'
message["From"] = sender_email

prof_label = Label(root, text='Nombre profesional: ', state='disabled')
prof_input = Entry(root, state='disabled')
prof_label.grid(row=3, column=0)
prof_input.grid(row=3, column=1)

fecha_label = Label(root, text='Fecha examen: ')
fecha_input = Entry(root)
fecha_label.grid(row=5, column=0)
fecha_input.grid(row=5, column=1)

hora_label = Label(root, text='Hora examen: ')
hora_input = Entry(root)
hora_label.grid(row=6, column=0)
hora_input.grid(row=6, column=1)

examen_label = Label(root, text='Examen: ')
examen_input = Entry(root)
examen_label.grid(row=7, column=0)
examen_input.grid(row=7, column=1)

def activate_prof():
    if is_checked.get():
        prof_label.configure(state='active')
        prof_input.configure(state='normal')
    else:
        prof_label.configure(state='disabled')
        prof_input.configure(state='disabled')

is_checked = IntVar()
Checkbutton(root, text='Profesional asignado',
            variable=is_checked, onvalue=1, offvalue=0, command=activate_prof).grid(row=4, column=1, sticky=W)

def env_mail():
    if is_checked.get():
        f = open('mail_prof_text.txt', 'r')
        mail_prof_text = f.read().format(prof_input.get(), examen_input.get(), fecha_input.get(), hora_input.get())
        f2 = open('mail_prof_html.txt', 'r')
        mail_prof_html = f2.read().format(prof_input.get(), examen_input.get(), fecha_input.get(), hora_input.get())
        chosen_text = mail_prof_text
        chosen_html = mail_prof_html
        f.close()
        f2.close()
    else:
        f = open('mail_no_prof_text.txt', 'r')
        mail_no_prof_text = f.read().format(examen_input.get(), fecha_input.get(), hora_input.get())
        f2 = open('mail_no_prof_html.txt', 'r')
        mail_no_prof_html = f2.read().format(examen_input.get(), fecha_input.get(), hora_input.get())
        chosen_text = mail_no_prof_text
        chosen_html = mail_no_prof_html
        f.close()
        f2.close()

    mail_mime_text = MIMEText(chosen_text, "plain")
    mail_mime_html = MIMEText(chosen_html, "html")

    message.attach(mail_mime_text)
    message.attach(mail_mime_html)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password_input.get())
        server.sendmail(
            sender_email, email_input.get(), message.as_string()
        )

def clear_fields(): # borra los campos
    prof_input.delete(0, END)
    prof_input.insert(0, "")
    email_input.delete(0, END)
    email_input.insert(0, "")
    fecha_input.delete(0, END)
    fecha_input.insert(0, "")
    hora_input.delete(0, END)
    hora_input.insert(0, "")
    examen_input.delete(0, END)
    examen_input.insert(0, "")

enviar_correo = Button(root, text='Enviar correo', command=env_mail)
enviar_correo.grid(row=8, column=0)

clear = Button(root, text='Borrar datos', command=clear_fields)
clear.grid(row=8, column=1)


root.mainloop()