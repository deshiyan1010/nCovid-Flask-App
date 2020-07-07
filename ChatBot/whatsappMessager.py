
from twilio.rest import Client

def message(country_code,number,text):

    number_str = "whatsapp:+"+str(country_code)+str(number)
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'ACd32d44dc1f8917f93b2738f2cfa070e3'
    auth_token = '8d03bf2f3fb999f8e4b6be41218ad67a'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body=text,
                                from_='whatsapp:+14155238886',
                                to=number_str
                            )

    return message.sid

if __name__=="__main__":

    print(message(91,7760849192,"Hello There"))