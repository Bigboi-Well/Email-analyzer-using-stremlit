import streamlit as st
import json
from datetime import datetime
from textblob import TextBlob

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Email Analyzer", page_icon="📧")
st.title("📧 Email Analysis Workshop")
st.write("Learn Python with AI-powered email analysis!")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("---")
st.sidebar.write("🎓 **Workshop Topics Covered:**")
st.sidebar.write("• File Database (JSON)")
st.sidebar.write("• AI Sentiment Analysis")
st.sidebar.write("• Phishing Detection")
st.sidebar.write("• Data Visualization")

# ---------------- AI CHECK FUNCTION ----------------
def ai_check(text):
    """
    Analyze text for sentiment and phishing indicators
    Returns: sentiment, security_status, sentiment_score
    """
    sentiment_score = TextBlob(text).sentiment.polarity

    if sentiment_score >= 0.05:
        sentiment = "😊 Positive"
    elif sentiment_score <= -0.05:
        sentiment = "😔 Negative"
    else:
        sentiment = "😐 Neutral"

    phishing_words = [
        "urgent", "click now", "verify account", "suspended",
        "limited time", "act now", "money", "free"
    ]
    phishing_count = sum(1 for word in phishing_words if word.lower() in text.lower())

    if phishing_count >= 2:
        security = "🚨 Possible Phishing"
    elif phishing_count == 1:
        security = "⚠️ Be Careful"
    else:
        security = "✅ Looks Safe"

    return sentiment, security, sentiment_score

# ---------------- DATABASE FUNCTIONS ----------------
def load_emails():
    try:
        with open("workshop_database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_emails(emails):
    with open("workshop_database.json", "w") as f:
        json.dump(emails, f, indent=2)

# ---------------- MAIN APP ----------------
tab1, tab2, tab3 = st.tabs(["✍️ Write Email", "📥 Inbox", "📊 Stats"])

# ---------- TAB 1: WRITE EMAIL ----------
with tab1:
    st.header("Write New Email")
    emails = load_emails()

    subject = st.text_input("Subject:")
    message = st.text_area("Message:", height=200)

    if st.button("📤 Send Email"):
        if subject and message:
            sentiment, security, score = ai_check(message)
            email = {
                "subject": subject,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "sentiment": sentiment,
                "security": security,
                "score": score
            }
            emails.append(email)
            save_emails(emails)
            st.success("✅ Email sent and saved to database!")
            st.info(f"AI Analysis: {sentiment} | {security}")
        else:
            st.error("Please fill in both subject and message!")

# ---------- TAB 2: INBOX ----------
with tab2:
    st.header("Email Inbox")
    emails = load_emails()

    if emails:
        for email in reversed(emails):
            with st.expander(f"📧 {email['subject']} - {email['timestamp']}"):
                st.write(f"**Message:** {email['message']}")
                st.write(f"**AI Sentiment:** {email['sentiment']}")
                st.write(f"**Security Check:** {email['security']}")
    else:
        st.info("No emails yet. Write your first email!")

# ---------- TAB 3: STATISTICS ----------
with tab3:
    st.header("Email Statistics")
    emails = load_emails()

    if emails:
        positive = sum(1 for e in emails if "😊" in e["sentiment"])
        negative = sum(1 for e in emails if "😔" in e["sentiment"])
        neutral = sum(1 for e in emails if "😐" in e["sentiment"])

        st.subheader("📈 Sentiment Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("😊 Positive", positive)
        col2.metric("😐 Neutral", neutral)
        col3.metric("😔 Negative", negative)

        sentiment_data = {"Sentiment": ["Positive", "Neutral", "Negative"],
                          "Count": [positive, neutral, negative]}
        st.bar_chart(sentiment_data, x="Sentiment", y="Count")

        st.subheader("🛡️ Security Analysis")
        safe = sum(1 for e in emails if "✅" in e["security"])
        warning = sum(1 for e in emails if "⚠️" in e["security"])
        phishing = sum(1 for e in emails if "🚨" in e["security"])

        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Safe", safe)
        col2.metric("⚠️ Careful", warning)
        col3.metric("🚨 Phishing", phishing)

        security_data = {"Security": ["Safe", "Careful", "Phishing"],
                         "Count": [safe, warning, phishing]}
        st.bar_chart(security_data, x="Security", y="Count")

        st.subheader("📉 Sentiment Trend Over Time")
        scores = [email["score"] for email in emails]
        score_data = {"Email Index": range(1, len(scores) + 1),
                      "Sentiment Score": scores}
        st.line_chart(score_data, x="Email Index", y="Sentiment Score")
    else:
        st.info("No data to analyze yet!")
