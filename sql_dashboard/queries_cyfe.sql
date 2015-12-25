
-- Usuarios mas populares
create table max_followers_trend (
	followers int 
);

insert into max_followers_trend (followers) 
(select max(u.followers_count)
from app_user u 
inner join app_tweet tt on (tt.author_id = u.id) 
inner join app_trend at on (at.id = tt.trend_id) 
group by tt.trend_id order by at.tweets_count desc limit 10);


select u.screen_name as 'Usuario', u.followers_count as 'Cantidad de seguidores'
from 
app_user u 
where u.followers_count in (select followers from max_followers_trend);


-- Tweets mas populares
select text as 'Tweet', created_at as 'Fecha 'from app_tweet where retweet_count in (
select max(tt.retweet_count) as 'cant'
from app_tweet tt
group by tt.trend_id order by 'cant' desc ) limit 5;

-- Query de ejemplo Cyfe
SELECT * FROM (SELECT `screen_name` AS `Name`, `followers_count` AS `Followers` 
	FROM `app_user` WHERE followers_count > 0 ORDER BY `followers_count` DESC) as `tb1` 
UNION SELECT 'Color', '#009dee'