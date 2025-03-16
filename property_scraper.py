import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
import random
import re
from datetime import datetime
from urllib.parse import quote

# Page configuration
st.set_page_config(
    page_title="Property Finder Data Exporter",
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            'Pragma': 'no-cache'
        }
        self.base_url = "https://www.propertyfinder.ae"
        self.results_dir = RESULTS_DIR

    def search_properties(self, search_term, property_type=None, min_price=None, max_price=None, bedrooms=None, max_pages=3, progress_bar=None):
        """Search properties on Property Finder"""
        all_properties = []
        
        for page in range(1, max_pages + 1):
            if progress_bar:
                progress_bar.progress((page - 1) / max_pages)
                
            # Build the search URL
            search_url = self._build_search_url(search_term, property_type, min_price, max_price, bedrooms, page)
            
            # Fetch and parse the page
            soup = self._fetch_page(search_url)
            if not soup:
                continue
                
            # Extract total count if first page
            if page == 1:
                total_count = self._extract_total_count(soup)
                if total_count == 0:
                    st.warning(f"No properties found for '{search_term}'")
                    break
            
            # Extract properties
            page_properties = self._extract_properties(soup, search_term)
            
            if not page_properties:
                st.warning(f"No properties found on page {page} for '{search_term}'")
                break
                
            all_properties.extend(page_properties)
            
            # Delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
        
        if progress_bar:
            progress_bar.progress(1.0)
            
        return all_properties
    
    def _build_search_url(self, search_term, property_type=None, min_price=None, max_price=None, bedrooms=None, page=1):
        """Build search URL with parameters"""
        search_query = quote(search_term)
        url = f"{self.base_url}/en/search?q={search_query}&page={page}"
        
        if property_type and property_type != "Any":
            property_type_code = self._get_property_type_code(property_type)
            url += f"&c={property_type_code}"
            
        if min_price:
            url += f"&pf={min_price}"
            
        if max_price:
            url += f"&pt={max_price}"
            
        if bedrooms and bedrooms != "Any":
            if bedrooms == "Studio":
                bed_value = "0"
            elif bedrooms == "5+":
                bed_value = "5"
            else:
                bed_value = bedrooms
            url += f"&bf={bed_value}&bt={bed_value}"
        
        return url
    
    def _get_property_type_code(self, property_type):
        """Convert property type to Property Finder category code"""
        codes = {
            "Apartment": "1",
            "Villa": "2",
            "Townhouse": "16",
            "Penthouse": "4",
            "Duplex": "8"
        }
        return codes.get(property_type, "0")
    
    def _fetch_page(self, url):
        """Fetch and parse a page with retry mechanism"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Add random delays between retries
                if retry_count > 0:
                    time.sleep(random.uniform(2, 5))
                
                response = requests.get(
                    url, 
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return BeautifulSoup(response.text, 'html.parser')
                elif response.status_code == 403:
                    st.error("Access denied by Property Finder. Try again later.")
                    return None
                else:
                    st.warning(f"Received status code {response.status_code} when fetching {url}")
                    retry_count += 1
            except Exception as e:
                st.error(f"Error fetching {url}: {e}")
                retry_count += 1
        
        return None
    
    def _extract_total_count(self, soup):
        """Extract total number of properties found"""
        try:
            count_element = soup.select_one('.search-results__header') or soup.select_one('.search-title')
            if count_element:
                text = count_element.text.strip()
                count_match = re.search(r'(\d+)', text)
                if count_match:
                    return int(count_match.group(1))
            return 0
        except Exception as e:
            st.error(f"Error extracting property count: {e}")
            return 0
    
    def _extract_properties(self, soup, search_term):
        """Extract property details from search results page"""
        properties = []
        
        # Try multiple selectors to find property cards
        property_cards = soup.select('.property-card') or soup.select('.card-list__item') or soup.select('.search-results__list .card')
        
        if not property_cards:
            # Try to find any embedded property JSON data
            json_data = self._extract_json_data(soup)
            if json_data:
                return json_data
            
            # If no cards or JSON found, try to see if there's a different layout
            alternate_cards = soup.select('[data-testid="property-card"]') or soup.select('.search-results-list-item')
            if alternate_cards:
                property_cards = alternate_cards
            else:
                st.error("Could not find property listings on the page. The website structure may have changed.")
                st.write("Please try a different search term or check the Property Finder website directly.")
                return []
        
        for card in property_cards:
            try:
                property_data = {}
                
                # Extract title
                title_element = (
                    card.select_one('.property-card__title') or 
                    card.select_one('.card-list__item-property-title') or
                    card.select_one('h2') or
                    card.select_one('[data-testid="property-card-title"]')
                )
                property_data['title'] = title_element.text.strip() if title_element else "N/A"
                
                # Extract project name from title or separate element
                property_data['project'] = self._extract_project_name(property_data['title'], search_term)
                
                # Extract price
                price_element = (
                    card.select_one('.property-card__price') or 
                    card.select_one('.card-list__item-property-price') or
                    card.select_one('[data-testid="property-card-price"]')
                )
                price_text = price_element.text.strip() if price_element else "N/A"
                property_data['price_display'] = price_text
                property_data['price'] = self._extract_number(price_text)
                
                # Extract location
                location_element = (
                    card.select_one('.property-card__location') or 
                    card.select_one('.card-list__item-property-location') or
                    card.select_one('[data-testid="property-card-location"]')
                )
                property_data['location'] = location_element.text.strip() if location_element else "N/A"
                
                # Extract details (beds, baths, size)
                property_data.update(self._extract_property_details(card))
                
                # Extract agent name
                agent_element = (
                    card.select_one('.property-card__agent') or 
                    card.select_one('.card-list__item-agent-name') or
                    card.select_one('[data-testid="property-card-agent"]')
                )
                property_data['agent_name'] = agent_element.text.strip() if agent_element else "N/A"
                
                # Extract URL
                link_element = card.select_one('a')
                if link_element and 'href' in link_element.attrs:
                    href = link_element['href']
                    property_data['url'] = self.base_url + href if not href.startswith('http') else href
                else:
                    property_data['url'] = "N/A"
                
                # Calculate price per sqft if possible
                if property_data['price'] > 0 and property_data['area_sqft'] > 0:
                    property_data['price_per_sqft'] = round(property_data['price'] / property_data['area_sqft'], 2)
                else:
                    property_data['price_per_sqft'] = 0
                
                properties.append(property_data)
            except Exception as e:
                st.error(f"Error extracting property details: {e}")
                continue
        
        return properties
    
    def _extract_property_details(self, card):
        """Extract bedrooms, bathrooms and area details"""
        details = {
            'bedrooms': 'N/A',
            'bathrooms': 'N/A',
            'area': 'N/A',
            'area_sqft': 0
        }
        
        # Try different selectors for property details
        details_container = (
            card.select_one('.property-card__facts') or 
            card.select_one('.card-list__item-property-features') or
            card.select_one('[data-testid="property-card-details"]')
        )
        
        if details_container:
            # Try to find list items or spans containing details
            detail_items = details_container.select('li') or details_container.select('span')
            
            for i, item in enumerate(detail_items):
                text = item.text.strip()
                
                if i == 0 or 'bed' in text.lower():
                    details['bedrooms'] = 'Studio' if 'studio' in text.lower() else text
                elif i == 1 or 'bath' in text.lower():
                    details['bathrooms'] = text
                elif i == 2 or 'sq' in text.lower():
                    details['area'] = text
                    details['area_sqft'] = self._extract_area(text)
        
        return details
    
    def _extract_json_data(self, soup):
        """Try to extract property data from embedded JSON"""
        try:
            script_tags = soup.find_all('script', {'type': 'application/ld+json'})
            properties = []
            
            for script in script_tags:
                try:
                    import json
                    data = json.loads(script.string)
                    
                    # Check if this is property listing data
                    if '@type' in data and data['@type'] in ['Property', 'PropertyListing', 'Product']:
                        property_data = {
                            'title': data.get('name', 'N/A'),
                            'project': self._extract_project_name(data.get('name', ''), ''),
                            'price_display': f"{data.get('price', 'N/A')} {data.get('priceCurrency', 'AED')}",
                            'price': float(data.get('price', 0)),
                            'location': data.get('address', {}).get('addressLocality', 'N/A'),
                            'bedrooms': str(data.get('numberOfRooms', 'N/A')),
                            'bathrooms': str(data.get('numberOfBathrooms', 'N/A')),
                            'area': f"{data.get('floorSize', {}).get('value', 'N/A')} {data.get('floorSize', {}).get('unitCode', 'sq.ft')}",
                            'area_sqft': float(data.get('floorSize', {}).get('value', 0)),
                            'agent_name': data.get('seller', {}).get('name', 'N/A'),
                            'url': data.get('url', 'N/A')
                        }
                        
                        # Calculate price per sqft
                        if property_data['price'] > 0 and property_data['area_sqft'] > 0:
                            property_data['price_per_sqft'] = round(property_data['price'] / property_data['area_sqft'], 2)
                        else:
                            property_data['price_per_sqft'] = 0
                            
                        properties.append(property_data)
                except:
                    continue
            
            return properties
        except Exception as e:
            st.error(f"Error extracting JSON data: {e}")
            return []
    
    def _extract_project_name(self, title, search_term):
        """Extract project name from title"""
        # First try to find exact matches for common project names
        common_projects = ["Damac Safa One", "Damac Safa Two", "Safa One", "Safa Two"]
        for project in common_projects:
            if project.lower() in title.lower():
                return project
        
        # If search term contains project name, use that
        if search_term and any(term in title.lower() for term in search_term.lower().split()):
            return search_term
            
        # Fallback to generic extraction
        title_parts = title.split(',')
        if len(title_parts) > 1:
            return title_parts[0].strip()
        else:
            return "Unknown Project"
    
    def _extract_number(self, text):
        """Extract numeric value from text"""
        try:
            # Remove commas and find all digits
            numbers = re.findall(r'[\d,]+', text.replace(',', ''))
            if numbers:
                return float(numbers[0])
            return 0
        except:
            return 0
    
    def _extract_area(self, text):
        """Extract area in sq.ft from text"""
        try:
            # Find numeric value
            area_match = re.search(r'([\d,\.]+)', text.replace(',', ''))
            if not area_match:
                return 0
                
            area_value = float(area_match.group(1))
            
            # Check unit and convert if necessary
            if 'm²' in text.lower() or 'sqm' in text.lower():
                # Convert from sq.m to sq.ft
                area_value *= 10.764
                
            return area_value
        except:
            return 0
    
    def save_to_csv(self, properties, search_term):
        """Save property data to CSV file"""
        if not properties:
            return None
            
        # Create DataFrame
        df = pd.DataFrame(properties)
        
        # Format filename
        filename = f"{search_term.replace(' ', '_').lower()}_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.results_dir, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        
        return filename, filepath
    
    def analyze_data(self, properties):
        """Analyze property data"""
        if not properties:
            return None
            
        df = pd.DataFrame(properties)
        
        # Basic statistics
        stats = {
            'total_listings': len(df),
            'avg_price': df['price'].mean() if 'price' in df.columns else 0,
            'min_price': df['price'].min() if 'price' in df.columns else 0,
            'max_price': df['price'].max() if 'price' in df.columns else 0,
            'median_price': df['price'].median() if 'price' in df.columns else 0
        }
        
        # Calculate price per sqft stats if available
        if 'price_per_sqft' in df.columns:
            stats['avg_price_per_sqft'] = df[df['price_per_sqft'] > 0]['price_per_sqft'].mean()
            stats['min_price_per_sqft'] = df[df['price_per_sqft'] > 0]['price_per_sqft'].min()
            stats['max_price_per_sqft'] = df[df['price_per_sqft'] > 0]['price_per_sqft'].max()
        
        # Property type breakdown
        if 'property_type' in df.columns:
            property_types = df['property_type'].value_counts().to_dict()
        else:
            property_types = {}
            
        # Bedroom breakdown
        if 'bedrooms' in df.columns:
            bedroom_counts = df['bedrooms'].value_counts().to_dict()
        else:
            bedroom_counts = {}
            
        # Agent breakdown
        if 'agent_name' in df.columns:
            agent_counts = df['agent_name'].value_counts().to_dict()
            top_agents = {k: agent_counts[k] for k in list(agent_counts.keys())[:5]} if agent_counts else {}
        else:
            agent_counts = {}
            top_agents = {}
            
        # Project breakdown
        if 'project' in df.columns:
            project_counts = df['project'].value_counts().to_dict()
        else:
            project_counts = {}
        
        return {
            'dataframe': df,
            'stats': stats,
            'property_types': property_types,
            'bedroom_counts': bedroom_counts,
            'agent_counts': agent_counts,
            'top_agents': top_agents,
            'project_counts': project_counts
        }
    
    def generate_visualizations(self, analysis, search_term):
        """Generate data visualizations"""
        if not analysis or 'dataframe' not in analysis or analysis['dataframe'].empty:
            return {}
            
        df = analysis['dataframe']
        figures = {}
        
        # Set style
        sns.set(style="whitegrid")
        
        # Price distribution
        try:
            if 'price' in df.columns and df['price'].sum() > 0:
                fig_price, ax_price = plt.subplots(figsize=(10, 5))
                sns.histplot(df['price'], kde=True, ax=ax_price)
                ax_price.set_title(f'Price Distribution for {search_term}')
                ax_price.set_xlabel('Price (AED)')
                ax_price.set_ylabel('Count')
                plt.tight_layout()
                figures['price'] = fig_price
        except Exception as e:
            st.error(f"Error generating price chart: {e}")
        
        # Price per sqft distribution
        try:
            if 'price_per_sqft' in df.columns and df['price_per_sqft'].sum() > 0:
                df_filtered = df[df['price_per_sqft'] > 0]  # Filter out zeros
                if len(df_filtered) > 0:
                    fig_sqft, ax_sqft = plt.subplots(figsize=(10, 5))
                    sns.histplot(df_filtered['price_per_sqft'], kde=True, ax=ax_sqft)
                    ax_sqft.set_title(f'Price per Sq.Ft Distribution for {search_term}')
                    ax_sqft.set_xlabel('Price per Sq.Ft (AED)')
                    ax_sqft.set_ylabel('Count')
                    plt.tight_layout()
                    figures['price_per_sqft'] = fig_sqft
        except Exception as e:
            st.error(f"Error generating price per sqft chart: {e}")
        
        # Project breakdown
        try:
            if 'project' in df.columns and len(df['project'].unique()) > 1:
                fig_project, ax_project = plt.subplots(figsize=(10, 5))
                project_counts = df['project'].value_counts()
                project_counts.plot(kind='bar', ax=ax_project)
                ax_project.set_title(f'Projects for {search_term}')
                ax_project.set_xlabel('Project')
                ax_project.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['projects'] = fig_project
        except Exception as e:
            st.error(f"Error generating project chart: {e}")
        
        # Bedroom breakdown
        try:
            if 'bedrooms' in df.columns and len(df['bedrooms'].unique()) > 1:
                fig_bed, ax_bed = plt.subplots(figsize=(10, 5))
                bedroom_counts = df['bedrooms'].value_counts()
                bedroom_counts.plot(kind='bar', ax=ax_bed)
                ax_bed.set_title(f'Bedroom Distribution for {search_term}')
                ax_bed.set_xlabel('Bedrooms')
                ax_bed.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['bedrooms'] = fig_bed
        except Exception as e:
            st.error(f"Error generating bedroom chart: {e}")
            
        # Agent breakdown
        try:
            if 'agent_name' in df.columns and len(df['agent_name'].unique()) > 1:
                fig_agent, ax_agent = plt.subplots(figsize=(10, 5))
                agent_counts = df['agent_name'].value_counts().head(10)  # Top 10 agents
                agent_counts.plot(kind='bar', ax=ax_agent)
                ax_agent.set_title(f'Top Agents for {search_term}')
                ax_agent.set_xlabel('Agent')
                ax_agent.set_ylabel('Number of Listings')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['agents'] = fig_agent
        except Exception as e:
            st.error(f"Error generating agent chart: {e}")
            
        return figures

# Main Streamlit App
def main():
    st.title("Property Finder Data Exporter")
    st.markdown("### Search and analyze properties from Property Finder")
    
    with st.expander("About This Tool", expanded=False):
        st.markdown("""
        This tool searches Property Finder for properties and exports the data for analysis. Enter a search term such as:
        - Property name (e.g., "Damac Safa Two")
        - Location (e.g., "Business Bay")
        - Developer (e.g., "Emaar")
        
        The tool will search Property Finder and extract available property data, saving it to CSV and generating analytics.
        """)
    
    # Search form
    with st.form("search_form"):
        st.subheader("Search Properties")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("Search Term (Project, Area, or Developer)", "Damac Safa Two")
            property_type = st.selectbox("Property Type", ["Any", "Apartment", "Villa", "Townhouse", "Penthouse", "Duplex"])
            
        with col2:
            min_price = st.number_input("Minimum Price (AED)", value=0, step=100000)
            max_price = st.number_input("Maximum Price (AED)", value=0, step=100000)
            bedrooms = st.selectbox("Bedrooms", ["Any", "Studio", "1", "2", "3", "4", "5+"])
            
        max_pages = st.slider("Maximum Pages to Search", min_value=1, max_value=10, value=3, 
                             help="Each page contains about 25 properties. Increasing this will find more properties but takes longer.")
        
        submit_button = st.form_submit_button("Search Properties")
    
    if submit_button:
        scraper = PropertyFinderScraper()
        
        with st.spinner(f"Searching for properties matching '{search_term}'..."):
            # Initialize progress bar
            progress_bar = st.progress(0)
            
            # Search for properties
            properties = scraper.search_properties(
                search_term, 
                property_type, 
                min_price if min_price > 0 else None, 
                max_price if max_price > 0 else None, 
                bedrooms, 
                max_pages, 
                progress_bar
            )
            
            if properties:
                st.success(f"Found {len(properties)} properties matching '{search_term}'")
                
                # Save to CSV
                csv_filename, csv_filepath = scraper.save_to_csv(properties, search_term)
                
                # Analyze data
                st.subheader("Property Analysis")
                analysis = scraper.analyze_data(properties)
                
                if analysis:
                    # Display summary statistics
                    st.write("### Summary Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Listings", analysis['stats']['total_listings'])
                    
                    with col2:
                        st.metric("Average Price", f"AED {analysis['stats']['avg_price']:,.2f}")
                    
                    with col3:
                        st.metric("Price Range", f"AED {analysis['stats']['min_price']:,.2f} - {analysis['stats']['max_price']:,.2f}")
                    
                    with col4:
                        if 'avg_price_per_sqft' in analysis['stats']:
                            st.metric("Avg Price/Sq.Ft", f"AED {analysis['stats']['avg_price_per_sqft']:,.2f}")
                        else:
                            st.metric("Avg Price/Sq.Ft", "N/A")
                    
                    # Generate visualizations
                    visualizations = scraper.generate_visualizations(analysis, search_term)
                    
                    if visualizations:
                        st.write("### Visualizations")
                        
                        # Use two columns for charts
                        for i in range(0, len(visualizations), 2):
                            cols = st.columns(2)
                            
                            # First chart
                            vis_keys = list(visualizations.keys())
                            if i < len(vis_keys):
                                with cols[0]:
                                    key1 = vis_keys[i]
                                    st.pyplot(visualizations[key1])
                            
                            # Second chart
                            if i + 1 < len(vis_keys):
                                with cols[1]:
                                    key2 = vis_keys[i + 1]
                                    st.pyplot(visualizations[key2])
                    
                    # Display project breakdown if available
                    if analysis['project_counts']:
                        st.write("### Projects")
                        project_df = pd.DataFrame({
                            'Project': list(analysis['project_counts'].keys()),
                            'Count': list(analysis['project_counts'].values())
                        }).sort_values('Count', ascending=False)
                        st.dataframe(project_df)
                    
                    # Display property data
                    st.write("### Property Listings")
                    st.dataframe(analysis['dataframe'])
                    
                    # Provide download link
                    with open(csv_filepath, "rb") as file:
                        st.download_button(
                            label="Download Data as CSV",
                            data=file,
                            file_name=csv_filename,
                            mime="text/csv"
                        )
                        
                    # Allow exporting specific projects
                    if 'project' in analysis['dataframe'].columns and len(analysis['dataframe']['project'].unique()) > 1:
                        st.write("### Export Specific Project")
                        project_to_export = st.selectbox("Select Project to Export", 
                                                       ["All"] + sorted(analysis['dataframe']['project'].unique().tolist()))
                        
                        if project_to_export != "All":
                            project_df = analysis['dataframe'][analysis['dataframe']['project'] == project_to_export]
                            project_csv = f"{project_to_export.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                            
                            st.download_button(
                                label=f"Download {project_to_export} Data",
                                data=project_df.to_csv(index=False).encode('utf-8'),
                                file_name=project_csv,
                                mime="text/csv"
                            )
            else:
                st.error(f"No properties found matching '{search_term}'. Try a different search term or check directly on Property Finder.")
                st.info("Property Finder may be blocking automated search requests. Try searching on the Property Finder website directly.")

if __name__ == "__main__":
    main()
