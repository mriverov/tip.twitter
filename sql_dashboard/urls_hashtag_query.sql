-- mole_urls (id_user, url)
-- mole_urlsgraph (user_oid_i, user_oid_j, ratio)
-- mole_centralityurl (user_id, centrality)

-- urls mas 'populares'
create table popular_urls (url varchar(150));
insert into popular_urls (url) (select max(url) from app_urls group by url order by count(url) desc limit 5);

#select max(url) from app_urls group by url order by count(url) desc limit 5;

-- usuarios mas populares
select screen_name, u.id, cu.centrality from mole_centralityurl cu
inner join mole_user u on (u.user_id = cu.user_id)
order by centrality desc 
limit 5

select screen_name as 'User', cu.centrality 'Centralidad'
from app_centralityurl cu 
inner join app_user u on (u.user_id = cu.user_id) 
where screen_name != "" 
order by cu.centrality desc  limit 5;

select screen_name as 'User', cu.centrality 'Centralidad'
from app_centralityhashtag cu 
inner join app_user u on (u.user_id = cu.user_id) 
where screen_name != "" 
order by cu.centrality desc  limit 5;


--- hashtag
create table popular_hashtags (hashtag varchar(150));
insert into popular_hashtags (hashtag) (select max(hashtag)
from app_hashtag 
group by hashtag 
order by count(hashtag) desc limit 5;;
