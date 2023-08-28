Create table card_pool(
pool_no INT primary key ,
pool_name char(30),
pool_up char(20) );

Create table card(
card_no INT primary key ,
card_name char(30),
card_kind char(10),
card_star char(5) );

Create table poolcard(
poolcard_no INTEGER primary key ,
pool_name char(30),
card_name char(30)
);

Create table draw_log(
draw_no INTEGER primary key ,
pool_name char(30),
card_name char(30));
