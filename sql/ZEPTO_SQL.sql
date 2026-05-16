DROP TABLE IF EXISTS zepto;

CREATE TABLE Zepto(
 Id SERIAL PRIMARY KEY ,
 Category VARCHAR(255),
 name VARCHAR(255) NOT NULL,
 mrp NUMERIC(8,2),
 discountPercent INTEGER,
 availableQuantity INTEGER,
 discountedSellingPrice NUMERIC(8,2),
 weightInGms INTEGER,
 outOfStock BOOLEAN,
 quantity INTEGER
);

SELECT  * FROM Zepto ;

--CLEANING--

SELECT COUNT(*) FROM Zepto;

SELECT * FROM ZEPTO 
WHERE Category IS NULL OR 
name IS NULL OR 
mrp IS NULL OR
discountPercent IS NULL OR 
availableQuantity IS NULL OR
discountedSellingPrice IS NULL OR
weightInGms IS NULL OR
outOfStock IS NULL OR
quantity IS NULL ;

SELECT * FROM Zepto LIMIT 10;

SELECT name, mrp , discountedsellingprice FROM Zepto
WHERE mrp = 0 OR discountedsellingprice = 0 ;

DELETE FROM Zepto WHERE mrp = 0;

UPDATE Zepto SET mrp=mrp/100;
UPDATE Zepto SET discountedsellingprice=discountedsellingprice/100;

--BUSINESS QUESTIONS--

-- Q1. Find the top 10 best-value products based on the discount percentage.

SELECT DISTINCT name , mrp, discountpercent , discountedsellingprice FROM Zepto 
ORDER BY discountpercent DESC
LIMIT 10;

--Q2.What are the Products with High MRP but Out of Stock

SELECT name,mrp FROM Zepto
WHERE outofstock = True AND mrp > 300
ORDER BY mrp DESC;

--Q3.Calculate Estimated Revenue for each category

SELECT category,SUM(discountedsellingprice*availablequantity) AS total_revenue
FROM Zepto
GROUP BY category 
ORDER BY total_revenue DESC;

-- Q4. Find all products where MRP is greater than ₹500 and discount is less than 10%.

SELECT DISTINCT name,mrp,discountpercent FROM Zepto
WHERE mrp > 500 AND
discountpercent < 10 
ORDER BY mrp,discountpercent DESC;

-- Q5. Identify the top 5 categories offering the highest average discount percentage.

SELECT category,ROUND(avg(discountpercent),2) AS avg_discount
FROM Zepto
GROUP BY category
ORDER BY avg_discount DESC
LIMIT 5;

-- Q6. Find the price per gram for products above 100g and sort by best value.

SELECT DISTINCT name,weightingms,discountedsellingprice, ROUND(mrp/weightingms,2) AS price_per_gram
FROM Zepto
WHERE weightingms >= 100
ORDER BY price_per_gram ;

--Q7.Group the products into categories like Low, Medium, Bulk.

SELECT DISTINCT name,weightingms,
CASE 
    WHEN weightingms <1000 THEN 'LOW'
	WHEN weightingms <5000 THEN 'MEDIUM'
	ELSE 'BULK'
	END AS weight_category
FROM Zepto;

--Q8.What is the Total Inventory Weight Per Category

SELECT category ,sum(weightingms * availablequantity) AS inventory_weight
FROM Zepto
GROUP BY category
ORDER BY inventory_weight DESC;
