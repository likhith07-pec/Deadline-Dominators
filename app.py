import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Data Viewer",
    page_icon="🔍",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
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

def main():
    # Title
    st.markdown('<h1 class="main-title">Deadline Dominators</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6B7280;">Upload any data file and search through it</p>', unsafe_allow_html=True)
    
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