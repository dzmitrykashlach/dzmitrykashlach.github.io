---
layout: post
title:  "Functional indexing"
date:   2024-04-11 17:37:07 +0300
categories: sql
---
&nbsp;&nbsp; I've decided to recap everything that I know about SQL indexes by this moment, and the book [USE THE INDEX, LUKE!](https://use-the-index-luke.com/) by Markus Winand looks perfect target which could guide me through this journey.  
&nbsp;&nbsp; In this post I've dive a bit into [functional indexes](https://use-the-index-luke.com/sql/where-clause/functions/user-defined-functions) - a special type of indexes, which are used for the cases when you have arithmetic function in `where` operator instead of static statement.  
&nbsp;&nbsp; So, here is an experiment.  
&nbsp;&nbsp; Let's create heavy table using the following SQL  
{% highlight sql %}  
CREATE TABLE scale_data (
section NUMERIC NOT NULL,
id1     NUMERIC NOT NULL,
id2     NUMERIC NOT NULL
);

INSERT INTO scale_data
SELECT sections.*, gen.*
, CEIL(RANDOM()*100)
FROM GENERATE_SERIES(1, 300)     sections,
GENERATE_SERIES(1, 900000) gen
WHERE gen <= sections * 3000;
{% endhighlight %}  
and check how much time will take simple select with `where` operator:  
{% highlight sql %}
explain analyze select id1 from scale_data sd where id1 > 899990;

Gather  (cost=1000.00..1567682.25 rows=13545 width=6) 
(actual time=15693.038..15710.051 rows=10 loops=1)
...
->  Parallel Seq Scan on scale_data sd  (cost=0.00..1565327.75 rows=5644 width=6) 
(actual time=15661.368..15661.369 rows=3 loops=3)
Filter: (id1 > '899990'::numeric)
Rows Removed by Filter: 45149997
...
Execution Time: 16073.845 ms
{% endhighlight %}  

&nbsp;&nbsp; Ok, ~16s.  
&nbsp;&nbsp; Now, let's add simple index to the `id1` column and re-check execution time again - 0.052ms, which is fine, because as we know, indexes improve performance at the cost of additional space usage. In our case table occupies ~50% more space (9.4G compared with 6.6G without index).  
But what will happen, if we use an arithmetic function in where clause?  
{% highlight sql %}  
explain analyze select id1 from scale_data sd where id1-5 > 899990;
Seq Scan on scale_data sd  (cost=0.00..2891609.00 rows=45150000 width=6) 
(actual time=73.147..36141.529 rows=5 loops=1)
...
Execution Time: 36142.316 ms
{% endhighlight %}  
&nbsp;&nbsp; Hm, execution time increased by 2 times, and it's clear why: `id1x` cannot be used anymore because in `where` we have arithmetic function, so time-consuming `Seq Scan` is performed.  
Fortunately, PostgreSQL have functional indexes, when index can be created not for clear column name, but for function. Let's try it.  
{% highlight sql %}
create index id1x_m_5 on scale_data ((id1-5))
{% endhighlight %}  
&nbsp;&nbsp; Although query takes now 25s instead of 36s (which is unexpected improvement for me), we see that index is not used during query execution.  
&nbsp;&nbsp; Additionally, with the 2nd index `id1x_minus_5` table has started to occupy 12G, which is 2 times increase compared to initial value.

{% highlight sql %}
Seq Scan on scale_data sd  (cost=0.00..2891609.00 rows=45150000 width=6)
(actual time=25389.553..25389.554 rows=5 loops=1)
...
Execution Time: 25389.815 ms
{% endhighlight %}  
&nbsp;&nbsp; My guess is that it may happen because of `>` operator. Let's change it to `=` and re-check.
{% highlight sql %}
Gather  (cost=13689.26..1718978.07 rows=677250 width=6) 
(actual time=25.943..26.046 rows=1 loops=1)
...
->  Parallel Bitmap Heap Scan on scale_data sd  
(cost=12689.26..1650253.07 rows=282188 width=6) 
(actual time=8.604..8.606 rows=0 loops=3)
Recheck Cond: ((id1 - '5'::numeric) = '899990'::numeric)
Heap Blocks: exact=1
->  Bitmap Index Scan on id1x_minus_5  (cost=0.00..12519.94 rows=677250 width=0) 
(actual time=0.018..0.018 rows=1 loops=1)
Index Cond: ((id1 - '5'::numeric) = '899990'::numeric)
...
Execution Time: 26.384 ms
{% endhighlight %}  
&nbsp;&nbsp; Execution time dropped to 26ms and `explain analyze` is showing that index was scanned.  
But we still need to have `>` and not `=`, so how should we act here?  
There is one more type of indexes, which can cover only selected range of values - [partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html).  
So, why not to try to mix them with functional ones?

{% highlight sql %}
create index id1x_m_5_partial on scale_data ((id1-5)) where (id1-5) > 899990
{% endhighlight %}  
&nbsp;&nbsp; Bingo!
{% highlight sql %}
Bitmap Heap Scan on scale_data sd  (cost=11295.66..2851286.60 rows=45150000 width=6) 
(actual time=26.890..26.897 rows=5 loops=1)
Recheck Cond: ((id1 - '5'::numeric) > '899990'::numeric)
Heap Blocks: exact=1
->  Bitmap Index Scan on id1_m_5_partial  (cost=0.00..8.16 rows=45150000 width=0) 
(actual time=0.010..0.010 rows=5 loops=1)
...
Execution Time: 27.140 ms
{% endhighlight %}  
&nbsp;&nbsp; Execution time dropped to 27ms at the cost of specifying exact range which we're going to use in `where` clause.  
How about disc space utilization?  
&nbsp;&nbsp; I've dropped `id1x` and `id1x_minus_5` indexes, and table size is back to initial value which shows that partial indexes are very compact.

#### Conclusion.  
&nbsp;&nbsp; 1) Functional indexes are helpful in narrow specific cases when we have to use expressions in `where` operator.  
&nbsp;&nbsp; 2) They are not a silver bullet and in some cases (like with `>`) might just not work.  
&nbsp;&nbsp; 3) It's possible to mix them with partial index for gaining flexibility.  
&nbsp;&nbsp; 4) It's very good practice to define area of index usage precisely, because (in general) it helps to select appropriate type of index and thus to save disc space and improve time execution.

&nbsp;&nbsp; Keep indexing! See you!