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
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 36px !important;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 20px;
        text-align: center;
    }
    .sub-header {
        font-size: 24px;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .project-title {
        font-size: 28px;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #1E3A8A;
    }
    .metric-label {
        font-size: 14px;
        color: #4B5563;
    }
    .info-box {
        background-color: #EFF6FF;
        border-left: 5px solid #1E3A8A;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .data-table {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .project-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .project-image {
        border-radius: 10px;
        max-width: 100%;
        margin-bottom: 15px;
    }
    .compare-table th {
        background-color: #EFF6FF;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        color: #6B7280;
        font-size: 12px;
    }
    .highlight {
        font-weight: 600;
        color: #1E3A8A;
    }
    .tab-content {
        padding: 20px 0;
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
        "payment_plan": "20/40/40",
        "description": "Safa One by de GRISOGONO is an ultra-luxury residential project featuring one of the highest hanging gardens in the world. Located in the prestigious Al Safa area along Sheikh Zayed Road, it offers stunning views of Burj Al Arab, Palm Jumeirah, and Dubai's iconic skyline.",
        "features": ["Hanging gardens", "Infinity pool", "Luxury spa", "Private beach access", "24/7 concierge", "Smart home technology", "Branded interiors by de GRISOGONO"]
    },
    "Safa Two": {
        "location": "Business Bay, Dubai",
        "developer": "Damac Properties",
        "delivery_date": "Q2 2027",
        "sales_started": "March 2023",
        "payment_plan": "20/55/25",
        "description": "Safa Two is a luxury residential development in Business Bay featuring de GRISOGONO interiors. The twin-tower project offers premium units with breathtaking views of Dubai Canal, Burj Khalifa, and the city skyline.",
        "features": ["Luxury branded residences", "Premium views", "Infinity pools", "Spa and wellness center", "Fitness facilities", "Kids play area", "De GRISOGONO interiors"]
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
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown(f"""
        <div class="info-box">
            <h3 style="color: #1E3A8A; margin-bottom: 15px;">{project} at a Glance</h3>
            <p><span class="highlight">Location:</span> {project_data['location']}</p>
            <p><span class="highlight">Developer:</span> {project_data['developer']}</p>
            <p><span class="highlight">Expected Delivery:</span> {project_data['delivery_date']}</p>
            <p><span class="highlight">Payment Plan:</span> {project_data['payment_plan']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-box">
            <h3 style="color: #1E3A8A; margin-bottom: 15px;">About {project}</h3>
            <p>{project_data['description']}</p>
            <h4 style="color: #1E3A8A; margin-top: 15px; margin-bottom: 10px;">Key Features</h4>
            <ul style="margin-top: 0;">
                {"".join([f"<li>{feature}</li>" for feature in project_data['features']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

def display_project_analysis(project_name, property_data):
    """Display analysis for a specific project"""
    # Analyze data
    analysis_results = analyze_data(property_data)
    
    # Display overall statistics
    stats = analysis_results['stats_overall']
    
    st.markdown(f'<div class="sub-header">Overview</div>', unsafe_allow_html=True)
    
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
    
    # Statistics by bedroom type
    st.markdown(f'<div class="sub-header">Unit Types Summary</div>', unsafe_allow_html=True)
    
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
    st.markdown(f'<div class="sub-header">Simplified Unit Types</div>', unsafe_allow_html=True)
    
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
    
    
    # Property listings
    st.markdown(f'<div class="sub-header">Property Listings</div>', unsafe_allow_html=True)
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        bedroom_filter = st.selectbox(f"Filter {project_name} by Bedrooms", 
                                     ["All"] + list(analysis_results['dataframe']['bedrooms'].unique()),
                                     key=f"{project_name}_bedroom_filter")
    with col2:
        price_sort = st.selectbox(f"Sort {project_name} by Price", 
                                 ["Low to High", "High to Low"],
                                 key=f"{project_name}_price_sort")
    
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

def display_comparison(safa_one_analysis, safa_two_analysis):
    """Display comparison between Safa One and Safa Two"""
    st.markdown('<div class="sub-header">Project Comparison</div>', unsafe_allow_html=True)
    
    # Price comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E3A8A; margin-bottom: 10px;">Safa One Averages</h3>
        """, unsafe_allow_html=True)
        
        safa_one_stats = safa_one_analysis['stats_overall']
        st.markdown(f"""
            <p><span class="highlight">Average Price:</span> {format_currency(safa_one_stats['avg_price'])}</p>
            <p><span class="highlight">Average Area:</span> {format_area(safa_one_stats['avg_area'])}</p>
            <p><span class="highlight">Average Price/sq.ft:</span> AED {safa_one_stats['avg_price_per_sqft']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E3A8A; margin-bottom: 10px;">Safa Two Averages</h3>
        """, unsafe_allow_html=True)
        
        safa_two_stats = safa_two_analysis['stats_overall']
        st.markdown(f"""
            <p><span class="highlight">Average Price:</span> {format_currency(safa_two_stats['avg_price'])}</p>
            <p><span class="highlight">Average Area:</span> {format_area(safa_two_stats['avg_area'])}</p>
            <p><span class="highlight">Average Price/sq.ft:</span> AED {safa_two_stats['avg_price_per_sqft']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Compare price per sqft by bedroom type
    st.markdown('<h3 style="color: #1E3A8A; margin-top: 20px;">Price per Sq.Ft Comparison by Bedroom Type</h3>', unsafe_allow_html=True)
    
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
    
    # Create comparison chart
    fig = px.bar(
        comparison_df, 
        x='Bedroom Type', 
        y='Avg Price/sq.ft', 
        color='Project',
        barmode='group',
        title='Average Price per Sq.Ft Comparison',
        labels={'Avg Price/sq.ft': 'Average Price per Sq.Ft (AED)'},
        color_discrete_map={'Safa One': '#1E3A8A', 'Safa Two': '#3B82F6'}
    )
    
    # Format axes and layout
    fig.update_layout(
        font_family="Arial",
        title_font_size=20,
        title_font_color='#1E3A8A',
        legend_title_font_color='#1E3A8A',
        plot_bgcolor='#EFF6FF',
        paper_bgcolor='white',
        height=500
    )
    
    fig.update_yaxes(tickformat=',', title_font=dict(size=14, color='#1F2937'))
    fig.update_xaxes(title_font=dict(size=14, color='#1F2937'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Investment comparison
    st.markdown('<h3 style="color: #1E3A8A; margin-top: 20px;">Investment Comparison</h3>', unsafe_allow_html=True)
    
    # Create comparison table
    investment_data = {
        'Metric': [
            'Expected Delivery', 
            'Payment Plan',
            'Avg. 1BR Price',
            'Avg. 2BR Price',
            'Avg. 3BR Price',
            'Price per Sq.Ft Range',
            'Location'
        ],
        'Safa One': [
            PROJECT_INFO['Safa One']['delivery_date'],
            PROJECT_INFO['Safa One']['payment_plan'],
            format_currency(safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '1', 'avg_price'].values[0]),
            format_currency(safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '2', 'avg_price'].values[0]),
            format_currency(safa_one_analysis['bedroom_stats'].loc[safa_one_analysis['bedroom_stats']['bedrooms'] == '3', 'avg_price'].values[0]),
            f"AED {safa_one_stats['min_price_per_sqft']:,.0f} - {safa_one_stats['max_price_per_sqft']:,.0f}",
            PROJECT_INFO['Safa One']['location']
        ],
        'Safa Two': [
            PROJECT_INFO['Safa Two']['delivery_date'],
            PROJECT_INFO['Safa Two']['payment_plan'],
            format_currency(safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '1', 'avg_price'].values[0]),
            format_currency(safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '2', 'avg_price'].values[0]),
            format_currency(safa_two_analysis['bedroom_stats'].loc[safa_two_analysis['bedroom_stats']['bedrooms'] == '3', 'avg_price'].values[0]),
            f"AED {safa_two_stats['min_price_per_sqft']:,.0f} - {safa_two_stats['max_price_per_sqft']:,.0f}",
            PROJECT_INFO['Safa Two']['location']
        ]
    }
    
    investment_df = pd.DataFrame(investment_data)
    
    st.markdown('<div class="compare-table">', unsafe_allow_html=True)
    st.table(investment_df.set_index('Metric'))
    st.markdown('</div>', unsafe_allow_html=True)

# Main function to run the Streamlit app
def main():
    # Header
    st.markdown('<div class="main-header">Damac Safa Properties Analysis</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="info-box">
        This dashboard provides a comprehensive analysis of Damac's premium Safa One and Safa Two projects in Dubai. 
        Explore property listings, pricing trends, and investment comparisons to make informed decisions.
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for navigation
    tab_overview, tab_safa_one, tab_safa_two, tab_comparison = st.tabs([
        "Overview", "Safa One Analysis", "Safa Two Analysis", "Project Comparison"
    ])
    
    # Analyze data
    safa_one_analysis = analyze_data(SAFA_ONE_DATA)
    safa_two_analysis = analyze_data(SAFA_TWO_DATA)
    
    # Overview tab
    with tab_overview:
        st.markdown('<div class="project-title">Damac Safa Projects Overview</div>', unsafe_allow_html=True)
        
        # Project cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h2 style="color: #1E3A8A; margin-bottom: 15px;">Safa One</h2>
                <img src="s1s2/your_image.jpg" class="project-image">
                <p><span class="highlight">Location:</span> Al Safa 1, Dubai</p>
                <p><span class="highlight">Delivery:</span> Q2 2026</p>
                <p><span class="highlight">Price Range:</span> AED 1.6M - AED 30M</p>
                <p>Ultra-luxury development featuring one of the world's highest hanging gardens, located along Sheikh Zayed Road with stunning views of Dubai's iconic landmarks.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h2 style="color: #1E3A8A; margin-bottom: 15px;">Safa Two</h2>
                <img src="uploaded_images/your_image2.jpg" class="project-image">
                <p><span class="highlight">Location:</span> Business Bay, Dubai</p>
                <p><span class="highlight">Delivery:</span> Q2 2027</p>
                <p><span class="highlight">Price Range:</span> AED 949K - AED 5M</p>
                <p>Luxury residential development in Business Bay featuring de GRISOGONO interiors, offering premium units with views of Dubai Canal and the city skyline.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Key statistics comparison
        st.markdown('<div class="sub-header">Quick Comparison</div>', unsafe_allow_html=True)
        
        safa_one_stats = safa_one_analysis['stats_overall']
        safa_two_stats = safa_two_analysis['stats_overall']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #1E3A8A; text-align: center; margin-bottom: 15px;">Average Price</h3>
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <p style="font-weight: 600; color: #1E3A8A;">Safa One</p>
                        <p style="font-size: 20px;">{}</p>
                    </div>
                    <div>
                        <p style="font-weight: 600; color: #3B82F6;">Safa Two</p>
                        <p style="font-size: 20px;">{}</p>
                    </div>
                </div>
            </div>
            """.format(
                format_currency(safa_one_stats['avg_price']),
                format_currency(safa_two_stats['avg_price'])
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #1E3A8A; text-align: center; margin-bottom: 15px;">Average Area</h3>
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <p style="font-weight: 600; color: #1E3A8A;">Safa One</p>
                        <p style="font-size: 20px;">{}</p>
                    </div>
                    <div>
                        <p style="font-weight: 600; color: #3B82F6;">Safa Two</p>
                        <p style="font-size: 20px;">{}</p>
                    </div>
                </div>
            </div>
            """.format(
                format_area(safa_one_stats['avg_area']),
                format_area(safa_two_stats['avg_area'])
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #1E3A8A; text-align: center; margin-bottom: 15px;">Avg Price/sq.ft</h3>
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <p style="font-weight: 600; color: #1E3A8A;">Safa One</p>
                        <p style="font-size: 20px;">AED {:,.0f}</p>
                    </div>
                    <div>
                        <p style="font-weight: 600; color: #3B82F6;">Safa Two</p>
                        <p style="font-size: 20px;">AED {:,.0f}</p>
                    </div>
                </div>
            </div>
            """.format(
                safa_one_stats['avg_price_per_sqft'],
                safa_two_stats['avg_price_per_sqft']
            ), unsafe_allow_html=True)
    
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
        
        # Investment insights
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #1E3A8A; margin-bottom: 15px;">Investment Insights</h3>
            <p>When comparing Safa One and Safa Two as investment opportunities, consider these key factors:</p>
            <ul>
                <li><strong>Delivery Timeline:</strong> Safa One is expected to be delivered in Q2 2026, approximately one year earlier than Safa Two (Q2 2027).</li>
                <li><strong>Location Value:</strong> Safa One in Al Safa 1 offers proximity to Sheikh Zayed Road and Dubai's established luxury areas, while Safa Two in Business Bay provides central location with Dubai Canal views.</li>
                <li><strong>Price Points:</strong> Safa Two offers more affordable entry points with studios starting from AED 949K, while Safa One commands premium pricing but may offer stronger appreciation potential.</li>
                <li><strong>Unit Sizes:</strong> On average, Safa One units are more spacious, particularly in the 2-3 bedroom categories, potentially appealing to end-users and long-term residents.</li>
                <li><strong>Luxury Appeal:</strong> Both developments feature de GRISOGONO interiors, but Safa One's hanging gardens concept provides a unique selling proposition in the luxury segment.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    # Download links for CSVs
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

# Run the Streamlit app
if __name__ == "__main__":
    main()
