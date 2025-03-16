import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Damac Safa Two Property Analysis",
    page_icon="🏢",
    layout="wide"
)

# Create a directory for results
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Hard-coded property data from Safa Two
PROPERTY_DATA = [
    # Studios
    {"project": "Safa Two", "property_type": "Apartment", "price": 949000, "area_sqft": 358, "bedrooms": "studio", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Spacious Layout | High Floor | Motivated Seller"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1280000, "area_sqft": 626, "bedrooms": "studio", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "2% commission | 6% BELOW OP | Luxurious Unit"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1320000, "area_sqft": 470, "bedrooms": "studio", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Stunning Views |Studio Apartment | High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1507000, "area_sqft": 730, "bedrooms": "studio", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Branded and Spacious Studio | High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1715000, "area_sqft": 697, "bedrooms": "studio", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Canal View | Mid Floor | 3.75% Payment Plan"},
    
    # 1 Bedroom
    {"project": "Safa Two", "property_type": "Apartment", "price": 1490000, "area_sqft": 791, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Super Distress Deal | Premium project | Below 20%"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1595000, "area_sqft": 683, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxurious Design | Amazing View | on Payment Plan"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1600000, "area_sqft": 789, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "12% Under OP | Investor Deal | Premium View | 2027 PP"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1634880, "area_sqft": 714, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Stunning Safa Views| High Floor | Branded Unit"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1660000, "area_sqft": 713, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "ULTRA LUXURY | INCREDIBLE VIEW | BELOW OP"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1700000, "area_sqft": 792, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "BELOW OP | SEA VIEW | HIGH FLOOR | FULLY PAID"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1700000, "area_sqft": 792, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "SEA VIEW | HIGH FLOOR | Q2 2027 | FULLY PAID"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1780000, "area_sqft": 830, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Prime location | 20% BELOW ORIGINAL PRICE"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1800000, "area_sqft": 744, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "1 Bed | High Floor | Payment Plan | Close to OP"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1825000, "area_sqft": 831, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "INVESTOR DEAL | PRIME LOCATION | HIGH FLOOR"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1843500, "area_sqft": 758, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Premium View | Luxurious | De Grisogono Interiors"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1850000, "area_sqft": 775, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "1BR with Spectacular View | High Floor | Spacious"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1900000, "area_sqft": 745, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Sea view | Safa 2 | Q3 2027 | Luxurious Design"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1900000, "area_sqft": 753, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Spacious >> Canal view >> Best price"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1990000, "area_sqft": 771, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Branded and fully furnished | cozy unit with balcony"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1999989, "area_sqft": 827, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "High Floor | Motivated Seller | Sea View"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2000000, "area_sqft": 803, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Distressed Deal Motivated Seller | Very High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2000000, "area_sqft": 744, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Damac | Safa Two | High floor | Q2 2027 Handover"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2170000, "area_sqft": 775, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Higher Floor || Modern Unit 1 Bedroom || Sea View"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2175000, "area_sqft": 762, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "LOW PRICE | PARK & SEA VIEW | HIGH FLOOR"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2200000, "area_sqft": 812, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxury 1-Bedroom Apartment with Stunning Views"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2200000, "area_sqft": 829, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Premium layout | High floor | Best price"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2222000, "area_sqft": 744, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Damac | Safa Two | Sea view | High floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2222000, "area_sqft": 771, "bedrooms": "1", "bathrooms": "1", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Damac | Safa Two | Sea view | High floor | 1Br"},
    
    # 1 Bedroom with 2 Bathrooms
    {"project": "Safa Two", "property_type": "Apartment", "price": 1599000, "area_sqft": 757, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "High ROI | Burj-Palm Views| Luxury High-Rise Tower"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1650000, "area_sqft": 794, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Below OP | High Floor | City View | Comfortable Payment Plan"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1690000, "area_sqft": 795, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Sea View | High Floor | Below Market Price"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1800000, "area_sqft": 776, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "High Floor | Sea View | Serious Seller"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1850000, "area_sqft": 776, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Sea View | Negotiable | Urgent Sale | High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1889999, "area_sqft": 774, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Original Price | Very High Floor | Downtown View"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 1900000, "area_sqft": 688, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Multiple Units | 1-Bedroom Apartment | Prime Location"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2800000, "area_sqft": 744, "bedrooms": "1", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Ultra Luxury Unit /Above 70th Floor /Full Seaview"},
    
    # 2 Bedrooms
    {"project": "Safa Two", "property_type": "Apartment", "price": 2293200, "area_sqft": 1154, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxury 2-bedroom | Middle Floor | Prime Location"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2405000, "area_sqft": 1208, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Sleek Design | Community View |Convenient Location"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2436525, "area_sqft": 1172, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "15% Below Original Price | Above 55TH Floor |"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2450000, "area_sqft": 1054, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Eminence Homes Real Estate"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2550000, "area_sqft": 1208, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Resale Payment Plan Branded Residence I High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2700000, "area_sqft": 1138, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxury Unit | Payment Plan | Exclusive Resale"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2750000, "area_sqft": 1355, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Distress | Lower OP | Damac Luxury 2br | Sea view"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2850000, "area_sqft": 1138, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "PERFECT LAYOUT l LUXURY UNIT | 2 BHK"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2900000, "area_sqft": 1144, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Iconic Design | Unique Feature | Ultra Luxury"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2900000, "area_sqft": 1172, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Resale| High floor| Dubai Canal and Park view"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3050000, "area_sqft": 1145, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxury + Spacious 2BR | Prime Location | City View"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3299000, "area_sqft": 1463, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Damac | Bargain | High floor | Q2 2027 Handover"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3375900, "area_sqft": 1148, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Excellent Location | Branded Luxury Residence | High View"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3450000, "area_sqft": 1049, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Great Investment | Prime Spot | Premium Amenities"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4300000, "area_sqft": 1420, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Exclusive | Luxury | High Floor | PHPP"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4554200, "area_sqft": 1311, "bedrooms": "2", "bathrooms": "2", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxury Branded Apartment | Exceptional Opportunity"},
    
    # 2 Bedrooms with 3 Bathrooms
    {"project": "Safa Two", "property_type": "Apartment", "price": 2600000, "area_sqft": 1172, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Branded Residence | Genuine Resale | High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2700000, "area_sqft": 1124, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Luxurious | Burj Khalifa View | High Floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2700000, "area_sqft": 1294, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "EZ Properties"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2850000, "area_sqft": 1130, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Welcome agents | Price is negotiable | Middle floor"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 2850000, "area_sqft": 1557, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "BELOW ORIGINAL PRICE | HUGE PREMIUM LAYOUT | BRANDED RESIDENCE"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3200000, "area_sqft": 1399, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Provident Estate"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3600000, "area_sqft": 1426, "bedrooms": "2", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Corner 2 beds, payment plan, Downtown view"},
    
    # 3 Bedrooms
    {"project": "Safa Two", "property_type": "Apartment", "price": 3269890, "area_sqft": 1493, "bedrooms": "3", "bathrooms": "4", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Skyline Views | Luxurious 3BR | Investor Deal"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3269990, "area_sqft": 1484, "bedrooms": "3", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Downtown Skyline Views | Luxury Living | Ready in 2027"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 3800000, "area_sqft": 1503, "bedrooms": "3", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "haus & haus Real Estate"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4250000, "area_sqft": 1735, "bedrooms": "3", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Exclusif 3 Bed, Corner, Tower A - Sea, Canal View"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4477000, "area_sqft": 1523, "bedrooms": "3", "bathrooms": "3", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Exclusive 3 Bedroom | 70+ Floor | Safa Two Tower A"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4500000, "area_sqft": 2001, "bedrooms": "3", "bathrooms": "4", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Driven Properties"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4900000, "area_sqft": 1658, "bedrooms": "3", "bathrooms": "4", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "High Floor | Corner Unit | Two balconies and study"},
    {"project": "Safa Two", "property_type": "Apartment", "price": 4995000, "area_sqft": 1710, "bedrooms": "3", "bathrooms": "4", "location": "Business Bay, Dubai", "developer": "Damac Properties", "description": "Premium View I Corner Unit I 3 BHK I At Safa Two"}
]

def analyze_data(property_data):
    """Analyze the property data"""
    # Convert to DataFrame
    df = pd.DataFrame(property_data)
    
    # Calculate price per sqft
    df['price_per_sqft'] = df['price'] / df['area_sqft']
    
    # Basic statistics overall
    stats_overall = {
        'total_listings': len(df),
        'avg_price': df['price'].mean(),
        'min_price': df['price'].min(),
        'max_price': df['price'].max(),
        'median_price': df['price'].median(),
        'avg_price_per_sqft': df['price_per_sqft'].mean(),
        'min_price_per_sqft': df['price_per_sqft'].min(),
        'max_price_per_sqft': df['price_per_sqft'].max(),
        'avg_area': df['area_sqft'].mean(),
        'min_area': df['area_sqft'].min(),
        'max_area': df['area_sqft'].max()
    }
    
    # Group by bedroom type and calculate statistics
    bedroom_stats = df.groupby('bedrooms').agg({
        'price': ['count', 'min', 'max', 'mean', 'median'],
        'area_sqft': ['min', 'max', 'mean'],
        'price_per_sqft': ['min', 'max', 'mean']
    }).reset_index()
    
    # Rename columns for clarity
    bedroom_stats.columns = ['bedrooms', 'count', 'min_price', 'max_price', 'avg_price', 'median_price', 
                            'min_area', 'max_area', 'avg_area', 'min_price_per_sqft', 
                            'max_price_per_sqft', 'avg_price_per_sqft']
    
    # Sort by bedrooms (with studio first, then numeric)
    bedroom_order = {'studio': 0, '1': 1, '2': 2, '3': 3}
    bedroom_stats['bedroom_order'] = bedroom_stats['bedrooms'].map(bedroom_order)
    bedroom_stats = bedroom_stats.sort_values('bedroom_order').drop('bedroom_order', axis=1)
    
    # Statistics by bathroom count
    bathroom_stats = df.groupby(['bedrooms', 'bathrooms']).agg({
        'price': ['count', 'min', 'max', 'mean'],
        'area_sqft': ['min', 'max', 'mean'],
        'price_per_sqft': 'mean'
    }).reset_index()
    
    # Rename columns for clarity
    bathroom_stats.columns = ['bedrooms', 'bathrooms', 'count', 'min_price', 'max_price', 'avg_price', 
                             'min_area', 'max_area', 'avg_area', 'avg_price_per_sqft']
    
    # Sort by bedrooms and bathrooms
    bathroom_stats['bedroom_order'] = bathroom_stats['bedrooms'].map(bedroom_order)
    bathroom_stats = bathroom_stats.sort_values(['bedroom_order', 'bathrooms']).drop('bedroom_order', axis=1)
    
    return {
        'dataframe': df,
        'stats_overall': stats_overall,
        'bedroom_stats': bedroom_stats,
        'bathroom_stats': bathroom_stats
    }

def generate_visualizations(analysis_results):
    """Generate visualizations from analysis results"""
    if not analysis_results or 'dataframe' not in analysis_results:
        return {}
        
    df = analysis_results['dataframe']
    figures = {}
    
    # Set the style
    sns.set(style="whitegrid")
    
    # Price distribution by bedroom type
    try:
        fig_price, ax_price = plt.subplots(figsize=(12, 6))
        
        # Create a box plot for price by bedroom type
        bedroom_order = ['studio', '1', '2', '3']
        sns.boxplot(x='bedrooms', y='price', data=df, order=bedroom_order, ax=ax_price)
        
        # Format y-axis to show in millions
        ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x/1000000:.1f}M"))
        
        ax_price.set_title('Price Distribution by Bedroom Type', fontsize=14)
        ax_price.set_xlabel('Bedrooms', fontsize=12)
        ax_price.set_ylabel('Price (AED)', fontsize=12)
        plt.tight_layout()
        
        figures['price_by_bedroom'] = fig_price
    except Exception as e:
        st.error(f"Error generating price by bedroom chart: {e}")
    
    # Area distribution by bedroom type
    try:
        fig_area, ax_area = plt.subplots(figsize=(12, 6))
        
        # Create a box plot for area by bedroom type
        sns.boxplot(x='bedrooms', y='area_sqft', data=df, order=bedroom_order, ax=ax_area)
        
        ax_area.set_title('Area Distribution by Bedroom Type', fontsize=14)
        ax_area.set_xlabel('Bedrooms', fontsize=12)
        ax_area.set_ylabel('Area (sq.ft)', fontsize=12)
        plt.tight_layout()
        
        figures['area_by_bedroom'] = fig_area
    except Exception as e:
        st.error(f"Error generating area by bedroom chart: {e}")
    
    # Price per sq.ft by bedroom type
    try:
        fig_ppsf, ax_ppsf = plt.subplots(figsize=(12, 6))
        
        # Create a box plot for price per sq.ft by bedroom type
        sns.boxplot(x='bedrooms', y='price_per_sqft', data=df, order=bedroom_order, ax=ax_ppsf)
        
        ax_ppsf.set_title('Price per Sq.Ft by Bedroom Type', fontsize=14)
        ax_ppsf.set_xlabel('Bedrooms', fontsize=12)
        ax_ppsf.set_ylabel('Price per Sq.Ft (AED)', fontsize=12)
        plt.tight_layout()
        
        figures['ppsf_by_bedroom'] = fig_ppsf
    except Exception as e:
        st.error(f"Error generating price per sq.ft by bedroom chart: {e}")
    
    # Distribution of price per sq.ft overall
    try:
        fig_ppsf_dist, ax_ppsf_dist = plt.subplots(figsize=(12, 6))
        
        # Create a histogram with KDE for price per sq.ft
        sns.histplot(df['price_per_sqft'], kde=True, ax=ax_ppsf_dist)
        
        ax_ppsf_dist.set_title('Distribution of Price per Sq.Ft', fontsize=14)
        ax_ppsf_dist.set_xlabel('Price per Sq.Ft (AED)', fontsize=12)
        ax_ppsf_dist.set_ylabel('Count', fontsize=12)
        
        # Add a vertical line for the mean
        mean_ppsf = df['price_per_sqft'].mean()
        ax_ppsf_dist.axvline(mean_ppsf, color='red', linestyle='dashed', linewidth=2)
        ax_ppsf_dist.text(mean_ppsf*1.05, ax_ppsf_dist.get_ylim()[1]*0.9, f'Mean: {mean_ppsf:.0f} AED', 
                       color='red', fontweight='bold')
        
        plt.tight_layout()
        figures['ppsf_distribution'] = fig_ppsf_dist
    except Exception as e:
        st.error(f"Error generating price per sq.ft distribution chart: {e}")
    
    # Scatter plot of price vs. area
    try:
        fig_scatter, ax_scatter = plt.subplots(figsize=(12, 6))
        
        # Create scatter plot with different colors for bedroom types
        for bed_type in bedroom_order:
            bed_data = df[df['bedrooms'] == bed_type]
            ax_scatter.scatter(bed_data['area_sqft'], bed_data['price'], 
                          label=f"{bed_type} BR", alpha=0.7)
        
        # Add best fit line
        sns.regplot(x='area_sqft', y='price', data=df, scatter=False, ax=ax_scatter, color='black')
        
        # Format y-axis to show in millions
        ax_scatter.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x/1000000:.1f}M"))
        
        ax_scatter.set_title('Price vs. Area', fontsize=14)
        ax_scatter.set_xlabel('Area (sq.ft)', fontsize=12)
        ax_scatter.set_ylabel('Price (AED)', fontsize=12)
        ax_scatter.legend(title="Bedrooms")
        plt.tight_layout()
        
        figures['price_vs_area'] = fig_scatter
    except Exception as e:
        st.error(f"Error generating price vs. area chart: {e}")
    
    return figures

def save_to_csv(df, filename="safa_two_properties.csv"):
    """Save DataFrame to CSV"""
    filepath = os.path.join(RESULTS_DIR, filename)
    df.to_csv(filepath, index=False)
    return filepath

def format_currency(value):
    """Format currency values for display"""
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        if value >= 1000000:
            return f"AED {value/1000000:.2f}M"
        return f"AED {value:,.0f}"
    return value

def format_area(value):
    """Format area values for display"""
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:,.0f} sq.ft"
    return value

# Main function to run the Streamlit app
def main():
    st.title("Damac Safa Two Property Analysis")
    
    # Analyze data
    analysis_results = analyze_data(PROPERTY_DATA)
    
    # Save to CSV
    csv_path = save_to_csv(analysis_results['dataframe'])
    
    # Display overall statistics
    st.header("Overview")
    stats = analysis_results['stats_overall']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Listings", stats['total_listings'])
    with col2:
        st.metric("Average Price", format_currency(stats['avg_price']))
    with col3:
        st.metric("Price Range", f"{format_currency(stats['min_price'])} - {format_currency(stats['max_price'])}")
    with col4:
        st.metric("Average Price/sq.ft", f"AED {stats['avg_price_per_sqft']:,.0f}")
    
    # Statistics by bedroom type
    st.header("Unit Types Summary")
    
    # Format the bedroom statistics table
    bedroom_stats = analysis_results['bedroom_stats'].copy()
    for col in ['min_price', 'max_price', 'avg_price', 'median_price']:
        bedroom_stats[col] = bedroom_stats[col].apply(format_currency)
    
    for col in ['min_area', 'max_area', 'avg_area']:
        bedroom_stats[col] = bedroom_stats[col].apply(format_area)
    
    for col in ['min_price_per_sqft', 'max_price_per_sqft', 'avg_price_per_sqft']:
        bedroom_stats[col] = bedroom_stats[col].apply(lambda x: f"AED {x:,.0f}")
    
    bedroom_stats.columns = ['Bedrooms', 'Count', 'Min Price', 'Max Price', 'Avg Price', 'Median Price', 
                           'Min Area', 'Max Area', 'Avg Area', 'Min Price/sq.ft', 
                           'Max Price/sq.ft', 'Avg Price/sq.ft']
    
    st.table(bedroom_stats)
    
    # Create simplified unit type summary box
    st.subheader("Simplified Unit Types")
    simplified_df = pd.DataFrame({
        'Unit Type': ['Studio', '1 Bedroom', '2 Bedroom', '3 Bedroom'],
        'Size Range (sq.ft)': [
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == 'studio', 'min_area'].values[0]:.0f} - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == 'studio', 'max_area'].values[0]:.0f}",
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '1', 'min_area'].values[0]:.0f} - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '1', 'max_area'].values[0]:.0f}",
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '2', 'min_area'].values[0]:.0f} - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '2', 'max_area'].values[0]:.0f}",
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '3', 'min_area'].values[0]:.0f} - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '3', 'max_area'].values[0]:.0f}"
        ],
        'Price Range (AED)': [
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == 'studio', 'min_price'].values[0]/1000000:.2f}M - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == 'studio', 'max_price'].values[0]/1000000:.2f}M",
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '1', 'min_price'].values[0]/1000000:.2f}M - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '1', 'max_price'].values[0]/1000000:.2f}M",
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '2', 'min_price'].values[0]/1000000:.2f}M - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '2', 'max_price'].values[0]/1000000:.2f}M",
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '3', 'min_price'].values[0]/1000000:.2f}M - {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '3', 'max_price'].values[0]/1000000:.2f}M"
        ],
        'Average Price/sq.ft': [
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == 'studio', 'avg_price_per_sqft'].values[0]:.0f}",
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '1', 'avg_price_per_sqft'].values[0]:.0f}",
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '2', 'avg_price_per_sqft'].values[0]:.0f}",
            f"AED {analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '3', 'avg_price_per_sqft'].values[0]:.0f}"
        ],
        'Available Units': [
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == 'studio', 'count'].values[0]:.0f}",
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '1', 'count'].values[0]:.0f}",
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '2', 'count'].values[0]:.0f}",
            f"{analysis_results['bedroom_stats'].loc[analysis_results['bedroom_stats']['bedrooms'] == '3', 'count'].values[0]:.0f}"
        ]
    })
    
    st.table(simplified_df)
    
    # Detailed analysis by bedroom and bathroom
    st.header("Detailed Analysis by Bedroom/Bathroom Configuration")
    
    # Format the bathroom statistics table
    bathroom_stats = analysis_results['bathroom_stats'].copy()
    bathroom_stats['unit_type'] = bathroom_stats.apply(lambda row: f"{row['bedrooms']} BR, {row['bathrooms']} Bath", axis=1)
    bathroom_stats['min_price'] = bathroom_stats['min_price'].apply(format_currency)
    bathroom_stats['max_price'] = bathroom_stats['max_price'].apply(format_currency)
    bathroom_stats['avg_price'] = bathroom_stats['avg_price'].apply(format_currency)
    bathroom_stats['min_area'] = bathroom_stats['min_area'].apply(format_area)
    bathroom_stats['max_area'] = bathroom_stats['max_area'].apply(format_area)
    bathroom_stats['avg_area'] = bathroom_stats['avg_area'].apply(format_area)
    bathroom_stats['avg_price_per_sqft'] = bathroom_stats['avg_price_per_sqft'].apply(lambda x: f"AED {x:,.0f}")
    
    bathroom_stats = bathroom_stats[['unit_type', 'count', 'min_price', 'max_price', 'avg_price', 
                                    'min_area', 'max_area', 'avg_area', 'avg_price_per_sqft']]
    bathroom_stats.columns = ['Unit Type', 'Count', 'Min Price', 'Max Price', 'Avg Price', 
                            'Min Area', 'Max Area', 'Avg Area', 'Avg Price/sq.ft']
    
    st.table(bathroom_stats)
    
    # Generate and display visualizations
    st.header("Visualizations")
    figures = generate_visualizations(analysis_results)
    
    # Display price by bedroom chart
    if 'price_by_bedroom' in figures:
        st.subheader("Price Distribution by Bedroom Type")
        st.pyplot(figures['price_by_bedroom'])
    
    # Display area by bedroom chart
    if 'area_by_bedroom' in figures:
        st.subheader("Area Distribution by Bedroom Type")
        st.pyplot(figures['area_by_bedroom'])
    
    # Display price per sq.ft by bedroom chart
    if 'ppsf_by_bedroom' in figures:
        st.subheader("Price per Sq.Ft by Bedroom Type")
        st.pyplot(figures['ppsf_by_bedroom'])
    
    # Display price per sq.ft distribution chart
    if 'ppsf_distribution' in figures:
        st.subheader("Distribution of Price per Sq.Ft")
        st.pyplot(figures['ppsf_distribution'])
    
    # Display price vs. area scatter plot
    if 'price_vs_area' in figures:
        st.subheader("Price vs. Area")
        st.pyplot(figures['price_vs_area'])
    
    # Property listings
    st.header("Property Listings")
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        bedroom_filter = st.selectbox("Filter by Bedrooms", 
                                    ["All"] + list(analysis_results['dataframe']['bedrooms'].unique()))
    with col2:
        price_sort = st.selectbox("Sort by Price", ["Low to High", "High to Low"])
    
    # Apply filters and sorting
    filtered_df = analysis_results['dataframe']
    if bedroom_filter != "All":
        filtered_df = filtered_df[filtered_df['bedrooms'] == bedroom_filter]
    
    if price_sort == "Low to High":
        filtered_df = filtered_df.sort_values('price')
    else:
        filtered_df = filtered_df.sort_values('price', ascending=False)
    
    # Format DataFrame for display
    display_df = filtered_df.copy()
    display_df['price'] = display_df['price'].apply(format_currency)
    display_df['area_sqft'] = display_df['area_sqft'].apply(format_area)
    display_df['price_per_sqft'] = display_df['price_per_sqft'].apply(lambda x: f"AED {x:,.0f}")
    
    # Select columns for display
    display_df = display_df[['bedrooms', 'bathrooms', 'price', 'area_sqft', 'price_per_sqft', 'description']]
    display_df.columns = ['Bedrooms', 'Bathrooms', 'Price', 'Area', 'Price/sq.ft', 'Description']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Download link for CSV
    st.download_button(
        label="Download Complete Data as CSV",
        data=open(csv_path, 'rb').read(),
        file_name="safa_two_properties.csv",
        mime="text/csv"
    )
    
    # Project information
    st.header("About Damac Safa Two")
    st.markdown("""
    ## Damac Safa Two
    
    Damac Safa Two is a luxury residential development by Damac Properties located in Business Bay, Dubai. 
    
    ### Key Information:
    - **Developer**: Damac Properties
    - **Location**: Business Bay, Dubai
    - **Expected Completion**: Q2 2027
    - **Unit Types**: Studios, 1, 2, and 3 Bedroom Apartments
    - **Payment Plan**: 20/55/25 or other flexible plans available
    
    ### Key Features:
    - Luxury branded residences with De Grisogono interiors
    - Premium views of Dubai Canal, Downtown, and sea views
    - High-end amenities including infinity pools, spa, fitness center
    - Strategic location close to Downtown Dubai and major attractions
    """)

# Run the Streamlit app
if __name__ == "__main__":
    main()
