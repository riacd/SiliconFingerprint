import streamlit as st
import Server.API
import UserEquipment.API
import global_API



st.sidebar.write('配置')
device_id = st.sidebar.selectbox('用户设备ID', global_API.UE_id_list)
server_id = st.sidebar.selectbox('服务器ID', global_API.Server_id_list)

protocol_tab, data_tab, message_tab = st.tabs(["协议运行", "数据库", "消息记录"])

with protocol_tab:
    "用户终端发起的协议请求："
    register, identify = st.columns(2)
    # You can use a column just like st.sidebar:
    register.button('注册', on_click=global_API.Manager.UE_list[device_id].register, args=[server_id])
    identify.button('认证')

    "用户终端当前协议状态："
    "用户i在服务器j上已完成（注册/双向认证，可以开始通信）"

with data_tab:
    "这部分显示用户终端用于协议认证的数据库"
    st.dataframe(global_API.Manager.UE_list[device_id].database.data)

with message_tab:
    "这部分显示协议认证过程消息"
    st.dataframe(global_API.Manager.UE_list[device_id].Msglog)

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")