import pandas as pd
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os


#Main Title and Caption
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align:left; color:#6EE7B7; margin:0;'>✦ Job Description Analyzer</h2>",
    unsafe_allow_html=True
)

# st.title("JOB DESCRIPTION ANALYZER")
st.caption("Analyze Job Description according to the skills")
st.divider()

#Main Variables
var = st.text_area("Paste Job Description")
skills=["python", "sql", "fastapi", "langchain", "pandas", "docker","html","css","javascript","rest api","ruby","java","aws"]
user_Skills=[word.strip().lower() for word in var.split()]

st.session_state.setdefault("match",[])
st.session_state.setdefault("missing",[])
st.session_state.setdefault("percentage",0)

#Main Analyze logic
if st.button("Analyze JD"):
    st.session_state["match"] = []
    st.session_state["missing"] = []
    if var!="":
        for i in skills:
            if i  in var.lower():
                st.session_state["match"].append(i)
            else:
                st.session_state["missing"].append(i)
    else:
        st.warning("Please paste a job description.")

#Main Display section
    c1,c2=st.columns(2)
    with c1:
        with st.container(height=300,border=True):
            st.subheader(f"Missing Skills({len(st.session_state['missing'])})")
            for items in st.session_state["missing"]:
                st.markdown(f"• {items}")

    with c2:
        with st.container(height=300,border=True):
            st.subheader(f"Match Skills({len(st.session_state['match'])})")
            for items in st.session_state["match"]:
                st.markdown(f"• {items}")

    st.session_state["percentage"]=round(len(st.session_state["match"])/len(skills)*100,2)
    st.metric(
        label="Percentage",
        value=(f"{st.session_state['percentage']}%"),
        delta=15,
        delta_color="normal",
    )
    st.bar_chart(
        pd.DataFrame(
            {"Skills": [len(st.session_state["match"]), len(st.session_state["missing"])]},
            index=["Matched Skills", "Missing Skills"]
        ),
        horizontal=True
    )


#Calling LLM 
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

prompt = f"""
Analyze this job description as an AI career advisor.
Explain the most important missing skills, why they matter,
learning priorities, and one practical project.

Job Description: {var}
Matched Skills: {st.session_state["match"]}
Missing Skills: {st.session_state["missing"]}

Keep it concise and beginner-friendly.
"""

st.session_state.setdefault("responce", "")

#AI Advice button Logic
if st.button("Get AI Advice"): 
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        st.session_state["responce"]=response.text

    except Exception as e:
        st.error(f"Something went wrong: {e}")

#Remove button Logic
if st.button("Remove Responce"):
    st.session_state["responce"] =""
    # st.write("removed")

if (st.session_state["responce"]!=""):
    st.write(st.session_state["responce"])

