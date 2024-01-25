import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import got 
import os 

#Network(notebook=True)
st.title('Glyco Interactome Network')
# make Network show itself with repr_html

#def net_repr_html(self):
#  nodes, edges, height, width, options = self.get_network_data()
#  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
#  return html

#Network._repr_html_ = net_repr_html
st.sidebar.title('Choose your favorite Graph')
path = 'data/html/'
graph_set = set()
for filename in os.listdir(path):
    if filename.endswith(".html"):
        graph_set.add(filename.replace('.html',''))
option=st.sidebar.selectbox('select graph',(graph_set))
physics=st.sidebar.checkbox('add physics interactivity?')
got.simple_func(physics)



HtmlFile = open(path+option+'.html', 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 900,width=900)


got.got_func(physics)

