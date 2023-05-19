import streamlit as st
from PIL import Image

st.write("# 混淆矩阵图如下")

image = Image.open('conf_mat.png')
st.image(image, caption='Confusion Matrix',use_column_width=True)