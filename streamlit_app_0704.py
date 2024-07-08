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

    # 排序条件集
    condition1_set = sorted(condition1_set)
    condition2_set = {key: sorted(values) for key, values in condition2_set.items()}

    # 确保 condition1_set 不为空，否则 selectbox 会返回 None
    if not condition1_set:
        st.error("No HTML files found in the specified directory.")
        return

    # Streamlit 侧边栏选择框
    option1 = st.sidebar.selectbox('Select condition1', condition1_set)

    # 检查 option1 是否为 None
    if option1 is None:
        st.error("Please select a valid condition1.")
        return

    # 根据第一个条件选择框的选择更新第二个条件选择框
    if option1 in condition2_set:
        option2 = st.sidebar.selectbox('Select condition2', condition2_set[option1])
    else:
        option2 = ""

    # 构造 HTML 文件路径
    if option2:
        html_file_path = f"{path}{option1}_{option2}.html"
    else:
        html_file_path = f"{path}{option1}.html"

    # 确认文件存在并读取
    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as HtmlFile:
            source_code = HtmlFile.read()
            st.components.v1.html(source_code, height=800, width=1000)
    else:
        st.error(f"File {html_file_path} does not exist.")

# Define a function to display the Figure section
def figure_page():
    st.sidebar.title("Choose your favorite interectome")
    st.title('Boxplot')
    path = 'data/boxplot/'
    protein1_set = set()
    protein2_set = {}
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            str = filename.replace('.png', '')
            p1, p2 = str.split('_')[0], str.split('_')[1]
            protein1_set.add(p1)
            if p1 not in protein2_set.keys():
                protein2_set[p1] = set()
            protein2_set[p1].add(p2)
    protein1_set = sorted(protein1_set)
    protein2_set = {x:sorted(protein2_set[x]) for x in protein2_set.keys()}
    protein1 = st.sidebar.selectbox('Select protein1', protein1_set)
    protein2 = st.sidebar.selectbox('Select protein2', protein2_set[protein1])
    #HtmlFile = open(path + option + '.html', 'r', encoding='utf-8')
    #source_code = HtmlFile.read()
    
    figure = st.empty()
    # get the row from source_code that contains "edges = new vis.DataSet"
    #edges_row = [row for row in source_code.splitlines() if "edges = new vis.DataSet" in row][0]
    
    #title_occurrences = re.findall(r'"title": "([^"]+)"', edges_row)

    edge_name = f"{protein1}_{protein2}"
    figure_filename = os.path.join('data/boxplot/', edge_name + ".png")  # Adjust the filename as needed
    file_exists = os.path.exists(figure_filename)
    if(file_exists):
        figure.image(figure_filename, use_column_width=True, caption=f"Abundance for Edge: {edge_name}",width=200)
    else:
        placeholder_filename = 'data/blank.png'
        figure.image(placeholder_filename, use_column_width=True, caption="No data available", width=200)

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
    selection = st.sidebar.radio("Go to", ["Home", "Network", "Interactome", "Contact"])

    # Page Display
    if selection == "Home":
        home_page()
    elif selection == "Network":
        network_page()
    elif selection == "Interactome":
        figure_page()
    elif selection == "Contact":
        contact_page()

if __name__ == "__main__":
    main()
