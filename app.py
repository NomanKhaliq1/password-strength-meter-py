import streamlit as st
import pyzxcvbn

# Modern UI Styling
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 14px;
        border-radius: 8px;
        border: none !important;  /* Fix: Removes extra borders */
        outline: none !important;
        background-color: #212529;
        color: white;
        width: 100%;
    }
    .stTextInput>div {
        position: relative;
        padding: 0px;
        height: 60px;
    }
    .stTextInput>div>div {
        display: flex;
        align-items: center;
    }
    .stTextInput>div>div>button {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: transparent;
        border: none;
        color: white;
    }
    .stMarkdown { text-align: center; }
    .strength-meter {
        padding: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        border-radius: 8px;
        margin-top: 10px;
    }
    .info-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-top: 10px;
    }
    .comp-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
    }
    .green { color: #0f9d58; font-weight: bold; }
    .red { color: #ff4b4b; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>Password Strength Meter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Try to make your passwords at least <b>15 characters long</b></p>", unsafe_allow_html=True)

# **Session state to prevent re-rendering multiple times**
if "password_input" not in st.session_state:
    st.session_state["password_input"] = ""

# **Function to check password strength**
def check_password_strength(password):
    if password:
        result = pyzxcvbn.zxcvbn(password)
        score = result['score']
        
        # Strength levels & colors
        strength_levels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
        colors = ["#ff4b4b", "#ffa500", "#f4d03f", "#4285F4", "#0f9d58"]

        # **Show strength meter**
        st.markdown(
            f"<div class='strength-meter' style='background-color:{colors[score]};'>"
            f"{strength_levels[score]}</div>",
            unsafe_allow_html=True
        )

        # **Time to crack**
        st.markdown(
            f"<div class='info-box'>⏳ <b>Time to crack your password:</b> {result['crack_times_display']['offline_slow_hashing_1e4_per_second']}</div>",
            unsafe_allow_html=True
        )

        # **Password composition horizontally**
        st.markdown(
            f"""
            <div class='comp-container'>
                <span>🔡 Lowercase: <span class='{"green" if any(c.islower() for c in password) else "red"}'>{"✅" if any(c.islower() for c in password) else "❌"}</span></span>
                <span>🔠 Uppercase: <span class='{"green" if any(c.isupper() for c in password) else "red"}'>{"✅" if any(c.isupper() for c in password) else "❌"}</span></span>
                <span>🔢 Numbers: <span class='{"green" if any(c.isdigit() for c in password) else "red"}'>{"✅" if any(c.isdigit() for c in password) else "❌"}</span></span>
                <span>🔣 Symbols: <span class='{"green" if any(not c.isalnum() for c in password) else "red"}'>{"✅" if any(not c.isalnum() for c in password) else "❌"}</span></span>
            </div>
            """,
            unsafe_allow_html=True
        )

# **Real-time password input (Fixes 'Enter to Apply' Issue)**
password = st.text_input("Type a password", type="password", key="password_input")
check_password_strength(password)
