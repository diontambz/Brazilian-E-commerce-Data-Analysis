import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

# KOnfigurasi Hhalaman
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("all_data.csv")
        
        # Handling mixed data types for categorical columns
        categorical_columns = ['customer_state', 'product_category_name_english', 'payment_type']
        for col in categorical_columns:
            if col in data.columns:
                # Convert NaN to empty string then to string type
                data[col] = data[col].fillna('').astype(str)
                # Convert empty strings back to NaN if needed
                data[col] = data[col].replace('', np.nan)
        
        # Convert timestamp columns to datetime
        datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 
                         'order_delivered_customer_date', 'order_estimated_delivery_date']
        for col in datetime_cols:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], errors='coerce')
        
        # Create year and month columns for time analysis
        if 'order_purchase_timestamp' in data.columns:
            data['year'] = data['order_purchase_timestamp'].dt.year
            data['month'] = data['order_purchase_timestamp'].dt.month
            data['yearmonth'] = data['order_purchase_timestamp'].dt.strftime('%Y-%m')
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return empty DataFrame with expected columns to prevent further errors
        return pd.DataFrame(columns=['customer_state', 'year', 'price', 'order_id', 'customer_id'])

# Main function
def main():
    # Title and description
    st.title("Brazilian E-commerce Dashboard")
    st.write("This dashboard provides insights into Brazilian e-commerce data.")
    
    # Load data
    with st.spinner("Loading data..."):
        try:
            df = load_data()
            if df.empty:
                st.error("No data loaded. Please check the file path and format.")
                return
        except Exception as e:
            st.error(f"An error occurred while loading data: {e}")
            return
    
    # Sidebar for filters
    st.sidebar.header("Filters")
    
    # Year filter
    if 'year' in df.columns and not df['year'].empty:
        # Handle mixed types by converting to string first
        years = df['year'].dropna().astype(int).unique().tolist()
        years.sort()  # Sort in-place
        selected_years = st.sidebar.multiselect("Select Years", years, default=years)
        if selected_years:
            df_filtered = df[df['year'].isin(selected_years)]
        else:
            df_filtered = df
    else:
        df_filtered = df
    
    # State filter
    if 'customer_state' in df.columns:
        # Safe way to get unique values, handling NaNs
        states = df['customer_state'].dropna().unique().tolist()
        # Convert all to string to be safe
        states = [str(state) for state in states if state]
        try:
            states.sort()  # Sort in-place
        except Exception:
            # If sorting fails, just leave it unsorted
            pass
            
        selected_states = st.sidebar.multiselect("Select States", states, default=None)
        if selected_states:
            df_filtered = df_filtered[df_filtered['customer_state'].isin(selected_states)]
    
    # Main KPIs row
    st.header("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate KPIs
    try:
        total_revenue = df_filtered['price'].sum() if 'price' in df_filtered.columns else 0
        total_orders = df_filtered['order_id'].nunique() if 'order_id' in df_filtered.columns else 0
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        unique_customers = df_filtered['customer_id'].nunique() if 'customer_id' in df_filtered.columns else 0
        
        # Format with better display
        formatted_revenue = f"$ {total_revenue:,.0f}"  # No decimal places
        formatted_aov = f"$ {avg_order_value:,.2f}"    # Two decimal places
        
        # Using markdown for better formatting control
        col1.markdown(f"### Total Revenue\n#### {formatted_revenue}")
        col2.markdown(f"### Total Orders\n#### {total_orders:,}")
        col3.markdown(f"### Average Order Value\n#### {formatted_aov}")
        col4.markdown(f"### Unique Customers\n#### {unique_customers:,}")
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Product Categories", "Revenue Trends", "Customer Distribution", "Payment Types"])
    
    with tab1:
        st.subheader("Top Selling Product Categories")
        
        try:
            # Prepare data only if required columns exist
            if all(col in df_filtered.columns for col in ['product_category_name_english', 'order_item_id', 'price']):
                product_sales = df_filtered.groupby('product_category_name_english').agg({
                    "order_item_id": "count", 
                    "price": "sum"
                }).reset_index()
                product_sales.columns = ['product_category', 'sales_count', 'revenue']
                product_sales = product_sales.sort_values(by="sales_count", ascending=False)
                
                # Slider to select number of categories to display
                max_categories = min(20, len(product_sales))
                if max_categories > 0:
                    top_n = st.slider("Select number of top categories to display", 5, max_categories, min(10, max_categories))
                    top_categories = product_sales.head(top_n)
                    
                    # Plot
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = px.bar(
                            top_categories,
                            y='product_category',
                            x='sales_count',
                            orientation='h',
                            title=f'Top {top_n} Product Categories by Sales Count',
                            color='sales_count',
                            color_continuous_scale='Viridis'
                        )
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(
                            top_categories,
                            y='product_category',
                            x='revenue',
                            orientation='h',
                            title=f'Top {top_n} Product Categories by Revenue',
                            color='revenue',
                            color_continuous_scale='Viridis'
                        )
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No product category data available.")
            else:
                st.warning("Required columns for product category analysis are missing.")
        except Exception as e:
            st.error(f"Error in Product Categories tab: {e}")

    with tab2:
        st.subheader("Revenue Trends Over Time")
        
        try:
            # Time period selector (only if we have year data)
            if 'year' in df_filtered.columns and not df_filtered['year'].empty:
                time_period = st.radio("Select Time Period", ["Monthly", "Yearly"], horizontal=True)
                
                if time_period == "Yearly" and 'year' in df_filtered.columns and 'price' in df_filtered.columns:
                    # Yearly revenue
                    revenue_per_year = df_filtered.groupby('year')['price'].sum().reset_index()
                    
                    fig = px.bar(
                        revenue_per_year,
                        x='year',
                        y='price',
                        title='Total Revenue per Year',
                        labels={'price': 'Revenue ($)', 'year': 'Year'},
                        color='price',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif time_period == "Monthly" and 'yearmonth' in df_filtered.columns and 'price' in df_filtered.columns:
                    # Monthly revenue
                    revenue_per_month = df_filtered.groupby('yearmonth')['price'].sum().reset_index()
                    revenue_per_month = revenue_per_month.sort_values('yearmonth')
                    
                    fig = px.line(
                        revenue_per_month,
                        x='yearmonth',
                        y='price',
                        title='Monthly Revenue Trend',
                        labels={'price': 'Revenue ($)', 'yearmonth': 'Month'},
                        markers=True
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Required data for the selected time period is not available.")
            else:
                st.warning("Time-based data is not available for analysis.")
        except Exception as e:
            st.error(f"Error in Revenue Trends tab: {e}")
    
    with tab3:
        st.subheader("Customer Distribution by State")
        
        try:
            # Count customers by state
            if all(col in df_filtered.columns for col in ['customer_state', 'customer_id', 'order_id', 'price']):
                customer_by_state = df_filtered.groupby('customer_state').agg({
                    'customer_id': 'nunique',
                    'order_id': 'nunique',
                    'price': 'sum'
                }).reset_index()
                customer_by_state.columns = ['state', 'customer_count', 'order_count', 'revenue']
                customer_by_state = customer_by_state.sort_values('customer_count', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        customer_by_state,
                        x='state',
                        y='customer_count',
                        title='Number of Unique Customers by State',
                        color='customer_count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Alternative visualization if map data is not available
                    fig = px.pie(
                        customer_by_state.head(10),
                        values='customer_count',
                        names='state',
                        title='Top 10 States by Customer Count (Distribution)',
                        hole=0.4
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Required columns for customer distribution analysis are missing.")
        except Exception as e:
            st.error(f"Error in Customer Distribution tab: {e}")
    
    with tab4:
        st.subheader("Payment Methods Analysis")
        
        try:
            # Count payment types
            if 'payment_type' in df_filtered.columns:
                payment_types = df_filtered['payment_type'].value_counts().reset_index()
                payment_types.columns = ['payment_type', 'count']
                
                # Check if payment value column exists
                if 'payment_value' in df_filtered.columns:
                    # Payment amount by type
                    payment_amount = df_filtered.groupby('payment_type')['payment_value'].sum().reset_index()
                    payment_amount = payment_amount.sort_values('payment_value', ascending=False)
                
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = px.bar(
                            payment_types,
                            y='payment_type',
                            x='count',
                            orientation='h',
                            title='Payment Methods by Frequency',
                            color='count',
                            color_continuous_scale='Viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.pie(
                            payment_types,
                            values='count',
                            names='payment_type',
                            title='Payment Method Distribution',
                            hole=0.4
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Average payment value by type
                    avg_payment = df_filtered.groupby('payment_type')['payment_value'].mean().reset_index()
                    avg_payment.columns = ['payment_type', 'avg_payment']
                    avg_payment = avg_payment.sort_values('avg_payment', ascending=False)
                    
                    fig = px.bar(
                        avg_payment,
                        x='payment_type',
                        y='avg_payment',
                        title='Average Payment Value by Method',
                        color='avg_payment',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Simplified view if payment_value is not available
                    fig = px.bar(
                        payment_types,
                        y='payment_type',
                        x='count',
                        orientation='h',
                        title='Payment Methods by Frequency',
                        color='count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Payment type data is not available.")
        except Exception as e:
            st.error(f"Error in Payment Types tab: {e}")
    
    # Footer
    st.markdown('---')
    st.caption('Dashboard created by Dion Sandy Ara Tambunan')

if __name__ == "__main__":
    main()