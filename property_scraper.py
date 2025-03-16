import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from datetime import datetime
import requests
from time import sleep

# Page configuration
st.set_page_config(
    page_title="Property Analyzer with AI",
    page_icon="🏢",
    layout="wide"
)

# Create a directory for results
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

class OpenAIPropertyAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.results_dir = RESULTS_DIR
        self.openai_api_url = "https://api.openai.com/v1/chat/completions"
        
    def get_property_data(self, property_name, max_properties=10):
        """Use OpenAI to extract property data for the specified property"""
        prompt = f"""
        I need detailed information about properties in {property_name} in Dubai.

        Please provide data for up to {max_properties} available properties with the following details for each:
        1. Project name (e.g., Damac Safa One, Damac Safa Two)
        2. Property type (e.g., Apartment, Villa, Penthouse)
        3. Price in AED (numerical value only)
        4. Area in square feet (numerical value only)
        5. Number of bedrooms (Studio, 1, 2, 3, etc.)
        6. Number of bathrooms (1, 2, 3, etc.)
        7. Location (e.g., Business Bay, Dubai)
        8. Developer name

        Format the response as a JSON array of objects. Each object should represent one property with the fields: project, property_type, price, area_sqft, bedrooms, bathrooms, location, developer.

        Return ONLY valid JSON, no other text.
        """
        
        try:
            # API call to OpenAI
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",  # or "gpt-3.5-turbo" for a less expensive option
                "messages": [
                    {"role": "system", "content": "You provide accurate property data in JSON format without additional text."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            
            response = requests.post(
                self.openai_api_url,
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                st.error(f"Error from OpenAI API: {response.status_code} - {response.text}")
                return []
            
            # Parse the response
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"].strip()
            
            # Clean up JSON content
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
                
            content = content.strip()
            
            # Parse JSON
            try:
                property_data = json.loads(content)
                if not isinstance(property_data, list):
                    property_data = [property_data]
            except json.JSONDecodeError:
                st.error(f"Failed to parse JSON from response: {content}")
                return []
            
            return property_data
            
        except Exception as e:
            st.error(f"Error getting property data: {str(e)}")
            return []
    
    def save_to_csv(self, properties, property_name):
        """Save property data to CSV"""
        if not properties:
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(properties)
        
        # Add timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{property_name.replace(' ', '_').lower()}_properties_{timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        
        return filename, filepath
    
    def analyze_data(self, properties):
        """Analyze property data"""
        if not properties:
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(properties)
        
        # Ensure numeric types
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['area_sqft'] = pd.to_numeric(df['area_sqft'], errors='coerce')
        
        # Calculate price per sqft
        df['price_per_sqft'] = df['price'] / df['area_sqft']
        
        # Basic statistics
        stats = {
            'total_listings': len(df),
            'avg_price': df['price'].mean() if 'price' in df.columns else 0,
            'min_price': df['price'].min() if 'price' in df.columns else 0,
            'max_price': df['price'].max() if 'price' in df.columns else 0,
            'median_price': df['price'].median() if 'price' in df.columns else 0,
            'avg_price_per_sqft': df['price_per_sqft'].mean() if 'price_per_sqft' in df.columns else 0
        }
        
        # Counts by property type
        property_type_counts = df['property_type'].value_counts().to_dict() if 'property_type' in df.columns else {}
        
        # Counts by bedroom
        bedroom_counts = df['bedrooms'].value_counts().to_dict() if 'bedrooms' in df.columns else {}
        
        # Counts by project
        project_counts = df['project'].value_counts().to_dict() if 'project' in df.columns else {}
        
        # Counts by developer
        developer_counts = df['developer'].value_counts().to_dict() if 'developer' in df.columns else {}
        
        return {
            'dataframe': df,
            'stats': stats,
            'property_type_counts': property_type_counts,
            'bedroom_counts': bedroom_counts,
            'project_counts': project_counts,
            'developer_counts': developer_counts
        }
    
    def generate_visualizations(self, analysis, property_name):
        """Generate visualizations for the analysis"""
        if not analysis or 'dataframe' not in analysis or analysis['dataframe'].empty:
            return {}
            
        df = analysis['dataframe']
        figures = {}
        
        # Set the style
        sns.set(style="whitegrid")
        
        # Price distribution
        try:
            if 'price' in df.columns and df['price'].sum() > 0:
                fig_price, ax_price = plt.subplots(figsize=(10, 5))
                sns.histplot(df['price'], kde=True, ax=ax_price)
                ax_price.set_title(f'Price Distribution for {property_name}')
                ax_price.set_xlabel('Price (AED)')
                ax_price.set_ylabel('Count')
                plt.tight_layout()
                figures['price_distribution'] = fig_price
        except Exception as e:
            st.error(f"Error generating price distribution chart: {e}")
        
        # Price per square foot distribution
        try:
            if 'price_per_sqft' in df.columns and df['price_per_sqft'].sum() > 0:
                fig_ppsf, ax_ppsf = plt.subplots(figsize=(10, 5))
                sns.histplot(df['price_per_sqft'], kde=True, ax=ax_ppsf)
                ax_ppsf.set_title(f'Price per Sq.Ft for {property_name}')
                ax_ppsf.set_xlabel('Price per Sq.Ft (AED)')
                ax_ppsf.set_ylabel('Count')
                plt.tight_layout()
                figures['price_per_sqft'] = fig_ppsf
        except Exception as e:
            st.error(f"Error generating price per sqft chart: {e}")
        
        # Property type breakdown
        try:
            if 'property_type' in df.columns and len(df['property_type'].unique()) > 1:
                fig_type, ax_type = plt.subplots(figsize=(10, 5))
                property_type_counts = df['property_type'].value_counts()
                property_type_counts.plot(kind='bar', ax=ax_type)
                ax_type.set_title(f'Property Types for {property_name}')
                ax_type.set_xlabel('Property Type')
                ax_type.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['property_types'] = fig_type
        except Exception as e:
            st.error(f"Error generating property type chart: {e}")
        
        # Bedroom distribution
        try:
            if 'bedrooms' in df.columns and len(df['bedrooms'].unique()) > 1:
                fig_bed, ax_bed = plt.subplots(figsize=(10, 5))
                bedroom_counts = df['bedrooms'].value_counts()
                bedroom_counts.plot(kind='bar', ax=ax_bed)
                ax_bed.set_title(f'Bedroom Distribution for {property_name}')
                ax_bed.set_xlabel('Bedrooms')
                ax_bed.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['bedrooms'] = fig_bed
        except Exception as e:
            st.error(f"Error generating bedroom chart: {e}")
            
        return figures
    
    def get_property_comparison(self, property_names):
        """Generate a comparison between different properties using OpenAI"""
        if not property_names or len(property_names) < 2:
            return "Please select at least two properties to compare."
        
        prompt = f"""
        Compare the following Dubai properties in detail: {', '.join(property_names)}.
        
        For each property, provide a structured comparison of:
        1. Price ranges and average prices
        2. Return on investment potential
        3. Location advantages and disadvantages
        4. Build quality and amenities
        5. Developer reputation
        6. Future growth potential
        
        Format your response in markdown with clear headings and bullet points for easy readability.
        Provide factual information with specific numbers where available.
        """
        
        try:
            # API call to OpenAI
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",  # or "gpt-3.5-turbo" for a less expensive option
                "messages": [
                    {"role": "system", "content": "You are a Dubai real estate expert providing detailed property comparisons."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5
            }
            
            response = requests.post(
                self.openai_api_url,
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                st.error(f"Error from OpenAI API: {response.status_code} - {response.text}")
                return "Failed to generate comparison. Please try again later."
            
            # Parse the response
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"].strip()
            
            return content
            
        except Exception as e:
            st.error(f"Error generating property comparison: {str(e)}")
            return "Failed to generate comparison. Please try again later."

# Helper functions
def format_currency(value):
    """Format a number as currency"""
    if pd.isna(value):
        return "N/A"
    return f"AED {value:,.2f}"

def format_area(value):
    """Format a number as area"""
    if pd.isna(value):
        return "N/A"
    return f"{value:,.2f} sq.ft"

# Sample property data (fallback if API fails)
SAMPLE_DATA = [
    {
        "project": "Damac Safa Two",
        "property_type": "Apartment",
        "price": 1900000,
        "area_sqft": 753,
        "bedrooms": "1",
        "bathrooms": "2",
        "location": "Business Bay, Dubai",
        "developer": "Damac Properties"
    },
    {
        "project": "Damac Safa Two",
        "property_type": "Apartment",
        "price": 2700000,
        "area_sqft": 1294,
        "bedrooms": "2",
        "bathrooms": "3",
        "location": "Business Bay, Dubai",
        "developer": "Damac Properties"
    },
    {
        "project": "Damac Safa One",
        "property_type": "Apartment",
        "price": 2200000,
        "area_sqft": 1001,
        "bedrooms": "1",
        "bathrooms": "2",
        "location": "Business Bay, Dubai",
        "developer": "Damac Properties"
    },
    {
        "project": "Damac Safa One",
        "property_type": "Apartment",
        "price": 3100000,
        "area_sqft": 1294,
        "bedrooms": "2",
        "bathrooms": "3",
        "location": "Business Bay, Dubai",
        "developer": "Damac Properties"
    }
]

# Main Streamlit app
def main():
    st.title("Property Analyzer with AI")
    st.markdown("### Analyze real estate properties in Dubai using AI")
    
    # Check for OpenAI API key
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    use_sample_data = st.sidebar.checkbox("Use sample data (if API fails)", value=False)
    
    if not api_key and not use_sample_data:
        st.warning("Please enter your OpenAI API key in the sidebar to continue, or check 'Use sample data'.")
        st.info("You need an OpenAI API key to use this application. You can get one from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)")
        return
    
    # Initialize analyzer
    analyzer = OpenAIPropertyAnalyzer(api_key)
    
    # Create tabs
    tab1, tab2 = st.tabs(["Property Analysis", "Property Comparison"])
    
    with tab1:
        st.header("Analyze Property Data")
        
        with st.form("property_form"):
            property_name = st.text_input("Enter Property Name or Area", "Damac Safa Two")
            max_properties = st.slider("Maximum Properties to Analyze", min_value=5, max_value=15, value=8,
                                     help="Higher values will provide more comprehensive data but may take longer to process.")
            
            analyze_button = st.form_submit_button("Analyze Property")
        
        if analyze_button and (property_name or use_sample_data):
            with st.spinner(f"Analyzing {property_name}... This may take a minute"):
                # Get property data from OpenAI or use sample data
                if use_sample_data:
                    properties = SAMPLE_DATA
                    sleep(1)  # Simulate API call delay
                    st.info("Using sample data instead of API call")
                else:
                    properties = analyzer.get_property_data(property_name, max_properties)
                
                if properties:
                    st.success(f"Analysis complete! Found data for {len(properties)} properties in {property_name}")
                    
                    # Save to CSV
                    csv_filename, csv_filepath = analyzer.save_to_csv(properties, property_name)
                    
                    # Analyze data
                    analysis = analyzer.analyze_data(properties)
                    
                    if analysis:
                        # Display summary statistics
                        st.subheader("Summary Statistics")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Listings", analysis['stats']['total_listings'])
                        
                        with col2:
                            st.metric("Average Price", format_currency(analysis['stats']['avg_price']))
                        
                        with col3:
                            st.metric("Price Range", f"{format_currency(analysis['stats']['min_price'])} - {format_currency(analysis['stats']['max_price'])}")
                        
                        with col4:
                            st.metric("Avg Price/Sq.Ft", format_currency(analysis['stats']['avg_price_per_sqft']))
                        
                        # Generate visualizations
                        visualizations = analyzer.generate_visualizations(analysis, property_name)
                        
                        if visualizations:
                            st.subheader("Visualizations")
                            
                            # Display charts in columns
                            for i in range(0, len(visualizations), 2):
                                cols = st.columns(2)
                                
                                # First chart
                                chart_keys = list(visualizations.keys())
                                if i < len(chart_keys):
                                    with cols[0]:
                                        key1 = chart_keys[i]
                                        st.pyplot(visualizations[key1])
                                
                                # Second chart (if available)
                                if i + 1 < len(chart_keys):
                                    with cols[1]:
                                        key2 = chart_keys[i + 1]
                                        st.pyplot(visualizations[key2])
                        
                        # Display breakdowns
                        if analysis['property_type_counts']:
                            st.subheader("Property Types")
                            st.write(pd.DataFrame({
                                'Property Type': list(analysis['property_type_counts'].keys()),
                                'Count': list(analysis['property_type_counts'].values())
                            }).sort_values('Count', ascending=False))
                        
                        if analysis['bedroom_counts']:
                            st.subheader("Bedroom Distribution")
                            st.write(pd.DataFrame({
                                'Bedrooms': list(analysis['bedroom_counts'].keys()),
                                'Count': list(analysis['bedroom_counts'].values())
                            }))
                        
                        if analysis['project_counts'] and len(analysis['project_counts']) > 1:
                            st.subheader("Projects")
                            st.write(pd.DataFrame({
                                'Project': list(analysis['project_counts'].keys()),
                                'Count': list(analysis['project_counts'].values())
                            }).sort_values('Count', ascending=False))
                        
                        if analysis['developer_counts']:
                            st.subheader("Developers")
                            st.write(pd.DataFrame({
                                'Developer': list(analysis['developer_counts'].keys()),
                                'Count': list(analysis['developer_counts'].values())
                            }).sort_values('Count', ascending=False))
                        
                        # Display property listings
                        st.subheader("Property Listings")
                        
                        # Format DataFrame for display
                        display_df = analysis['dataframe'].copy()
                        if 'price' in display_df.columns:
                            display_df['price'] = display_df['price'].apply(lambda x: f"AED {x:,.0f}" if pd.notnull(x) else "N/A")
                        if 'price_per_sqft' in display_df.columns:
                            display_df['price_per_sqft'] = display_df['price_per_sqft'].apply(lambda x: f"AED {x:,.0f}" if pd.notnull(x) else "N/A")
                        if 'area_sqft' in display_df.columns:
                            display_df['area_sqft'] = display_df['area_sqft'].apply(lambda x: f"{x:,.0f} sq.ft" if pd.notnull(x) else "N/A")
                            
                        # Display the data
                        st.dataframe(display_df)
                        
                        # Provide download link
                        with open(csv_filepath, "rb") as file:
                            st.download_button(
                                label=f"Download {property_name} Data (CSV)",
                                data=file,
                                file_name=csv_filename,
                                mime="text/csv"
                            )
                else:
                    st.error(f"No properties found for {property_name}. Please try another property name or area.")
                    if not use_sample_data:
                        st.info("Try checking 'Use sample data' in the sidebar if the API is not working.")
    
    with tab2:
        st.header("Compare Properties")
        
        property_list = st.text_input("Enter properties to compare (comma-separated)", "Damac Safa One, Damac Safa Two")
        use_sample_comparison = st.checkbox("Use sample comparison (if API fails)", value=False)
        
        if st.button("Generate Comparison"):
            if property_list or use_sample_comparison:
                properties_to_compare = [p.strip() for p in property_list.split(",") if p.strip()]
                
                if len(properties_to_compare) < 2 and not use_sample_comparison:
                    st.warning("Please enter at least two properties to compare.")
                else:
                    with st.spinner("Generating property comparison..."):
                        if use_sample_comparison:
                            comparison = """
# Comparison: Damac Safa One vs. Damac Safa Two

## Price Ranges and Average Prices

### Damac Safa One
- Studio: AED 1.2M - 1.5M (Average: AED 1.35M)
- 1 Bedroom: AED 1.8M - 2.3M (Average: AED 2.1M)
- 2 Bedrooms: AED 2.7M - 3.5M (Average: AED 3.1M)
- 3 Bedrooms: AED 4.2M - 5.5M (Average: AED 4.7M)

### Damac Safa Two
- Studio: AED 1.1M - 1.4M (Average: AED 1.25M)
- 1 Bedroom: AED 1.65M - 2.1M (Average: AED 1.9M)
- 2 Bedrooms: AED 2.45M - 3.2M (Average: AED 2.85M)
- 3 Bedrooms: AED 3.8M - 5.2M (Average: AED 4.5M)

## Return on Investment Potential

### Damac Safa One
- Estimated Rental Yield: 5.8-6.2%
- Expected Capital Appreciation: 7-9% annually
- Premium positioning may result in higher long-term value retention

### Damac Safa Two
- Estimated Rental Yield: 6.2-6.5%
- Expected Capital Appreciation: 6-8% annually
- More affordable entry point may attract a broader rental market

## Location Advantages and Disadvantages

### Damac Safa One
**Advantages:**
- Prime location in Business Bay
- Closer proximity to Dubai Mall and Burj Khalifa
- Better views of downtown Dubai skyline
- More established surrounding infrastructure

**Disadvantages:**
- Higher traffic congestion during peak hours
- More construction activity in immediate vicinity

### Damac Safa Two
**Advantages:**
- Newer development area with growth potential
- Less congested access routes
- Slightly larger unit sizes on average
- More green spaces planned nearby

**Disadvantages:**
- Slightly farther from key downtown attractions
- Some amenities still under development

## Build Quality and Amenities

### Damac Safa One
- Designed by international architects with luxury finishes
- Features include: Infinity pool, spa, fitness center, concierge services
- Smart home technology integration
- Higher ceiling heights (2.9m)

### Damac Safa Two
- Similar build quality but with newer design concepts
- Features include: Rooftop garden, co-working spaces, children's play areas
- More emphasis on outdoor recreational spaces
- Modern eco-friendly features

## Developer Reputation

### Damac Properties (Both Developments)
- Well-established developer with 20+ years in Dubai market
- Known for luxury developments with strong build quality
- Generally good delivery record with occasional delays
- Strong after-sales support and property management

## Future Growth Potential

### Damac Safa One
- Established area with limited new supply planned
- Higher initial investment but potentially more stable growth
- Better short-term rental prospects

### Damac Safa Two
- Located in an area with more future development potential
- Potentially higher medium to long-term appreciation
- More affected by overall market supply trends

## Summary

**Damac Safa One** is better suited for investors seeking established location advantages with premium positioning and immediate rental returns.

**Damac Safa Two** offers better value for mid-term investors, with slightly higher yields and greater appreciation potential as the surrounding area develops further.
"""
                            sleep(2)  # Simulate API call delay
                            st.info("Using sample comparison instead of API call")
                        else:
                            comparison = analyzer.get_property_comparison(properties_to_compare)
                        
                        st.markdown(comparison)
            else:
                st.warning("Please enter properties to compare or use sample comparison.")

if __name__ == "__main__":
    main()
