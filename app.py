import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime
from PIL import Image
import base64

# Set page config
st.set_page_config(
    page_title="Data Viewer",
    page_icon="🔍",
    layout="wide"
)

# Simple CSS with logo positioning
st.markdown("""
<style>
    /* Header container */
    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        padding: 10px 0;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Logo styling */
    .logo-container {
        margin-right: 20px;
        padding: 5px;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .logo-img {
        max-height: 60px;
        width: auto;
        object-fit: contain;
    }
    
    /* Title styling */
    .title-container {
        flex-grow: 1;
    }
    
    .main-title {
        font-size: 2rem;
        color: #1E3A8A;
        margin: 0;
        padding: 0;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #6B7280;
        margin: 0;
        padding: 0;
    }
    
    /* Content sections */
    .upload-box {
        border: 2px dashed #3B82F6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #F8FAFC;
        margin: 20px 0;
    }
    
    .search-box {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def format_record(record, df_columns):
    """Simple format: one column per line"""
    text = ""
    for col in df_columns:
        value = record[col]
        if pd.isna(value):
            value = ""
        text += f"{col}: {value}\n"
    return text.strip()  # Remove extra newline at the end

def load_logo():
    """Load logo from image file"""
    try:
        # Open the logo image
        logo = Image.open("C:\Users\ADMIN\Desktop\bablu\WhatsApp Image 2025-12-04 at 19.31.40_78cd7018.jpg")
        
        # Resize while maintaining aspect ratio
        max_size = (200, 80)  # Max width 200px, max height 80px
        logo.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return logo
    except Exception as e:
        st.warning(f"Logo not found: {str(e)}")
        return None

def main():
    # Create header with logo and title
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Load and display logo
        logo = load_logo()
        if logo:
            st.image(logo, use_container_width=True)
        else:
            # Placeholder if logo not found
            st.markdown('<div class="logo-container" style="height: 60px; display: flex; align-items: center; justify-content: center; color: #6B7280; font-style: italic;">Logo</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h1 class="main-title">Deadline Dominators</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Upload any data file and search through it</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    
    # File Upload Section
    st.markdown("## 📤 Upload Your Data")
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload any dataset here"
    )
    
    if uploaded_file is not None:
        with st.spinner('Uploading...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            try:
                # Read the file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                st.session_state.file_uploaded = True
                st.session_state.file_name = uploaded_file.name
                
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show uploaded data
    if st.session_state.file_uploaded:
        df = st.session_state.df
        
        # Show all data
        st.markdown("## 📋 Your Data")
        st.dataframe(df, use_container_width=True)
        
        # Search Section
        st.markdown("## 🔍 Search Data")
        st.markdown('<div class="search-box">', unsafe_allow_html=True)
        
        # Let user choose which column to search
        search_column = st.selectbox(
            "Search in column:",
            df.columns.tolist(),
            help="Choose which column to search in"
        )
        
        # Search input
        search_text = st.text_input(
            "Search for:",
            placeholder="Enter search term...",
            help="Search in the selected column"
        )
        
        if search_text:
            # Perform search
            try:
                # Convert everything to string and search (case-insensitive)
                mask = df[search_column].astype(str).str.contains(search_text, case=False, na=False)
                search_results = df[mask]
                
                if len(search_results) > 0:
                    st.success(f"Found {len(search_results)} record(s)")
                    
                    # Show results in table
                    st.dataframe(search_results, use_container_width=True)
                    
                    # Show copyable format for each record
                    st.markdown("## 📋 Copy Data")
                    
                    # Process each record
                    for idx, (_, record) in enumerate(search_results.iterrows()):
                        # Create copyable text
                        copy_text = format_record(record, df.columns)
                        
                        st.markdown(f"**Record {idx + 1}:**")
                        
                        # Display text in a text area
                        text_area = st.text_area(
                            f"Text for Record {idx + 1}:",
                            copy_text,
                            height=150,
                            key=f"text_{idx}"
                        )
                        
                        # Copy to clipboard button at the end
                        if st.button(f"📋 Copy Record {idx + 1} to Clipboard", key=f"copy_{idx}"):
                            st.success(f"✅ Record {idx + 1} text is ready to copy!")
                            st.info("Select the text above and press Ctrl+C to copy")
                        
                        st.markdown("---")
                    
                else:
                    st.warning("No records found matching your search")
                    
            except Exception as e:
                st.error(f"Search error: {str(e)}")
        else:
            # If no search text, show message
            st.info("👆 Enter a search term above to find records")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Instructions if no file uploaded
    else:
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("""
        1. **Upload** any data file (CSV or Excel)
        2. Your data will appear
        3. **Search** for any record
        4. **Copy** the text using the copy button
        """)
        
        st.info("👆 Upload your file to see your data")

if __name__ == "__main__":
    main()