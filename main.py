import streamlit as st
import pandas as pd
import os

# ---------- App Title ----------
st.title("🎓 Student Feedback Analyzer")

# ---------- Feedback Storage ----------
FEEDBACK_FILE = "feedback.csv"

# Create CSV file if not exists
if not os.path.exists(FEEDBACK_FILE):
    df = pd.DataFrame(columns=["Name", "Subject", "Rating", "Comment"])
    df.to_csv(FEEDBACK_FILE, index=False)

# ---------- Sidebar Navigation ----------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Submit Feedback", "Dashboard"])

# ---------- Submit Feedback Page ----------
if page == "Submit Feedback":
    st.subheader("✍️ Submit Feedback")

    name = st.text_input("Student Name")
    subject = st.selectbox("Subject", ["Math", "Science", "History", "English"])
    rating = st.slider("Rating (1=Poor, 5=Excellent)", 1, 5, 3)
    comment = st.text_area("Comment")

    if st.button("Submit"):
        if name.strip() == "":
            st.error("⚠️ Please enter your name before submitting.")
        else:
            # Append new feedback
            new_feedback = pd.DataFrame([[name, subject, rating, comment]],
                                        columns=["Name", "Subject", "Rating", "Comment"])
            df = pd.read_csv(FEEDBACK_FILE)
            df = pd.concat([df, new_feedback], ignore_index=True)
            df.to_csv(FEEDBACK_FILE, index=False)

            st.success(f"✅ Feedback submitted by {name} for {subject}!")

# ---------- Dashboard Page ----------
elif page == "Dashboard":
    st.subheader("📊 Feedback Dashboard")

    df = pd.read_csv(FEEDBACK_FILE)

    if df.empty:
        st.info("No feedback submitted yet.")
    else:
        # Show all feedback
        st.write("### All Feedback")
        st.dataframe(df)

        # Average rating by subject
        st.write("### 📈 Average Rating by Subject")
        avg_rating = df.groupby("Subject")["Rating"].mean().reset_index()
        st.bar_chart(avg_rating.set_index("Subject"))

        # Overall stats
        st.write("### 📌 Summary")
        st.metric("Total Feedbacks", len(df))
        st.metric("Average Rating", round(df["Rating"].mean(), 2))
