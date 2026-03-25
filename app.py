"""
中小学Python编程辅导助手
技术栈：Python + Streamlit + Claude API
面向中小学生的Python入门学习应用
"""

import streamlit as st
import os
from anthropic import Anthropic

# 获取 API 密钥的函数
def get_api_key():
    """优先级：输入框 > 环境变量"""
    if st.session_state.api_key:
        return st.session_state.api_key
    return os.environ.get("ANTHROPIC_API_KEY", "")

# 调用 AI 的函数
def get_ai_response():
    """调用 Claude API 获取回复"""
    client = Anthropic(api_key=st.session_state.api_key)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    )

    return response.content[0].text

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="Python小助手 - 中小学编程辅导",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS样式 ====================
custom_css = """
<style>
/* 全局字体设置 */
.stApp {
    font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #306998 0%, #2a5d8a 100%);
    color: white;
}

[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stSelectbox > div > div > select,
[data-testid="stSidebar"] .stTextArea > div > div > textarea {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
}

/* 标题样式 */
.stTitle {
    color: #306998 !important;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

/* 聊天消息容器 */
.chat-message {
    padding: 20px;
    border-radius: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 用户消息样式 */
.user-message {
    background: linear-gradient(135deg, #FFD43B 0%, #ffc800 100%);
    margin-left: 20%;
    text-align: right;
    border-bottom-right-radius: 5px;
}

/* 助手消息样式 */
.assistant-message {
    background: white;
    border-left: 5px solid #306998;
    margin-right: 20%;
    border-bottom-left-radius: 5px;
}

/* 代码块样式 */
.assistant-message pre {
    background-color: #f5f5f5;
    border-radius: 10px;
    padding: 15px;
    overflow-x: auto;
    border: 2px solid #FFD43B;
}

.assistant-message code {
    color: #306998;
    font-family: 'Consolas', 'Monaco', monospace;
}

/* 输入框样式 */
.stChatInput > div {
    border-radius: 25px;
    border: 3px solid #306998;
}

.stChatInput > div > div > textarea {
    border-radius: 20px;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #FFD43B 0%, #ffc800 100%);
    color: #306998;
    border: none;
    border-radius: 25px;
    padding: 10px 30px;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
}

/* 功能卡片样式 */
.feature-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-left: 4px solid #FFD43B;
    transition: transform 0.3s;
}

.feature-card:hover {
    transform: translateX(5px);
}

/* 示例按钮 */
.example-btn {
    background-color: #306998;
    color: white;
    padding: 8px 15px;
    border-radius: 15px;
    margin: 5px;
    display: inline-block;
    cursor: pointer;
    transition: all 0.3s;
}

.example-btn:hover {
    background-color: #FFD43B;
    color: #306998;
}

/* 装饰图标 */
.icon-decoration {
    font-size: 50px;
    text-align: center;
    margin: 20px 0;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* 成功/提示框 */
.success-box {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

.info-box {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

/* 页脚 */
.footer {
    text-align: center;
    padding: 20px;
    color: #306998;
    font-size: 14px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==================== 系统提示词 ====================
SYSTEM_PROMPT = """你是专业的中小学Python编程辅导老师。你的教学原则如下：

【知识范围】
仅讲解以下Python入门知识：
- print() 输出语句
- 变量与数据类型（整数、小数、字符串）
- 基本运算（加减乘除、求余）
- 条件语句（if-else）
- 循环（for、while）
- 基础函数定义
- 列表的基础操作

【教学风格】
1. 语言通俗易懂，用生活中的例子做类比
2. 每段代码都有详细注释，解释每一行的作用
3. 语气亲切耐心，多用鼓励的话（"你做得很好！"、"继续加油！"）
4. 循序渐进，一次只讲一个知识点

【代码辅导】
1. 帮学生找出错误并解释原因
2. 指出修改方向，但不直接给出完整答案
3. 鼓励学生自己思考和修改
4. 拒绝代写作业或完成编程比赛题目

【拒绝处理】
- 类、对象、继承等面向对象概念
- 装饰器、生成器、lambda等高级特性
- 异常处理、模块导入、文件操作等复杂功能
- 网络编程、数据库、GUI等实际应用
- 任何超出中小学大纲的内容

遇到超纲问题时，请温和说明："这个知识点你以后会学到，现在我们先打好基础哦！"然后引导到相关的基础知识点。"""

# ==================== 初始化会话 ====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🐍 你好呀！我是Python小助手，专门帮中小学生学习Python编程的！\n\n你可以问我：\n• \"Python怎么输出文字？\"\n• \"什么是变量呀？\"\n• \"帮我看看这段代码哪里错了\"\n• \"给我出个有趣的编程练习\"\n\n我们一起来快乐学编程吧！💪"}
    ]

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>🎓 Python学习助手</h2>", unsafe_allow_html=True)

    st.markdown("<div class='icon-decoration'>🐍</div>", unsafe_allow_html=True)

    # API Key 输入
    st.subheader("⚙️ 设置")
    # 从云端环境变量读取API Key，更安全
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if api_key:
        st.session_state.api_key = api_key
        st.markdown("<div class='success-box'>✅ API密钥已设置</div>", unsafe_allow_html=True)
    elif os.environ.get("ANTHROPIC_API_KEY"):
        st.session_state.api_key = os.environ.get("ANTHROPIC_API_KEY")
        st.markdown("<div class='success-box'>✅ 已使用云端配置的API密钥</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>ℹ️ 请设置API密钥后使用</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 快速入门示例
    st.subheader("📚 快速入门")
    examples = {
        "🖨️ print输出": "Python的print怎么用？",
        "📦 变量讲解": "什么是变量？给我举个例子",
        "🔄 循环结构": "for循环怎么写？",
        "🔀 条件语句": "if-else怎么用？",
        "📝 函数定义": "怎么定义一个函数？",
        "🐛 找错误": "帮我看下这个错在哪：print(Hello)",
        "🎮 趣味案例": "给我出个有趣的编程练习"
    }

    for icon, prompt in examples.items():
        if st.button(icon, key=prompt, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.last_example = prompt

            # 检查 API 密钥
            if get_api_key():
                try:
                    assistant_response = get_ai_response()
                except Exception as e:
                    error_str = str(e)
                    if "401" in error_str or "unauthorized" in error_str.lower():
                        assistant_response = "❌ API密钥错误：请检查你的密钥是否正确"
                    elif "429" in error_str or "rate limit" in error_str.lower():
                        assistant_response = "⏱️ 请求太频繁啦！请稍等一会儿再试哦~"
                    else:
                        assistant_response = f"😅 出错了：{error_str}"
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "⚠️ 请先在左侧设置你的Claude API密钥哦！"
                })
            st.rerun()

    # 显示最近使用的示例提示
    if "last_example" in st.session_state and st.session_state.last_example:
        st.caption(f"💡 已选择：{st.session_state.last_example}")

    st.markdown("---")

    # 清除聊天
    if st.button("🗑️ 清除聊天记录", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "🐍 记录已清除！我们重新开始吧！有什么问题尽管问我~"}
        ]
        st.rerun()

    st.markdown(f"<div class='footer'>适合：小学三年级~初中三年级</div>", unsafe_allow_html=True)

# ==================== 主界面 ====================
st.markdown("<div style='text-align: center;'><h1>🐍 Python编程小助手 🐍</h1></div>", unsafe_allow_html=True)

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👦" if message["role"] == "user" else "🐍"):
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

# ==================== 用户输入与响应 ====================
if prompt := st.chat_input("✍️ 输入你的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 显示用户消息
    with st.chat_message("user", avatar="👦"):
        st.markdown(f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True)

    # 检查API密钥
    if not get_api_key():
        # 检查最后一条消息是否已经是API密钥提示，避免重复
        last_msg = st.session_state.messages[-1] if st.session_state.messages else None
        is_duplicate = (last_msg and last_msg.get("role") == "assistant" and
                        "API密钥" in last_msg.get("content", ""))

        with st.chat_message("assistant", avatar="🐍"):
            st.markdown(f"<div class='chat-message assistant-message'>⚠️ 请先在左侧设置你的Claude API密钥哦！获取地址：https://console.anthropic.com/</div>", unsafe_allow_html=True)

        if not is_duplicate:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ 请先在左侧设置你的Claude API密钥哦！获取地址：https://console.anthropic.com/"
            })
    else:
        # 调用Claude API
        with st.chat_message("assistant", avatar="🐍"):
            with st.spinner("🐍 正在思考中..."):
                try:
                    client = Anthropic(api_key=st.session_state.api_key)

                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",  # 使用稳定版本
                        max_tokens=2000,
                        system=SYSTEM_PROMPT,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]
                    )

                    assistant_response = response.content[0].text

                except Exception as e:
                    error_str = str(e)
                    if "401" in error_str or "unauthorized" in error_str.lower():
                        assistant_response = "❌ API密钥错误：请检查你的密钥是否正确，或者密钥是否已过期。"
                    elif "429" in error_str or "rate limit" in error_str.lower():
                        assistant_response = "⏱️ 请求太频繁啦！请稍等一会儿再试哦~"
                    elif "500" in error_str or "502" in error_str or "503" in error_str:
                        assistant_response = "🔧 服务器暂时出问题啦，请稍后再试~"
                    elif "invalid_request" in error_str.lower() or "context_length" in error_str.lower():
                        assistant_response = "📄 对话内容太长啦，点击「清除聊天记录」重新开始吧！"
                    else:
                        assistant_response = f"😅 出错了：{error_str}\n\n请检查：\n1. API密钥是否正确\n2. 网络连接是否正常\n3. API余额是否充足"

            # 显示助手回复
            st.markdown(f"<div class='chat-message assistant-message'>{assistant_response}</div>", unsafe_allow_html=True)

            # 添加到历史
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# ==================== 底部信息 ====================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: #306998; font-size: 14px;'>
        📚 快乐学编程 • 轻松掌握Python • 从零开始学编程 🐍
    </div>
    """, unsafe_allow_html=True)
