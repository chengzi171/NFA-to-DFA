from graphviz import Digraph

class NFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

def draw(dfa):
    """使用 Graphviz 绘制 DFA 图"""
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")  # 从左到右绘制

    # 添加状态节点
    for state in dfa.states:
        # 对状态集合排序并转换为字符串
        state_label = str(sorted(state))  # 将 frozenset 转换为排序后的字符串
        if state in dfa.accept_states:
            dot.node(state_label, shape="doublecircle")  # 接受状态用双圆表示
        else:
            dot.node(state_label, shape="circle")  # 普通状态用单圆表示

    # 添加起始状态箭头
    start_label = str(sorted(dfa.start_state))  # 对起始状态排序并转换为字符串
    dot.node("start", shape="none", label="")  # 起始箭头的虚拟节点
    dot.edge("start", start_label)

    # 添加转移关系
    for (current_state, symbol), next_state in dfa.transition_function.items():
        current_label = str(sorted(current_state))  # 对当前状态排序并转换为字符串
        next_label = str(sorted(next_state))  # 对下一个状态排序并转换为字符串
        dot.edge(current_label, next_label, label=symbol)

    # 保存并渲染图像
    dot.render("dfa_graph", view=False)  # 保存为 dfa_graph.png 

def epsilon_closure(nfa, states):
    """计算给定状态集合的 ε 闭包"""
    closure = set(states)  # 初始化闭包为自身
    stack = list(states)  # 使用栈来处理状态

    while stack:
        state = stack.pop()
        # 如果存在 ε 转换，加入闭包
        if (state, '') in nfa.transition_function:
            for next_state in nfa.transition_function[(state, '')]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

    return frozenset(closure)  # 返回 frozenset

def nfa_to_dfa(nfa):
    """将 NFA 转换为 DFA"""
    # 初始化 DFA 的状态
    dfa_states = []  # DFA 状态集合
    dfa_transition_function = {}  # DFA 转移函数
    dfa_start_state = epsilon_closure(nfa, nfa.start_state)  # 计算起始状态的 ε 闭包
    dfa_start_state = frozenset(dfa_start_state)  # 转换为 frozenset
    dfa_accept_states = set()  # DFA 接受状态集合

    # 待处理的状态队列
    unprocessed_states = [dfa_start_state]  # 队列初始化为 DFA 的起始状态
    processed_states = set()  # 已处理的状态集合

    while unprocessed_states:
        current_state = unprocessed_states.pop(0)  # 取出队列的第一个状态
        processed_states.add(current_state)  # 将当前状态标记为已处理

        # 如果当前状态包含 NFA 的接受状态，则它是 DFA 的接受状态
        if any(state in nfa.accept_states for state in current_state):
            dfa_accept_states.add(current_state)

        # 计算当前状态对每个字母的转移
        for symbol in nfa.alphabet:
            next_state = set()  # 用于存储下一个状态集合
            for sub_state in current_state:  # 遍历当前状态集合中的每个状态
                if (sub_state, symbol) in nfa.transition_function:  # 检查是否有转移
                    next_state.update(nfa.transition_function[(sub_state, symbol)])  # 更新下一个状态集合

            # 计算转移后状态的 ε 闭包
            next_state = epsilon_closure(nfa, next_state)
            next_state = frozenset(next_state)  # 转换为 frozenset
            dfa_transition_function[(current_state, symbol)] = next_state  # 更新 DFA 转移函数

            # 如果新状态未处理过，则加入队列
            if next_state not in processed_states and next_state not in unprocessed_states:
                unprocessed_states.append(next_state)  # 将新状态加入待处理队列

    # 将所有状态收集到 DFA 的状态集合中
    dfa_states = list(processed_states)

    return DFA(dfa_states, nfa.alphabet, dfa_transition_function, dfa_start_state, dfa_accept_states)

# 示例用法
if __name__ == "__main__":
    # 示例 NFA
    nfa_states = {"S", "P", "Z"}
    nfa_alphabet = {"0", "1"}
    nfa_transition_function = {
        ("S", "0"): {"P"},
        ("S", "1"): {"S", "Z"},
        ("P", ""): {"Z"},
        ("Z", "0"): {"P"},
        ("Z", "1"): {"P"}
    }
    nfa_start_state = {"S", "P"}
    nfa_accept_states = {"q2"}

    nfa = NFA(nfa_states, nfa_alphabet, nfa_transition_function, nfa_start_state, nfa_accept_states)

    # 将 NFA 转换为 DFA
    dfa = nfa_to_dfa(nfa)

    # 输出 DFA 的信息
    print("DFA States:", dfa.states)
    print("DFA Alphabet:", dfa.alphabet)
    print("DFA Transition Function:", dfa.transition_function)
    print("DFA Start State:", dfa.start_state)
    print("DFA Accept States:", dfa.accept_states)

    draw(dfa)