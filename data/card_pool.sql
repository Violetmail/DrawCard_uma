Create table card_pool(
pool_no INT primary key ,
pool_name char(30),
poo_up char(20) );

Create table card(
card_no INT primary key ,
card_name char(30),
card_kind char(10),
card_star char(5) );

Create table poolcard(
poocard_no INT primary key ,
pool_no int,
card_no int,
foreign key(pool_no) references card_pool(pool_no),
foreign key(card_no) references card(card_no));

Create table draw_log(
draw_no INT primary key ,
pool_no int,
card_no int,
foreign key(pool_no) references card_pool(pool_no),
foreign key(card_no) references card(card_no));
