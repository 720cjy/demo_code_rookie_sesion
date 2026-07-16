import streamlit as st
import RAG_02
import time

st.title("智能客服")
#记住file_upload中间括号有东西的！！
file_upload = st.file_uploader(
    "请上传txt文件",
    type = ["txt"],
    accept_multiple_files = False,  # 是否接受多个文件上传
)
if "service" not in st.session_state:   #st.session_state 因为原本streamlit是不保存的
    # 所以需要在每次运行时都创建一个很麻烦，所以用session_state来保存
    st.session_state["service"] = RAG_02.KnowledgeBaseService()

if file_upload is not None:
    file_name = file_upload.name
    file_size = file_upload.size/1024
    file_type = file_upload.type

    st.subheader(f"文件名{file_name}")
    st.write(f"文件大小{file_size:.2f}KB,文件格式{file_type}")
    text = file_upload.getvalue().decode("utf-8")
    #getvalue() 是获取上传文件信息。decode是解码成utf-8格式让人看得懂，不然就是byte数字
    #decode byte 转 utf-8    encode 是  utf-8  转   byte
    # st.write(text)    #注意不要写成print
    with st.spinner("加载中"):
        time.sleep(3)

        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)
