import streamlit as st
from textblob import TextBlob

st.title("📧 Email Sentiment Analyzer")

email_text = st.text_area("Paste your email text below:")

if st.button("Analyze"):
    if email_text.strip():
        blob = TextBlob(email_text)
        sentiment = blob.sentiment
        st.write("**Polarity:**", sentiment.polarity)
        st.write("**Subjectivity:**", sentiment.subjectivity)
        
        if sentiment.polarity > 0:
            st.success("The email has a positive tone 😊")
        elif sentiment.polarity < 0:
            st.error("The email has a negative tone 😟")
        else:
            st.info("The email seems neutral 😐")
    else:
        st.warning("Please enter some text to analyze.")
