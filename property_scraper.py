import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import time
from datetime import datetime
import openai
import re

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
        openai.api_key = api_key
        self.results_dir = RESULTS_DIR
        
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
        9. Brief description of the property

        For each property, format the response as a JSON object as follows:
        ```json
        {
          "project": "Property project name",
          "property_type": "Property type",
          "price": 1000000,
          "area_sqft": 1200,
          "bedrooms": "2",
          "bathrooms": "2",
          "location": "Location",
          "developer": "Developer name",
          "description": "Brief description"
        }
        ```

        I need the response to be ONLY valid JSON objects in an array, nothing else. Use the most up-to-date information available.
        """
        
        try:
            # Make API call to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or gpt-3.5-turbo if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides accurate real estate data in Dubai. You output only valid JSON without any additional text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for more focused, deterministic output
                max_tokens=2000
            )
            
            # Extract content from the response
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from the content (in case there's any extra text)
            json_match = re.search(r'```json(.*?)```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                json_str = content
            
            # Clean up JSON string
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON data
            try:
                property_data = json.loads(json_str)
                if not isinstance(property_data, list):
                    property_data = [property_data]
            except json.JSONDecodeError:
                # If the JSON is not an array, try wrapping it
                try:
                    json_str = f"[{json_str}]"
                    property_data = json.loads(json_str)
                except json.JSONDecodeError:
                    st.error(f"Failed to parse property data from OpenAI response: {content}")
                    return []
            
            return property_data
        
        except Exception as e:
            st.error(f"Error getting property data from OpenAI: {str(e)}")
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
        
        # Project breakdown
        try:
            if 'project' in df.columns and len(df['project'].unique()) > 1:
                fig_project, ax_project = plt.subplots(figsize=(10, 5))
                project_counts = df['project'].value_counts()
                project_counts.plot(kind='bar', ax=ax_project)
                ax_project.set_title(f'Projects in {property_name}')
                ax_project.set_xlabel('Project')
                ax_project.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['projects'] = fig_project
        except Exception as e:
            st.error(f"Error generating project chart: {e}")
        
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
            # Make API call to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or gpt-3.5-turbo if preferred
                messages=[
                    {"role": "system", "content": "You are a Dubai real estate expert providing detailed property comparisons."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # Extract content from the response
            content = response.choices[0].message.content.strip()
            return content
            
        except Exception as e:
            st.error(f"Error generating property comparison: {str(e)}")
            return "Failed to generate comparison. Please try again later."
    
    def get_investment_advice(self, property_name, budget=None):
        """Get investment advice for a specific property using OpenAI"""
        budget_text = f"with a budget of AED {budget}" if budget else ""
        
        prompt = f"""
        Provide detailed investment advice for {property_name} in Dubai {budget_text}.
        
        Include the following in your analysis:
        1. Current market conditions for this property/area
        2. Expected ROI (rental yield and capital appreciation)
        3. Best unit types to invest in (studio, 1BR, 2BR, etc.)
        4. Payment plans available (if known)
        5. Risks and considerations
        6. Alternative investment options in similar price range
        7. Long-term outlook (3-5 years)
        
        Format your response in markdown with clear headings and bullet points for easy readability.
        Provide factual information with specific numbers where available.
        """
        
        try:
            # Make API call to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or gpt-3.5-turbo if preferred
                messages=[
                    {"role": "system", "content": "You are a Dubai real estate investment advisor providing detailed market analysis and investment advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # Extract content from the response
            content = response.choices[0].message.content.strip()
            return content
            
        except Exception as e:
            st.error(f"Error generating investment advice: {str(e)}")
            return "Failed to generate investment advice. Please try again later."

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

# Main Streamlit app
def main():
    st.title("Property Analyzer with AI")
    st.markdown("### Analyze real estate properties in Dubai using AI")
    
    # Check for OpenAI API key
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        st.info("You need an OpenAI API key to use this application. You can get one from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)")
        return
    
    # Initialize analyzer
    analyzer = OpenAIPropertyAnalyzer(api_key)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Property Analysis", "Property Comparison", "Investment Advice"])
    
    with tab1:
        st.header("Analyze Property Data")
        
        with st.form("property_form"):
            property_name = st.text_input("Enter Property Name or Area", "Damac Safa Two")
            max_properties = st.slider("Maximum Properties to Analyze", min_value=5, max_value=20, value=10,
                                     help="Higher values will provide more comprehensive data but may take longer to process.")
            
            analyze_button = st.form_submit_button("Analyze Property")
        
        if analyze_button and property_name:
            with st.spinner(f"Analyzing {property_name}... This may take a minute"):
                # Get property data from OpenAI
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
    
    with tab2:
        st.header("Compare Properties")
        
        property_list = st.text_input("Enter properties to compare (comma-separated)", "Damac Safa One, Damac Safa Two")
        
        if st.button("Generate Comparison"):
            if property_list:
                properties_to_compare = [p.strip() for p in property_list.split(",") if p.strip()]
                
                if len(properties_to_compare) < 2:
                    st.warning("Please enter at least two properties to compare.")
                else:
                    with st.spinner("Generating property comparison..."):
                        comparison = analyzer.get_property_comparison(properties_to_compare)
                        st.markdown(comparison)
            else:
                st.warning("Please enter properties to compare.")
    
    with tab3:
        st.header("Get Investment Advice")
        
        property_for_advice = st.text_input("Enter property or area for investment advice", "Damac Safa Two")
        budget = st.number_input("Your budget (AED)", min_value=0, value=2000000, step=100000)
        
        if st.button("Get Investment Advice"):
            if property_for_advice:
                with st.spinner("Generating investment advice..."):
                    advice = analyzer.get_investment_advice(property_for_advice, budget if budget > 0 else None)
                    st.markdown(advice)
            else:
                st.warning("Please enter a property or area.")

if __name__ == "__main__":
    main()
