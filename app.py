import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('cardata.csv')
    return df

df = load_data()

if 'Year' in df.columns:
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
else:
    st.error("The dataset is missing the 'Year' column. Please check the data.")
    df = pd.DataFrame()

st.title("Car Price Analysis")

if not df.empty:
    st.sidebar.title("Filters")

    year_filter = st.sidebar.slider(
        "Select Year Range",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(2010, 2020)
    )
    fuel_type_filter = st.sidebar.multiselect("Fuel Type", options=df['Fuel_Type'].unique(), default=df['Fuel_Type'].unique())
    seller_type_filter = st.sidebar.multiselect("Seller Type", options=df['Seller_Type'].unique(), default=df['Seller_Type'].unique())
    transmission_filter = st.sidebar.multiselect("Transmission", options=df['Transmission'].unique(), default=df['Transmission'].unique())
    owner_filter = st.sidebar.selectbox("Owner Type", options=df['Owner'].unique())

    filtered_df = df[
        (df['Year'] >= year_filter[0]) & (df['Year'] <= year_filter[1]) &
        (df['Fuel_Type'].isin(fuel_type_filter)) &
        (df['Seller_Type'].isin(seller_type_filter)) &
        (df['Transmission'].isin(transmission_filter)) &
        (df['Owner'] == owner_filter)
    ]

    st.subheader("Filtered Dataset")
    st.write(filtered_df)

    st.subheader("Selling Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['Selling_Price'], kde=True, ax=ax)
    ax.set_title("Distribution of Selling Prices")
    ax.set_xlabel("Selling Price")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.subheader("Selling Price vs Present Price")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='Present_Price', y='Selling_Price', hue='Fuel_Type', ax=ax)
    ax.set_title("Selling Price vs Present Price")
    ax.set_xlabel("Present Price")
    ax.set_ylabel("Selling Price")
    st.pyplot(fig)

    st.subheader("Average Selling Price by Fuel Type")
    avg_price_by_fuel = filtered_df.groupby('Fuel_Type')['Selling_Price'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_price_by_fuel.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Average Selling Price by Fuel Type")
    ax.set_xlabel("Fuel Type")
    ax.set_ylabel("Average Selling Price")
    st.pyplot(fig)
    
    st.subheader("Correlation Heatmap")
if not filtered_df.empty:
    # Select only numeric columns for correlation calculation
    numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
    
    if numeric_df.shape[1] > 1:  # Ensure there are at least two numeric columns
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Correlation Between Features")
        st.pyplot(fig)
    else:
        st.warning("Not enough numeric data available for a correlation heatmap.")
else:
    st.warning("No data available to generate the correlation heatmap.")


st.subheader("Yearly Trend of Average Selling Price")
if not filtered_df.empty:
    avg_price_by_year = filtered_df.groupby('Year')['Selling_Price'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_price_by_year.plot(kind='line', marker='o', ax=ax)
    ax.set_title("Average Selling Price Over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Selling Price")
    st.pyplot(fig)
else:
    st.warning("No data available to generate the yearly trend of average selling price.")

st.sidebar.header("Predict Selling Price")
present_price = st.sidebar.number_input("Present Price (in lakhs)", min_value=0.0, max_value=50.0, step=0.1, value=5.0)
years_old = st.sidebar.number_input("Age of the Car (Years)", min_value=0, max_value=30, step=1, value=5)
fuel_type = st.sidebar.selectbox("Fuel Type", options=['Petrol', 'Diesel', 'CNG'])

if st.sidebar.button("Predict"):
    predicted_price = max(present_price * 0.8 - years_old * 0.1, 0)  # Ensure non-negative price
    st.sidebar.write(f"Predicted Selling Price: ₹{predicted_price:.2f} lakhs")
else:
    st.sidebar.write("Enter details above and click 'Predict' to estimate selling price.")


    st.sidebar.write("Additional insights coming soon!")



