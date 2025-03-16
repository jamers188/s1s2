import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import json

# Page configuration
st.set_page_config(
    page_title="Property Data Collector",
    page_icon="🏢",
    layout="wide"
)

# Create a directory for results
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Helper functions
def load_data():
    """Load existing property data or create empty DataFrame"""
    try:
        if os.path.exists(os.path.join(RESULTS_DIR, "property_data.csv")):
            return pd.read_csv(os.path.join(RESULTS_DIR, "property_data.csv"))
        else:
            return pd.DataFrame(columns=[
                'project', 'property_type', 'price', 'area_sqft', 'bedrooms', 
                'bathrooms', 'location', 'agent_name', 'property_url', 'entry_date'
            ])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=[
            'project', 'property_type', 'price', 'area_sqft', 'bedrooms', 
            'bathrooms', 'location', 'agent_name', 'property_url', 'entry_date'
        ])

def save_data(df):
    """Save property data to CSV"""
    try:
        df.to_csv(os.path.join(RESULTS_DIR, "property_data.csv"), index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def analyze_data(df, project_filter=None):
    """Analyze the property data"""
    if df.empty:
        return None
    
    # Apply project filter if specified
    if project_filter:
        df = df[df['project'] == project_filter]
        
    if df.empty:
        return None
    
    # Convert price and area to numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['area_sqft'] = pd.to_numeric(df['area_sqft'], errors='coerce')
    
    # Calculate price per sqft
    df['price_per_sqft'] = df['price'] / df['area_sqft']
    
    # Basic statistics
    stats = {
        'total_listings': len(df),
        'avg_price': df['price'].mean(),
        'min_price': df['price'].min(),
        'max_price': df['price'].max(),
        'median_price': df['price'].median(),
        'avg_price_per_sqft': df['price_per_sqft'].mean(),
        'min_price_per_sqft': df['price_per_sqft'].min(),
        'max_price_per_sqft': df['price_per_sqft'].max(),
    }
    
    # Count by property type
    property_type_counts = df['property_type'].value_counts().to_dict()
    
    # Count by bedroom
    bedroom_counts = df['bedrooms'].value_counts().to_dict()
    
    # Count by agent
    agent_counts = df['agent_name'].value_counts().to_dict()
    
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

def generate_visualizations(analysis_results, project_name):
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
            bedroom_counts = df['bedrooms'].value_counts().sort_index()
            bedroom_counts.plot(kind='bar', ax=ax_bed)
            ax_bed.set_title(f'Bedroom Distribution for {project_name}')
            ax_bed.set_xlabel('Bedrooms')
            ax_bed.set_ylabel('Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            figures['bedrooms'] = fig_bed
    except Exception as e:
        st.error(f"Error generating bedroom chart: {e}")
    
    # Price per square foot
    try:
        if 'price_per_sqft' in df.columns:
            df_filtered = df[df['price_per_sqft'] > 0]  # Filter out zeros or NaN
            if len(df_filtered) > 0:
                fig_sqft, ax_sqft = plt.subplots(figsize=(10, 5))
                sns.histplot(df_filtered['price_per_sqft'], kde=True, ax=ax_sqft)
                ax_sqft.set_title(f'Price per Sq.Ft Distribution for {project_name}')
                ax_sqft.set_xlabel('Price per Sq.Ft (AED)')
                ax_sqft.set_ylabel('Count')
                plt.tight_layout()
                figures['price_per_sqft'] = fig_sqft
    except Exception as e:
        st.error(f"Error generating price per sqft chart: {e}")
    
    return figures

def format_number(value):
    """Format numbers for display with commas as thousand separators"""
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:,.2f}"
    return value

# Streamlit app
def main():
    st.title("Property Data Collector")
    
    # Load existing data
    df = load_data()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Add Properties", "View & Edit Data", "Analyze Data"])
    
    with tab1:
        st.header("Add New Property")
        
        with st.form("add_property_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project = st.text_input("Project Name", "Damac Safa Two")
                property_type = st.selectbox("Property Type", ["Apartment", "Villa", "Townhouse", "Penthouse", "Duplex", "Other"])
                price = st.number_input("Price (AED)", value=0, min_value=0, step=100000)
                area_sqft = st.number_input("Area (sq.ft)", value=0, min_value=0, step=10)
                bedrooms = st.selectbox("Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
            
            with col2:
                bathrooms = st.selectbox("Bathrooms", ["1", "2", "3", "4", "5+"])
                location = st.text_input("Location", "Business Bay, Dubai")
                agent_name = st.text_input("Agent Name", "")
                property_url = st.text_input("Property URL", "")
            
            submit_button = st.form_submit_button("Add Property")
        
        if submit_button:
            # Create new property record
            new_property = {
                'project': project,
                'property_type': property_type,
                'price': price,
                'area_sqft': area_sqft,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'location': location,
                'agent_name': agent_name,
                'property_url': property_url,
                'entry_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add to DataFrame
            df = pd.concat([df, pd.DataFrame([new_property])], ignore_index=True)
            
            # Save updated data
            if save_data(df):
                st.success("Property added successfully!")
            else:
                st.error("Failed to save property data.")
        
        # Bulk import section
        st.header("Bulk Import from CSV")
        uploaded_file = st.file_uploader("Upload CSV file with property data", type="csv")
        
        if uploaded_file is not None:
            try:
                import_df = pd.read_csv(uploaded_file)
                required_columns = ['project', 'property_type', 'price', 'area_sqft', 'bedrooms', 'bathrooms']
                
                # Check if required columns exist
                if all(col in import_df.columns for col in required_columns):
                    # Add entry_date if not present
                    if 'entry_date' not in import_df.columns:
                        import_df['entry_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Merge with existing data
                    df = pd.concat([df, import_df], ignore_index=True)
                    
                    # Save updated data
                    if save_data(df):
                        st.success(f"Successfully imported {len(import_df)} properties!")
                    else:
                        st.error("Failed to save imported data.")
                else:
                    missing_cols = [col for col in required_columns if col not in import_df.columns]
                    st.error(f"CSV is missing required columns: {', '.join(missing_cols)}")
            except Exception as e:
                st.error(f"Error importing CSV: {e}")
    
    with tab2:
        st.header("View & Edit Property Data")
        
        if df.empty:
            st.info("No property data available. Add properties in the 'Add Properties' tab.")
        else:
            # Filter options
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                filter_project = st.selectbox("Filter by Project", ["All"] + sorted(df['project'].unique().tolist()))
            
            with filter_col2:
                filter_property_type = st.selectbox("Filter by Property Type", ["All"] + sorted(df['property_type'].unique().tolist()))
            
            # Apply filters
            filtered_df = df.copy()
            if filter_project != "All":
                filtered_df = filtered_df[filtered_df['project'] == filter_project]
            if filter_property_type != "All":
                filtered_df = filtered_df[filtered_df['property_type'] == filter_property_type]
            
            # Display data
            st.write(f"Showing {len(filtered_df)} of {len(df)} properties")
            
            # Enable editing
            edited_df = st.data_editor(
                filtered_df,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "project": st.column_config.TextColumn("Project"),
                    "price": st.column_config.NumberColumn("Price (AED)"),
                    "area_sqft": st.column_config.NumberColumn("Area (sq.ft)"),
                    "entry_date": st.column_config.DatetimeColumn("Entry Date")
                }
            )
            
            if st.button("Save Changes"):
                # Update the main dataframe with edited values
                if filter_project != "All" or filter_property_type != "All":
                    # If filtered, we need to update only the filtered rows
                    for idx, row in edited_df.iterrows():
                        # Find the corresponding index in the original DataFrame
                        # This is a simplified approach and might need refinement for complex cases
                        match_idx = df.index[
                            (df['project'] == row['project']) & 
                            (df['price'] == row['price']) & 
                            (df['entry_date'] == row['entry_date'])
                        ].tolist()
                        
                        if match_idx:
                            df.loc[match_idx[0]] = row
                else:
                    # If not filtered, we can replace the entire DataFrame
                    df = edited_df.copy()
                
                # Save updated data
                if save_data(df):
                    st.success("Changes saved successfully!")
                else:
                    st.error("Failed to save changes.")
            
            # Add delete functionality
            if st.button("Delete Selected Properties"):
                # Get indices to delete (this is simplified and might need refinement)
                to_delete = edited_df.index
                df = df.drop(to_delete).reset_index(drop=True)
                
                # Save updated data
                if save_data(df):
                    st.success("Selected properties deleted successfully!")
                else:
                    st.error("Failed to delete properties.")
                
                # Refresh the page to show updated data
                st.experimental_rerun()
            
            # Export data
            if st.download_button(
                "Export Data as CSV",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name=f"property_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            ):
                st.success("Data exported successfully!")
    
    with tab3:
        st.header("Analyze Property Data")
        
        if df.empty:
            st.info("No property data available for analysis. Add properties in the 'Add Properties' tab.")
        else:
            # Select project to analyze
            analyze_project = st.selectbox("Select Project to Analyze", ["All"] + sorted(df['project'].unique().tolist()))
            
            # Perform analysis
            if analyze_project == "All":
                analysis = analyze_data(df)
                project_name = "All Projects"
            else:
                analysis = analyze_data(df, analyze_project)
                project_name = analyze_project
            
            if analysis:
                # Display summary statistics
                st.subheader("Summary Statistics")
                stats_col1, stats_col2, stats_col3, stats_col4, stats_col5 = st.columns(5)
                
                with stats_col1:
                    st.metric("Total Listings", analysis['stats']['total_listings'])
                
                with stats_col2:
                    st.metric("Average Price", f"AED {format_number(analysis['stats']['avg_price'])}")
                
                with stats_col3:
                    st.metric("Min/Max Price", f"AED {format_number(analysis['stats']['min_price'])} - {format_number(analysis['stats']['max_price'])}")
                
                with stats_col4:
                    st.metric("Median Price", f"AED {format_number(analysis['stats']['median_price'])}")
                
                with stats_col5:
                    st.metric("Avg Price/Sq.Ft", f"AED {format_number(analysis['stats']['avg_price_per_sqft'])}")
                
                # Generate visualizations
                figures = generate_visualizations(analysis, project_name)
                
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
                    st.write(pd.DataFrame({
                        'Bedrooms': list(analysis['bedroom_counts'].keys()),
                        'Count': list(analysis['bedroom_counts'].values())
                    }))
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
                
                # Display detailed data
                st.subheader("Property Listings")
                st.dataframe(
                    analysis['dataframe'],
                    use_container_width=True,
                    column_config={
                        "price": st.column_config.NumberColumn("Price (AED)", format="%.2f"),
                        "area_sqft": st.column_config.NumberColumn("Area (sq.ft)", format="%.2f"),
                        "price_per_sqft": st.column_config.NumberColumn("Price/sq.ft", format="%.2f")
                    }
                )
            else:
                st.warning(f"No data available for {project_name}.")

if __name__ == "__main__":
    main()
