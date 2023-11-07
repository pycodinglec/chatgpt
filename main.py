import openai
import streamlit as st
import os

# GPT_MODEL = 'gpt-3.5-turbo'
GPT_MODEL = 'gpt-4-1106-preview'

def initialize_conversation():
    system_message = 'You are a helpful assistant'
    hello_message = '안녕하세요, 무엇을 도와드릴까요?'
    return [
        {'role': 'system', 'content': system_message},
        {'role': 'assistant', 'content': hello_message}
    ]


def main():
    st.title('ChatGPT - for personal use')    
    openai.api_key = os.getenv('OPENAI_API_KEY') # for debug
     
    if 'msgs' not in st.session_state:
        st.session_state['msgs'] = initialize_conversation()

    for msg in st.session_state['msgs'][1:]:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    
    if prompt:= st.chat_input("Prompt"):
        st.session_state['msgs'].append({'role':'user', 'content': prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            responses = openai.ChatCompletion.create(
                model = GPT_MODEL,
                messages = st.session_state['msgs'],
                stream = True,
            )
            for response in responses:
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state['msgs'].append({"role": "assistant", "content": full_response})

if __name__=='__main__':
    main()
