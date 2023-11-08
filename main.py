from openai import OpenAI
import streamlit as st
import os
import hashlib

client = OpenAI()

# GPT_MODEL = 'gpt-3.5-turbo'
GPT_MODEL = 'gpt-4-1106-preview'

def initialize_conversation():
    system_message = 'You are a helpful assistant'
    hello_message = '안녕하세요, 무엇을 도와드릴까요?'
    return [
        {'role': 'system', 'content': system_message},
        {'role': 'assistant', 'content': hello_message}
    ]

def chatbot_page():
    st.title('ChatGPT - for personal use')
    #openai.api_key = os.getenv('OPENAI_API_KEY') # for debug
     
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
            try:
                responses = client.chat.completions.create(
                    model=GPT_MODEL,
                    messages=st.session_state['msgs'],
                    stream=True,
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
            for response in responses:
                if response.choices[0].delta.content:
                    full_response += response.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state['msgs'].append({"role": "assistant", "content": full_response})

def verify_password(input_password):
    correct_password_hash = os.getenv('PASSWORD_HASH')
    password_hash = hashlib.md5(input_password.encode()).hexdigest()
    return password_hash == correct_password_hash

def main():
    with st.container():
        input_password = st.text_input("패스워드를 입력하세요", type="password")
        if st.button("로그인"):
            if verify_password(input_password):
                st.session_state['authenticated'] = True
            else:
                st.error("패스워드가 잘못되었습니다.")

    if st.session_state.get('authenticated', False):
        chatbot_page()

if __name__=='__main__':
    main()
