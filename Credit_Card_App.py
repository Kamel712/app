import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Load the dataset
credit_card = pd.read_csv('BankChurners.csv')

# Set up the Streamlit app layout
col1, col2 = st.columns([2,1])  
with col1:
    st.title("Credit Card Analysis")
with col2:
    st.image("credit_card_PNG123.png", width=150)  
st.sidebar.header('Navigation')
st.sidebar.markdown("Created by [Kamel Emad](https://www.linkedin.com/in/kamel-emad/)")

# Sidebar - Selection

sidebar_option = st.sidebar.radio("Choose an option:",["Data Overview", "EDA", "Visualizations"])

# Display the data overview:
if sidebar_option == "Data Overview" :
    st.header("Data Overview :")
    st.write("This dataset provides information about credit card across different customer behavior.")
    st.write(credit_card.head())

    st.subheader("Numeric DataSet Summary :")
    st.write("This Summary provides information about the measures of center and measures of speard for the numeric columns.")
    numeric_cols = credit_card.select_dtypes(include='number').columns
    for i in range(0,len(numeric_cols), 3):
        col_pair = numeric_cols[i:i+3]  # Get three columns at a time
        cols = st.columns(3)  # Create three side-by-side columns
        for j, col in enumerate(col_pair):
         with cols[j]:
            st.write(f"Describe for: {col}")
            st.write(credit_card[col].describe())
            
# Exploratory Data Analysis (EDA)
elif sidebar_option == "EDA" :
   st.header("Exploratory Data Analysis :")
   st.write("One of the first things you'll want to do after you some data into a pandas DataFrame is to start exploring it." \
   "pandas has many built in functions which allow you to quickly get information about a DataFrame." \
   "Lets explore Education_Level Column using the credit card DataFrame :")
   
   # explore Education_Level Column :
   value_counts = credit_card['Education_Level'].nunique()
   null_count = credit_card['Education_Level'].isna().sum()
   duplicate_count = credit_card['Education_Level'].duplicated().sum()
   info = pd.DataFrame({
    "Value_Count_Unique": [value_counts],
    "Null_Count": [null_count],
    "Duplicate_Count": [duplicate_count]})
   st.write(info)
 
   st.subheader("Customer_Age Category Distribution")
   fig,ax = plt.subplots()
   sns.histplot(data=credit_card,x='Customer_Age', hue='Attrition_Flag', kde=True,bins=25)
   st.pyplot(fig)
    
   st.subheader("Total Transaction Amount Distribution by Marital_Status")
   fig1 = px.bar(credit_card, x='Marital_Status', y='Total_Trans_Amt', color='Marital_Status', title="Transaction Amount across Marital_Status")
   st.plotly_chart(fig1)

   st.subheader("Avg Utilization Ratio by Education_Level")
   fig2,ax2 = plt.subplots(figsize=(8,5))
   sns.boxplot(data=credit_card,x='Education_Level',y='Avg_Utilization_Ratio')
   ax2.set(xlabel ="Education Level", ylabel="Avg Utilization Ratio",title ="Avg Utilization Ratio across  Education_Level")
   st.pyplot(fig2)

# Visualizations with Interactive Widgets
elif sidebar_option == "Visualizations" :
   st.header("Interactive Visualizations")
   select_gender = st.sidebar.selectbox("Select Gender :",credit_card['Gender'].unique())
   select_marital_status = st.sidebar.selectbox("Select Marital Status :",credit_card['Marital_Status'].unique())
   filtered_data = credit_card[(credit_card['Gender']==select_gender) & (credit_card['Marital_Status']==select_marital_status)]
   st.write(f"Showing data for Gender: {select_gender} and Marital Status: {select_marital_status}") 
   st.write(filtered_data)
   
   st.subheader("Gender Distribution Split by Attrition Flag :")
   st.write("86.7% of male and 83.2% of female married customers are Existing Customers, indicating continued engagement with their credit cards." \
           "Conversely, 13.3% of male and 16.8% of female married customers are Attrited Customers, suggesting they have discontinued their credit card usage.")
   st.write("Note: You can apply filters to analyze specific customer segments based on gender, marital status.")
   filtered_data['Gender_Attrition'] = filtered_data['Gender'] + ' - ' + filtered_data['Attrition_Flag']
   fig3 = px.pie(filtered_data,names='Gender_Attrition',title="Combined Gender and Attrition Distribution",hole=0.4)
   fig3.update_traces(textinfo='percent+label')
   st.plotly_chart(fig3)

   st.subheader("Total Utilization Ratio VS Attrition Flag :")
   st.markdown("**Utilization Ratio Insight :**")
   st.write("Customers with a lower average utilization ratio demonstrate a significantly higher likelihood of churning their credit cards." \
   " Specifically, within the utilization range of 2.4% to 7.4%, " \
   "we observed that approximately 65% of all churned customers fall into this category. " \
   " This suggests that limited engagement with credit card usage may be a strong indicator of potential attrition.")
   fig4=px.histogram(credit_card, x='Avg_Utilization_Ratio', color='Attrition_Flag', nbins=25, marginal='rug', opacity=0.75)
   st.plotly_chart(fig4)
   st.markdown("**Strategic Recommendation :**")
   st.markdown(
    "To proactively reduce churn, financial institutions should:\n\n"
    "1- Identify customers with low utilization patterns in early stages.\n\n"
    "2- Implement targeted engagement strategies, such as personalized offers, cashback incentives, or educational content that encourages higher card usage.\n\n"
    "3- Use predictive models to flag underutilized accounts likely to churn, enabling timely interventions.\n\n" \
    "4- Communication campaigns—for low-spending customers to encourage usage and reduce churn risk.")

   st.subheader("Total Relationship Count VS Attrition Flag :")
   st.markdown("**Relationship Products Insight :**")
   st.write("Customers with a lower Relationship Count (i.e., fewer bank products/services such as loans, savings accounts, etc.) " \
   "demonstrate a significantly higher likelihood of churning their credit cards.  " "Specifically, " \
   "when the Relationship Count is less than 3, approximately 60% of all churned customers fall into this segment." \
   "This suggests that limited product engagement is a strong indicator of potential attrition.")
   fig5=px.histogram(credit_card, x='Total_Relationship_Count', color='Attrition_Flag', nbins=25, marginal='rug', opacity=0.75)
   st.plotly_chart(fig5)
   st.markdown("**Strategic Recommendation:**")
   st.markdown(
     "To reduce customer churn, banks should implement strategies that increase product bundling and cross-selling:\n\n"
     "1- Encouraging customers to open additional accounts or use more services (such as loans, savings.\n\n" 
     "2- investment products can strengthen overall engagement, foster loyalty, and reduce the likelihood of credit card attrition.")
   
   st.subheader("Total Transaction Amount VS Attrition Flag :")
   st.markdown("**Total Transaction Amount Insight :**")
   st.write("Customers with lower total transaction amounts demonstrate a significantly higher likelihood of churning their credit cards." \
   "Specifically, within the transaction range of 1$ to 2999$($), approximately 75% of all churned customers fall into this category." \
   " This trend suggests that limited credit card usage is a strong indicator of potential attrition")
   fig6=px.histogram(credit_card, x='Total_Trans_Amt', color='Attrition_Flag', nbins=25, marginal='rug', opacity=0.75)
   st.plotly_chart(fig6)

   st.subheader("Relationship between Total Transaction Amount and Credit Limit :")
   fig7 = px.scatter(credit_card, x='Credit_Limit', y='Total_Trans_Amt',title="Sactter Plot : Total Transaction Amount VS Credit Limit",
                    labels={'Credit_Limit': 'Credit Limit','Total_Trans_Amt': 'Total Transaction Amount'},color='Attrition_Flag')
   st.plotly_chart(fig7)

   st.subheader("Correlation Matrix Between All Numeric Columns :")
   excluded_columns = ['Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2',
                        'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1']
   filtered_data_corr = credit_card.drop(columns=excluded_columns)
   correlation_matrix = filtered_data_corr.corr(numeric_only= True)
   fig8= plt.figure(figsize=(10,6))
   sns.heatmap(correlation_matrix,annot=True,cmap='Blues',linewidths=2,linecolor='r',vmin=-1,vmax=+1)
   st.pyplot(fig8)

st.sidebar.markdown("***")
st.sidebar.write("End of App")



   