import streamlit as st

st.write("# 模糊提取器")
server_id_list = ['1', '2', '3', '4']

st.sidebar.write('配置')
server_id = st.sidebar.selectbox('服务器ID', server_id_list)

protocol_tab, data_tab, message_tab, feature_extraction_tab = st.tabs(["协议运行", "数据库", "消息记录", "特征提取"])

with protocol_tab:
    "服务器端只会被动运行协议，接收到用户终端发送请求后进行处理及消息返回"
    "此界面显示当前运行的协议"

with data_tab:
    "这部分显示服务器用于协议认证的数据库"

with message_tab:
    "这部分显示协议认证过程消息"

with feature_extraction_tab:
    '这部分显示放深度学习部分相关数据'

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")