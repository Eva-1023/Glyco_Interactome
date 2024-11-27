import pandas as pd
import streamlit as st
import os
import re 

# Define a function to display the network visualization
def network_page():
    st.title('Glyco Interactome Network')

    # 设置文件路径
    path = 'data/Total_html/'

    # 初始化条件集合
    condition1_set = set()
    condition2_set = {}

    # 遍历目录中的文件
    for filename in os.listdir(path):
        if filename.endswith('.html'):
            base_name = filename.replace('.html', '')
            if '_' in base_name:
                p1, p2 = base_name.split('_')
                condition1_set.add(p1)
                if p1 not in condition2_set:
                    condition2_set[p1] = set()
                condition2_set[p1].add(p2)
            else:
                condition1_set.add(base_name)

    # 替换映射字典
    replacement_dict = {
        'F': 'Fucosylated (F) type',
        'S': 'Sialylated (S) type',
        'FS': 'Sialofucosylated (FS) type',
        'Neu': 'Neutral (Neu) type',
        'HM': 'High Mannose (HM) type',
        'Total': 'Total'

    }

    # 替换和排序 condition1_set
    condition1_set_id = sorted([replacement_dict.get(cond, cond) for cond in condition1_set])

    # 替换和排序 condition2_set
    condition2_set_id = {
        replacement_dict.get(key, key): sorted(values)
        for key, values in condition2_set.items()
    }
    print(condition2_set)
    print(condition2_set_id)
    # 确保 condition1_set 不为空，否则 selectbox 会返回 None
    if not condition1_set:
        st.error("No HTML files found in the specified directory.")
        return
    st.sidebar.title("Choose your interested glycosylation conditions")
    # Streamlit 侧边栏选择框
    option1 = st.sidebar.selectbox('Select condition1', condition1_set_id)

    # 检查 option1 是否为 None
    if option1 is None:
        st.error("Please select a valid condition1.")
        return

    # 根据第一个条件选择框的选择更新第二个条件选择框
    if option1 in condition2_set_id:
        option2 = st.sidebar.selectbox('Select condition2', condition2_set_id[option1])
    else:
        option2 = ""
    option1_file = [key for key, value in replacement_dict.items() if value == option1]
    option2_file = [key for key, value in replacement_dict.items() if value == option2]
    #print(option1_file[0])
    #print(type(option1_file[0]))
    # 构造 HTML 文件路径
    if option2:
        html_file_path = f"{path}{option1_file[0]}_{option2}.html"
    else:
        #print(option1_file)
        #print(type(option1_file))
        html_file_path = f"{path}{option1_file[0]}.html"

    # 确认文件存在并读取
    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as HtmlFile:
            source_code = HtmlFile.read()
            st.components.v1.html(source_code, height=800, width=1000)
    else:
        st.error(f"File {html_file_path} does not exist.")

# Define a function to display the Figure section

import os
import streamlit as st


def figure_page():
    st.sidebar.title("Choose your interested protein-protein pair")
    #st.title('Boxplot')
    path = 'data/boxplot_normalized/'
    protein1_set = set()
    protein2_set = {}

    for filename in os.listdir(path):
        if filename.endswith(".png"):
            name_str = filename.replace('.png', '')
            p1, p2 = name_str.split('_')[0], name_str.split('_')[1]
            protein1_set.add(p1)
            if p1 not in protein2_set:
                protein2_set[p1] = set()
            protein2_set[p1].add(p2)

    protein1_set = sorted(protein1_set)
    protein2_set = {x: sorted(protein2_set[x]) for x in protein2_set}
    protein1 = st.sidebar.selectbox('Select protein1', protein1_set)
    protein2 = st.sidebar.selectbox('Select protein2', protein2_set[protein1])

    edge_name = f"{protein1}_{protein2}"

    # Define the paths for each image
    paths = [
        ('data/boxplot_normalized/', 'Abundance for Edge'),
        ('data/boxplot_relative/', 'Relative Abundance for Edge'),
        ('data/TopS_Score/', 'TopS score for Edge')
    ]

    for img_path, caption in paths:
        figure_filename = os.path.join(img_path, edge_name + ".png")
        file_exists = os.path.exists(figure_filename)

        if file_exists:
            st.image(figure_filename, use_column_width=True, caption=f"{caption}: {edge_name}")
        else:
            placeholder_filename = 'data/blank.png'
            st.image(placeholder_filename, use_column_width=True, caption="No data available")
# Define a function to display the Home page content
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
def home_page():
    st.title('Abstract')
    st.image('data/image/Abstract.svg', use_column_width=True)
    text = """
        <div style="text-align: justify; text-indent: 2em;font-size:24px">
            Protein-protein interactions (PPIs) offer crucial insights into comprehending the complicated molecular mechanisms and signaling pathways within cells that regulate developmental processes or the progression of disease-related phenotypes. Meanwhile, proteins are frequently subject to post-translational modifications (PTMs) that enable the regulation of their functions for specific cellular events. One of the key challenges in studying PPIs lies in the development of methods to detect changes in interactions resulting from these PTMs. Notably, the glycosylation of cell membrane proteins to form the glycocalyx presents a considerable hurdle, as the significance of various types of glycans has largely been overlooked in most studies of membrane protein interactions. In this study, we introduced a novel approach termed glycan-dependent affinity purification followed by mass spectrometry analysis (GAP-MS) to assess variations in PPIs for any glycoprotein of interest under different glycosylation conditions. Within the framework of GAP-MS, we combined the manipulation of Glycan Phenotypes in cultured cells using a set of glycan modifier toolboxes with the classic affinity purification coupled with mass spectrometry analysis (AP-MS) approach. As a proof of principle, we selected four glycoproteins, namely BSG, CD44, EGFR, and SLC3A2, as baits to compare their co-purified partners across five distinct Glycan Phenotypes. The findings demonstrated the capability of GAP-MS in identifying PPIs that are influenced by altered glycosylation status. PPI networks based on the interactions of the aforementioned four baits were generated for each Glycan Phenotype. Moreover, the GAP-MS workflow is well-suited for systematically investigating a broader collection of glycoproteins of interest compared to the study relied on the glycosite mutagenesis, thereby allowing for the expansion of these networks as more bait proteins are analyzed in future studies, which assists the development of new therapeutics targeting glycosylated proteins.
        </div>
        """
    st.write(text, unsafe_allow_html=True)

# Define a function to display the Contact page content
def contact_page():
    st.title('Contact Us')
    #data = pd.DataFrame({'lat':[22.73],'lon':[113.53]})
    #st.map(data)
    # import pydeck as pdk
    #
    # # 定义数据
    # data = [{'lat': 22.73, 'lon': 113.53, 'name': 'GREATER BAY AREA INSTITUTE OF PRECISION MEDICINE'}]
    #
    # # 定义地图图层
    # layer = pdk.Layer(
    #     'ScatterplotLayer',
    #     data=data,
    #     get_position='[lon, lat]',
    #     get_radius=1000,
    #     get_color=[255, 0, 0],
    #     pickable=True
    # )
    #
    # # 定义地图视图
    # view_state = pdk.ViewState(
    #     latitude=22.7894,
    #     longitude=113.5500,
    #     zoom=14,
    #     pitch=50
    # )
    #
    # # 定义标注图层
    # text_layer = pdk.Layer(
    #     "TextLayer",
    #     data=data,
    #     get_position='[lon, lat]',
    #     get_text='name',
    #     get_color=[0, 0, 0, 200],
    #     get_size=16,
    #     get_alignment_baseline="'bottom'"
    # )
    #
    # # 显示地图
    # r = pdk.Deck(layers=[layer, text_layer], initial_view_state=view_state,map_style='mapbox://styles/mapbox/light-v9')
    # st.pydeck_chart(r)
    text = """
    <div style="text-align: justify; font-size: 24px">
        More information is available here: <a href="https://github.com/Eva-1023/Glyco_Interactome">GitHub Repository.</a><br>
        If you have any question, you can reach out to us at <a href="mailto:liy24@m.fudan.edu.cn">liy24@m.fudan.edu.cn</a>
    </div>
    """
    st.write(text, unsafe_allow_html=True)


# Define the main app layout
def main():
    st.set_page_config(
        page_title="Myco Interactome Network",
        page_icon="🌐",
        layout="wide",
    )

    # Navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Abstract", "Network", "Protein-protein Pair", "Contact"])

    # Page Display
    if selection == "Abstract":
        home_page()
    elif selection == "Network":
        network_page()
    elif selection == "Protein-protein Pair":
        figure_page()
    elif selection == "Contact":
        contact_page()

if __name__ == "__main__":
    main()
