import streamlit as st
from zhipuai import ZhipuAI

# 1. 网页全局配置
st.set_page_config(page_title="AI 嘴替神器", page_icon="🎭")

# 2. 侧边栏配置
with st.sidebar:
    st.header("⚙️ 控制面板")
    st.markdown("在这里配置你的 AI 大脑")
    
    user_api_key = st.text_input("🔑 请输入智谱 API Key：", type="password")
    st.divider() 
    
    personas = {
        "温柔贴心小天使 (INFP)": "你是一个有着多年恋爱经验的恋爱高手，说话温柔，体贴入微，高情商，谦虚，语气真诚，射手座，INFP。",
        "冷酷无情霸道总裁 (ENTJ)": "你是雷厉风行、极其强势的职场高管。你的回复需要极其简短、直击要害，高冷且具有压迫感，不用顾忌对方感受，但不能爆粗口。白羊座，ENTJ。",
        "金牌销售 (ESTP)": "你能力强、会沟通，懂客户，专业守信敢开口，情绪稳定，懂人性，专业靠谱、执行力强，能察觉需求，善于表达，守信坚韧、业绩稳定，非常了解计算机考研、调剂、陕师大计算机考研相关信息，态度真诚，不废话，ESTP，你的主要任务是为了推销你的复试资料。"
    }
    selected_style = st.selectbox("🎭 选择 AI 人设：", list(personas.keys()))

# 3. 主界面
st.title("✨ 高情商嘴替神器 Pro Max")
st.markdown("收到棘手的消息不知道怎么回？让 AI 帮你高情商圆场！")

boss_message = st.text_area("📩 别人发给你的消息是：", "这只荷兰猪可爱嘛")
my_thought = st.text_input("💭 你的真实想法是：", "它看着笨死了还贪吃")

# 4. 核心生成逻辑
if st.button("🚀 帮我生成神回复"):
    if not user_api_key:
        st.warning("⚠️ 哎呀，你还没在左侧边栏输入 API Key 呢！")
    else:
        client = ZhipuAI(api_key=user_api_key)
        with st.spinner(f"AI 正在以【{selected_style}】的身份疯狂构思中..."):
            
            response = client.chat.completions.create(
                model="glm-4",  
                messages=[
                    {"role": "system", "content": personas[selected_style]},
                    {"role": "user", "content": f"对方发来消息：{boss_message}\n我的真实想法是：{my_thought}\n请帮我写一段回复。"}
                ]
            )
            
            # 把 AI 的回复提取出来存入一个变量
            reply_text = response.choices[0].message.content
            
            st.success("搞定！请看我的表演：")
            
            # 🌟 进阶魔法 4：利用 st.code 实现一键复制！
            # language="text" 保证它显示为普通文本而不是彩色的代码
            st.code(reply_text, language="text")
            
            # 🌟 进阶魔法 5：生成成功后，放个气球庆祝一下！
            st.balloons()