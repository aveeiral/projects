select * from weekly_sales
select count(segment), segment
from weekly_sales
group by segment
/* Data Cleansing
Convert the week_date to a DATE format
*/
/*Add a week_number as the second column for each week_date value, for example any value 
from the 1st of January to 7th of January will be 1, 8th to 14th will be 2 etc */

/*Add a month_number with the calendar month for each week_date value as the 3rd column */

/*Add a calendar_year column as the 4th column containing either 2018, 2019 or 2020 values */
/*Add a new column called age_band after the original segment column using the following 
mapping on the number inside the segment value
Add a new demographic column using the following mapping for the first letter in the segment values:
Ensure all null string values with an "unknown" string value in the original segment column 
as well as the new age_band and demographic columns

Generate a new avg_transaction column as the sales value divided by transactions rounded 
to 2 decimal places for each record
*/

with cte1 as (
select week_date, CAST(CONVERT(DATETIME, week_date, 3) AS DATE) as new_date, region, platform, segment, 
customer_type, transactions, sales
from weekly_sales 
)

select new_date, 
DATEPART(week, new_date) week_number, 
DATEPART(m, new_date) month_number,
DATEPART(yyyy, new_date) calender_year,
region, 
platform, 
CASE
WHEN segment = 'null' THEN 'unknown'
ELSE segment
END as segment,
CASE
WHEN SUBSTRING(segment, 2, 1) =  '1' THEN 'Young Adults'
WHEN SUBSTRING(segment, 2, 1) =  '2' THEN 'Middle Aged'
WHEN SUBSTRING(segment, 2, 1) =  '3' THEN 'Retirees'
WHEN SUBSTRING(segment, 2, 1) =  '4' THEN 'Retirees'
ELSE 'unknown'
END as age_band,
CASE
WHEN SUBSTRING(segment, 1, 1) =  'C' THEN 'Couples'
WHEN SUBSTRING(segment, 1, 1) =  'F' THEN 'Families'
ELSE 'unknown'
END as demographic,
customer_type, 
transactions, 
sales,
ROUND((sales/transactions), 2) as avg_transaction
INTO clean_weekly_sales
from cte1

select * from clean_weekly_sales



/* Data Exploration */
/*What day of the week is used for each week_date value? */
select new_date, DATEPART(day, new_date) day_of_week, DATENAME(WEEKDAY, new_date) DayNam
from clean_weekly_sales

/*What range of week numbers are missing from the dataset?  Ans 1-12 and 37-52*/

select DISTINCT(week_number) as week_num
from clean_weekly_sales
order by week_num asc

/*How many total transactions were there for each year in the dataset?  */
select DATEPART(yyyy, new_date) as transaction_year, sum(transactions) Total_Transaction
from clean_weekly_sales
group by DATEPART(yyyy, new_date)

/*What is the total sales for each region for each month? */
select * from clean_weekly_sales
select region, month_number, SUM(CAST(sales AS bigint)) Total_Sales
from clean_weekly_sales
group by region, month_number
order by region ASC, month_number ASC

/*What is the total count of transactions for each platform */
select platform, SUM(CAST(sales AS bigint)) Total_Sales
from clean_weekly_sales
group BY platform
order by platform ASC 

/*What is the percentage of sales for Retail vs Shopify for each month? */

with sales as(
select calender_year,month_number,
sum(case when platform='Retail' then cast(sales as bigint) end) as Retail,
sum(case when platform='Shopify' then cast(sales as bigint) end) as Shopify,
sum(cast(sales as bigint))as total_sale
from clean_weekly_sales
group by calender_year,month_number
)
select calender_year,month_number,round(cast((Retail*100.0/total_sale) as float),2) as retail_percent,
round(cast((Shopify*100.0/total_sale ) as float),2) as shopify_percent
from sales
order by 1,2
/*What is the percentage of sales by demographic for each year in the dataset?*/
with demographics_sales as(
select calender_year,
sum(case when demographic='Couples' 
then cast(sales as bigint) end) as couples_sales,
sum(case when demographic='Families'
 then cast(sales as bigint) end) as families_sales,
sum(case when demographic='Unknown'
 then cast(sales as bigint) end) as unknown_sales,
sum(cast(sales as bigint)) as total_sales
from clean_weekly_sales
group by calender_year
)
select calender_year, 
round(cast((couples_sales*100.0/ total_sales) as float),2) as couples_sales_percent,
round(cast((families_sales*100.0/ total_sales) as float),2) as families_sales_percent,
round(cast((unknown_sales*100.0/ total_sales) as float),2) as unknown_sales_percent
from demographics_sales
order by 1

/*Which age_band and demographic values contribute the most to Retail sales? */
select * from clean_weekly_sales
select age_band, demographic, SUM(CAST(sales AS bigint)) as Total_Sales
from clean_weekly_sales
where platform = 'Retail'
group by age_band, demographic
order by Total_Sales DESC
/*Can we use the avg_transaction column to find the average transaction size for each year 
for Retail vs Shopify? If not - how would you calculate it instead? */
with tranx as(
select calender_year,sum(case when platform='Retail' then transactions end) as retail_tranx_sum,
sum(case when platform='Shopify' then transactions end) as shopify_tranx_sum,
sum(case when platform='Retail' then  cast(sales as bigint) end) as retail_sales_sum,
sum(case when platform='Shopify' then cast(sales as bigint) end) as shopify_sales_sum
from clean_weekly_sales
group by calender_year)
select calender_year,round(cast(avg(retail_sales_sum*100.0/retail_tranx_sum) as float),2) as retail_avg,
round(cast(avg(shopify_sales_sum*100.0/shopify_tranx_sum) as float),2) as shopify_avg
from tranx
group by calender_year
order by 1

/*This technique is usually used when we inspect an important event and want to inspect 
the impact before and after a certain point in time.

Taking the week_date value of 2020-06-15 as the baseline week where the Data Mart 
sustainable packaging changes came into effect.

We would include all week_date values for 2020-06-15 as the start of the period after 
the change and the previous week_date values would be before
Using this analysis approach - answer the following questions:

What is the total sales for the 4 weeks before and after 2020-06-15? What is the growth 
or reduction rate in actual values and percentage of sales? */
select * from clean_weekly_sales


DECLARE @DC AS DATETIME
SET @DC = '2020-06-15'
 select distinct(dateadd(week, -4, @DC)) as Date_Before, 
(dateadd(week, 4, @DC)) as Date_After
from clean_weekly_sales;

with bef_aft as
(select *,
case when new_date>='2020-06-15' then 'after'
else 'before' end as before_after
from clean_weekly_sales
where calender_year='2020'
),
 sales_tab as(
select 
sum(case when  before_after='before' and new_date>='2020-05-18' then cast(sales as bigint)end) as before_sales,
sum(case when  before_after='after' and new_date<='2020-07-13' then cast(sales as bigint)end) as after_sales
from 
 bef_aft
 )
 select *,  (after_sales- before_sales) as sales_diff, round(cast((after_sales- before_sales)*100.0/before_sales as float),2) as percent_change
 from sales_tab


/*What about the entire 12 weeks before and after? */

select distinct(dateadd(week, -12, '2020-06-15')) as Date_Before, 
(dateadd(week, 12, '2020-06-15')) as Date_After
from clean_weekly_sales;

with bef_aft as
(select *,
case when new_date>='2020-06-15' then 'after'
else 'before' end as before_after
from clean_weekly_sales
where calender_year='2020'
),
 sales_tab as(
select 
sum(case when  before_after='before' and new_date>='2020-03-23' then cast(sales as bigint)end) as before_sales,
sum(case when  before_after='after' and new_date<='2020-09-07' then cast(sales as bigint)end) as after_sales
from 
 bef_aft
 )
 select *,  (after_sales- before_sales) as sales_diff, round(cast((after_sales- before_sales)*100.0/before_sales as float),2) as percent_change
 from sales_tab


 /*How do the sale metrics for these 2 
 periods before and after compare with the previous years in 2018 and 2019? */

 select distinct week_number
from clean_weekly_sales
where new_date = '2020-06-15'  and calender_year = '2020';
  
with sales as
(
select calender_year, week_number, sum(cast(sales as bigint)) as Total_Sales
from clean_weekly_sales
where week_number between 21 and 28
group by calender_year, week_number
),
bef_aft as
(
select calender_year, 
sum(case when week_number between 21 and 24 then total_sales end) as before_sales, 
sum(case when week_number between 25 and 28 then total_sales end) as after_sales
from sales
group by calender_year
)
select calender_year, before_sales, after_sales, (after_sales- before_sales) as sales_diff,
((after_sales - before_sales) * 100.0 / before_sales) as percent_diff
from bef_aft;

/*4. Bonus Question
Which areas of the business have the highest negative impact in sales 
metrics performance in 2020 for the 12 week before and after period?

region
platform
age_band
demographic
customer_type
*/
			

select * from clean_weekly_sales


