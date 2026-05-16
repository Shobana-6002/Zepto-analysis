# 🛒 Zepto E-Commerce Data Analysis

A complete end-to-end data analytics project analyzing Zepto's product catalog with 3,731 SKUs across 14 categories.Built to demonstrate real-world data analytics skills for portfolio purposes.

## 📌 Project Overview

This project analyzes a Zepto e-commerce dataset to extract actionable business insights across pricing, inventory, revenue, and discount strategy using SQL, Python, and interactive dashboards.

## 🛠️ Tools & Technologies

| Tool                                 | Purpose                         |
| ------------------------------------ | ------------------------------- |
| PostgreSQL                           | Data storage and SQL analysis   |
| Python (Pandas, Matplotlib, Seaborn) | Data cleaning and EDA           |
| Plotly                               | Interactive visualizations      |
| Streamlit                            | Interactive web dashboard       |
| Power BI                             | Business intelligence dashboard |

## 📁 Project Structure

zepto-analytics/
├── sql/
│ └── zepto_queries.sql ← All SQL business queries
├── notebooks/
│ └── Zepto_EDA.ipynb ← Python EDA notebook
├── dashboard/
│ ├── app.py ← Streamlit dashboard
│ └── requirements.txt ← Required libraries
├── powerbi/
│ └── Zepto_Dashboard.pbix ← Power BI dashboard
└── README.md

## 🗄️ Dataset

• _Source:_ Kaggle (Zepto product listings) [ Dataset Download link : https://www.kaggle.com/datasets/devshahoff/zepto-dataset]
• _Size:_ 3,731 rows × 10 columns
• _Key Columns:_ category, name, MRP, discount percent, available quantity, discounted selling price, weight in gmrs, out of stock status

## 🧹 Data Cleaning

• Removed records with MRP = 0
• Converted prices from paise to rupees [ divided by 100 ]
• Fixed boolean column type issues
• Verified null values across all columns
• Created estimated revenue column [ selling price × available quantity ]

## 📊 SQL Business Questions Answered

### 1. Top 10 Best Value Products

Identified products with highest discount percentages to find heavily promoted items for marketing campaigns.

### 2. Missed Revenue Opportunity

Found high-value products (MRP > ₹300) currently out of stock — representing direct revenue loss.

### 3. Estimated Category Revenue

Calculated total estimated revenue per category by multiplying selling price with available quantity.

### 4. Premium Popularity

Identified expensive products (MRP > ₹500) that sell well even with low discounts (< 10%) — showing strong brand loyalty.

### 5. Marketing Optimization

Found top 5 categories with highest average discounts to identify where price cuts are most aggressive.

### 6. Value for Money Analysis

Calculated price per gram for products over 100g to help customers compare true value across products.

### 7. Logistics Segmentation

Used CASE statements to classify products into Low, Medium, and Bulk weight categories for delivery planning.

### 8. Warehouse Planning

Calculated total inventory weight per category to identify heaviest categories for warehouse management.

## 🔍 Key Business Insights

• Cooking Essentials & Munchies contribute 35% of total revenue, indicating strong revenue concentration in a few categories.

• Fruits & Vegetables receive the highest average discount (15%) but generate comparatively low revenue.

• Meats, Fish & Eggs contains the lowest product variety (63 products) among all categories.

• Approximately 12.14% of products are currently out of stock (~453 products unavailable).

## 💡 Business Recommendations

• Zepto should reduce dependency on a small number of high-revenue categories by expanding growth in underperforming segments.

• Increasing discounts alone may not improve sales performance. The Fruits & Vegetables category suggests that product availability and demand alignment are more important than aggressive discounting.

• High stockout rates may directly impact customer satisfaction and revenue. Improving inventory forecasting for categories like Meats, Fish & Eggs can reduce missed sales opportunities.

• Inventory distribution is uneven across categories, suggesting need for better planning.

• Cooking Essentials & Munchies shows strong demand and revenue consistency, making it a strong candidate for category expansion and promotional focus.

## 🚀 How to Run the Streamlit Dashboard

**Step 1 — Clone the repository**
git clone https://github.com/Shobana-2025/zepto-analytics.git

**Step 2 — Navigate to dashboard folder**
cd zepto-analytics/dashboard

**Step 3 — Create virtual environment**
python -m venv venv1
venv1\Scripts\activate

**Step 4 — Install required libraries**
pip install -r requirements.txt

**Step 5 — Create .env file with your database credentials**
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=yourdatabasename

**Step 6 — Run the app**
streamlit run app.py

## 📸 Dashboard Screenshots

### Power BI Dashboard

<img width="1623" height="873" alt="image" src="https://github.com/user-attachments/assets/bf541f24-9ba0-40e7-a501-007243310d09" />

### Streamlit Dashboard — General Overview

<img width="1920" height="907" alt="image-1" src="https://github.com/user-attachments/assets/daf6ace3-8303-484c-9a33-fddd2a6d18ea" />

### Streamlit Dashboard — Category Analysis

<img width="1920" height="913" alt="image-2" src="https://github.com/user-attachments/assets/f8432946-824a-4db7-8e83-a955e370777f" />

## 👩‍💻 Author

_D.Shobana_

- LinkedIn: [www.linkedin.com/in/shobana-d-96287b374]
- GitHub: [https://github.com/Shobana-2025]

## 📄 License

This project is open source and available for
educational and portfolio purposes.
