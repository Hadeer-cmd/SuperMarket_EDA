
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout= 'wide', page_title= 'SuperMarket EDA', page_icon= '✨')

page = st.sidebar.radio('Pages', ['Dataset','Statistical Questions','Univariate Analysis', 'Bivariate Analysis', 'Multivariate Analysis', 'Get by Date & City'])
supermarket = pd.read_csv('supermarket_sales - Sheet1.csv')
if page == 'Dataset':
    st.dataframe(supermarket)
elif page == 'Univariate Analysis':
    question = st.selectbox('Select Question', ['What is the distribution of unit prices across all transactions?', 'What is the frequency of each payment method?', 'What is the distribution of customer ratings?','Which product line is the most frequently purchased?','What is the average quantity purchased across all product lines?'])
    if question == 'What is the distribution of unit prices across all transactions?':
        st.plotly_chart(px.box(supermarket, x='Unit price',))
    elif question == 'What is the frequency of each payment method?':
        st.plotly_chart(px.histogram(supermarket, x='Payment'))
    elif question == 'What is the distribution of customer ratings?':
        st.plotly_chart(px.box(supermarket, x='Rating'))
    elif question == 'Which product line is the most frequently purchased?':
        mostfrequentlyProductLine = supermarket.groupby('Product line')['Invoice ID'].count().reset_index().sort_values(by='Invoice ID', ascending=False)
        mostfrequentlyProductLine
        st.plotly_chart(px.histogram(supermarket, x='Product line',category_orders={'Product line': mostfrequentlyProductLine['Product line'].tolist()}))
        st.plotly_chart(px.pie(supermarket,  'Product line'))
    elif question == 'What is the average quantity purchased across all product lines?':
        st.plotly_chart(px.box(supermarket, x='Quantity'))
elif page == 'Statistical Questions':
    question = st.selectbox('Select Question', ['What is the average gross income per transaction, and how does it vary by product line?', 'Which city generates the highest average total sales?', 'What is the distribution of customer ratings, and are there any outliers?','Is there a significant difference in total sales between male and female customers?','What are the most common payment methods, and what is the average total spent per method?'])
    if question == 'What is the average gross income per transaction, and how does it vary by product line?':
        averageGrossIncome = supermarket['gross income'].mean()
        averageGrossIncome
        averageGrossIncomePerProductLine = supermarket.groupby('Product line')['gross income'].mean().sort_values(ascending=False)
        averageGrossIncomePerProductLine
    elif question == 'Which city generates the highest average total sales?':
        highestAverageTotalSalesCity = supermarket.groupby('City')['Total'].sum().reset_index().sort_values(by='Total', ascending=False).head(1)
        highestAverageTotalSalesCity
    elif question == 'What is the distribution of customer ratings, and are there any outliers?':
        distributionOfRating = supermarket['Rating'].describe().reset_index().round(2) 
        distributionOfRating
    elif question == 'Is there a significant difference in total sales between male and female customers?':
        diffrenceInTotalSalesByGender = supermarket.groupby('Gender')['Total'].sum().reset_index().sort_values(by='Total', ascending=False)
        diffrenceInTotalSalesByGender
    elif question == 'What are the most common payment methods, and what is the average total spent per method?':
        mostCommonPaymentMethod = supermarket.groupby('Payment')['Invoice ID'].count().reset_index().sort_values(by='Invoice ID', ascending=False).head(1)
        mostCommonPaymentMethod  
        averageTotalSpendPerMethos = supermarket.groupby('Payment')['Total'].mean().reset_index().sort_values(by='Total', ascending=False)
        averageTotalSpendPerMethos

elif page == 'Get by Date & City':
    supermarket['Date'] = pd.to_datetime(supermarket['Date'])
    min_date = supermarket['Date'].min().date()
    max_date = supermarket['Date'].max().date()
    start_date = st.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input('End Date', value=min_date, min_value=min_date, max_value=max_date)

    City = st.multiselect('City', supermarket['City'].unique())

    supermarket_filtered =supermarket[(supermarket.Date >= str(start_date)) & (supermarket.Date <= str(end_date))]

    supermarket_filtered = supermarket_filtered[(supermarket_filtered.City.isin(City))]

    st.dataframe(supermarket_filtered)

    product_count = supermarket_filtered['Product line'].value_counts().reset_index()
    product_count.columns = ['Product line', 'count']

# Plot bar chart
    st.plotly_chart(px.bar(product_count, x='Product line', y='count'))
elif page == 'Bivariate Analysis':
    question = st.selectbox('Select Question', ['How does total purchase amount vary across different product lines?', 'Is there a correlation between unit price and quantity purchased?', 'What is the average gross income per gender?','Is there a trend between customer rating and total sales?'])
    if question == 'How does total purchase amount vary across different product lines?':
        df1 = supermarket.groupby('Product line')['Total'].sum().reset_index().sort_values(by='Total', ascending=False)
        df1
        st.plotly_chart(px.bar(df1, x='Product line', y='Total'))
    elif question == 'Is there a correlation between unit price and quantity purchased?':
        supermarket['gross margin percentage'] = (supermarket['gross income'] / supermarket['Total']) * 100
        corr = supermarket.corr(numeric_only=True).round(2)
        corr
        st.plotly_chart(px.imshow(corr,text_auto=True))
    elif question == 'What is the average gross income per gender?':
        st.plotly_chart(px.histogram(supermarket, x='Gender',y='gross income'))
    elif question == 'Is there a trend between customer rating and total sales?':
        st.plotly_chart(px.scatter(supermarket,x= 'Rating',y='Total'))
elif page == 'Multivariate Analysis':
    question = st.selectbox('Select Question',['How does gross income vary by city and customer type?','What is the relationship between unit price, quantity, and total sales?','Do different genders prefer different product lines and how does it affect gross income?','Which combination of branch and product line yields the highest average rating?','How do total sales differ by time of day and payment method across branches?'])
    if question == 'How does gross income vary by city and customer type?':
        st.plotly_chart(px.box(supermarket,x = 'City',y= 'gross income',color= 'Customer type'))

    elif question == 'What is the relationship between unit price, quantity, and total sales?':
        st.plotly_chart(px.scatter(supermarket, x='Unit price',y='Quantity',size = 'Total',color='Product line'))

    elif question == 'Do different genders prefer different product lines and how does it affect gross income?':
        df3 = supermarket.groupby(['Gender','Product line'])['gross income'].mean().reset_index()
        df3
        st.plotly_chart(px.bar(df3, x='Product line', y='gross income', color='Gender', barmode='group',title='Average Gross Income by Product Line and Gender'))

    elif question == 'Which combination of branch and product line yields the highest average rating?':
        df4 = supermarket.groupby(['Branch','Product line'])['Rating'].mean().reset_index()
        df4
        st.plotly_chart(px.bar(df4, x='Branch', y='Rating', color='Product line', barmode='group',title='Average Rating by Branch and Product Line'))  
 
    elif question == 'How do total sales differ by time of day and payment method across branches?':
        df5 = supermarket.groupby(['Branch','Date','Payment'])['Total'].sum().reset_index()
        df5
        st.plotly_chart(px.scatter(df5, x='Date', y='Total', color='Payment', facet_col='Branch', title='Total Sales by Hour and Payment Method per Branch'))


