select * from app_user au
where followers_count in (
	select max(u.followers_count)
	from app_user u
	inner join app_tweet tt on (tt.author_id = u.id)
	inner join app_trend at on (at.id = tt.trend_id)
	order by at.tweets_count desc
	group by tt.trend_id) limit 5;

SELECT date as 'Tweet date', 
	   tweets_count AS `Tweets Count` 
	   FROM `app_trend`


select * from app_user au
where followers_count in (
);

create temporary table max_followers (
	followers int 
)

insert into max_followers (followers) 
(select max(u.followers_count)
from app_user u 
inner join app_tweet tt on (tt.author_id = u.id) 
inner join app_trend at on (at.id = tt.trend_id) 
group by tt.trend_id order by at.tweets_count desc limit 10)


select u.screen_name, u.followers_count from 
app_user u 
where u.followers_count in (select followers from max_followers)

select u.id as 'user id', u.followers_count,  u.screen_name as 'username', tt.id as 'tweet id' #, tt.text as 'tweet'
from app_user u 
inner join app_tweet tt on (tt.author_id = u.id) 
inner join app_trend at on (at.id = tt.trend_id) 
group by tt.trend_id order by at.tweets_count desc limit 10;



select id from app_trend order by tweet_count desc limit 5

select * from app_tweet
where trend_id in (select id from app_trend order by tweet_count desc limit 5
)

select * app_user where id in (
select author_id from app_tweet
where trend_id in (select id from app_trend order by tweet_count desc limit 5
))