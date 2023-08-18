import pandas as pd
import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit.components.v1 as components
plt.rcParams["font.sans-serif"] = ["SimHei"]

st.set_page_config(layout="wide")
st.title('温度变化曲线对比')
st.subheader("默认设定温度26度")
machine_option = st.sidebar.selectbox(
    "空调型号",
    ("机型A", "机型B", "机型C", "机型D", "机型E")
)

env_no = st.sidebar.selectbox(
    "工况",
    ("工况1", "工况2", "工况3")
)

button = st.sidebar.button("执行")


def gen_chart(no, sn):
    machine_type = {"机型A": "26CB1", "机型B": "35CB1", "机型C": "50CB1", "机型D": "26KS", "机型E": "35KS"}
    env_type = {"工况1": 1, "工况2": 2, "工况3": 3}
    sheet_name = machine_type[sn]
    table_no = env_type[no]
    demo_data = pd.read_excel(f"./demo_data_{table_no}.xlsx", sheet_name=sheet_name)
    data1 = demo_data["普通制冷"].values
    data2 = demo_data["Ieco"].values
    fig, ax = plt.subplots(figsize=(13, 5))
    xdata, ydata1, ydata2 = [], [], []
    ln1, = plt.plot([], [], 'ro', label="传统制冷")
    le1 = plt.legend(loc=1)
    ln2, = plt.plot([], [], 'g*', label="智能制冷")
    le2 = plt.legend(loc=1)

    def init():
        ax.set_xlim(1, 50)
        ax.set_ylim(22, 34)
        return ln1, ln2,

    def update(frame, data1, data2):
        xdata.append(frame)
        ydata1.append(data1[frame - 1])
        ydata2.append(data2[frame - 1])
        ln1.set_data(xdata, ydata1)
        ln2.set_data(xdata, ydata2)
        return ln1, ln2,

    ani = animation.FuncAnimation(fig, update, frames=range(1, 50), fargs=(data1, data2),
                                  init_func=init, blit=True, interval=1000)

    components.html(ani.to_jshtml(), height=2000, width=3000)


if button:
    gen_chart(no=env_no, sn=machine_option)

