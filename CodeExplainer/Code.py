import streamlit as st
import google.generativeai as genai
import os


def configure_genai(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring API: {e}")
        return False


def get_explanation(code_snippet, language):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an expert programming instructor. Please explain the following {language} code snippet clearly and concisely.

Structure your response exactly as follows:
1. **Summary**: A 1–2 sentence high-level overview of what the code does.
2. **Line-by-Line Breakdown**: Explain each significant line using bullet points.
3. **Key Concepts**: List the main programming concepts used.

Code Snippet:
{code_snippet}

css
Copy code
"""

    try:
        with st.spinner("Analyzing code..."):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Error generating explanation: {e}"


# Page configuration
st.set_page_config(
    page_title="Code Explainer with GenAI",
    page_icon="👨‍💻",
    layout="wide",
)


def main():
    # Sidebar
    with st.sidebar:
        st.header("🛞 Settings")
        default_key = os.getenv("GOOGLE_API_KEY", "")
        api_key = st.text_input(
            "Enter Google Gemini API Key",
            value=default_key,
            type="password",
            help="Get your key from https://aistudio.google.com/app/apikey",
        )
        st.markdown("---")
        st.markdown(
            "Built with [Streamlit](https://streamlit.io) and "
            "[Google Gemini](https://deepmind.google/technologies/gemini/)."
        )

    # Main content
    st.title("AI Code Explainer")
    st.markdown("Paste a code snippet below and I’ll explain it line by line.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Code")
        language = st.selectbox(
            "Select language (optional)",
            ["Python", "JavaScript", "Java", "C++", "HTML/CSS", "SQL", "Other"],
        )

        code_input = st.text_area(
            "Enter code",
            height=400,
            placeholder="def hello_world():\n    print('Hello, Streamlit')",
        )

        analyze_button = st.button(
            "🔍 Explain Code", use_container_width=True
        )

    with col2:
        st.subheader("Explanation")
        if analyze_button:
            if not api_key:
                st.warning("⚠️ Please enter your Google Gemini API key.")
            elif not code_input.strip():
                st.warning("⚠️ Please paste some code to analyze.")
            else:
                if configure_genai(api_key):
                    explanation = get_explanation(code_input, language)
                    st.markdown(explanation)


if __name__ == "__main__":
    main()