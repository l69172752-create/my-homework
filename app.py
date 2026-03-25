import streamlit as st
from openai import OpenAI

# 设置页面配置
st.set_page_config(
    page_title="Python编程小助手",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式（100%原样保留你的设计）
st.markdown("""
<style>
/* 全局样式 */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

/* 主容器 */
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* 标题样式 */
.title-box {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 30px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    animation: fadeIn 1s ease-in;
}

/* 聊天容器 */
.chat-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* 消息样式 */
.chat-message {
    padding: 15px 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    line-height: 1.6;
    font-size: 16px;
    position: relative;
    animation: slideIn 0.3s ease-out;
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 60px;
    border-bottom-right-radius: 5px;
}

.assistant-message {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    margin-right: 60px;
    border-bottom-left-radius: 5px;
}

/* 按钮样式 */
.stButton>button {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255,107,107,0.3);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255,107,107,0.4);
}

/* 输入框样式 */
.stTextInput>div>div>input {
    border-radius: 25px;
    border: 2px solid #667eea;
    padding: 12px 20px;
    font-size: 16px;
}

/* 侧边栏样式 */
.css-1d391kg {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
}

/* 提示框样式 */
.success-box {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
    margin: 10px 0;
    font-weight: bold;
    text-align: center;
}

.info-box {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
    margin: 10px 0;
    font-weight: bold;
    text-align: center;
}

/* 动画效果 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

/* 代码块样式 */
pre {
    background: rgba(0, 0, 0, 0.8);
    color: #f8f8f2;
    border-radius: 10px;
    padding: 15px;
    overflow-x: auto;
    border-left: 4px solid #4ecdc4;
}

code {
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 主页面内容
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<div class='title-box'>🐍 Python编程小助手</div>", unsafe_allow_html=True)

# 侧边栏设置
with st.sidebar:
    st.markdown("## 🎯 功能菜单")
    st.markdown("---")
    
    st.subheader("⚙️ 设置")
    # 已填入你的DeepSeek密钥
    api_key = "sk-57d87bba45dd4a9ca835268569c3e5fc"
    st.session_state.api_key = api_key
    
    if api_key:
        st.markdown("<div class='success-box'>✅ API密钥已设置</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>⚠️ 请输入有效的API密钥</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📋 快速示例")
    examples = [
        "Python怎么打印Hello World?",
        "for循环怎么用?",
        "if判断语句讲解",
        "列表是什么?",
        "简单的Python小游戏"
    ]
    
    for i, example in enumerate(examples):
        if st.button(f"🔹 {example}", key=f"example_{i}"):
            st.session_state.messages = [{"role": "user", "content": example}]
    
    st.markdown("---")
    
    if st.button("🗑️ 清除聊天记录", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 使用提示")
    st.markdown("""
    - 适合**中小学Python基础学习**
    - 提问尽量**简单明确**
    - 代码会**详细讲解**
    - 耐心引导，循序渐进
    """)

# 聊天区域
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# 显示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-message user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 用户输入
prompt = st.chat_input("💬 请输入你的Python问题...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# AI回复处理（DeepSeek API）
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    if not hasattr(st.session_state, 'api_key') or not st.session_state.api_key:
        with st.chat_message("assistant", avatar="🐍"):
            st.markdown("<div class='chat-message assistant-message'>⚠️ 请先在左侧设置API密钥哦！</div>", unsafe_allow_html=True)
        st.session_state.messages.append({
            "role": "assistant",
            "content": "⚠️ 请先在左侧设置API密钥哦！"
        })
    else:
        try:
            with st.spinner("🤔 正在思考中..."):
                # DeepSeek 配置
                client = OpenAI(
                    api_key=st.session_state.api_key,
                    base_url="https://api.deepseek.com"
                )
                
                # 系统提示词
                system_prompt = """你是专业的中小学Python编程辅导老师。你的教学原则如下：
                【知识范围】只讲解Python基础语法、简单逻辑、入门知识，严格限制在中小学编程范围内。
                【教学风格】语言通俗、耐心细致、鼓励为主、循序渐进，多用比喻和生活例子。
                【回答要求】
                1. 代码简洁规范，带详细注释
                2. 讲解通俗易懂，避免专业术语
                3. 适合中小学生理解能力
                4. 积极鼓励，激发兴趣
                【禁止内容】
                - 不讲复杂算法、爬虫、黑客技术
                - 不讲解超出中小学范围的内容
                - 不回答编程以外的问题
                """
                
                # 构建消息
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
                
                # 调用DeepSeek API
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                assistant_response = response.choices[0].message.content
                
                # 显示AI回复
                with st.chat_message("assistant", avatar="🐍"):
                    st.markdown(f"<div class='chat-message assistant-message'>{assistant_response}</div>", unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                
        except Exception as e:
            error_msg = str(e).lower()
            if "401" in error_msg:
                reply = "❌ API密钥错误：请检查密钥是否正确。"
            elif "429" in error_msg:
                reply = "⏱️ 请求太频繁啦！请稍等一会儿再试哦~"
            else:
                reply = f"😅 出错了：{str(e)}"
            
            with st.chat_message("assistant", avatar="🐍"):
                st.markdown(f"<div class='chat-message assistant-message'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("</div>", unsafe_allow_html=True)
