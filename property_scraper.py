import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import time
import random
import re
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

class PropertyFinderScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.base_url = "https://www.propertyfinder.ae"
        self.search_url = "https://www.propertyfinder.ae/en/search"
        self.results_dir = RESULTS_DIR
        
    def build_search_url(self, query, property_type=None, min_price=None, max_price=None, bedrooms=None, page=1):
        """Build search URL with parameters"""
        # Format query for URL
        formatted_query = query.lower().replace(" ", "+")
        
        # Start with base URL and add query
        url = f"{self.search_url}?q={formatted_query}&page={page}"
        
        # Add optional filters
        if property_type and property_type != "Any":
            url += f"&c={self._get_property_type_code(property_type)}"
            
        if min_price:
            url += f"&pf={min_price}"
            
        if max_price:
            url += f"&pt={max_price}"
            
        if bedrooms and bedrooms != "Any":
            if bedrooms == "Studio":
                bed_code = "0"
            elif bedrooms == "5+":
                bed_code = "5"
            else:
                bed_code = bedrooms
            url += f"&bf={bed_code}&bt={bed_code}"
        
        return url
    
    def _get_property_type_code(self, property_type):
        """Convert property type to Property Finder category code"""
        type_codes = {
            "Apartment": "1",
            "Villa": "2",
            "Townhouse": "16",
            "Penthouse": "4",
            "Duplex": "8"
        }
        return type_codes.get(property_type, "0")
    
    def fetch_page(self, url):
        """Fetch and parse a page with retry mechanism"""
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                # Check if we got a proper HTML response
                if "<!DOCTYPE html>" in response.text:
                    return BeautifulSoup(response.text, 'html.parser')
                else:
                    retries += 1
                    time.sleep(2 * retries)  # Exponential backoff
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching {url}: {e}")
                retries += 1
                time.sleep(2 * retries)
        
        return None
    
    def extract_json_data(self, soup):
        """Extract property data from embedded JSON in the page"""
        try:
            # Look for script tags with JSON data
            script_tags = soup.find_all('script', {'type': 'application/ld+json'})
            
            properties = []
            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    # Check if this is a property listing
                    if isinstance(data, dict) and data.get('@type') == 'PropertyListing':
                        properties.append(data)
                except json.JSONDecodeError:
                    continue
            
            return properties
        except Exception as e:
            st.error(f"Error extracting JSON data: {e}")
            return []
    
    def extract_property_details(self, property_element):
        """Extract details from a property card element using proper selectors"""
        try:
            property_data = {}
            
            # Title
            title_element = property_element.select_one('.property-card__title') or property_element.select_one('.card-list__item-property-title')
            if title_element:
                property_data['title'] = title_element.text.strip()
            else:
                property_data['title'] = 'N/A'
            
            # Price
            price_element = property_element.select_one('.property-card__price') or property_element.select_one('.card-list__item-property-price')
            if price_element:
                price_text = price_element.text.strip()
                property_data['price'] = price_text
                property_data['price_value'] = self.extract_price_value(price_text)
            else:
                property_data['price'] = 'N/A'
                property_data['price_value'] = 0
            
            # Location
            location_element = property_element.select_one('.property-card__location') or property_element.select_one('.card-list__item-property-location')
            if location_element:
                property_data['location'] = location_element.text.strip()
            else:
                property_data['location'] = 'N/A'
            
            # Property details (beds, baths, area)
            details_container = property_element.select_one('.property-card__facts') or property_element.select_one('.card-list__item-property-features')
            if details_container:
                details_items = details_container.select('li')
                
                # Extract bedrooms
                if len(details_items) > 0:
                    bed_text = details_items[0].text.strip()
                    property_data['bedrooms'] = 'Studio' if 'studio' in bed_text.lower() else bed_text
                else:
                    property_data['bedrooms'] = 'N/A'
                
                # Extract bathrooms
                if len(details_items) > 1:
                    property_data['bathrooms'] = details_items[1].text.strip()
                else:
                    property_data['bathrooms'] = 'N/A'
                
                # Extract area
                if len(details_items) > 2:
                    area_text = details_items[2].text.strip()
                    property_data['area'] = area_text
                    property_data['area_sqft'] = self.extract_area_value(area_text)
                else:
                    property_data['area'] = 'N/A'
                    property_data['area_sqft'] = 0
            else:
                property_data['bedrooms'] = 'N/A'
                property_data['bathrooms'] = 'N/A'
                property_data['area'] = 'N/A'
                property_data['area_sqft'] = 0
            
            # Property type
            property_type_element = property_element.select_one('.property-card__type') or property_element.select_one('.card-list__item-property-type')
            if property_type_element:
                property_data['property_type'] = property_type_element.text.strip()
            else:
                property_data['property_type'] = self.infer_property_type(property_data['title'])
            
            # Link to property
            link_element = property_element.select_one('a.property-card__link') or property_element.select_one('a.card-list__item-link')
            if link_element and 'href' in link_element.attrs:
                href = link_element['href']
                property_data['link'] = self.base_url + href if not href.startswith('http') else href
            else:
                property_data['link'] = 'N/A'
            
            # Agent name (may need to visit individual property page to get this)
            agency_element = property_element.select_one('.property-card__agent') or property_element.select_one('.card-list__item-agent-name')
            if agency_element:
                property_data['agent_name'] = agency_element.text.strip()
            else:
                property_data['agent_name'] = 'N/A'
            
            # Calculate price per sqft if both values are available
            if property_data['price_value'] > 0 and property_data['area_sqft'] > 0:
                property_data['price_per_sqft'] = round(property_data['price_value'] / property_data['area_sqft'], 2)
            else:
                property_data['price_per_sqft'] = 0
            
            return property_data
        except Exception as e:
            st.error(f"Error extracting property details: {e}")
            return {}
    
    def extract_price_value(self, price_text):
        """Extract numeric price value from text"""
        try:
            # Remove currency symbols, commas, and convert to float
            digits = re.findall(r'\d+', price_text.replace(',', ''))
            if digits:
                return float(''.join(digits))
            return 0
        except:
            return 0
    
    def extract_area_value(self, area_text):
        """Extract numeric area value from text"""
        try:
            # Extract digits and convert to float
            digits = re.findall(r'\d+\.?\d*', area_text.replace(',', ''))
            if digits:
                value = float(digits[0])
                # Convert to sq.ft if necessary
                if 'm²' in area_text.lower() or 'sqm' in area_text.lower():
                    value *= 10.764  # Convert square meters to square feet
                return value
            return 0
        except:
            return 0
    
    def infer_property_type(self, title):
        """Infer property type from title if not explicitly provided"""
        title_lower = title.lower()
        if 'apartment' in title_lower:
            return 'Apartment'
        elif 'villa' in title_lower:
            return 'Villa'
        elif 'townhouse' in title_lower:
            return 'Townhouse'
        elif 'penthouse' in title_lower:
            return 'Penthouse'
        elif 'duplex' in title_lower:
            return 'Duplex'
        else:
            return 'Other'
    
    def extract_total_results(self, soup):
        """Extract total number of results from the page"""
        try:
            total_element = soup.select_one('.search-results__header') or soup.select_one('.search-title')
            if total_element:
                text = total_element.text.strip()
                # Extract digits from text like "123 Properties for Sale"
                digits = re.findall(r'\d+', text)
                if digits:
                    return int(digits[0])
            return None
        except:
            return None
        
    def scrape_properties(self, query, property_type=None, min_price=None, max_price=None, bedrooms=None, max_pages=3, progress_bar=None):
        """Scrape property listings matching search criteria"""
        all_properties = []
        total_results = None
        
        for page in range(1, max_pages + 1):
            if progress_bar:
                if total_results:
                    progress = min((page - 1) * 25 / total_results, 1.0) if total_results > 0 else 0
                else:
                    progress = (page - 1) / max_pages
                progress_bar.progress(progress)
            
            url = self.build_search_url(query, property_type, min_price, max_price, bedrooms, page)
            soup = self.fetch_page(url)
            
            if not soup:
                continue
            
            # Get total number of results if not yet determined
            if not total_results:
                total_results = self.extract_total_results(soup)
            
            # Check if we've reached the end of results
            no_results = soup.select_one('.no-result-message') or "no results found" in soup.text.lower()
            if no_results and page == 1:
                st.info(f"No results found for '{query}' with the selected filters.")
                break
                
            # Try to extract properties from embedded JSON data first
            json_properties = self.extract_json_data(soup)
            if json_properties:
                # Process JSON property data
                for prop in json_properties:
                    try:
                        property_data = {
                            'title': prop.get('name', 'N/A'),
                            'price': prop.get('offers', {}).get('price', 'N/A'),
                            'price_value': float(prop.get('offers', {}).get('price', 0)),
                            'location': prop.get('address', {}).get('addressLocality', 'N/A'),
                            'bedrooms': prop.get('numberOfRooms', 'N/A'),
                            'bathrooms': prop.get('numberOfBathroomsTotal', 'N/A'),
                            'area': f"{prop.get('floorSize', {}).get('value', 'N/A')} {prop.get('floorSize', {}).get('unitText', 'sq.ft')}",
                            'area_sqft': float(prop.get('floorSize', {}).get('value', 0)),
                            'property_type': prop.get('category', 'Other'),
                            'link': prop.get('url', 'N/A'),
                            'agent_name': prop.get('seller', {}).get('name', 'N/A')
                        }
                        
                        # Calculate price per sqft
                        if property_data['price_value'] > 0 and property_data['area_sqft'] > 0:
                            property_data['price_per_sqft'] = round(property_data['price_value'] / property_data['area_sqft'], 2)
                        else:
                            property_data['price_per_sqft'] = 0
                            
                        all_properties.append(property_data)
                    except Exception as e:
                        st.error(f"Error processing JSON property data: {e}")
            else:
                # Fallback to HTML scraping
                property_elements = soup.select('.property-card') or soup.select('.card-list__item')
                
                if not property_elements:
                    st.warning(f"No property listings found on page {page} for '{query}'. The website structure may have changed.")
                    break
                
                for property_element in property_elements:
                    details = self.extract_property_details(property_element)
                    if details:
                        all_properties.append(details)
            
            # If we've scraped all available properties, break
            if total_results and len(all_properties) >= total_results:
                break
            
            # Add a small delay to avoid overloading the server
            time.sleep(random.uniform(1, 3))
        
        if progress_bar:
            progress_bar.progress(1.0)
            
        return all_properties, total_results
    
    def analyze_data(self, properties_data):
        """Analyze the property data"""
        if not properties_data:
            return None
        
        df = pd.DataFrame(properties_data)
        
        # Basic statistics
        stats = {
            'total_listings': len(df),
            'avg_price': df['price_value'].mean() if len(df) > 0 else 0,
            'min_price': df['price_value'].min() if len(df) > 0 else 0,
            'max_price': df['price_value'].max() if len(df) > 0 else 0,
            'median_price': df['price_value'].median() if len(df) > 0 else 0,
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
            sns.histplot(df['price_value'], kde=True, ax=ax_price)
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
            # Convert bedrooms to categories with a specific order
            bedroom_order = ['Studio', '1', '2', '3', '4', '5+']
            
            # Filter and count values
            bedroom_values = df['bedrooms'].astype(str).replace('N/A', pd.NA).dropna()
            bedroom_counts = bedroom_values.value_counts().reindex(bedroom_order, fill_value=0)
            
            if len(bedroom_counts) > 1:
                fig_bed, ax_bed = plt.subplots(figsize=(10, 5))
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
                df_filtered = df[df['price_per_sqft'] > 0]  # Filter out zeros
                if len(df_filtered) > 0:
                    fig_sqft, ax_sqft = plt.subplots(figsize=(10, 5))
                    sns.histplot(df_filtered['price_per_sqft'], kde=True, ax=ax_sqft)
                    ax_sqft.set_title(f'Price per Sq.Ft Distribution for {query}')
                    ax_sqft.set_xlabel('Price per Sq.Ft (AED)')
                    ax_sqft.set_ylabel('Count')
                    plt.tight_layout()
                    figures['price_per_sqft'] = fig_sqft
        except Exception as e:
            st.error(f"Error generating price per sqft chart: {e}")
        
        # Agent distribution
        try:
            if 'agent_name' in df.columns and len(df['agent_name'].unique()) > 1:
                # Get top 10 agents
                top_agents = df['agent_name'].value_counts().head(10)
                if len(top_agents) > 1:
                    fig_agent, ax_agent = plt.subplots(figsize=(10, 5))
                    top_agents.plot(kind='bar', ax=ax_agent)
                    ax_agent.set_title(f'Top Agents for {query}')
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
    
    with st.expander("About This Tool", expanded=True):
        st.markdown("""
        This application searches Property Finder for real estate listings and provides analytics including:
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
            min_price = st.number_input("Minimum Price (AED)", value=0, min_value=0, step=100000)
            bedrooms = st.selectbox("Bedrooms", ["Any", "Studio", "1", "2", "3", "4", "5+"])
        
        with col2:
            property_type = st.selectbox("Property Type", ["Any", "Apartment", "Villa", "Townhouse", "Penthouse", "Duplex"])
            max_price = st.number_input("Maximum Price (AED)", value=0, min_value=0, step=100000)
            max_pages = st.slider("Maximum Pages to Fetch", min_value=1, max_value=10, value=3, 
                                help="Each page contains about 25 properties. Increasing this will fetch more properties but may take longer.")
        
        search_button = st.form_submit_button("Search Properties", type="primary")
    
    # Clean up inputs
    if min_price == 0:
        min_price = None
    if max_price == 0:
        max_price = None
    
    # Execute search when button is clicked
    if search_button and query:
        with st.spinner(f"Searching for properties matching '{query}'..."):
            st.subheader(f"Analyzing Properties: {query}")
            progress_bar = st.progress(0)
            
            # Initialize scraper and get properties
            scraper = PropertyFinderScraper()
            properties, total_available = scraper.scrape_properties(
                query, property_type, min_price, max_price, bedrooms, max_pages, progress_bar
            )
            
            if properties:
                st.success(f"Found {len(properties)} listings" + (f" out of approximately {total_available} total available" if total_available else ""))
                
                # Save data
                csv_filename, csv_filepath = scraper.save_results(properties, query)
                
                # Analyze data
                analysis = scraper.analyze_data(properties)
                
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
                    if analysis['property_type_counts']:
                        st.write(pd.DataFrame({
                            'Property Type': list(analysis['property_type_counts'].keys()),
                            'Count': list(analysis['property_type_counts'].values())
                        }).sort_values('Count', ascending=False))
                    else:
                        st.info("No property type data available.")
                    
                    # Display bedroom breakdown
                    st.subheader("Bedroom Distribution")
                    if analysis['bedroom_counts']:
                        # Create a DataFrame with formatted index for better display
                        bedroom_df = pd.DataFrame({
                            'Bedrooms': list(analysis['bedroom_counts'].keys()),
                            'Count': list(analysis['bedroom_counts'].values())
                        })
                        st.write(bedroom_df)
                    else:
                        st.info("No bedroom data available.")
                    
                    # Display top agents
                    st.subheader("Top Agents")
                    if analysis['top_agents']:
                        st.write(pd.DataFrame({
                            'Agent': list(analysis['top_agents'].keys()),
                            'Number of Listings': list(analysis['top_agents'].values())
                        }))
                    else:
                        st.info("No agent data available.")
                    
                    # Generate and display visualizations
                    figures = scraper.generate_visualizations(analysis, query)
                    
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
                    display_cols = ['title', 'price', 'price_value', 'area', 'area_sqft', 'price_per_sqft', 
                                    'bedrooms', 'bathrooms', 'property_type', 'location', 'agent_name', 'link']
                    
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
