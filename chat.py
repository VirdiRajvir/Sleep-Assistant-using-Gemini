import streamlit as st
import google.generativeai as genai
import time


genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

#configurations -----------------------------------------
model = genai.GenerativeModel('gemini-1.0-pro-latest')

#---------------------------------------------------------
#Headers and text
st.subheader("Sleep Assistant", divider=True)
st.write("I am your very own Sleep Assistant. Using the power of a trained LLM, I will hold conversations, provide tips and play music to help you fight your insomnia")
st.write("Click the button to toggle relaxing music")
st.audio("sleep.mp3", format="audio/mp3")
st.divider()

st.subheader("Steps to start your sleeping journey: ")
st.write("I will measure your sentiment throughout our conversation, so that I can estimate if the conversation is effectively tackling your insomnia. The results of this measurement is shown in a progress bar, which is presented after every prompt. To make it easier for me to do so, kindly your prompt by providing information regarding how you are feeling as I provide tips")
st.divider()
#----------------------------------------------------------
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Progress tracker, which touches 100 when sleep objective is achieved, ending with celebratory balloons
if "progress" not in st.session_state:
    st.session_state.progress=0


if st.session_state.progress == 100:
    st.balloons()

    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with   st.chat_message(message["role"]):
        st.markdown(message["content"])
#---------------------------------------------------------

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")


# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    #st.session_state.progress += 1

    
# Display assistant response in chat message container
if prompt:
    with st.chat_message("assistant"):
        with st.spinner('Thinking...'):
            time.sleep(1)
        response = model.generate_content(prompt)
        response2 = model.generate_content("Give only a integer score, no decimals, for this statement, between -10 to 10, -10 being most negative and +10 being positive." + prompt)
        score = int(response2.text)
        newprog=st.session_state.progress+score
        if newprog < 0:
            newprog = 0
        elif newprog > 100:
            newprog = 100
        st.session_state.progress = newprog
    
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})


#popover for progress bar
with st.popover("Open Progress bar"):
    progress_text = "Progress:"
    my_bar = st.progress(st.session_state.progress, text=progress_text)