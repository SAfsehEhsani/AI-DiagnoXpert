import streamlit as st
from groq import Groq  # Import the Groq client
from PIL import Image # Keep PIL for potential future use, but not used now
import os
import io

# --- Configuration ---
st.set_page_config(page_title="AI Doctor Assistant (Groq)", page_icon=":stethoscope:", layout="wide")

# --- Crucial Safety Disclaimer ---
st.title("🩺 AI Doctor Assistant (Informational Only - Powered by Groq)")
st.warning(
    """
    **Disclaimer:** This AI assistant is for informational purposes ONLY and CANNOT replace professional medical advice, diagnosis, or treatment.
    Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
    Never disregard professional medical advice or delay in seeking it because of something you have read from this AI.
    The AI's suggestions may be inaccurate or incomplete. Relying on this AI for medical decisions is strongly discouraged.
    **Image analysis features are not available in this version using the Groq API.**
    """
)

# --- API Key Input ---
# Use Streamlit secrets management for deployment:
# groq_api_key = st.secrets["GROQ_API_KEY"]
# Or environment variable:
# groq_api_key = os.getenv("GROQ_API_KEY")

# For simple demonstration, allow user input (less secure for shared apps)
groq_api_key = st.text_input("Enter your Groq API Key:", type="password", help="Get your key from GroqCloud Console")

# --- Groq Client Initialization ---
client = None
if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
        st.success("Groq Client Initialized Successfully!")
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        st.stop() # Stop execution if client fails to initialize

# --- AI Model Selection (Optional) ---
# You can let the user choose or fix it
available_models = ["llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"] # Add more as needed
selected_model = st.selectbox("Select Groq Model:", available_models, index=0)

# --- Groq API Call Function ---
def get_groq_response(prompt, model_name):
    """Gets response from the specified Groq model."""
    if not client:
        st.error("Groq client not initialized. Please enter a valid API key.")
        return None
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI medical information assistant providing general information. You are NOT a real doctor and must always state this clearly. Do not provide diagnoses. Focus on potential conditions, general precautions, and general OTC medicine types, always advising consultation with a healthcare professional."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
            temperature=0.7, # Adjust creativity/factualness
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False, # Set to True for streaming output if desired
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response from Groq: {e}")
        # Check for specific API key errors (example, might need refinement based on Groq errors)
        if "authentication" in str(e).lower():
             st.error("Your Groq API key seems invalid or expired. Please check it.")
        return None # Return None on error

# --- Main Application Logic ---
if client: # Proceed only if the client is successfully initialized

    st.header("Describe Your Symptoms")
    user_symptoms = st.text_area("Please list your symptoms in detail:", height=150)

    if st.button(f"Analyze Symptoms using {selected_model}"):
        if user_symptoms:
            # Construct a detailed prompt for the AI (similar to before)
            prompt = f"""
            **Act as a helpful AI medical information assistant (NOT a real doctor).**

            **User Symptoms:**
            {user_symptoms}

            **Instructions:**
            1.  **Analyze Symptoms:** Briefly analyze the provided symptoms based on general knowledge.
            2.  **Potential Conditions:** List 2-3 possible general conditions that *might* be associated with these symptoms. Clearly state these are POSSIBILITIES, require professional evaluation, and are NOT diagnoses.
            3.  **Recommended Precautions:** Suggest general precautions the user could take (e.g., rest, hydration, hygiene, avoiding triggers if known).
            4.  **General Medicine Types (Over-the-Counter):** Mention general types of over-the-counter medications that *might* help alleviate *some* symptoms (e.g., 'pain relievers like ibuprofen or acetaminophen for headache', 'antihistamines for suspected mild allergic reactions'). **DO NOT recommend specific prescription drugs or dosages.** Emphasize consulting a pharmacist or doctor before taking any medication.
            5.  **Crucial Disclaimer:** ALWAYS prominently include the following disclaimer: "This is AI-generated information and NOT a substitute for professional medical advice. Consult a doctor or qualified healthcare provider for diagnosis and treatment."

            **Output Format:** Use clear headings for each section (Potential Conditions, Precautions, General Medicine Types, Disclaimer). Ensure the disclaimer is highly visible.
            """
            with st.spinner(f"Groq AI ({selected_model}) is analyzing symptoms..."):
                response = get_groq_response(prompt, selected_model)
                if response:
                    st.subheader("AI Analysis Result:")
                    st.markdown(response) # Use markdown to render formatting
                else:
                    st.error("Could not get a response from the AI. Please check your API key and network connection.")
        else:
            st.warning("Please enter your symptoms first.")

    # --- Note about Image Analysis Removal ---
    st.markdown("---")
    st.info("ℹ️ Note: Image analysis functionality is currently unavailable as the Groq API used in this version does not support direct image input.")

else:
    st.info("Please enter your Groq API Key above to activate the assistant.")

st.markdown("---")
st.caption("Developed By Syed Afseh Ehsani.")