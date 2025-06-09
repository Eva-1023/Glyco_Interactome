"""
Glyco Interactome Network Visualization Application

This Streamlit application provides interactive visualization of protein-protein interactions
under different glycosylation conditions using the GAP-MS (Glycan-dependent Affinity 
Purification followed by Mass Spectrometry) approach.

Author: Eva-1023
Repository: https://github.com/Eva-1023/Glyco_Interactome
Contact: liy24@m.fudan.edu.cn
"""

import os
import re
import logging
from typing import Dict, Set, List, Tuple, Optional
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable PIL's DecompressionBombWarning for large images
Image.MAX_IMAGE_PIXELS = None

# Constants
DATA_PATHS = {
    'network_html': 'data/Total_html/',
    'boxplot_normalized': 'data/boxplot_normalized/',
    'boxplot_relative': 'data/boxplot_relative/',
    'tops_score': 'data/TopS_Score/',
    'abstract_image': 'data/image/Abstract.jpg',
    'blank_image': 'data/blank.png'
}

GLYCOSYLATION_TYPES = {
    'F': 'Fucosylated (F) type',
    'S': 'Sialylated (S) type',
    'FS': 'Sialofucosylated (FS) type',
    'Neu': 'Neutral (Neu) type',
    'HM': 'High Mannose (HM) type',
    'Total': 'Total'
}


def validate_data_paths() -> bool:
    """
    Validate that required data directories exist.
    
    Returns:
        bool: True if all required paths exist, False otherwise
    """
    missing_paths = []
    for path_name, path_value in DATA_PATHS.items():
        if not os.path.exists(path_value):
            missing_paths.append(path_value)
            logger.warning(f"Missing data path: {path_value}")
    
    if missing_paths:
        st.error(f"Missing required data directories: {', '.join(missing_paths)}")
        return False
    return True


def get_network_conditions(html_path: str) -> Tuple[Set[str], Dict[str, Set[str]]]:
    """
    Extract available network conditions from HTML files.
    
    Args:
        html_path (str): Path to directory containing HTML files
        
    Returns:
        Tuple[Set[str], Dict[str, Set[str]]]: Primary conditions and secondary conditions
    """
    try:
        condition1_set = set()
        condition2_set = {}
        
        if not os.path.exists(html_path):
            logger.error(f"HTML path does not exist: {html_path}")
            return set(), {}
        
        for filename in os.listdir(html_path):
            if filename.endswith('.html'):
                base_name = filename.replace('.html', '')
                if '_' in base_name:
                    p1, p2 = base_name.split('_', 1)  # Split only on first underscore
                    condition1_set.add(p1)
                    if p1 not in condition2_set:
                        condition2_set[p1] = set()
                    condition2_set[p1].add(p2)
                else:
                    condition1_set.add(base_name)
        
        return condition1_set, condition2_set
    
    except Exception as e:
        logger.error(f"Error extracting network conditions: {e}")
        return set(), {}


def get_protein_pairs(boxplot_path: str) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Extract available protein pairs from boxplot PNG files.
    
    Args:
        boxplot_path (str): Path to directory containing boxplot PNG files
        
    Returns:
        Tuple[List[str], Dict[str, List[str]]]: Primary proteins and secondary proteins
    """
    try:
        protein1_set = set()
        protein2_set = {}
        
        if not os.path.exists(boxplot_path):
            logger.error(f"Boxplot path does not exist: {boxplot_path}")
            return [], {}
        
        for filename in os.listdir(boxplot_path):
            if filename.endswith(".png"):
                name_str = filename.replace('.png', '')
                parts = name_str.split('_')
                if len(parts) >= 2:
                    p1, p2 = parts[0], parts[1]
                    protein1_set.add(p1)
                    if p1 not in protein2_set:
                        protein2_set[p1] = set()
                    protein2_set[p1].add(p2)
        
        protein1_list = sorted(protein1_set)
        protein2_dict = {x: sorted(protein2_set[x]) for x in protein2_set}
        
        return protein1_list, protein2_dict
    
    except Exception as e:
        logger.error(f"Error extracting protein pairs: {e}")
        return [], {}


def network_page():
    """Display the network visualization page."""
    st.title('🌐 Glyco Interactome Network')
    st.markdown("---")
    
    # Get network conditions
    condition1_set, condition2_set = get_network_conditions(DATA_PATHS['network_html'])
    
    if not condition1_set:
        st.error("❌ No network data found. Please ensure HTML files are present in the data directory.")
        return
    
    # Map conditions to display names
    condition1_display = sorted([GLYCOSYLATION_TYPES.get(cond, cond) for cond in condition1_set])
    condition2_display = {
        GLYCOSYLATION_TYPES.get(key, key): sorted(values)
        for key, values in condition2_set.items()
    }
    
    # Sidebar controls
    st.sidebar.title("🔬 Glycosylation Conditions")
    st.sidebar.markdown("Select conditions to visualize protein interaction networks:")
    
    option1 = st.sidebar.selectbox(
        'Primary Condition',
        condition1_display,
        help="Select the primary glycosylation condition"
    )
    
    if option1 is None:
        st.error("Please select a valid primary condition.")
        return
    
    # Secondary condition selection
    option2 = ""
    if option1 in condition2_display:
        option2 = st.sidebar.selectbox(
            'Secondary Condition',
            condition2_display[option1],
            help="Select the secondary condition (if available)"
        )
    
    # Map display names back to file names
    option1_file = [key for key, value in GLYCOSYLATION_TYPES.items() if value == option1]
    
    if not option1_file:
        st.error(f"Invalid condition selected: {option1}")
        return
    
    # Construct HTML file path
    if option2:
        html_file_path = os.path.join(DATA_PATHS['network_html'], f"{option1_file[0]}_{option2}.html")
    else:
        html_file_path = os.path.join(DATA_PATHS['network_html'], f"{option1_file[0]}.html")
    
    # Display network visualization
    try:
        if os.path.exists(html_file_path):
            with open(html_file_path, 'r', encoding='utf-8') as html_file:
                source_code = html_file.read()
                st.components.v1.html(source_code, height=800, width=1000)
                
                # Add information about the current network
                st.info(f"📊 Currently displaying: **{option1}**" + 
                       (f" → **{option2}**" if option2 else ""))
        else:
            st.error(f"❌ Network file not found: {os.path.basename(html_file_path)}")
            
    except Exception as e:
        logger.error(f"Error loading network visualization: {e}")
        st.error("❌ Failed to load network visualization. Please try again.")


def figure_page():
    """Display the protein-protein pair analysis page."""
    st.title('📊 Protein-Protein Pair Analysis')
    st.markdown("---")
    
    # Get protein pairs
    protein1_list, protein2_dict = get_protein_pairs(DATA_PATHS['boxplot_normalized'])
    
    if not protein1_list:
        st.error("❌ No protein pair data found. Please ensure PNG files are present in the data directory.")
        return
    
    # Sidebar controls
    st.sidebar.title("🧬 Protein Selection")
    st.sidebar.markdown("Select protein pairs to analyze their interactions:")
    
    protein1 = st.sidebar.selectbox(
        'Primary Protein',
        protein1_list,
        help="Select the first protein in the interaction pair"
    )
    
    if protein1 and protein1 in protein2_dict:
        protein2 = st.sidebar.selectbox(
            'Secondary Protein',
            protein2_dict[protein1],
            help="Select the second protein in the interaction pair"
        )
    else:
        st.error("No secondary proteins available for the selected primary protein.")
        return
    
    edge_name = f"{protein1}_{protein2}"
    
    # Display analysis plots
    st.subheader(f"Analysis for {protein1} ↔ {protein2}")
    
    # Define the analysis types and their paths
    analysis_paths = [
        (DATA_PATHS['boxplot_normalized'], 'Abundance for Edge', '📈'),
        (DATA_PATHS['boxplot_relative'], 'Relative Abundance for Edge', '📊'),
        (DATA_PATHS['tops_score'], 'TopS Score for Edge', '🎯')
    ]
    
    # Create columns for better layout
    cols = st.columns(len(analysis_paths))
    
    for i, (img_path, caption, icon) in enumerate(analysis_paths):
        with cols[i]:
            figure_filename = os.path.join(img_path, f"{edge_name}.png")
            
            if os.path.exists(figure_filename):
                st.image(
                    figure_filename,
                    #use_container_width=True,
                    caption=f"{icon} {caption}: {edge_name}"
                )
            else:
                # Display placeholder or warning
                if os.path.exists(DATA_PATHS['blank_image']):
                    st.image(
                        DATA_PATHS['blank_image'],
                        #use_container_width=True,
                        caption=f"⚠️ No data available for {caption}"
                    )
                else:
                    st.warning(f"⚠️ No data available for {caption}: {edge_name}")


def home_page():
    """Display the home page with project abstract."""
    st.title('🧬 Glyco Interactome Network')
    st.markdown("### Understanding Protein-Protein Interactions in Glycosylation Context")
    st.markdown("---")
    
    # Display abstract image if available
    if os.path.exists(DATA_PATHS['abstract_image']):
        st.image(DATA_PATHS['abstract_image'])
    else:
        st.warning("⚠️ Abstract image not found")
    
    # Project description
    st.markdown("""
    <div style="text-align: justify; text-indent: 2em; font-size: 18px; line-height: 1.6;">
        <strong>Abstract:</strong><br><br>
        Protein-protein interactions (PPIs) offer crucial insights into comprehending the complicated 
        molecular mechanisms and signaling pathways within cells that regulate developmental processes 
        or the progression of disease-related phenotypes. Meanwhile, proteins are frequently subject 
        to post-translational modifications (PTMs) that enable the regulation of their functions for 
        specific cellular events. One of the key challenges in studying PPIs lies in the development 
        of methods to detect changes in interactions resulting from these PTMs. 
        <br><br>
        Notably, the glycosylation of cell membrane proteins to form the glycocalyx presents a 
        considerable hurdle, as the significance of various types of glycans has largely been 
        overlooked in most studies of membrane protein interactions. In this study, we introduced 
        a novel approach termed <strong>glycan-dependent affinity purification followed by mass 
        spectrometry analysis (GAP-MS)</strong> to assess variations in PPIs for any glycoprotein 
        of interest under different glycosylation conditions.
        <br><br>
        Within the framework of GAP-MS, we combined the manipulation of Glycan Phenotypes in 
        cultured cells using a set of glycan modifier toolboxes with the classic affinity 
        purification coupled with mass spectrometry analysis (AP-MS) approach. As a proof of 
        principle, we selected four glycoproteins, namely <strong>BSG, CD44, EGFR, and SLC3A2</strong>, 
        as baits to compare their co-purified partners across five distinct Glycan Phenotypes.
        <br><br>
        The findings demonstrated the capability of GAP-MS in identifying PPIs that are influenced 
        by altered glycosylation status. PPI networks based on the interactions of the aforementioned 
        four baits were generated for each Glycan Phenotype. Moreover, the GAP-MS workflow is 
        well-suited for systematically investigating a broader collection of glycoproteins of 
        interest compared to studies relying on glycosite mutagenesis, thereby allowing for the 
        expansion of these networks as more bait proteins are analyzed in future studies, which 
        assists the development of new therapeutics targeting glycosylated proteins.
    </div>
    """, unsafe_allow_html=True)


def contact_page():
    """Display the contact information page."""
    st.title('📧 Contact Us')
    st.markdown("---")

    # Project Information
    st.markdown("""
    <div style="font-size: 18px;">
        <h3>🔗 Project Information</h3>
        <p>
            For more detailed information about this project, please visit our 
            <a href="https://github.com/Eva-1023/Glyco_Interactome" target="_blank">
                GitHub Repository
            </a>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Contact Information
    st.markdown("""
    <div style="font-size: 18px;">
        <h3>📨 Get in Touch</h3>
        <p>
            If you have any questions, please email us at:
            <br>
            <a href="mailto:lyi24@m.fudan.edu.cn">lyi24@m.fudan.edu.cn</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Institution
    st.markdown("""
    <div style="font-size: 18px;">
        <h3>🏛️ Institution</h3>
        <p>
            This research was conducted at the Greater Bay Area Institute of Precision Medicine.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Citation
    st.markdown("""
    <div style="font-size: 18px;">
        <h3>📄 Citation</h3>
        <p>
            If you use this tool or data in your research, please cite our work appropriately.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Glyco Interactome Network",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Validate data paths before proceeding
    if not validate_data_paths():
        st.stop()
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stSelectbox > div > div > select {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation sidebar
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("Select a section to explore:")
    
    selection = st.sidebar.radio(
        "Go to",
        ["🏠 Abstract", "🌐 Network", "📊 Protein-Protein Pair", "📧 Contact"],
        index=0
    )
    
    # Page routing
    try:
        if selection == "🏠 Abstract":
            home_page()
        elif selection == "🌐 Network":
            network_page()
        elif selection == "📊 Protein-Protein Pair":
            figure_page()
        elif selection == "📧 Contact":
            contact_page()
    except Exception as e:
        logger.error(f"Error in page rendering: {e}")
        st.error("❌ An error occurred while loading the page. Please try again.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Glyco Interactome Network v1.0**")
    st.sidebar.markdown("*Powered by Streamlit*")


if __name__ == "__main__":
    main()
