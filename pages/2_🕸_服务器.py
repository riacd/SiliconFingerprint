import streamlit as st
from PIL import Image
import global_API


st.write("# 模糊提取器")

st.sidebar.write('配置')
server_id = st.sidebar.selectbox('服务器ID', global_API.Server_id_list)

protocol_tab, data_tab, message_tab, feature_extraction_tab, fuzzy_extraction_tab= st.tabs(["协议运行", "数据库", "消息记录", "特征提取", "射频指纹提取"])

with protocol_tab:
    "服务器端只会被动运行协议，接收到用户终端发送请求后进行处理及消息返回"
    "此界面显示当前运行的协议"

with data_tab:
    "这部分显示服务器用于协议认证的数据库"
    st.dataframe(global_API.Manager.Server_list[server_id].database.data)

with message_tab:
    "这部分显示协议认证过程消息"
    st.dataframe({'消息记录': global_API.Manager.Server_list[server_id].Msglog})


with feature_extraction_tab:
    '这部分显示放深度学习部分相关数据'

with fuzzy_extraction_tab:
    st.write("# 混淆矩阵图如下")

    # image = Image.open('conf_mat.png')
    # st.image(image, caption='Confusion Matrix', use_column_width=True)
# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")