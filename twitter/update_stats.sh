mongo mole --quiet -eval "db.user.count()" > /var/www/html/mole/users.txt
mongo mole --quiet -eval "db.tweet.count()+db.stream.count() " > /var/www/html/mole/stream.txt
mongo mole --quiet -eval "db.tweet.count() " > /var/www/html/mole/tweet.txt
mongo mole --quiet -eval 'db.user.count({"followers.0":{$exists:true}})' > /var/www/html/mole/followers.txt
