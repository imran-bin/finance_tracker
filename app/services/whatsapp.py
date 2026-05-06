import pywhatkit as kit

def send_whatsapp(phone, msg):
    kit.sendwhatmsg_instantly(phone, msg, wait_time=10)