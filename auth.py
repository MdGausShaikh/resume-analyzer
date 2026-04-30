import streamlit as st

USERS = {
    "admin": "1234",
    "gaus": "resumeai",
    "recruiter": "resume123"
}


def login():

    st.markdown("""
    <style>
    .stApp{
        background: linear-gradient(135deg,#0f172a,#1e293b,#334155);
    }

    header, #MainMenu, footer{
        visibility:hidden;
    }

    .block-container{
        padding-top:1rem !important;
        max-width:100%;
    }

    .brand-logo{
        text-align:center;
        font-size:72px;
        margin-top:5px;
        margin-bottom:5px;
    }

    .brand-name{
        text-align:center;
        font-size:42px;
        font-weight:800;
        color:white;
    }

    .brand-sub{
        text-align:center;
        font-size:15px;
        color:#dbeafe;
        margin-bottom:20px;
    }

    div[data-testid="stForm"]{
        background:rgba(255,255,255,0.97);
        padding:32px;
        border-radius:22px;
        box-shadow:0 10px 28px rgba(0,0,0,0.25);
    }

    .login-title{
        color:#0f172a;
        font-size:28px;
        font-weight:800;
        text-align:center;
        margin-bottom:15px;
    }

    .stTextInput label{
        color:#0f172a !important;
        font-weight:700 !important;
    }

    .stTextInput>div>div>input{
        border-radius:12px;
        border:1px solid #dbe2ea;
        padding:12px;
    }

    .stFormSubmitButton>button{
        width:100%;
        background:linear-gradient(135deg,#0f172a,#1e293b);
        color:white;
        border:none;
        border-radius:12px;
        padding:12px;
        font-weight:700;
    }

    .mini-text{
        text-align:center;
        color:#475569;
        font-size:14px;
        line-height:1.8;
        margin-top:18px;
    }
    </style>
    """, unsafe_allow_html=True)

    l, c, r = st.columns([1,1.1,1])

    with c:
        st.markdown("<div class='brand-logo'>🧠</div>", unsafe_allow_html=True)
        st.markdown("<div class='brand-name'>ResumeIQ1</div>", unsafe_allow_html=True)
        st.markdown("<div class='brand-sub'>Enterprise AI Resume Intelligence & Hiring Platform</div>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<div class='login-title'>🔐 Secure Recruiter Login</div>", unsafe_allow_html=True)

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Login to Dashboard")

            st.markdown("""
            <div class='mini-text'>
            📄 ATS Screening<br>
            🤖 AI Career Coach<br>
            📊 Recruiter Analytics<br>
            📥 PDF Reports<br><br>
            </b>
            </div>
            """, unsafe_allow_html=True)

            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
