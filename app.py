import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlalchemy
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Zepto Dashbord",
                   page_icon=":shopping_cart:", layout='wide')
st.title("Zepto Dashboard")
st.markdown(
    """<style> .block-container{padding-top:2rem;} </style>""", unsafe_allow_html=True)


# Database connection


@st.cache_data
def load_data():
    user=os.getenv('DB_USER')
    password=os.getenv('DB_PASSWORD')
    host=os.getenv('DB_HOST')
    port=os.getenv('DB_PORT')
    db=os.getenv('DB_NAME')

    engine = sqlalchemy.create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db}")
    query = "SELECT * FROM Zepto"
    df = pd.read_sql(query, engine)
    return df


data = load_data()


st.sidebar.title("features")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File Upload Successfull !!! ")
else:
    df = data

df['revenue'] = df['discountedsellingprice']*df['availablequantity']

max_price=df['discountedsellingprice'].max()
min_price=df['discountedsellingprice'].min()

price_range=st.sidebar.slider("Select Price Range", min_value=int(min_price), max_value=int(max_price), value=(int(min_price),int(max_price)))
price_filtered_df=df[(df['discountedsellingprice']>=price_range[0])&(df['discountedsellingprice']<=price_range[1])]

max_discount=price_filtered_df['discountpercent'].max()
min_discount=price_filtered_df['discountpercent'].min()

discount_range=st.sidebar.slider("Select Discount Range",min_value=int(min_discount),max_value=int(max_discount),value=(int(min_discount),int(max_discount)))
final_df=price_filtered_df[(price_filtered_df['discountpercent']>=discount_range[0])&(price_filtered_df['discountpercent']<=discount_range[1])]

with st.sidebar.expander("Data Preview"):
    st.dataframe(final_df)
with st.sidebar.expander("📌 About This Project"):
    st.write("""
        This project analyzes Zepto retail data to understand product performance, revenue trends, pricing behavior, and inventory status.
             
        **Tools Used:** Python, Pandas, SQL, Streamlit, Plotly
    
         **Dataset:** 3731 products across 14 categories
    
        **Source:** Zepto E-Commerce inventory dataset""")

tab1,tab2,tab3,tab4=st.tabs(["Overview","Revenue Analysis","Stock Analysis","Categorical Analysis"])

with tab1:
    st.markdown("""<h1 style='text-align:center;'>Overview</h1>""",unsafe_allow_html=True)     
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Products", value=final_df['name'].count())
    with col2:
        st.metric(label="Total Revenue", value=f"₹{round(final_df['revenue'].sum()/100000,2)} Lakhs")
    with col3:
        st.metric(label="No_Of_Category", value=final_df['category'].nunique())
    

    
    st.subheader("Key Findings:")
    st.info(f"""
        • Cooking Essentials & Munchies contribute 35% of total revenue, indicating strong revenue concentration in a few categories.

        • Fruits & Vegetables receive the highest average discount (15%) but generate comparatively low revenue.

        • Meats, Fish & Eggs contains the lowest product variety (63 products) among all categories.

        • Approximately 12.14% of products are currently out of stock (~453 products unavailable).""")
    
    
    st.subheader("Business Insights:")
    st.info("""
        • Zepto should reduce dependency on a small number of high-revenue categories by expanding growth in underperforming segments.

        • Increasing discounts alone may not improve sales performance. The Fruits & Vegetables category suggests that product availability and demand alignment are more important than aggressive discounting.

        • High stockout rates may directly impact customer satisfaction and revenue. Improving inventory forecasting for categories like Meats, Fish & Eggs can reduce missed sales opportunities.

        • Inventory distribution is uneven across categories, suggesting need for better planning.
            
        • Cooking Essentials & Munchies shows strong demand and revenue consistency, making it a strong candidate for category expansion and promotional focus.""")


with tab2:
    st.markdown("""<h1 style='text-align:center;'>Revenue Analysis</h1>""",unsafe_allow_html=True)
#2nd Row
    col1,col2=st.columns(2)

#Revenue by Category
    with col1:
        revenue_by_category = final_df.groupby(['category'])['revenue'].sum().sort_values(ascending=False).reset_index()
    
        top_rev_category=revenue_by_category['category'].iloc[0]
        highest_revenue=round(revenue_by_category['revenue'].iloc[0]/100000,2)

        low_rev_category=revenue_by_category['category'].iloc[-1]
        lowest_revenue=round(revenue_by_category['revenue'].iloc[-1]/100000,2)

        fig2=px.bar(revenue_by_category,x='revenue',y='category',orientation='h',title="Revenue By Category",color_discrete_sequence=['blue'])
        st.plotly_chart(fig2)

        st.info(f"{top_rev_category} is the category with the highest revenue with {highest_revenue} Lakhs rupees.")
        st.info(f"{low_rev_category} is the category with the lowest revenue with {lowest_revenue} Lakhs rupees.")


#Dual_axis chart [revenue vs discout precentage by category]
    with col2:
        revenue_by_category = final_df.groupby(['category'])['revenue'].sum().sort_values(ascending=False).reset_index()
        discount_per_category=final_df.groupby(['category'])['discountpercent'].mean().sort_values(ascending=False).reset_index()

        fig3 = make_subplots(rows=1,cols=1,specs=[[{"secondary_y":True}]])
        fig3.add_trace(go.Bar(x=revenue_by_category['category'],y=revenue_by_category['revenue'],name='Revenue',marker_color='blue'),secondary_y=False)
        fig3.add_trace(go.Scatter(x=discount_per_category['category'],y=discount_per_category['discountpercent'],name='Dicount_Percentage',mode='markers+text',text=[f"{ x :.2f}%" for x in discount_per_category['discountpercent']],textposition='top center',textfont=dict(size=10),marker=dict(size=10),marker_color='purple'),secondary_y=True)
        fig3.update_layout(title="Revenue Vs Discount Percentage Per Category",xaxis_title="Category",yaxis_title="Revenue",yaxis2_title="Discount Percentage")
        st.plotly_chart(fig3)
  
        st.info("The above chart shows the relationship between revenue and discount percentage for each category. This information tells that high discounted category are not often generates high revenue, which indicates that offering high discounts may not always lead to increased sales and revenue. It is important to carefully consider the discount strategy for each category to maximize revenue while maintaining profitability.")

with tab3:
    st.markdown("""<h1 style='text-align:center;'>Stock Analysis</h1>""",unsafe_allow_html=True)

#row1
    col1,col2=st.columns(2)

#Products Per Category
    with col1:
        Category_count=final_df['category'].value_counts().sort_values(ascending=False).rename('count').reset_index()

        top_category=Category_count['category'].iloc[0]
        high_products=final_df['name'].count()

        last_category=Category_count['category'].iloc[-1]
        low_products=Category_count['count'].iloc[-1]

        fig1=px.bar(Category_count,x='count',y='category',orientation='h',title="No Of Products per Category",color_discrete_sequence=['blue'])
        st.plotly_chart(fig1)
        st.info(f"{top_category} is the category with the highest number of products with {high_products} products.")
        st.info(f"{ last_category} is the category with the lowest number of products with {low_products} products.")
#Stock Availablity")

    with col2:
        final_df['outofstock_no']=(final_df['outofstock'].astype(str).str.upper()=='TRUE').astype(int)
        stock_summary=final_df.groupby('category').agg(Total_products=('name','count'),out_of_stock=('outofstock_no',sum )).reset_index()
        stock_summary['out_of_stock%']= (stock_summary['out_of_stock']/stock_summary['Total_products'])*100
        stock_summary['in_stock%']=100-stock_summary['out_of_stock%']

        fig5=go.Figure()
        fig5.add_trace(go.Bar(x=stock_summary['category'],y=stock_summary['in_stock%'],name='In Stock',marker_color='Blue'))
        fig5.add_trace(go.Bar(x=stock_summary['category'],y=stock_summary['out_of_stock%'],name='Out Of Stock',marker_color='red'))
        fig5.update_layout(title="Stock status by category",xaxis_title="Category",yaxis_title="Percentage",barmode='group')
        st.plotly_chart(fig5)

        st.info("The above chart shows the percentage of products that are in stock and out of stock for each category. This information can help identify which categories may need attention in terms of inventory management.")



with tab4:
# Categorical Analysis

    st.markdown("""<h1 style='text-align:center;'>Categorical Analysis</h1>""",unsafe_allow_html=True)

    category=st.selectbox("Select A Category for Categorical Analysis",final_df['category'].unique(),key='select_category')

    category_selected=final_df[final_df['category']==category]

#row1
    col1,col2,col3=st.columns(3)

#top 10 products by revenue in selected category
    with col1:
        top_prd=category_selected.groupby('name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()

        top1_prd=top_prd['name'].iloc[0]
        top_rev=round(top_prd['revenue'].iloc[0]/100000,2)

        cat_fig1=px.bar(top_prd,x='revenue',y='name',title=f'Top 10 Products By Revenue in {category}',orientation='h',color_discrete_sequence=['blue'])
        cat_fig1.update_layout(xaxis_title="Revenue",yaxis_title="Products",yaxis_tickfont=dict(size=8))
        st.plotly_chart(cat_fig1)
    
        st.info(f"The above chart shows the top 10 products in the {category_selected['category']} category based on revenue. This information can help identify which products are the most highly purchased and genetrates more revenue ,which is usefull in inventory management and marketing strategies.")
        st.info(f"{top1_prd} is the product with the highest revenue with{top_rev} Lakh rupees in {category} category")

#top 10 Products By Discount in Selected Category
    with col2:
        top_discount_prd=category_selected.groupby('name')['discountpercent'].mean().sort_values(ascending=False).head(10).reset_index()

        top_dis_prd=top_discount_prd['name'].iloc[0]
        top_dis=round(top_discount_prd['discountpercent'].iloc[0],2)

        cat_fig4=px.bar(top_discount_prd,x='discountpercent',y='name',title=f'Top 10 Products By Discount Percentage in {category}',orientation='h',color_discrete_sequence=['blue'])
        cat_fig4.update_layout(xaxis_title="Discount Percentage",yaxis_title="Products",yaxis_tickfont=dict(size=8))
        st.plotly_chart(cat_fig4,use_container_width=True)
 
        st.info("The above chart shows the top 10 products in the {category_selected} category based on discount percentage. This information can help identify which products are being offered at the highest discounts, which may indicate that they are not selling well or that they are being used as loss leaders to attract customers. It is important to carefully consider the discount strategy for each product to maximize revenue while maintaining profitability.")
        st.info(f"{top_dis_prd} is the product with the highest discount percentage with {top_dis}% discount in {category} category")


#Stock Status By Category
    with col3:
        category_selected['stockstatus']= df['outofstock'].map({False: 'In Stock', True: 'Out of Stock'})

        stock_counts = category_selected['stockstatus'].value_counts(normalize=True)
        in_stock_percent = round(stock_counts.get('In Stock', 0) * 100,2)
        out_of_stock_percent = round(stock_counts.get('Out of Stock', 0) * 100,2)

        cat_fig5=px.pie(category_selected,names='stockstatus',title=f"Stock Status Of {category} category",color_discrete_sequence=['Blue','red'])
        cat_fig5.update_layout(legend_title_text='stock status')
        st.plotly_chart(cat_fig5,use_container_width=True)

        st.info(f"The above chart displays that the percentage of products that are in stock and out of stock for the {category} category. This information can help identify the inventory status of products in this category and can be useful for inventory manegement and restocking decisions.")
        st.info(f"{category} category has {in_stock_percent}% products in stock and {out_of_stock_percent}% products out of stock.")




