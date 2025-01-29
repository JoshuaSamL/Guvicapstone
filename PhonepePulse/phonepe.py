import pandas as pd
import geopandas as gpd
import mysql.connector
import streamlit as st
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
import plotly.express as px
from streamlit_option_menu import option_menu

# Connect to MySQL database and fetch data
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Joshua@2020",
    database="phonepe"
)
mycursor = mydb.cursor()

# Fetch aggregated transaction data
mycursor.execute("SELECT * FROM aggregated_transaction")
table1 = mycursor.fetchall()
Aggre_transaction = pd.DataFrame(table1, columns=["States", "Years", "Quarter", "Transaction_type",
                                                  "Transaction_count", "Transaction_amount"])

# Fetch aggregated user data
mycursor.execute("SELECT * FROM aggregated_user")
table2 = mycursor.fetchall()
Aggre_user = pd.DataFrame(table2, columns=["States", "Years", "Quarter", "Brands",
                                           "Transaction_count", "Percentage"])

# Fetch map transaction data
mycursor.execute("SELECT * FROM map_transaction")
table3 = mycursor.fetchall()
Map_transaction = pd.DataFrame(table3, columns=["States", "Years", "Quarter", "District",
                                                "Transaction_count", "Transaction_amount"])

# Fetch map user data
mycursor.execute("SELECT * FROM map_user")
table4 = mycursor.fetchall()
Map_user = pd.DataFrame(table4, columns=["States", "Years", "Quarter", "District",
                                         "RegisteredUser", "AppOpens"])

# Fetch top transaction data
mycursor.execute("SELECT * FROM top_transaction")
table5 = mycursor.fetchall()
Top_transaction = pd.DataFrame(table5, columns=["States", "Years", "Quarter", "Pincodes",
                                                "Transaction_count", "Transaction_amount"])

# Fetch top user data
mycursor.execute("SELECT * FROM top_user")
table6 = mycursor.fetchall()
Top_user = pd.DataFrame(table6, columns=["States", "Years", "Quarter", "Pincodes", "RegisteredUsers"])

# Load shapefile for India states
gdf = gpd.read_file('J:\Studies\GUVI\projects\capstone\Phonepe\gadm41_IND_1.json\gadm41_IND_1.shp')

# Streamlit Page Config
st.set_page_config(layout="wide")

# Sidebar Navigation
with st.sidebar:
    selected_section = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts"])

# --- Define Analysis Functions ---
def ques1():
    # Top Brands Of Mobiles Used
    brand = Aggre_user.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand_df = pd.DataFrame(brand).reset_index()
    fig = px.pie(brand_df, values="Transaction_count", names="Brands", title="Top Mobile Brands Used")
    st.plotly_chart(fig)

def ques2():
    # States With Lowest Transaction Amount
    lt = Aggre_transaction.groupby("States")["Transaction_amount"].sum().nsmallest(10).reset_index()
    fig = px.bar(lt, x="States", y="Transaction_amount", title="States with Lowest Transaction Amount")
    st.plotly_chart(fig)

def ques3():
    # Districts With Highest Transaction Amount
    htd = Map_transaction.groupby("District")["Transaction_amount"].sum().nlargest(10).reset_index()
    fig = px.pie(htd, values="Transaction_amount", names="District", title="Top 10 Districts with Highest Transaction Amount")
    st.plotly_chart(fig)

def ques4():
    # Top 10 Districts With Lowest Transaction Amount
    ltd = Map_transaction.groupby("District")["Transaction_amount"].sum().nsmallest(10).reset_index()
    fig = px.bar(ltd, x="District", y="Transaction_amount", title="Top 10 Districts with Lowest Transaction Amount")
    st.plotly_chart(fig)

def ques5():
    # Top 10 States With AppOpens
    app_opens = Map_user.groupby("States")["AppOpens"].sum().nlargest(10).reset_index()
    fig = px.bar(app_opens, x="States", y="AppOpens", title="Top 10 States with App Opens")
    st.plotly_chart(fig)

def ques6():
    # Least 10 States With AppOpens
    least_app_opens = Map_user.groupby("States")["AppOpens"].sum().nsmallest(10).reset_index()
    fig = px.bar(least_app_opens, x="States", y="AppOpens", title="Least 10 States with App Opens")
    st.plotly_chart(fig)

def ques7():
    # States With Lowest Transaction Count
    lt_count = Aggre_transaction.groupby("States")["Transaction_count"].sum().nsmallest(10).reset_index()
    fig = px.bar(lt_count, x="States", y="Transaction_count", title="States with Lowest Transaction Count")
    st.plotly_chart(fig)

def ques8():
    # States With Highest Transaction Count
    ht_count = Aggre_transaction.groupby("States")["Transaction_count"].sum().nlargest(10).reset_index()
    fig = px.bar(ht_count, x="States", y="Transaction_count", title="States with Highest Transaction Count")
    st.plotly_chart(fig)

def ques9():
    # States With Highest Transaction Amount
    ht_amount = Aggre_transaction.groupby("States")["Transaction_amount"].sum().nlargest(10).reset_index()
    fig = px.bar(ht_amount, x="States", y="Transaction_amount", title="States with Highest Transaction Amount")
    st.plotly_chart(fig)

def ques10():
    # Top 50 Districts With Lowest Transaction Amount
    lowest_districts = Map_transaction.groupby("District")["Transaction_amount"].sum().nsmallest(50).reset_index()
    fig = px.bar(lowest_districts, x="District", y="Transaction_amount", title="Top 50 Districts with Lowest Transaction Amount")
    st.plotly_chart(fig)

# Home Section
if selected_section == "Home":
    st.title("PhonePe Pulse Interactive Map")
    st.write("Explore PhonePe transaction data interactively.")

# Data Exploration Section
if selected_section == "Data Exploration":
    tab1, tab2 = st.tabs(["Map Analysis", "Transaction Analysis"])

    # Map Analysis
    with tab1:
        st.write("Select Year and Quarter to view transaction data:")
        
        # Year and Quarter selection
        years = Aggre_transaction['Years'].unique()
        quarters = Aggre_transaction['Quarter'].unique()

        selected_year = st.selectbox("Select Year", years)
        selected_quarter = st.selectbox("Select Quarter", quarters)

        # Filter data based on selection
        filtered_data = Aggre_transaction[
            (Aggre_transaction['Years'] == selected_year) & 
            (Aggre_transaction['Quarter'] == selected_quarter)
        ]

        # Aggregate transaction data by state
        transaction_data = filtered_data.groupby('States')['Transaction_amount'].sum().reset_index()

        # Merge GeoDataFrame with transaction data
        merged_gdf = gdf.merge(transaction_data, left_on='NAME_1', right_on='States', how='left')

        # Create a Folium map
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

        # Add choropleth layer to the map
        choropleth = folium.Choropleth(
            geo_data=merged_gdf.to_json(),
            data=merged_gdf,
            columns=['States', 'Transaction_amount'],
            key_on='feature.properties.NAME_1',
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'Transaction Amount in INR ({selected_year} Q{selected_quarter})'
        ).add_to(m)

        # Add tooltips for interactive information
        tooltip = GeoJsonTooltip(
            fields=['NAME_1', 'Transaction_amount'],
            aliases=['State: ', 'Transaction Amount: '],
            localize=True
        )
        folium.GeoJson(
            merged_gdf.to_json(),
            tooltip=tooltip
        ).add_to(m)

        # Display map in Streamlit
        st_folium(m, width=700, height=500)

    # Transaction Analysis
    # Transaction Analysis
    with tab2:
        st.write("### Detailed Analysis of Transactions")
        
        # Filter data for the selected year and quarter
        filtered_data = Aggre_transaction[
            (Aggre_transaction['Years'] == selected_year) & 
            (Aggre_transaction['Quarter'] == selected_quarter)
        ]
        
        # Show aggregated data by state
        transaction_summary = filtered_data.groupby("States")["Transaction_amount"].sum().reset_index()
        transaction_summary = transaction_summary.sort_values(by="Transaction_amount", ascending=False)
        st.write("#### Transaction Summary by State")
        st.dataframe(transaction_summary)
        
        # Bar chart for top 5 states by transaction amount
        st.write("#### Top 5 States by Transaction Amount")
        top_states = transaction_summary.head(5)
        bar_chart = px.bar(top_states, x="States", y="Transaction_amount", 
                        title="Top 5 States by Transaction Amount",
                        labels={"Transaction_amount": "Transaction Amount (INR)"})
        st.plotly_chart(bar_chart)
        
        # Line chart for quarterly trends
        st.write("#### Quarterly Transaction Trends")
        selected_state = st.selectbox("Select a State to view trends", transaction_summary["States"].unique())
        state_data = Aggre_transaction[
            Aggre_transaction["States"] == selected_state
        ].groupby(["Years", "Quarter"])["Transaction_amount"].sum().reset_index()
        state_data["Quarter_Label"] = state_data["Years"].astype(str) + " Q" + state_data["Quarter"].astype(str)
        
        line_chart = px.line(state_data, x="Quarter_Label", y="Transaction_amount",
                            title=f"Transaction Trends for {selected_state}",
                            labels={"Transaction_amount": "Transaction Amount (INR)"})
        st.plotly_chart(line_chart)

            # Here you can add additional graphs or details based on selected transaction data

# Top Charts Section
if selected_section == "Top Charts":
    st.subheader("Explore Key Metrics")
    ques = st.selectbox("Select the Question", [
        'Top Brands Of Mobiles Used', 'States With Lowest Transaction Amount',
        'Districts With Highest Transaction Amount', 'Top 10 Districts With Lowest Transaction Amount',
        'Top 10 States With AppOpens', 'Least 10 States With AppOpens',
        'States With Lowest Transaction Count', 'States With Highest Transaction Count',
        'States With Highest Transaction Amount', 'Top 50 Districts With Lowest Transaction Amount'
    ])
    
    if ques == "Top Brands Of Mobiles Used":
        ques1()
    elif ques == "States With Lowest Transaction Amount":
        ques2()
    elif ques == "Districts With Highest Transaction Amount":
        ques3()
    elif ques == "Top 10 Districts With Lowest Transaction Amount":
        ques4()
    elif ques == "Top 10 States With AppOpens":
        ques5()
    elif ques == "Least 10 States With AppOpens":
        ques6()
    elif ques == "States With Lowest Transaction Count":
        ques7()
    elif ques == "States With Highest Transaction Count":
        ques8()
    elif ques == "States With Highest Transaction Amount":
        ques9()
    elif ques == "Top 50 Districts With Lowest Transaction Amount":
        ques10()
