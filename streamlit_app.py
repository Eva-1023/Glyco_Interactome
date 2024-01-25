import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import got
import os

# Define a function to display the "Contact" tab content
def contact_tab():
    st.title('Contact Us')
    st.write("You can reach out to us at contact@example.com")

# Define the main app
def main():
    st.title('Glyco Interactome Network')

    # Add your existing code for the network visualization here

    st.sidebar.title('Choose your favorite Graph')
    path = 'data/html/'
    graph_set = set()
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            graph_set.add(filename.replace('.html', ''))
    option = st.sidebar.selectbox('Select graph', (graph_set))

    HtmlFile = open(path + option + '.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=1600, width=1000)

    # Add a "Contact" tab to the sidebar
    if st.sidebar.button('Contact'):
        contact_tab()

if __name__ == "__main__":
    main()
