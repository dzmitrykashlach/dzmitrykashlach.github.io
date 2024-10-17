---
layout: post
title: "UUID in SQL: insert & reindex performance"
date: 2024-08-14 10:00:00 +0300
categories: sql 
---

&nbsp;&nbsp; This article is inspired by discussion about is it worth using `UUID` as primary key for Hibernate entity to overcome issue with [`equals()` & `hashCode()`](https://thorben-janssen.com/lombok-hibernate-how-to-avoid-common-pitfalls/) methods. Some say it is, some say - no. Reasons?  
&nbsp;&nbsp; First, because of larger size (16 bytes instead of 8 in bigint), `UUID` takes more disk space.  
&nbsp;&nbsp; Second, due to random nature of `UUID` which is not created by incrementing previous value by 1 as `bigint`, adjacent rows in table may be located far from one another in index.  
&nbsp;&nbsp; But despite this the major benefit of using `UUID` is that each `UUID` will be unique in distributed microservice system, hence if we base `hashCode()` & `equals()` on it, there won't be any collisions ever.  
&nbsp;&nbsp; The trade-off is obvious: strong uniqueness vs performance penalty.  
So, let's clarify, how much should we pay for such benefits on the database side.  
&nbsp;&nbsp; I'll use PostgreSQL for this experiment and scenario is pretty simple:

- create two similar tables, `huge_table_with_uuid` & `huge_table_with_bigint` with the only difference in primary key type. In first table it will be `UUID`, in 2nd - `bigint`.
- fill both tables with 60M rows (which approximately will take ~5-6 Gb of disk space).
- add 1M rows more and measure time of re-indexing.

&nbsp;&nbsp; The 3rd step is needed because every time when we add new rows to the table it should be re-indexed in order to keep maximum index efficiency, so it will show cost of adding rows to table during system work.  
&nbsp;&nbsp; For filling tables with data I'll use custom function:

{% highlight sql %}  
CREATE OR REPLACE FUNCTION gen_random_string(_min_length INT = 3)
RETURNS VARCHAR
LANGUAGE SQL
AS '
SELECT substring(
md5(random()::TEXT),
0,
_min_length + floor(random() * 10 + 1)::INT
)
';
{% endhighlight %}  
&nbsp;&nbsp; Let's start.  
&nbsp;&nbsp; I'll create extension for generating `UUID`'s and create a table with `UUID` as primary key:  
{% highlight sql %}  
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT exists huge_table_with_uuid (
id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
column1 VARCHAR(255) NOT NULL,
column2 VARCHAR(255) NOT NULL,
column3 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
{% endhighlight %}  
&nbsp;&nbsp; Now it's time to fill this table with data....  
{% highlight sql %}  
DO
$do$
BEGIN
FOR index IN 1..60000000 LOOP
INSERT INTO huge_table_with_uuid (column1,column2)
SELECT gen_random_string(),
gen_random_string();
END LOOP;
END
$do$;
{% endhighlight %}  
.... and get out for a workout :-), because process will take several hours.  
&nbsp;&nbsp; Yeah, it took 3 hours and 6.1 Gb of disk in order to generate 60 M of rows.  
&nbsp;&nbsp; Let's make the 2nd table and fill it with data.  
{% highlight sql %}  
CREATE TABLE IF NOT exists huge_table_with_bigint (
id bigint GENERATED ALWAYS AS IDENTITY
PRIMARY KEY,
column1 VARCHAR(255) NOT NULL,
column2 VARCHAR(255) NOT NULL,
column3 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

DO
$do$
BEGIN
FOR index IN 1..60000000 LOOP
INSERT INTO huge_table_with_bigint (column1,column2)
SELECT gen_random_string(),
gen_random_string();
END LOOP;
END
$do$;
{% endhighlight %}  
&nbsp;&nbsp; This time process is much faster and took 15 minutes and 4.9 Gb of disk space.  
Let's switch back to `huge_table_with_uuid`, add 1M rows and re-index:
{% highlight sql %}  
DO
$do$
BEGIN
FOR index IN 1..1000000 LOOP
INSERT INTO huge_table_with_uuid (column1,column2)
SELECT gen_random_string(),
gen_random_string();
END LOOP;
END
$do$

reindex index huge_table_with_uuid_pkey
{% endhighlight %}  
The same for `huge_table_with_bigint`:  
{% highlight sql %}
DO
$do$
BEGIN
FOR index IN 1..1000000 LOOP
INSERT INTO huge_table_with_bigint (column1,column2)
SELECT gen_random_string(),
gen_random_string();
END LOOP;
END
$do$

reindex index huge_table_with_bigint_pkey
{% endhighlight %}  
&nbsp;&nbsp; The same difference with `INSERT`, but time spent on re-index is the same in both tables.

&nbsp;&nbsp; To summarize, here are my findings:  
- `huge_table_with_uuid` has size 6.1 Gb while huge_table_with_bigint has 4.9 Gb, `UUID` took ~20% more for the table with 2 columns of useful payload. For larger tables this proportion will be lower.  
- `INSERT` with `UUID` is 12 times slower than with incrementally increasing bigint.  
- `REINDEX` has the same performance in both cases.

#### Conclusion.

&nbsp;&nbsp; I think that in case if you do not expect frequent batch inserts, `UUID` performance penalty won't affect end-users, but will give strong JPA entity's uniqueness.  
&nbsp;&nbsp; Need to add, that to ensure that the benefit received exceeds the cost of disk space, table should have significant amount of columns in order to balance the cost of `UUID`. Otherwise the game is not worth the candle.  
&nbsp;&nbsp; Taking into account all the above conditions, `UUID` is worth to be used as primary key in some certain situations.