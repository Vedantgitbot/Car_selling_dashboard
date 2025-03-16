# Car Price Analysis Dashboard

This interactive dashboard, built using **Streamlit**, provides insights into car price trends and helps predict selling prices based on various factors.

## Features
- **Data Filtering:** Filter cars based on year, fuel type, seller type, transmission, and owner type.  
- **Visualizations:**  
  - Distribution of selling prices  
  - Selling Price vs Present Price  
  - Average selling price by fuel type  
  - Correlation heatmap  
  - Yearly trend of average selling prices  
- **Price Prediction:** Predict the selling price based on present price, car age, and fuel type.

## Requirements
Install the required libraries using:
```bash
pip install streamlit pandas seaborn matplotlib
```

## How to Run
1. Clone the repository or download the code.  
2. Ensure the dataset (`cardata.csv`) is placed in the correct path.  
3. Run the following command:
```bash
streamlit run app.py
```

## Dataset
The dataset used for this project is sourced from **Kaggle**:  
https://www.kaggle.com/code/melikedilekci/eda-car-data-analysis/input

Ensure your dataset includes key columns like:
- `Year`
- `Selling_Price`
- `Present_Price`
- `Fuel_Type`
- `Seller_Type`
- `Transmission`
- `Owner`

## Prediction Logic
The prediction model estimates the selling price as:  
\[
\text{Predicted Price} = \max(\text{Present Price} \times 0.8 - \text{Years Old} \times 0.1, 0)
\]

