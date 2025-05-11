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
