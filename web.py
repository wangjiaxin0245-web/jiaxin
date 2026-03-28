import streamlit as st
from zhipuai import ZhipuAI

st.set_page_config(page_title="AI 嘴替神器", page_icon="🎭")

# ==========================================
# ⚙️ 侧边栏：控制面板
# ==========================================
with st.sidebar:
    st.header("⚙️ 控制面板")
    user_api_key = st.text_input("🔑 请输入智谱 API Key：", type="password")
    st.divider() 
    
    personas = {
        "温柔贴心小天使 (INFP)": "你是一个有着多年恋爱经验的恋爱高手，说话温柔，体贴入微，高情商，谦虚，语气真诚，射手座，INFP。",
        "冷酷无情霸道总裁 (ENTJ)": "你是雷厉风行、极其强势的职场高管。你的回复需要极其简短、直击要害，高冷且具有压迫感，不用顾忌对方感受，但不能爆粗口。白羊座，ENTJ。",
        "金牌销售 (ESTP)": "你能力强、会沟通，懂客户，专业守信敢开口，情绪稳定，懂人性，专业靠谱、执行力强，能察觉需求，善于表达，守信坚韧、业绩稳定，非常了解计算机考研、调剂、陕师大计算机考研相关信息，态度真诚，不废话，ESTP，你的主要任务是为了推销你的复试资料。"
    }
    selected_style = st.selectbox("🎭 选择 AI 人设：", list(personas.keys()))
    
    st.divider()
    # 🌟 进阶魔法 1：增加一个联网开关！
    st.markdown("### 🌐 进阶超能力")
    enable_search = st.toggle("开启 5G 冲浪模式 (结合实时天气/热搜抖机灵)")

# ==========================================
# 🖥️ 主界面
# ==========================================
st.title("✨ 高情商嘴替神器 5G 联网版")
st.markdown("收到棘手的消息不知道怎么回？让 AI 帮你高情商圆场！")

boss_message = st.text_area("📩 别人发给你的消息是：", "周末去哪玩呀？")
my_thought = st.text_input("💭 你的真实想法是：", "哪都不去，想在家躺尸")

if st.button("🚀 帮我生成神回复"):
    if not user_api_key:
        st.warning("⚠️ 哎呀，你还没在左侧边栏输入 API Key 呢！")
    else:
        client = ZhipuAI(api_key=user_api_key)
        
        # 🌟 进阶魔法 2：根据开关，决定给 AI 什么样的指令
        final_prompt = f"对方发来消息：{boss_message}\n我的真实想法是：{my_thought}\n请帮我写一段回复。"
        
        # 如果用户打开了开关，就在指令后面悄悄加上一句“紧箍咒”
        if enable_search:
            final_prompt += "\n(特别要求：请先调用网页搜索工具，查询今天的实时天气或热门微博热搜，并极其巧妙、幽默地将这些实时信息结合到你的回复中！)"
            
        # 🌟 进阶魔法 3：配置工具库（给 AI 发放上网许可证）
        tools_config = [{"type": "web_search", "web_search": {"enable": True}}] if enable_search else None

        with st.spinner(f"AI 正在构思中...{' (正在全网冲浪搜集中 🏄‍♂️)' if enable_search else ''}"):
            response = client.chat.completions.create(
                model="glm-4",  
                messages=[
                    {"role": "system", "content": personas[selected_style]},
                    {"role": "user", "content": final_prompt}
                ],
                # 把工具包递给 AI
                tools=tools_config
            )
            
            reply_text = response.choices[0].message.content
            st.success("搞定！请看我的表演：")
            st.code(reply_text, language="text")
            st.balloons()
