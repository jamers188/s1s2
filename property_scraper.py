import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import json

# Page configuration
st.set_page_config(
    page_title="Property Finder Analysis Tool",
    page_icon="🏢",
    layout="wide"
)

# Create a directory for results
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

class PropertyFinderAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.propertyfinder.ae/v2"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.results_dir = RESULTS_DIR
    
    def search_properties(self, query, location=None, property_type=None, min_price=None, max_price=None, bedrooms=None, page=1, limit=50):
        """Search for properties using the API"""
        endpoint = f"{self.base_url}/properties/search"
        
        # Build the query parameters
        params = {
            'q': query,
            'page': page,
            'limit': limit,
            'sort': 'price_asc'  # Sort by price ascending
        }
        
        # Add optional filters
        if location:
            params['location'] = location
        if property_type:
            params['property_type'] = property_type
        if min_price:
            params['price_min'] = min_price
        if max_price:
            params['price_max'] = max_price
        if bedrooms:
            params['bedrooms'] = bedrooms
            
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return {"data": [], "meta": {"total": 0}}
    
    def get_all_properties(self, query, location=None, property_type=None, min_price=None, max_price=None, bedrooms=None, max_pages=5, progress_bar=None):
        """Get all properties matching search criteria, handling pagination"""
        all_properties = []
        page = 1
        total_fetched = 0
        total_available = None
        
        while page <= max_pages:
            if progress_bar and total_available:
                progress = min(total_fetched / total_available, 1.0) if total_available > 0 else 0
                progress_bar.progress(progress)
                
            results = self.search_properties(
                query, location, property_type, min_price, max_price, bedrooms, page=page
            )
            
            if not results or not results.get('data'):
                break
                
            properties = results.get('data', [])
            all_properties.extend(properties)
            
            # Update totals for progress tracking
            if not total_available and 'meta' in results and 'total' in results['meta']:
                total_available = results['meta']['total']
                
            total_fetched += len(properties)
            
            # Check if we've reached the end of results
            if 'meta' in results and 'next_page' in results['meta'] and not results['meta']['next_page']:
                break
                
            page += 1
        
        if progress_bar:
            progress_bar.progress(1.0)
            
        return all_properties, total_available
    
    def process_properties(self, properties):
        """Process and extract relevant information from property data"""
        processed_data = []
        
        for prop in properties:
            # Extract basic property details
            property_data = {
                'id': prop.get('id', 'N/A'),
                'title': prop.get('title', 'N/A'),
                'price': prop.get('price', {}).get('amount', 0),
                'currency': prop.get('price', {}).get('currency', 'AED'),
                'property_type': prop.get('category', {}).get('name', 'N/A'),
                'bedrooms': prop.get('bedrooms', 'N/A'),
                'bathrooms': prop.get('bathrooms', 'N/A'),
                'area_sqft': prop.get('size', {}).get('value', 0) if prop.get('size', {}) else 0,
                'status': prop.get('status', 'N/A'),
                'completion_status': prop.get('completion_status', 'N/A'),
                'location': self._extract_location(prop),
                'agent_name': self._extract_agent(prop),
                'property_url': prop.get('share_url', 'N/A')
            }
            
            # Calculate price per sqft if both values are available
            if property_data['price'] and property_data['area_sqft']:
                property_data['price_per_sqft'] = round(property_data['price'] / property_data['area_sqft'], 2)
            else:
                property_data['price_per_sqft'] = 0
                
            processed_data.append(property_data)
            
        return processed_data
    
    def _extract_location(self, property_data):
        """Extract location information from property data"""
        location = 'N/A'
        
        if 'location' in property_data:
            loc_data = property_data['location']
            if isinstance(loc_data, dict):
                location_parts = []
                if 'community' in loc_data and loc_data['community']:
                    location_parts.append(loc_data['community'].get('name', ''))
                if 'area' in loc_data and loc_data['area']:
                    location_parts.append(loc_data['area'].get('name', ''))
                if 'city' in loc_data and loc_data['city']:
                    location_parts.append(loc_data['city'].get('name', ''))
                    
                location = ', '.join(filter(None, location_parts))
        
        return location
    
    def _extract_agent(self, property_data):
        """Extract agent information from property data"""
        agent = 'N/A'
        
        if 'agent' in property_data and property_data['agent']:
            agent_data = property_data['agent']
            if isinstance(agent_data, dict) and 'name' in agent_data:
                agent = agent_data['name']
                
        return agent
    
    def analyze_data(self, properties_data):
        """Analyze the property data"""
        if not properties_data:
            return None
        
        df = pd.DataFrame(properties_data)
        
        # Basic statistics
        stats = {
            'total_listings': len(df),
            'avg_price': df['price'].mean() if len(df) > 0 else 0,
            'min_price': df['price'].min() if len(df) > 0 else 0,
            'max_price': df['price'].max() if len(df) > 0 else 0,
            'median_price': df['price'].median() if len(df) > 0 else 0,
            'avg_price_per_sqft': df['price_per_sqft'].mean() if 'price_per_sqft' in df.columns and len(df) > 0 else 0
        }
        
        # Count by property type
        property_type_counts = df['property_type'].value_counts().to_dict() if len(df) > 0 else {}
        
        # Count by bedroom
        bedroom_counts = df['bedrooms'].value_counts().to_dict() if len(df) > 0 else {}
        
        # Count by agent
        agent_counts = df['agent_name'].value_counts().to_dict() if len(df) > 0 else {}
        
        # Get top 5 agents
        top_agents = {k: agent_counts[k] for k in list(agent_counts.keys())[:5]} if agent_counts else {}
        
        return {
            'dataframe': df,
            'stats': stats,
            'property_type_counts': property_type_counts,
            'bedroom_counts': bedroom_counts,
            'agent_counts': agent_counts,
            'top_agents': top_agents
        }
    
    def generate_visualizations(self, analysis_results, query):
        """Generate visualizations for the analysis results"""
        if not analysis_results or len(analysis_results['dataframe']) == 0:
            return {}
        
        df = analysis_results['dataframe']
        figures = {}
        
        # Set the style
        sns.set(style="whitegrid")
        
        # Price distribution
        try:
            fig_price, ax_price = plt.subplots(figsize=(10, 5))
            sns.histplot(df['price'], kde=True, ax=ax_price)
            ax_price.set_title(f'Price Distribution for {query}')
            ax_price.set_xlabel('Price (AED)')
            ax_price.set_ylabel('Count')
            plt.tight_layout()
            figures['price_distribution'] = fig_price
        except Exception as e:
            st.error(f"Error generating price distribution: {e}")
        
        # Property type distribution
        try:
            if len(df['property_type'].unique()) > 1:
                fig_type, ax_type = plt.subplots(figsize=(10, 5))
                property_type_counts = df['property_type'].value_counts()
                property_type_counts.plot(kind='bar', ax=ax_type)
                ax_type.set_title(f'Property Types for {query}')
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
                bedroom_counts = df['bedrooms'].value_counts().sort_index()
                bedroom_counts.plot(kind='bar', ax=ax_bed)
                ax_bed.set_title(f'Bedroom Distribution for {query}')
                ax_bed.set_xlabel('Bedrooms')
                ax_bed.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['bedrooms'] = fig_bed
        except Exception as e:
            st.error(f"Error generating bedroom chart: {e}")
        
        # Price per square foot
        try:
            if 'price_per_sqft' in df.columns and df['price_per_sqft'].sum() > 0:
                fig_sqft, ax_sqft = plt.subplots(figsize=(10, 5))
                df_filtered = df[df['price_per_sqft'] > 0]  # Filter out zeros
                sns.histplot(df_filtered['price_per_sqft'], kde=True, ax=ax_sqft)
                ax_sqft.set_title(f'Price per Sq.Ft Distribution for {query}')
                ax_sqft.set_xlabel('Price per Sq.Ft (AED)')
                ax_sqft.set_ylabel('Count')
                plt.tight_layout()
                figures['price_per_sqft'] = fig_sqft
        except Exception as e:
            st.error(f"Error generating price per sqft chart: {e}")
        
        # Top agents
        try:
            if 'agent_name' in df.columns and len(df['agent_name'].unique()) > 1:
                fig_agent, ax_agent = plt.subplots(figsize=(10, 5))
                agent_counts = df['agent_name'].value_counts().head(10)  # Top 10 agents
                agent_counts.plot(kind='bar', ax=ax_agent)
                ax_agent.set_title(f'Top 10 Agents for {query}')
                ax_agent.set_xlabel('Agent')
                ax_agent.set_ylabel('Number of Listings')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['top_agents'] = fig_agent
        except Exception as e:
            st.error(f"Error generating agent chart: {e}")
        
        return figures
    
    def save_results(self, properties_data, query):
        """Save the property data to a CSV file"""
        if not properties_data:
            return None
        
        df = pd.DataFrame(properties_data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        query_safe = query.replace(" ", "_").replace("/", "_").lower()
        filename = f"{query_safe}_properties_{timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)
        df.to_csv(filepath, index=False)
        
        return filename, filepath

# Streamlit app
def main():
    st.title("Property Finder Analysis Tool")
    st.markdown("### Search for properties and analyze market trends")
    
    # API key input (you would normally store this securely)
    api_key = st.text_input("Enter your Property Finder API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your Property Finder API key to continue.")
        st.markdown("""
        Don't have an API key? 
        
        1. Visit the [Property Finder Developer Portal](https://developers.propertyfinder.ae/)
        2. Sign up for an account
        3. Create a new application to get your API key
        """)
        return
    
    # Initialize API client
    property_finder = PropertyFinderAPI(api_key)
    
    with st.expander("About This Tool", expanded=True):
        st.markdown("""
        This application uses the Property Finder API to search for properties and provide analytics including:
        - Total available inventory (number of listings)
        - Price statistics (average, minimum, maximum, median)
        - Price per square foot analysis
        - Breakdown by property type
        - Breakdown by number of bedrooms
        - Top agents with the most listings
        - Detailed property data for further analysis
        
        The data is updated each time you run a search.
        """)
    
    # Create form for search parameters
    with st.form("search_form"):
        st.subheader("Search Parameters")
        
        # Main search query
        query = st.text_input("Search Query (e.g., 'Damac Safa One', 'Palm Jumeirah')", "Damac Safa")
        
        # Create columns for filters
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input("Location (optional)", "")
            min_price = st.number_input("Minimum Price (AED)", value=0, min_value=0, step=100000)
            bedrooms = st.selectbox("Bedrooms", ["Any", "Studio", "1", "2", "3", "4", "5+"])
        
        with col2:
            property_type = st.selectbox("Property Type", ["Any", "Apartment", "Villa", "Townhouse", "Penthouse", "Duplex"])
            max_price = st.number_input("Maximum Price (AED)", value=0, min_value=0, step=100000)
            max_pages = st.slider("Maximum Pages to Fetch", min_value=1, max_value=10, value=3, 
                                help="Each page contains up to 50 properties. Increasing this will fetch more properties but may take longer.")
        
        search_button = st.form_submit_button("Search Properties", type="primary")
    
    # Clean up inputs
    if property_type == "Any":
        property_type = None
    if bedrooms == "Any":
        bedrooms = None
    elif bedrooms == "Studio":
        bedrooms = "0"
    elif bedrooms == "5+":
        bedrooms = "5"
    
    if min_price == 0:
        min_price = None
    if max_price == 0:
        max_price = None
    
    # Execute search when button is clicked
    if search_button and query:
        with st.spinner(f"Searching for properties matching '{query}'..."):
            st.subheader(f"Analyzing Properties: {query}")
            progress_bar = st.progress(0)
            
            # Get properties from API
            properties, total_available = property_finder.get_all_properties(
                query, location, property_type, min_price, max_price, bedrooms, max_pages, progress_bar
            )
            
            if properties:
                st.success(f"Found {len(properties)} listings out of {total_available} total available")
                
                # Process property data
                processed_properties = property_finder.process_properties(properties)
                
                # Save data
                csv_filename, csv_filepath = property_finder.save_results(processed_properties, query)
                
                # Analyze data
                analysis = property_finder.analyze_data(processed_properties)
                
                if analysis:
                    # Display summary statistics
                    st.subheader("Summary Statistics")
                    stats_col1, stats_col2, stats_col3, stats_col4, stats_col5 = st.columns(5)
                    with stats_col1:
                        st.metric("Total Listings", analysis['stats']['total_listings'])
                    with stats_col2:
                        st.metric("Average Price", f"AED {analysis['stats']['avg_price']:,.2f}")
                    with stats_col3:
                        st.metric("Minimum Price", f"AED {analysis['stats']['min_price']:,.2f}")
                    with stats_col4:
                        st.metric("Maximum Price", f"AED {analysis['stats']['max_price']:,.2f}")
                    with stats_col5:
                        st.metric("Avg Price/Sq.Ft", f"AED {analysis['stats']['avg_price_per_sqft']:,.2f}")
                    
                    # Display property type breakdown
                    st.subheader("Property Types")
                    st.write(pd.DataFrame({
                        'Property Type': list(analysis['property_type_counts'].keys()),
                        'Count': list(analysis['property_type_counts'].values())
                    }).sort_values('Count', ascending=False))
                    
                    # Display bedroom breakdown
                    st.subheader("Bedroom Distribution")
                    st.write(pd.DataFrame({
                        'Bedrooms': list(analysis['bedroom_counts'].keys()),
                        'Count': list(analysis['bedroom_counts'].values())
                    }).sort_values('Bedrooms'))
                    
                    # Display top agents
                    st.subheader("Top Agents")
                    st.write(pd.DataFrame({
                        'Agent': list(analysis['top_agents'].keys()),
                        'Number of Listings': list(analysis['top_agents'].values())
                    }))
                    
                    # Generate and display visualizations
                    figures = property_finder.generate_visualizations(analysis, query)
                    
                    if figures:
                        st.subheader("Visualizations")
                        
                        # Use two columns for the charts
                        for i in range(0, len(figures), 2):
                            cols = st.columns(2)
                            
                            # First chart
                            fig_keys = list(figures.keys())
                            if i < len(fig_keys):
                                with cols[0]:
                                    key1 = fig_keys[i]
                                    st.pyplot(figures[key1])
                            
                            # Second chart
                            if i + 1 < len(fig_keys):
                                with cols[1]:
                                    key2 = fig_keys[i + 1]
                                    st.pyplot(figures[key2])
                    
                    # Display property data table
                    st.subheader("Property Listings")
                    
                    # Select columns to display
                    display_cols = ['title', 'price', 'area_sqft', 'price_per_sqft', 'bedrooms', 
                                   'bathrooms', 'property_type', 'location', 'agent_name', 'property_url']
                    
                    # Ensure all columns exist in the dataframe
                    available_cols = [col for col in display_cols if col in analysis['dataframe'].columns]
                    
                    st.dataframe(analysis['dataframe'][available_cols])
                    
                    # Provide download link
                    with open(csv_filepath, "rb") as file:
                        st.download_button(
                            label=f"Download Complete Data (CSV)",
                            data=file,
                            file_name=csv_filename,
                            mime="text/csv",
                        )
            else:
                st.error(f"No data found for '{query}'. Try adjusting your search parameters.")

if __name__ == "__main__":
    main()
