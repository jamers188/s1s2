import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Damac Safa Properties Analysis",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced custom CSS styling
st.markdown("""
<style>
    /* General typography */
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Header styles */
    .main-header {
        font-size: 38px !important;
        font-weight: 700;
        color: #0d3b66;
        margin-bottom: 30px;
        text-align: center;
        padding: 20px 0;
        border-bottom: 2px solid #f0f2f6;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 24px;
        font-weight: 600;
        color: #0d3b66;
        margin-top: 35px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid #e0e7ff;
    }
    
    .project-title {
        font-size: 30px;
        font-weight: 600;
        color: #0d3b66;
        margin: 25px 0 20px 0;
        text-align: center;
        padding: 10px 0;
        border-bottom: 1px solid #e0e7ff;
    }
    
    /* Card styles */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        border: 1px solid #f0f2f6;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0d3b66;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
    }
    
    .info-box {
        background-color: #f0f7ff;
        border-left: 5px solid #0d3b66;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .data-table {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
        margin-top: 15px;
        margin-bottom: 30px;
    }
    
    .project-card {
        background-color: white;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease;
        border: 1px solid #f0f2f6;
        height: 100%;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .project-image {
        border-radius: 8px;
        width: 100%;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .project-image:hover {
        transform: scale(1.02);
    }
    
    /* Table styles */
    .compare-table th {
        background-color: #f0f7ff;
        padding: 12px !important;
    }
    
    .compare-table td {
        padding: 12px !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc;
        border-radius: 4px 4px 0 0;
        padding: 8px 20px !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0d3b66 !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0d3b66;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 4px 15px;
        border: none;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:hover {
        background-color: #0a2a4a;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 6px;
        background-color: #f8fafc;
        border-color: #e2e8f0;
    }
    
    /* Dataframe styling */
    .dataframe-container {
        border-radius: 12px !important;
        overflow: hidden !important;
        margin-top: 15px;
    }
    
    .dataframe-container [data-testid="stDataFrame"] div {
        border-radius: 12px !important;
    }
    
    .highlight {
        font-weight: 600;
        color: #0d3b66;
    }
    
    .tab-content {
        padding: 25px 0;
    }
    
    .footer {
        margin-top: 60px;
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding: 20px 0;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Custom badges */
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
    }
    
    .badge-blue {
        background-color: #dbeafe;
        color: #1e40af;
    }
    
    .badge-green {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .badge-orange {
        background-color: #ffedd5;
        color: #9a3412;
    }
    
    /* Feature list styling */
    .feature-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    .feature-list li {
        margin-bottom: 8px;
        position: relative;
        padding-left: 22px;
    }
    
    .feature-list li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #0d3b66;
        font-weight: bold;
    }
    
    /* Container styling */
    .content-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
    
    /* Misc */
    hr.divider {
        margin: 30px 0;
        border: none;
        height: 1px;
        background-color: #e2e8f0;
    }
    
    .plotly-chart {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        padding: 15px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Create a directory for results
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Hard-coded property data from Safa Two
SAFA_TWO_DATA = [
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

# Hard-coded property data from Safa One
SAFA_ONE_DATA = [
    # 1 Bedroom properties 
    {"project": "Safa One", "property_type": "Apartment", "price": 1600000, "area_sqft": 838, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "-14% Below Original Price | High Floor | HO 2026"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1699990, "area_sqft": 840, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "High Floor | Prime Location | Handover 2026"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1742182, "area_sqft": 838, "bedrooms": "1", "bathrooms": "1", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Sea, Burj Al Arab View | Prime Location | Spacious"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1750000, "area_sqft": 836, "bedrooms": "1", "bathrooms": "1", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "High Floor | Amazing View | Exclusive Listing"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1790000, "area_sqft": 838, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Below Original Price | High Floor | Handover 2026"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1811000, "area_sqft": 838, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Amazing View | High Floor | Pool-Canal View"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1811000, "area_sqft": 838, "bedrooms": "1", "bathrooms": "1", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Investor Deal | Spacious | Canal View"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1850000, "area_sqft": 836, "bedrooms": "1", "bathrooms": "1", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Urgent Sale | Selling Below Original Price"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1873000, "area_sqft": 850, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Investor Deal | High Floor | Sea and Sunset View"},
    {"project": "Safa One", "property_type": "Apartment", "price": 1873000, "area_sqft": 840, "bedrooms": "1", "bathrooms": "1", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Prime Location| Sea Views | High ROI"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2100000, "area_sqft": 850, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Prime Location | Burj Al Arab View | Higher Floor"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2200000, "area_sqft": 838, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Handover 2026 | Genuine Resale | Prime Location"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2500000, "area_sqft": 838, "bedrooms": "1", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Safa One | 1 bed | Sea View | Mid floor"},
    
    # 2 Bedroom properties
    {"project": "Safa One", "property_type": "Apartment", "price": 2393000, "area_sqft": 1231, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Best Deal | Corner Unit | Park, Sea and Burj Views"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2393000, "area_sqft": 1231, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Exclusive Offer | High ROI | Investor Deal"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2480998, "area_sqft": 1231, "bedrooms": "2", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Full Sea and Burj Al Arab View | Luxury Living"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2566000, "area_sqft": 1226, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Wasl Park View | High Floor | Branded"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2600000, "area_sqft": 1222, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Exclusive Resale | 2BR in Al Safa One | Investment"},
    {"project": "Safa One", "property_type": "Apartment", "price": 2900000, "area_sqft": 1231, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Investor Deal I Mid Floor I Modern Living"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3050000, "area_sqft": 1229, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Spacious Living I Good Location I Investor Deal"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3050000, "area_sqft": 1223, "bedrooms": "2", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Stunning Views | 2BR-Luxury Layout | Investor Deal"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3100000, "area_sqft": 1221, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Investor Deal I Exclusive Luxury 2 BHK"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3100000, "area_sqft": 1231, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Luxurious Living I Good Location I Investor Deal"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3400000, "area_sqft": 1223, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Stunning View IHigh Floor |Resale w/ Payment Plan"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3528000, "area_sqft": 1616, "bedrooms": "2", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Below Original Price | Park View | Safa One"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3725000, "area_sqft": 1586, "bedrooms": "2", "bathrooms": "4", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "10% Below Original Price | Best Views |High Floor"},
    {"project": "Safa One", "property_type": "Apartment", "price": 3900000, "area_sqft": 1221, "bedrooms": "2", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "2-BR | High Floor | Full Sea View Ultra Luxurious"},
    {"project": "Safa One", "property_type": "Apartment", "price": 4210000, "area_sqft": 2099, "bedrooms": "2", "bathrooms": "2", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Prime Location| Sea Views | High ROI"},
    {"project": "Safa One", "property_type": "Apartment", "price": 5000000, "area_sqft": 1943, "bedrooms": "2", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Spacious Living I Exclusive 2 BHK I Investor Deal"},
    
    # 3 Bedroom properties
    {"project": "Safa One", "property_type": "Apartment", "price": 4265508, "area_sqft": 2098, "bedrooms": "3", "bathrooms": "4", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Amazing View | High Floor | Selling Below Market"},
    {"project": "Safa One", "property_type": "Apartment", "price": 5037944, "area_sqft": 2630, "bedrooms": "3", "bathrooms": "3", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Panoramic Sea View | Luxurious | Prime Location"},
    {"project": "Safa One", "property_type": "Apartment", "price": 5800000, "area_sqft": 2147, "bedrooms": "3", "bathrooms": "4", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Luxury 3 BHK I Best in Price I Investor Deal"},
    
    # 4 Bedroom properties
    {"project": "Safa One", "property_type": "Apartment", "price": 7923000, "area_sqft": 2870, "bedrooms": "4", "bathrooms": "4", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Rare 4 Bed Duplex Townhouse | Full Safa Park View"},
    {"project": "Safa One", "property_type": "Apartment", "price": 30000000, "area_sqft": 6357, "bedrooms": "4", "bathrooms": "6", "location": "Al Safa 1, Dubai", "developer": "Damac Properties", "description": "Full Floor Penthouse | Panoramic View | High Floor"}
]

# Project information
PROJECT_INFO = {
    "Safa One": {
        "location": "Al Safa 1, Dubai",
        "developer": "Damac Properties",
        "delivery_date": "Q2 2026",
        "sales_started": "September 2022",
        "construction_progress": "5.86%",
        "payment_plan": "20/40/40",
        "description": "Safa One by de GRISOGONO is an ultra-luxury residential project featuring one of the highest hanging gardens in the world. Located in the prestigious Al Safa area along Sheikh Zayed Road, it offers stunning views of Burj Al Arab, Palm Jumeirah, and Dubai's iconic skyline.",
        "features": ["Hanging gardens", "Infinity pool", "Luxury spa", "Private beach access", "24/7 concierge", "Smart home technology", "Branded interiors by de GRISOGONO"],
        "image_url": "https://www.propertytrader.ae/assets/blogs/September2022/YVkNZeD7m9FxozmkV1T8.jpg"
    },
    "Safa Two": {
        "location": "Business Bay, Dubai",
        "developer": "Damac Properties",
        "delivery_date": "Q2 2027",
        "sales_started": "March 2023",
        "construction_progress": "3.25%",
        "payment_plan": "20/55/25",
        "description": "Safa Two is a luxury residential development in Business Bay featuring de GRISOGONO interiors. The twin-tower project offers premium units with breathtaking views of Dubai Canal, Burj Khalifa, and the city skyline.",
        "features": ["Luxury branded residences", "Premium views", "Infinity pools", "Spa and wellness center", "Fitness facilities", "Kids play area", "De GRISOGONO interiors"],
        "image_url": "https://www.damacproperties.com/en/wp-content/uploads/2023/03/safa-two-hero-md.jpg"
    }
}

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
    bedroom_order = {'studio': 0, '1': 1, '2': 2, '3': 3, '4': 4}
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

def generate_visualizations(analysis_results, project_name):
    """Generate Plotly visualizations from analysis results"""
    if not analysis_results or 'dataframe' not in analysis_results:
        return {}
        
    df = analysis_results['dataframe']
    figures = {}
    
    # Use a sophisticated color palette
    colors = {
        'primary': '#0d3b66',
        'secondary': '#3a86ff',
        'accent': '#ff006e',
        'light': '#f0f7ff',
        'dark': '#1f2937',
        'studio': '#4361ee',
        '1': '#3a86ff',
        '2': '#00b4d8',
        '3': '#0077b6',
        '4': '#023e8a'
    }
    
    # Price distribution by bedroom type
    try:
        bedroom_order = ['studio', '1', '2', '3', '4']
        present_bedroom_types = [b for b in bedroom_order if b in df['bedrooms'].unique()]
        
        fig_price = px.box(
            df, 
            x='bedrooms', 
            y='price', 
            color='bedrooms',
            category_orders={'bedrooms': present_bedroom_types},
            title=f'Price Distribution by Bedroom Type - {project_name}',
            labels={'price': 'Price (AED)', 'bedrooms': 'Bedrooms'},
            color_discrete_map={b: colors.get(b, colors['primary']) for b in present_bedroom_types}
        )
        
        # Format axes and layout
        fig_price.update_layout(
            font_family="'Segoe UI', Arial, sans-serif",
            title_font_size=22,
            title_font_color=colors['primary'],
            legend_title_font_color=colors['primary'],
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            ),
            boxmode="group",
            boxgap=0.3
        )
        
        # Format y-axis to show in millions
        fig_price.update_yaxes(
            tickformat=',', 
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        fig_price.update_xaxes(
            title_font=dict(size=14, color=colors['dark']),
            tickfont=dict(size=12)
        )
        
        figures['price_by_bedroom'] = fig_price
    except Exception as e:
        st.error(f"Error generating price by bedroom chart: {e}")
    
    # Area distribution by bedroom type
    try:
        fig_area = px.box(
            df, 
            x='bedrooms', 
            y='area_sqft', 
            color='bedrooms',
            category_orders={'bedrooms': present_bedroom_types},
            title=f'Area Distribution by Bedroom Type - {project_name}',
            labels={'area_sqft': 'Area (sq.ft)', 'bedrooms': 'Bedrooms'},
            color_discrete_map={b: colors.get(b, colors['primary']) for b in present_bedroom_types}
        )
        
        # Format axes and layout
        fig_area.update_layout(
            font_family="'Segoe UI', Arial, sans-serif",
            title_font_size=22,
            title_font_color=colors['primary'],
            legend_title_font_color=colors['primary'],
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            ),
            boxmode="group",
            boxgap=0.3
        )
        
        fig_area.update_yaxes(
            tickformat=',', 
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        fig_area.update_xaxes(
            title_font=dict(size=14, color=colors['dark']),
            tickfont=dict(size=12)
        )
        
        figures['area_by_bedroom'] = fig_area
    except Exception as e:
        st.error(f"Error generating area by bedroom chart: {e}")
    
    # Price per sq.ft by bedroom type
    try:
        fig_ppsf = px.box(
            df, 
            x='bedrooms', 
            y='price_per_sqft', 
            color='bedrooms',
            category_orders={'bedrooms': present_bedroom_types},
            title=f'Price per Sq.Ft by Bedroom Type - {project_name}',
            labels={'price_per_sqft': 'Price per Sq.Ft (AED)', 'bedrooms': 'Bedrooms'},
            color_discrete_map={b: colors.get(b, colors['primary']) for b in present_bedroom_types}
        )
        
        # Format axes and layout
        fig_ppsf.update_layout(
            font_family="'Segoe UI', Arial, sans-serif",
            title_font_size=22,
            title_font_color=colors['primary'],
            legend_title_font_color=colors['primary'],
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            ),
            boxmode="group",
            boxgap=0.3
        )
        
        fig_ppsf.update_yaxes(
            tickformat=',', 
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        fig_ppsf.update_xaxes(
            title_font=dict(size=14, color=colors['dark']),
            tickfont=dict(size=12)
        )
        
        figures['ppsf_by_bedroom'] = fig_ppsf
    except Exception as e:
        st.error(f"Error generating price per sq.ft by bedroom chart: {e}")
    
    # Distribution of price per sq.ft overall
    try:
        fig_ppsf_dist = px.histogram(
            df, 
            x='price_per_sqft', 
            nbins=20,
            title=f'Distribution of Price per Sq.Ft - {project_name}',
            labels={'price_per_sqft': 'Price per Sq.Ft (AED)', 'count': 'Number of Properties'},
            opacity=0.8,
            color_discrete_sequence=[colors['secondary']]
        )
        
        # Add a KDE curve
        fig_ppsf_dist.update_traces(histnorm='probability density')
        
        # Add a vertical line for the mean
        mean_ppsf = df['price_per_sqft'].mean()
        fig_ppsf_dist.add_vline(
            x=mean_ppsf, 
            line_dash="dash", 
            line_color=colors['accent'],
            annotation_text=f"Mean: {mean_ppsf:,.0f} AED",
            annotation_position="top right",
            annotation_font_color=colors['accent'],
            annotation_font_size=14
        )
        
        # Format axes and layout
        fig_ppsf_dist.update_layout(
            font_family="'Segoe UI', Arial, sans-serif",
            title_font_size=22,
            title_font_color=colors['primary'],
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        fig_ppsf_dist.update_xaxes(
            tickformat=',', 
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        fig_ppsf_dist.update_yaxes(
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        figures['ppsf_distribution'] = fig_ppsf_dist
    except Exception as e:
        st.error(f"Error generating price per sq.ft distribution chart: {e}")
    
    # Scatter plot of price vs. area
    try:
        fig_scatter = px.scatter(
            df, 
            x='area_sqft', 
            y='price', 
            color='bedrooms',
            category_orders={'bedrooms': present_bedroom_types},
            title=f'Price vs. Area - {project_name}',
            labels={'price': 'Price (AED)', 'area_sqft': 'Area (sq.ft)', 'bedrooms': 'Bedrooms'},
            color_discrete_map={b: colors.get(b, colors['primary']) for b in present_bedroom_types},
            trendline='ols',
            opacity=0.8,
            size_max=15,
            template='plotly_white'
        )
        
        # Format axes and layout
        fig_scatter.update_layout(
            font_family="'Segoe UI', Arial, sans-serif",
            title_font_size=22,
            title_font_color=colors['primary'],
            legend_title_font_color=colors['primary'],
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            )
        )
        
        fig_scatter.update_yaxes(
            tickformat=',', 
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        fig_scatter.update_xaxes(
            tickformat=',', 
            title_font=dict(size=14, color=colors['dark']),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        figures['price_vs_area'] = fig_scatter
    except Exception as e:
        st.error(f"Error generating price vs. area chart: {e}")
    
    return figures

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

def display_project_info(project, project_data):
    """Display project information in a stylish card"""
    st.markdown(f"""
    <div class="content-container">
        <h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">
            {project} Overview
        </h2>
        
        <div class="row" style="display: flex; flex-wrap: wrap; margin: 0 -10px;">
            <div class="column" style="flex: 40%; padding: 10px; box-sizing: border-box;">
                <img src="{project_data['image_url']}" alt="{project} Project" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
            </div>
            
            <div class="column" style="flex: 60%; padding: 10px; box-sizing: border-box;">
                <div style="background-color: #f0f7ff; border-radius: 12px; padding: 20px; height: 100%;">
                    <h3 style="color: #0d3b66; margin-bottom: 15px;">Project Details</h3>
                    
                    <div style="display: flex; margin-bottom: 10px;">
                        <div style="flex: 50%;">
                            <p><span class="highlight">Location:</span> {project_data['location']}</p>
                            <p><span class="highlight">Developer:</span> {project_data['developer']}</p>
                            <p><span class="highlight">Expected Delivery:</span> {project_data['delivery_date']}</p>
                        </div>
                        <div style="flex: 50%;">
                            <p><span class="highlight">Construction Progress:</span> {project_data['construction_progress']}</p>
                            <p><span class="highlight">Payment Plan:</span> {project_data['payment_plan']}</p>
                            <p><span class="highlight">Sales Started:</span> {project_data['sales_started']}</p>
                        </div>
                    </div>
                    
                    <div style="margin-top: 20px;">
                        <p style="text-align: justify;">{project_data['description']}</p>
                    </div>
                    
                    <h3 style="color: #0d3b66; margin-top: 20px; margin-bottom: 10px;">Key Features</h3>
                    <ul class="feature-list">
                        {"".join([f"<li>{feature}</li>" for feature in project_data['features']])}
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_project_analysis(project_name, property_data):
    """Display analysis for a specific project"""
    # Analyze data
    analysis_results = analyze_data(property_data)
    
    # Display overall statistics
    stats = analysis_results['stats_overall']
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">Key Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_listings']}</div>
            <div class="metric-label">Total Listings</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_currency(stats['avg_price'])}</div>
            <div class="metric-label">Average Price</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_area(stats['avg_area'])}</div>
            <div class="metric-label">Average Area</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">AED {stats['avg_price_per_sqft']:,.0f}</div>
            <div class="metric-label">Average Price/sq.ft</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics by bedroom type
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">Unit Types Analysis</h2>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.table(bedroom_stats)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create simplified unit type summary box
    st.markdown('<h3 style="color: #0d3b66; margin-top: 30px; margin-bottom: 15px;">Simplified Unit Types</h3>', unsafe_allow_html=True)
    
    # Create a simplified dataframe for the unit types
    simplified_df = pd.DataFrame({
        'Unit Type': [],
        'Size Range (sq.ft)': [],
        'Price Range (AED)': [],
        'Average Price/sq.ft': [],
        'Available Units': []
    })
    
    # Add row for each bedroom type if it exists in the data
    for bed_type in ['studio', '1', '2', '3', '4']:
        if bed_type in analysis_results['bedroom_stats']['bedrooms'].values:
            bed_data = analysis_results['bedroom_stats'][analysis_results['bedroom_stats']['bedrooms'] == bed_type]
            
            # Format the bedroom display name
            if bed_type == 'studio':
                display_name = 'Studio'
            else:
                display_name = f"{bed_type} Bedroom"
                
            # Create a new row
            new_row = pd.DataFrame({
                'Unit Type': [display_name],
                'Size Range (sq.ft)': [f"{bed_data['min_area'].values[0]:.0f} - {bed_data['max_area'].values[0]:.0f}"],
                'Price Range (AED)': [f"AED {bed_data['min_price'].values[0]/1000000:.2f}M - {bed_data['max_price'].values[0]/1000000:.2f}M"],
                'Average Price/sq.ft': [f"AED {bed_data['avg_price_per_sqft'].values[0]:.0f}"],
                'Available Units': [f"{bed_data['count'].values[0]:.0f}"]
            })
            
            # Append to simplified dataframe
            simplified_df = pd.concat([simplified_df, new_row], ignore_index=True)
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.table(simplified_df)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate and display visualizations
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">Data Visualizations</h2>', unsafe_allow_html=True)
    
    figures = generate_visualizations(analysis_results, project_name)
    
    # Display visualizations in tabs
    viz_tabs = st.tabs([
        "🏢 Price Analysis", 
        "📐 Area Analysis", 
        "💰 Price per Sq.Ft", 
        "📊 Price vs Area"
    ])
    
    with viz_tabs[0]:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if 'price_by_bedroom' in figures:
            st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
            st.plotly_chart(figures['price_by_bedroom'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_tabs[1]:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if 'area_by_bedroom' in figures:
            st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
            st.plotly_chart(figures['area_by_bedroom'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_tabs[2]:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if 'ppsf_by_bedroom' in figures:
            st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
            st.plotly_chart(figures['ppsf_by_bedroom'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if 'ppsf_distribution' in figures:
            st.markdown('<div class="plotly-chart" style="margin-top: 20px;">', unsafe_allow_html=True)
            st.plotly_chart(figures['ppsf_distribution'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_tabs[3]:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if 'price_vs_area' in figures:
            st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
            st.plotly_chart(figures['price_vs_area'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Property listings
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">Available Properties</h2>', unsafe_allow_html=True)
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        bedroom_filter = st.selectbox(f"Filter by Bedroom Type", 
                                     ["All Bedrooms"] + ["Studio" if b == "studio" else f"{b} Bedroom" for b in sorted(analysis_results['dataframe']['bedrooms'].unique(), key=lambda x: 0 if x == 'studio' else int(x))],
                                     key=f"{project_name}_bedroom_filter")
    with col2:
        price_sort = st.selectbox(f"Sort by Price", 
                                 ["Low to High", "High to Low"],
                                 key=f"{project_name}_price_sort")
    
    # Apply filters and sorting
    filtered_df = analysis_results['dataframe']
    if bedroom_filter != "All Bedrooms":
        bedroom_value = "studio" if bedroom_filter == "Studio" else bedroom_filter.split()[0]
        filtered_df = filtered_df[filtered_df['bedrooms'] == bedroom_value]
    
    if price_sort == "Low to High":
        filtered_df = filtered_df.sort_values('price')
    else:
        filtered_df = filtered_df.sort_values('price', ascending=False)
    
    # Format DataFrame for display
    display_df = filtered_df.copy()
    
    # Create badges for display
    def format_bedrooms(value):
        if value == 'studio':
            return '<span class="badge badge-blue">Studio</span>'
        return f'<span class="badge badge-blue">{value} BR</span>'
    
    def format_bathrooms(value):
        return f'<span class="badge badge-green">{value} Bath</span>'
    
    display_df['bedrooms'] = display_df['bedrooms'].apply(format_bedrooms)
    display_df['bathrooms'] = display_df['bathrooms'].apply(format_bathrooms)
    display_df['price'] = display_df['price'].apply(format_currency)
    display_df['area_sqft'] = display_df['area_sqft'].apply(format_area)
    display_df['price_per_sqft'] = display_df['price_per_sqft'].apply(lambda x: f"AED {x:,.0f}")
    
    # Prepare for display
    display_df = display_df[['bedrooms', 'bathrooms', 'price', 'area_sqft', 'price_per_sqft', 'description']]
    display_df.columns = ['Bedrooms', 'Bathrooms', 'Price', 'Area', 'Price/sq.ft', 'Description']
    
    # Display as HTML to allow badges
    st.markdown(f"""
    <div class="dataframe-container">
        <table class="dataframe">
            <thead>
                <tr>
                    <th>Bedrooms</th>
                    <th>Bathrooms</th>
                    <th>Price</th>
                    <th>Area</th>
                    <th>Price/sq.ft</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {"".join([f"""
                <tr>
                    <td>{row['Bedrooms']}</td>
                    <td>{row['Bathrooms']}</td>
                    <td>{row['Price']}</td>
                    <td>{row['Area']}</td>
                    <td>{row['Price/sq.ft']}</td>
                    <td>{row['Description']}</td>
                </tr>
                """ for _, row in display_df.iterrows()])}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Total listings shown
    st.markdown(f"<p style='text-align: right; color: #64748b; font-size: 13px; margin-top: 5px;'>Showing {len(display_df)} of {stats['total_listings']} total listings</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_comparison(safa_one_analysis, safa_two_analysis):
    """Display comparison between Safa One and Safa Two"""
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">Project Comparison</h2>', unsafe_allow_html=True)
    
    # Price comparison
    st.markdown("<h3 style='color: #0d3b66; margin-bottom: 15px;'>Average Metrics Comparison</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0d3b66; margin-bottom: 15px; text-align: center; border-bottom: 1px solid #e0e7ff; padding-bottom: 10px;">Safa One</h3>
        """, unsafe_allow_html=True)
        
        safa_one_stats = safa_one_analysis['stats_overall']
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Average Price:</span>
                <span style="font-weight: 700; color: #0d3b66;">{format_currency(safa_one_stats['avg_price'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Average Area:</span>
                <span style="font-weight: 700; color: #0d3b66;">{format_area(safa_one_stats['avg_area'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Average Price/sq.ft:</span>
                <span style="font-weight: 700; color: #0d3b66;">AED {safa_one_stats['avg_price_per_sqft']:,.0f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Total Listings:</span>
                <span style="font-weight: 700; color: #0d3b66;">{safa_one_stats['total_listings']}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 600; color: #64748b;">Price Range:</span>
                <span style="font-weight: 700; color: #0d3b66;">{format_currency(safa_one_stats['min_price'])} - {format_currency(safa_one_stats['max_price'])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0d3b66; margin-bottom: 15px; text-align: center; border-bottom: 1px solid #e0e7ff; padding-bottom: 10px;">Safa Two</h3>
        """, unsafe_allow_html=True)
        
        safa_two_stats = safa_two_analysis['stats_overall']
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Average Price:</span>
                <span style="font-weight: 700; color: #0d3b66;">{format_currency(safa_two_stats['avg_price'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Average Area:</span>
                <span style="font-weight: 700; color: #0d3b66;">{format_area(safa_two_stats['avg_area'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Average Price/sq.ft:</span>
                <span style="font-weight: 700; color: #0d3b66;">AED {safa_two_stats['avg_price_per_sqft']:,.0f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #64748b;">Total Listings:</span>
                <span style="font-weight: 700; color: #0d3b66;">{safa_two_stats['total_listings']}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 600; color: #64748b;">Price Range:</span>
                <span style="font-weight: 700; color: #0d3b66;">{format_currency(safa_two_stats['min_price'])} - {format_currency(safa_two_stats['max_price'])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Compare price per sqft by bedroom type
    st.markdown('<h3 style="color: #0d3b66; margin-top: 30px; margin-bottom: 15px;">Price per Sq.Ft Comparison by Bedroom Type</h3>', unsafe_allow_html=True)
    
    # Create comparison dataframe
    comparison_data = []
    
    # Process Safa One data
    for _, row in safa_one_analysis['bedroom_stats'].iterrows():
        bedroom_type = row['bedrooms']
        comparison_data.append({
            'Project': 'Safa One',
            'Bedroom Type': 'Studio' if bedroom_type == 'studio' else f"{bedroom_type} Bedroom",
            'Avg Price/sq.ft': row['avg_price_per_sqft'],
            'Min Price/sq.ft': row['min_price_per_sqft'],
            'Max Price/sq.ft': row['max_price_per_sqft']
        })
    
    # Process Safa Two data
    for _, row in safa_two_analysis['bedroom_stats'].iterrows():
        bedroom_type = row['bedrooms']
        comparison_data.append({
            'Project': 'Safa Two',
            'Bedroom Type': 'Studio' if bedroom_type == 'studio' else f"{bedroom_type} Bedroom",
            'Avg Price/sq.ft': row['avg_price_per_sqft'],
            'Min Price/sq.ft': row['min_price_per_sqft'],
            'Max Price/sq.ft': row['max_price_per_sqft']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Create comparison chart with improved styling
    fig = px.bar(
        comparison_df, 
        x='Bedroom Type', 
        y='Avg Price/sq.ft', 
        color='Project',
        barmode='group',
        title='Average Price per Sq.Ft Comparison',
        labels={'Avg Price/sq.ft': 'Average Price per Sq.Ft (AED)'},
        color_discrete_map={'Safa One': '#0d3b66', 'Safa Two': '#3a86ff'},
        template='plotly_white'
    )
    
    # Format axes and layout
    fig.update_layout(
        font_family="'Segoe UI', Arial, sans-serif",
        title_font_size=22,
        title_font_color='#0d3b66',
        legend_title_font_color='#0d3b66',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        )
    )
    
    fig.update_yaxes(
        tickformat=',', 
        title_font=dict(size=14, color='#1f2937'),
        gridcolor='#f8fafc',
        tickfont=dict(size=12)
    )
    
    fig.update_xaxes(
        title_font=dict(size=14, color='#1f2937'),
        tickfont=dict(size=12)
    )
    
    st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Investment comparison
    st.markdown('<h3 style="color: #0d3b66; margin-top: 30px; margin-bottom: 15px;">Investment Comparison</h3>', unsafe_allow_html=True)
    
    # Create comparison table
    investment_data = {
        'Metric': [
            'Expected Delivery', 
            'Payment Plan',
            'Construction Progress',
            'Avg. 1BR Price',
            'Avg. 2BR Price',
            'Avg. 3BR Price',
            'Price per Sq.Ft Range',
            'Location'
        ],
        'Safa One': [
            PROJECT_INFO['Safa One']['delivery_date'],
            PROJECT_INFO['Safa One']['payment_plan'],
            PROJECT_INFO['Safa One']['construction_progress'],
            format_currency(safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '1', 'avg_price'].values[0]),
            format_currency(safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '2', 'avg_price'].values[0]),
            format_currency(safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '3', 'avg_price'].values[0]),
            f"AED {safa_one_stats['min_price_per_sqft']:,.0f} - {safa_one_stats['max_price_per_sqft']:,.0f}",
            PROJECT_INFO['Safa One']['location']
        ],
        'Safa Two': [
            PROJECT_INFO['Safa Two']['delivery_date'],
            PROJECT_INFO['Safa Two']['payment_plan'],
            PROJECT_INFO['Safa Two']['construction_progress'],
            format_currency(safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '1', 'avg_price'].values[0]),
            format_currency(safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '2', 'avg_price'].values[0]),
            format_currency(safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '3', 'avg_price'].values[0]),
            f"AED {safa_two_stats['min_price_per_sqft']:,.0f} - {safa_two_stats['max_price_per_sqft']:,.0f}",
            PROJECT_INFO['Safa Two']['location']
        ]
    }
    
    investment_df = pd.DataFrame(investment_data)
    
    st.markdown('<div class="data-table compare-table">', unsafe_allow_html=True)
    st.table(investment_df.set_index('Metric'))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Investment insights card
    st.markdown("""
    <div class="info-box" style="margin-top: 30px;">
        <h3 style="color: #0d3b66; margin-bottom: 15px;">Investment Insights</h3>
        <p style="margin-bottom: 15px;">When comparing Safa One and Safa Two as investment opportunities, consider these key factors:</p>
        <div style="display: flex; flex-wrap: wrap; margin: 0 -10px;">
            <div style="flex: 50%; padding: 0 10px; box-sizing: border-box;">
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="color: #0d3b66; margin-bottom: 10px;">Delivery Timeline</h4>
                    <p>Safa One is expected to be delivered in Q2 2026, approximately one year earlier than Safa Two (Q2 2027).</p>
                </div>
                
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="color: #0d3b66; margin-bottom: 10px;">Price Points</h4>
                    <p>Safa Two offers more affordable entry points with studios starting from AED 949K, while Safa One commands premium pricing but may offer stronger appreciation potential.</p>
                </div>
            </div>
            
            <div style="flex: 50%; padding: 0 10px; box-sizing: border-box;">
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="color: #0d3b66; margin-bottom: 10px;">Location Value</h4>
                    <p>Safa One in Al Safa 1 offers proximity to Sheikh Zayed Road and Dubai's established luxury areas, while Safa Two in Business Bay provides central location with Dubai Canal views.</p>
                </div>
                
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="color: #0d3b66; margin-bottom: 10px;">Unit Sizes</h4>
                    <p>On average, Safa One units are more spacious, particularly in the 2-3 bedroom categories, potentially appealing to end-users and long-term residents.</p>
                </div>
            </div>
        </div>
        
        <div style="background-color: white; border-radius: 8px; padding: 15px; margin-top: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="color: #0d3b66; margin-bottom: 10px;">Luxury Appeal</h4>
            <p>Both developments feature de GRISOGONO interiors, but Safa One's hanging gardens concept provides a unique selling proposition in the luxury segment.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main function to run the Streamlit app
def main():
    # App header with logo
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
        <img src="https://www.damacproperties.com/images/shared/logo-white-bg.png" alt="Damac Logo" style="height: 60px; margin-right: 15px;">
    </div>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<div class="main-header">Damac Safa Properties Analysis</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="info-box">
        <h3 style="color: #0d3b66; margin-bottom: 10px;">About This Dashboard</h3>
        <p>This dashboard provides a comprehensive analysis of Damac's premium Safa One and Safa Two projects in Dubai. 
        Explore property listings, pricing trends, and investment comparisons to make informed decisions about these luxury 
        residential developments in two of Dubai's most prestigious locations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for navigation
    tab_overview, tab_safa_one, tab_safa_two, tab_comparison = st.tabs([
        "📊 Overview", "🏢 Safa One", "🏙️ Safa Two", "🔄 Comparison"
    ])
    
    # Analyze data
    safa_one_analysis = analyze_data(SAFA_ONE_DATA)
    safa_two_analysis = analyze_data(SAFA_TWO_DATA)
    
    # Overview tab
    with tab_overview:
        st.markdown("""
        <div class="content-container">
            <h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px; text-align: center;">
                Damac Safa Projects Overview
            </h2>
            
            <!-- Projects comparison grid -->
            <div style="display: flex; flex-wrap: wrap; margin: 0 -15px;">
                <!-- Safa One Card -->
                <div style="flex: 50%; padding: 0 15px; box-sizing: border-box;">
                    <div class="project-card" style="position: relative;">
                        <span class="badge badge-orange" style="position: absolute; top: 15px; right: 15px; font-size: 14px; padding: 5px 10px;">
                            Luxury Segment
                        </span>
                        <h2 style="color: #0d3b66; margin-bottom: 15px;">Safa One</h2>
                        <img src="https://www.propertytrader.ae/assets/blogs/September2022/YVkNZeD7m9FxozmkV1T8.jpg" alt="Safa One" class="project-image">
                        <div style="display: flex; flex-wrap: wrap; margin-bottom: 15px;">
                            <div class="badge badge-blue" style="margin-right: 8px; margin-bottom: 8px;">Al Safa 1</div>
                            <div class="badge badge-green" style="margin-right: 8px; margin-bottom: 8px;">Q2 2026</div>
                            <div class="badge badge-orange" style="margin-bottom: 8px;">AED 1.6M - 30M</div>
                        </div>
                        <p style="margin-bottom: 15px; text-align: justify;">Ultra-luxury development featuring one of the world's highest hanging gardens, located along Sheikh Zayed Road with stunning views of Dubai's iconic landmarks.</p>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <div style="text-align: center; flex: 33%;">
                                <p style="font-size: 20px; font-weight: 700; color: #0d3b66; margin: 0;">"""+f"{safa_one_analysis['stats_overall']['total_listings']}"+"""</p>
                                <p style="font-size: 12px; color: #64748b; margin: 0;">Available Units</p>
                            </div>
                            <div style="text-align: center; flex: 33%;">
                                <p style="font-size: 20px; font-weight: 700; color: #0d3b66; margin: 0;">"""+f"AED {safa_one_analysis['stats_overall']['avg_price_per_sqft']:,.0f}"+"""</p>
                                <p style="font-size: 12px; color: #64748b; margin: 0;">Avg. Price/sq.ft</p>
                            </div>
                            <div style="text-align: center; flex: 33%;">
                                <p style="font-size: 20px; font-weight: 700; color: #0d3b66; margin: 0;">20/40/40</p>
                                <p style="font-size: 12px; color: #64748b; margin: 0;">Payment Plan</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Safa Two Card -->
                <div style="flex: 50%; padding: 0 15px; box-sizing: border-box;">
                    <div class="project-card" style="position: relative;">
                        <span class="badge badge-blue" style="position: absolute; top: 15px; right: 15px; font-size: 14px; padding: 5px 10px;">
                            Premium Segment
                        </span>
                        <h2 style="color: #0d3b66; margin-bottom: 15px;">Safa Two</h2>
                        <img src="https://www.damacproperties.com/en/wp-content/uploads/2023/03/safa-two-hero-md.jpg" alt="Safa Two" class="project-image">
                        <div style="display: flex; flex-wrap: wrap; margin-bottom: 15px;">
                            <div class="badge badge-blue" style="margin-right: 8px; margin-bottom: 8px;">Business Bay</div>
                            <div class="badge badge-green" style="margin-right: 8px; margin-bottom: 8px;">Q2 2027</div>
                            <div class="badge badge-orange" style="margin-bottom: 8px;">AED 949K - 5M</div>
                        </div>
                        <p style="margin-bottom: 15px; text-align: justify;">Luxury residential development in Business Bay featuring de GRISOGONO interiors, offering premium units with views of Dubai Canal and the city skyline.</p>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <div style="text-align: center; flex: 33%;">
                                <p style="font-size: 20px; font-weight: 700; color: #0d3b66; margin: 0;">"""+f"{safa_two_analysis['stats_overall']['total_listings']}"+"""</p>
                                <p style="font-size: 12px; color: #64748b; margin: 0;">Available Units</p>
                            </div>
                            <div style="text-align: center; flex: 33%;">
                                <p style="font-size: 20px; font-weight: 700; color: #0d3b66; margin: 0;">"""+f"AED {safa_two_analysis['stats_overall']['avg_price_per_sqft']:,.0f}"+"""</p>
                                <p style="font-size: 12px; color: #64748b; margin: 0;">Avg. Price/sq.ft</p>
                            </div>
                            <div style="text-align: center; flex: 33%;">
                                <p style="font-size: 20px; font-weight: 700; color: #0d3b66; margin: 0;">20/55/25</p>
                                <p style="font-size: 12px; color: #64748b; margin: 0;">Payment Plan</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key statistics comparison
        st.markdown("""
        <div class="content-container">
            <h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">
                Quick Comparison
            </h2>
            
            <div style="display: flex; flex-wrap: wrap; margin: 0 -10px;">
                <div style="flex: 33.33%; padding: 0 10px; box-sizing: border-box; margin-bottom: 20px;">
                    <div class="metric-card">
                        <h3 style="color: #0d3b66; text-align: center; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid #e0e7ff;">Average Price</h3>
                        <div style="display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; align-items: center;">
                                <span style="font-weight: 600; color: #0d3b66;">Safa One:</span>
                                <span style="font-size: 18px; font-weight: 700; color: #0d3b66;">"""+f"{format_currency(safa_one_analysis['stats_overall']['avg_price'])}"+"""</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 600; color: #3a86ff;">Safa Two:</span>
                                <span style="font-size: 18px; font-weight: 700; color: #3a86ff;">"""+f"{format_currency(safa_two_analysis['stats_overall']['avg_price'])}"+"""</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="flex: 33.33%; padding: 0 10px; box-sizing: border-box; margin-bottom: 20px;">
                    <div class="metric-card">
                        <h3 style="color: #0d3b66; text-align: center; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid #e0e7ff;">Average Area</h3>
                        <div style="display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; align-items: center;">
                                <span style="font-weight: 600; color: #0d3b66;">Safa One:</span>
                                <span style="font-size: 18px; font-weight: 700; color: #0d3b66;">"""+f"{format_area(safa_one_analysis['stats_overall']['avg_area'])}"+"""</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 600; color: #3a86ff;">Safa Two:</span>
                                <span style="font-size: 18px; font-weight: 700; color: #3a86ff;">"""+f"{format_area(safa_two_analysis['stats_overall']['avg_area'])}"+"""</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="flex: 33.33%; padding: 0 10px; box-sizing: border-box; margin-bottom: 20px;">
                    <div class="metric-card">
                        <h3 style="color: #0d3b66; text-align: center; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid #e0e7ff;">Avg Price/sq.ft</h3>
                        <div style="display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; align-items: center;">
                                <span style="font-weight: 600; color: #0d3b66;">Safa One:</span>
                                <span style="font-size: 18px; font-weight: 700; color: #0d3b66;">AED """+f"{safa_one_analysis['stats_overall']['avg_price_per_sqft']:,.0f}"+"""</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 600; color: #3a86ff;">Safa Two:</span>
                                <span style="font-size: 18px; font-weight: 700; color: #3a86ff;">AED """+f"{safa_two_analysis['stats_overall']['avg_price_per_sqft']:,.0f}"+"""</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; flex-wrap: wrap; margin: 0 -10px;">
                <div style="flex: 50%; padding: 0 10px; box-sizing: border-box; margin-bottom: 20px;">
                    <div class="metric-card">
                        <h3 style="color: #0d3b66; text-align: center; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid #e0e7ff;">Available Unit Types</h3>
                        <div style="display: flex; justify-content: space-between;">
                            <div style="text-align: center; flex: 50%;">
                                <h4 style="color: #0d3b66; margin-bottom: 10px;">Safa One</h4>
                                <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
                                    <span class="badge badge-blue">1 Bedroom</span>
                                    <span class="badge badge-blue">2 Bedroom</span>
                                    <span class="badge badge-blue">3 Bedroom</span>
                                    <span class="badge badge-blue">4 Bedroom</span>
                                </div>
                            </div>
                            <div style="text-align: center; flex: 50%;">
                                <h4 style="color: #3a86ff; margin-bottom: 10px;">Safa Two</h4>
                                <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
                                    <span class="badge badge-blue">Studio</span>
                                    <span class="badge badge-blue">1 Bedroom</span>
                                    <span class="badge badge-blue">2 Bedroom</span>
                                    <span class="badge badge-blue">3 Bedroom</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="flex: 50%; padding: 0 10px; box-sizing: border-box; margin-bottom: 20px;">
                    <div class="metric-card">
                        <h3 style="color: #0d3b66; text-align: center; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid #e0e7ff;">Project Timeline</h3>
                        <div style="display: flex; justify-content: space-between;">
                            <div style="text-align: center; flex: 50%;">
                                <h4 style="color: #0d3b66; margin-bottom: 10px;">Safa One</h4>
                                <p style="margin-bottom: 5px;"><span style="font-weight: 600; color: #64748b;">Sales Started:</span> Sep 2022</p>
                                <p style="margin-bottom: 5px;"><span style="font-weight: 600; color: #64748b;">Construction:</span> 5.86%</p>
                                <p><span style="font-weight: 600; color: #64748b;">Delivery:</span> Q2 2026</p>
                            </div>
                            <div style="text-align: center; flex: 50%;">
                                <h4 style="color: #3a86ff; margin-bottom: 10px;">Safa Two</h4>
                                <p style="margin-bottom: 5px;"><span style="font-weight: 600; color: #64748b;">Sales Started:</span> Mar 2023</p>
                                <p style="margin-bottom: 5px;"><span style="font-weight: 600; color: #64748b;">Construction:</span> 3.25%</p>
                                <p><span style="font-weight: 600; color: #64748b;">Delivery:</span> Q2 2027</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create price comparison chart
        price_comparison = {
            'Unit Type': ['Studio', '1 Bedroom', '2 Bedroom', '3 Bedroom'],
            'Safa One': [
                0,  # No studios in Safa One
                safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '1', 'avg_price'].values[0],
                safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '2', 'avg_price'].values[0],
                safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '3', 'avg_price'].values[0]
            ],
            'Safa Two': [
                safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == 'studio', 'avg_price'].values[0],
                safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '1', 'avg_price'].values[0],
                safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '2', 'avg_price'].values[0],
                safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '3', 'avg_price'].values[0]
            ]
        }
        
        price_df = pd.DataFrame(price_comparison)
        
        # Melt the dataframe for plotting
        price_df_melted = pd.melt(
            price_df, 
            id_vars=['Unit Type'], 
            value_vars=['Safa One', 'Safa Two'],
            var_name='Project', 
            value_name='Average Price'
        )
        
        # Create the chart
        fig = px.bar(
            price_df_melted,
            x='Unit Type',
            y='Average Price',
            color='Project',
            barmode='group',
            title='Average Price Comparison by Unit Type',
            color_discrete_map={'Safa One': '#0d3b66', 'Safa Two': '#3a86ff'},
            template='plotly_white'
        )
        
        # Format axes and layout
        fig.update_layout(
            font_family="'Segoe UI', Arial, sans-serif",
            title_font_size=22,
            title_font_color='#0d3b66',
            legend_title_font_color='#0d3b66',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            )
        )
        
        # Format y-axis to show in millions
        fig.update_yaxes(
            tickformat=',', 
            title='Average Price (AED)',
            title_font=dict(size=14, color='#1f2937'),
            gridcolor='#f8fafc',
            tickfont=dict(size=12)
        )
        
        fig.update_xaxes(
            title_font=dict(size=14, color='#1f2937'),
            tickfont=dict(size=12)
        )
        
        st.markdown("""
        <div class="content-container">
            <h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">
                Price Comparison by Unit Type
            </h2>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add interpretation
        st.markdown("""
            <div class="info-box" style="margin-top: 15px;">
                <p><strong>Key Insights:</strong></p>
                <ul>
                    <li>Safa One properties command a premium price across all unit types compared to Safa Two.</li>
                    <li>The price gap widens significantly for larger units, especially in the 3-bedroom category.</li>
                    <li>Safa Two offers studio units starting from AED 949K, providing a more accessible entry point.</li>
                    <li>For investors, Safa Two may offer better rental yields due to lower purchase prices, while Safa One may have stronger long-term appreciation potential.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Safa One tab
    with tab_safa_one:
        st.markdown('<div class="project-title">Safa One Analysis</div>', unsafe_allow_html=True)
        
        # Display project information
        display_project_info("Safa One", PROJECT_INFO["Safa One"])
        
        # Display analysis
        display_project_analysis("Safa One", SAFA_ONE_DATA)
    
    # Safa Two tab
    with tab_safa_two:
        st.markdown('<div class="project-title">Safa Two Analysis</div>', unsafe_allow_html=True)
        
        # Display project information
        display_project_info("Safa Two", PROJECT_INFO["Safa Two"])
        
        # Display analysis
        display_project_analysis("Safa Two", SAFA_TWO_DATA)
    
    # Comparison tab
    with tab_comparison:
        st.markdown('<div class="project-title">Safa One vs Safa Two</div>', unsafe_allow_html=True)
        
        # Display comparison
        display_comparison(safa_one_analysis, safa_two_analysis)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Damac Safa Properties Analysis Dashboard • Data last updated: March 2025</p>
        <p>This analysis is based on current property listings and is for informational purposes only.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Save to CSV
    safa_one_path = os.path.join(RESULTS_DIR, "safa_one_properties.csv")
    safa_two_path = os.path.join(RESULTS_DIR, "safa_two_properties.csv")
    
    safa_one_analysis['dataframe'].to_csv(safa_one_path, index=False)
    safa_two_analysis['dataframe'].to_csv(safa_two_path, index=False)
    
    # Add download section
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #0d3b66; margin-bottom: 20px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px;">Download Property Data</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="margin-bottom: 20px;">
        Download the complete property data for further analysis or reference. The CSV files contain all property details including prices, 
        areas, bedroom types, and descriptions.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download Safa One Data",
            data=open(safa_one_path, 'rb').read(),
            file_name="safa_one_properties.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="Download Safa Two Data",
            data=open(safa_two_path, 'rb').read(),
            file_name="safa_two_properties.csv",
            mime="text/csv"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
