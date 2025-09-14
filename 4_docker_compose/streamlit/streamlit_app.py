import streamlit as st
import requests
import plotly.graph_objects as go
import time

# Configure page
st.set_page_config(
    page_title="AI Sentiment Analyzer",
    page_icon="🤖",
    layout="wide"
)

# App header
st.title("🤖 AI Sentiment Analysis Service")
st.markdown("**Powered by Docker Compose + FastAPI + Redis + TextBlob**")

# API endpoint (Docker Compose networking)
API_URL = "http://fastapi-service:8000"

def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def analyze_text(text):
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"text": text},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Sidebar - Service Status
with st.sidebar:
    st.header("🔧 Service Status")
    if check_api_health():
        st.success("✅ API Service Online")
        st.success("✅ Redis Cache Online")
    else:
        st.error("❌ API Service Offline")
    
    st.markdown("---")
    st.markdown("**Architecture:**")
    st.markdown("- 🎯 Streamlit Frontend")
    st.markdown("- ⚡ FastAPI ML Service") 
    st.markdown("- 🗄️ Redis Cache")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Text Analysis")
    
    # Text input
    user_text = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type something here... (e.g., 'I love this new AI service!')"
    )
    
    analyze_button = st.button("🚀 Analyze Sentiment", type="primary")
    
    if analyze_button and user_text.strip():
        with st.spinner("Analyzing sentiment..."):
            start_time = time.time()
            result = analyze_text(user_text)
            analysis_time = time.time() - start_time
        
        if result:
            st.success("Analysis Complete!")
            
            # Results display
            col1_result, col2_result = st.columns(2)
            
            with col1_result:
                st.metric("Sentiment", result["sentiment"])
                st.metric("Confidence", result["confidence"])
            
            with col2_result:
                st.metric("Polarity Score", result["polarity"])
                cache_status = "🟢 From Cache" if result["cached"] else "🔵 Fresh Analysis"
                st.metric("Cache Status", cache_status)
            
            # Polarity visualization
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = result["polarity"],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Sentiment Polarity"},
                delta = {'reference': 0},
                gauge = {
                    'axis': {'range': [-1, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-1, -0.2], 'color': "lightcoral"},
                        {'range': [-0.2, 0.2], 'color': "lightgray"},
                        {'range': [0.2, 1], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance metrics
            st.info(f"⏱️ Analysis completed in {analysis_time:.3f} seconds")
    
    elif analyze_button:
        st.warning("Please enter some text to analyze!")

with col2:
    st.header("📊 Quick Examples")
    
    example_texts = [
        "I absolutely love this new AI technology!",
        "This service is okay, nothing special.",
        "I'm really disappointed with these results.",
        "The weather today is quite nice.",
        "This Docker tutorial is incredibly helpful!"
    ]
    
    for i, example in enumerate(example_texts):
        if st.button(f"Example {i+1}", key=f"example_{i}"):
            st.session_state.example_text = example
            st.experimental_rerun()
    
    if hasattr(st.session_state, 'example_text'):
        st.text_area("Selected example:", st.session_state.example_text, height=100, disabled=True)

# Footer
st.markdown("---")
st.markdown("**Built with Docker Compose** | FastAPI + Streamlit + Redis")