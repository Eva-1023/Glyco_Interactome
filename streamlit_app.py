import streamlit as st
import os
import re 

# Define a function to display the network visualization
def network_page():
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
    st.components.v1.html(source_code, height=800, width=1000)
    st.sidebar.title("Figure")
    figure = st.empty()
    # get the row from source_code that contains "edges = new vis.DataSet"
    edges_row = [row for row in source_code.splitlines() if "edges = new vis.DataSet" in row][0]
    
    
    title_occurrences = re.findall(r'"title": "([^"]+)"', edges_row)
    
    clicked_edge = st.sidebar.selectbox("Select an Edge:", title_occurrences)
    if clicked_edge:
        edge_name = clicked_edge
        figure_filename = os.path.join('data/boxplot/', edge_name + ".png")  # Adjust the filename as needed
        figure.image(figure_filename, use_column_width=True, caption=f"Figure for Edge: {edge_name}")
    


# Define a function to display the Home page content
def home_page():
    st.title('Home')
    st.write('This is the home page content.')

# Define a function to display the Contact page content
def contact_page():
    st.title('Contact Us')
    st.write("You can reach out to us at contact@example.com")

# Define the main app layout
def main():
    st.set_page_config(
        page_title="Myco Interactome Network",
        page_icon="🌐",
        layout="wide",
    )

    # Navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Network", "Contact"])

    # Page Display
    if selection == "Home":
        home_page()
    elif selection == "Network":
        network_page()
    elif selection == "Contact":
        contact_page()

if __name__ == "__main__":
    main()
