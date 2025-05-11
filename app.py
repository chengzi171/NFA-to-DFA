"""
这是一个用于将 NFA 转换为 DFA 的 python 应用程序。
主要使用 Streamlit 库来创建用户界面，并使用 NFA 模块来处理 NFA 和 DFA 的转换, 并使用 Graphviz 来可视化 DFA 的状态图。
所调用的第三方库信息保存在 requirements.txt 文件中。
在终端运行以下命令来下载所需第三方库：
pip install -r requirements.txt
在终端中运行以下命令来启动应用程序:
streamlit run app.py
在浏览器中打开终端中显示的链接即可访问应用程序。

这里提供一个参考NFA信息的示例:
NFA状态 : {"q0", "q1", "q2"}
NFA字母表 : {"a", "b"}
NFA 转换函数 : {
    ("q0", "a"): {"q0", "q1"},
    ("q0", "b"): {"q0"},
    ("q1", "b"): {"q2"}
}
NFA 起始状态 : {"q0"}
NFA 接受状态 : {"q2"}
"""
import streamlit as st
import pandas as pd
import NFA

st.write('## NFA的确定')
st.write('### 1. 输入NFA的状态数和字母表')
nfa_states_count = st.number_input('NFA的状态数', min_value=1, value=3, step=1)
nfa_states = set(st.text_input('NFA的状态(状态之间用逗号隔开)', 'S,P,Z').split(','))  # 转换为集合
nfa_alphabet = set(st.text_input('NFA的字母表(字母之间用逗号隔开)', '0,1').split(','))  # 转换为集合
nfa_alphabet = {symbol.strip() for symbol in nfa_alphabet if symbol.strip()}  # 去除空格和空字符串

st.write('### 2. 输入NFA的转移函数(无转移的状态不需要输入)')
nfa_transition_function = {}
for state in nfa_states:
    for symbol in nfa_alphabet | {''}:  # 添加ε到字母表中
        state_transitions = st.text_input(f'状态 {state} 对字母 {symbol if symbol else "ε"} 的转移 (用逗号分隔)', '').split(',')
        state_transitions = {s.strip() for s in state_transitions if s.strip()}  # 转换为集合
        if state_transitions:
            nfa_transition_function[(state, symbol)] = state_transitions

st.write('### 3. 输入NFA的起始状态和接受状态')
nfa_start_state = set(st.text_input('NFA的起始状态(状态之间用逗号隔开)', 'S,P').split(','))  # 转换为集合
nfa_accept_states = set(st.text_input('NFA的接受状态(状态之间用逗号隔开)', 'Z').split(','))  # 转换为集合

# 打印调试信息
print("NFA状态:", nfa_states)
print("NFA字母表:", nfa_alphabet)
print("NFA转移函数:", nfa_transition_function)
print("NFA起始状态:", nfa_start_state)
print("NFA接受状态:", nfa_accept_states)

if st.button('确定NFA'):
    # 创建 NFA 对象
    nfa = NFA.NFA(
        states=nfa_states,
        alphabet=nfa_alphabet,
        transition_function=nfa_transition_function,
        start_state=nfa_start_state,
        accept_states=nfa_accept_states
    )

    # 将 NFA 转换为 DFA
    dfa = NFA.nfa_to_dfa(nfa)
    NFA.draw(dfa)

    # 输出 DFA 的状态信息
    dfa_states_table = pd.DataFrame(
        {"状态": [str(sorted(state)) for state in dfa.states]}  # 对状态集合排序并转换为字符串
    )
    st.write("DFA 的状态信息:")
    st.dataframe(dfa_states_table)

    # 输出 DFA 的字母表
    dfa_alphabet_table = pd.DataFrame(
        {"字母表": [str(symbol) for symbol in dfa.alphabet]}  
    )
    st.write("DFA 的字母表:")
    st.dataframe(dfa_alphabet_table)

    # 输出 DFA 的转移函数
    dfa_transition_table = pd.DataFrame([
        {
            "当前状态": str(sorted(k[0])),  # 对当前状态排序并转换为字符串
            "输入符号": k[1],
            "下一个状态": str(sorted(v))  # 对下一个状态排序并转换为字符串
        }
        for k, v in dfa.transition_function.items()
    ])
    st.write("DFA 的转移函数:")
    st.dataframe(dfa_transition_table)

    # 输出 DFA 的起始状态和接受状态
    dfa_start_and_accept_state_table = pd.DataFrame(
        {
            "起始状态": [str(sorted(dfa.start_state))] * len(dfa.accept_states),  # 对起始状态排序
            "接受状态": [str(sorted(state)) for state in dfa.accept_states]  # 对接受状态排序
        }
    )
    st.write("DFA 的起始状态和接受状态:")
    st.dataframe(dfa_start_and_accept_state_table)

    # 输出 DFA 的状态图
    st.write("DFA 的状态图:")
    st.image("dfa_graph.png", caption="DFA 状态图", use_container_width=True)