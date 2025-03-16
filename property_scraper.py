import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Damac Safa Property Analysis",
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
            'Upgrade-Insecure-Requests': '1'
        }
        self.base_url = "https://www.propertyfinder.ae"
        self.results_dir = RESULTS_DIR
    
    def get_search_url(self, project_name, page=1):
        """Generate search URL for a specific project"""
        # Format the project name for URL (replace spaces with hyphens and lowercase)
        formatted_name = project_name.lower().replace(" ", "-")
        return f"{self.base_url}/en/search?c=1&l=1&ob=nd&page={page}&q={formatted_name}"
    
    def fetch_page(self, url):
        """Fetch and parse a page"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_property_details(self, property_element):
        """Extract details from a property listing element"""
        try:
            # Extract price
            price_element = property_element.select_one('.property-price')
            price = price_element.text.strip() if price_element else "N/A"
            price_value = self.clean_price(price)
            
            # Extract property type and bedrooms
            property_facts = property_element.select_one('.property-facts')
            bedrooms = "N/A"
            property_type = "N/A"
            if property_facts:
                facts = property_facts.text.strip().split('\n')
                facts = [f.strip() for f in facts if f.strip()]
                if len(facts) >= 1:
                    bedrooms = facts[0]
                if len(facts) >= 2:
                    property_type = facts[1]
            
            # Extract location
            location_element = property_element.select_one('.property-location')
            location = location_element.text.strip() if location_element else "N/A"
            
            # Extract title/description
            title_element = property_element.select_one('.property-title')
            title = title_element.text.strip() if title_element else "N/A"
            
            # Extract link
            link_element = property_element.select_one('a.property-link')
            link = self.base_url + link_element['href'] if link_element and 'href' in link_element.attrs else "N/A"
            
            return {
                'title': title,
                'price': price,
                'price_value': price_value,
                'bedrooms': bedrooms,
                'property_type': property_type,
                'location': location,
                'link': link
            }
        except Exception as e:
            st.warning(f"Error extracting property details: {e}")
            return {}
    
    def clean_price(self, price_text):
        """Convert price text to numeric value"""
        try:
            # Remove currency symbol, commas, and convert to float
            price_digits = ''.join(c for c in price_text if c.isdigit() or c == '.')
            if price_digits:
                return float(price_digits)
            return 0
        except:
            return 0
    
    def scrape_project(self, project_name, max_pages=3, progress_bar=None):
        """Scrape all properties for a specific project"""
        all_properties = []
        
        for page in range(1, max_pages + 1):
            if progress_bar:
                progress_bar.progress((page - 1) / max_pages)
                
            url = self.get_search_url(project_name, page)
            soup = self.fetch_page(url)
            
            if not soup:
                continue
            
            # Check if we've reached the end of results
            no_results = soup.select_one('.no-results-found')
            if no_results or "No results found" in soup.text:
                if page == 1:
                    st.info(f"No results found for {project_name}")
                else:
                    st.info(f"Reached end of results for {project_name} at page {page}")
                break
            
            # Extract property listings
            property_listings = soup.select('.property-card')
            
            if not property_listings:
                st.info(f"No property listings found on page {page} for {project_name}")
                break
            
            for property_element in property_listings:
                details = self.extract_property_details(property_element)
                if details:
                    details['project'] = project_name
                    all_properties.append(details)
            
            # Add a small delay to avoid overloading the server
            time.sleep(random.uniform(0.5, 1.5))
        
        if progress_bar:
            progress_bar.progress(1.0)
            
        return all_properties
    
    def analyze_data(self, properties_data):
        """Analyze the scraped property data"""
        if not properties_data:
            return None
        
        df = pd.DataFrame(properties_data)
        
        # Basic statistics
        stats = {
            'total_listings': len(df),
            'avg_price': df['price_value'].mean() if len(df) > 0 else 0,
            'min_price': df['price_value'].min() if len(df) > 0 else 0,
            'max_price': df['price_value'].max() if len(df) > 0 else 0,
            'median_price': df['price_value'].median() if len(df) > 0 else 0
        }
        
        # Count by property type
        property_type_counts = df['property_type'].value_counts().to_dict() if len(df) > 0 else {}
        
        # Count by bedroom
        bedroom_counts = df['bedrooms'].value_counts().to_dict() if len(df) > 0 else {}
        
        return {
            'dataframe': df,
            'stats': stats,
            'property_type_counts': property_type_counts,
            'bedroom_counts': bedroom_counts
        }
    
    def generate_visualizations(self, analysis_results, project_name):
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
            ax_price.set_title(f'Price Distribution for {project_name}')
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
                ax_type.set_title(f'Property Types for {project_name}')
                ax_type.set_xlabel('Property Type')
                ax_type.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['property_types'] = fig_type
        except Exception as e:
            st.error(f"Error generating property type chart: {e}")
        
        # Bedroom distribution
        try:
            if len(df['bedrooms'].unique()) > 1:
                fig_bed, ax_bed = plt.subplots(figsize=(10, 5))
                bedroom_counts = df['bedrooms'].value_counts()
                bedroom_counts.plot(kind='bar', ax=ax_bed)
                ax_bed.set_title(f'Bedroom Distribution for {project_name}')
                ax_bed.set_xlabel('Bedrooms')
                ax_bed.set_ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                figures['bedrooms'] = fig_bed
        except Exception as e:
            st.error(f"Error generating bedroom chart: {e}")
        
        return figures
    
    def save_results(self, properties_data, project_name):
        """Save the scraped data to a CSV file"""
        if not properties_data:
            return None
        
        df = pd.DataFrame(properties_data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{project_name}_properties_{timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)
        df.to_csv(filepath, index=False)
        
        return filename, filepath

# Streamlit app
def main():
    st.title("Damac Safa Property Analysis")
    st.markdown("### Check inventory and prices for Damac Safa One and Safa Two on Property Finder")
    
    with st.expander("About This Tool", expanded=True):
        st.markdown("""
        This application scrapes property listings for Damac Safa One and Safa Two from Property Finder and provides analysis of:
        - Total available inventory (number of listings)
        - Price statistics (average, minimum, maximum, median)
        - Breakdown by property type
        - Breakdown by number of bedrooms
        - Visualizations of key data points
        
        The data is updated each time you run the analysis.
        """)
    
    # Project selection
    st.subheader("Select Projects to Analyze")
    col1, col2 = st.columns(2)
    with col1:
        analyze_safa_one = st.checkbox("Damac Safa One", value=True)
    with col2:
        analyze_safa_two = st.checkbox("Damac Safa Two", value=True)
    
    projects = []
    if analyze_safa_one:
        projects.append("Damac Safa One")
    if analyze_safa_two:
        projects.append("Damac Safa Two")
    
    # Start analysis button
    if st.button("Start Analysis", type="primary"):
        if not projects:
            st.warning("Please select at least one project to analyze.")
        else:
            scraper = PropertyFinderScraper()
            
            all_results = {}
            
            for project in projects:
                with st.spinner(f"Scraping data for {project}..."):
                    st.subheader(f"Analyzing {project}")
                    progress_bar = st.progress(0)
                    
                    # Scrape data
                    properties = scraper.scrape_project(project, progress_bar=progress_bar)
                    
                    if properties:
                        st.success(f"Found {len(properties)} listings for {project}")
                        
                        # Save data
                        csv_filename, csv_filepath = scraper.save_results(properties, project)
                        
                        # Analyze data
                        analysis = scraper.analyze_data(properties)
                        
                        if analysis:
                            # Display summary statistics
                            st.subheader("Summary Statistics")
                            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                            with stats_col1:
                                st.metric("Total Listings", analysis['stats']['total_listings'])
                            with stats_col2:
                                st.metric("Average Price", f"AED {analysis['stats']['avg_price']:,.2f}")
                            with stats_col3:
                                st.metric("Minimum Price", f"AED {analysis['stats']['min_price']:,.2f}")
                            with stats_col4:
                                st.metric("Maximum Price", f"AED {analysis['stats']['max_price']:,.2f}")
                            
                            # Generate and display visualizations
                            figures = scraper.generate_visualizations(analysis, project)
                            
                            if figures:
                                st.subheader("Visualizations")
                                viz_cols = st.columns(len(figures))
                                
                                for i, (viz_type, fig) in enumerate(figures.items()):
                                    with viz_cols[i]:
                                        st.pyplot(fig)
                            
                            # Display property data table
                            st.subheader("Property Listings")
                            st.dataframe(analysis['dataframe'])
                            
                            # Provide download link
                            with open(csv_filepath, "rb") as file:
                                st.download_button(
                                    label=f"Download {project} Data",
                                    data=file,
                                    file_name=csv_filename,
                                    mime="text/csv",
                                )
                            
                            # Store results for comparison
                            all_results[project] = analysis
                    else:
                        st.error(f"No data found for {project}")
            
            # Compare projects if we have multiple
            if len(all_results) > 1:
                st.header("Projects Comparison")
                comparison_data = {}
                
                for project, analysis in all_results.items():
                    comparison_data[project] = {
                        "Total Listings": analysis['stats']['total_listings'],
                        "Average Price (AED)": analysis['stats']['avg_price'],
                        "Median Price (AED)": analysis['stats']['median_price'],
                    }
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df)

if __name__ == "__main__":
    main()
