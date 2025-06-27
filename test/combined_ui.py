"""
Insight Project - Combined UI
Unified Streamlit interface for all three AI services
"""

import streamlit as st
import requests

# Configure Streamlit page
st.set_page_config(
    page_title="🧠 Insight Project - AI Services Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown(
    """
<style>
.main-header {
    background: linear-gradient(90deg, #2c3e50, #3498db, #9b59b6);
    color: white;
    padding: 2rem;
    text-align: center;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.service-header {
    background: linear-gradient(90deg, #e74c3c, #f39c12);
    color: white;
    padding: 1rem;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 1rem;
}
.status-success { color: #27ae60; font-weight: bold; }
.status-warning { color: #f39c12; font-weight: bold; }
.status-error { color: #e74c3c; font-weight: bold; }
.info-box {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #3498db;
    margin: 1rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)


def check_api_connection():
    """Check if API is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, (
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        return False, str(e)


def main():
    """Main application"""

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🧠 Insight Project - AI Services Platform</h1>
        <p>Unified platform for AI-powered document and image analysis</p>
        <p>📋 Form Reader | 💰 Money Reader | 📄 PPT/PDF Reader</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check API connection
    api_connected, api_info = check_api_connection()

    if not api_connected:
        st.error(f"❌ Cannot connect to API at {API_BASE_URL}")
        st.error(f"Error: {api_info}")
        st.info("💡 Make sure the server is running with the start script")
        st.stop()

    # Display API status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ API Connected")
    with col2:
        if api_info:
            st.info(f"🔄 Status: {api_info.get('status', 'Unknown')}")
    with col3:
        if api_info:
            st.info(f"📊 Sessions: {api_info.get('total_sessions', 0)}")

    # Service tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Form Reader", "💰 Money Reader", "📄 PPT/PDF Reader", "ℹ️ System Info"]
    )

    with tab1:
        form_reader_interface()

    with tab2:
        money_reader_interface()

    with tab3:
        ppt_pdf_reader_interface()

    with tab4:
        system_info_interface(api_info)


def form_reader_interface():
    """Form Reader service interface"""
    st.markdown(
        """
    <div class="service-header">
        <h2>📋 Form Reader - AI-Powered Form Analysis</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["png", "jpg", "jpeg"], key="form_upload"
    )

    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language", ["ar", "en"], key="form_lang")
    with col2:
        include_boxes = st.checkbox(
            "Include box detection", value=True, key="form_boxes"
        )

    if uploaded_file and st.button("🔍 Analyze Form", key="form_analyze"):
        with st.spinner("Analyzing form..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/form-reader/upload-image",
                    files={"file": uploaded_file},
                    data={"language": language, "include_boxes": include_boxes},
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis complete!")
                    st.json(result)
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def money_reader_interface():
    """Money Reader service interface"""
    st.markdown(
        """
    <div class="service-header">
        <h2>💰 Money Reader - Currency Detection</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["png", "jpg", "jpeg"], key="money_upload"
    )

    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language", ["ar", "en"], key="money_lang")
    with col2:
        detect_bills = st.checkbox("Detect bills", value=True, key="money_bills")

    if uploaded_file and st.button("💰 Analyze Money", key="money_analyze"):
        with st.spinner("Analyzing money..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/money-reader/upload-image",
                    files={"file": uploaded_file},
                    data={"language": language, "detect_bills": detect_bills},
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis complete!")
                    st.json(result)
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def ppt_pdf_reader_interface():
    """PPT/PDF Reader service interface"""
    st.markdown(
        """
    <div class="service-header">
        <h2>📄 PPT/PDF Reader - Document Analysis</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a document", type=["pptx", "ppt", "pdf"], key="doc_upload"
    )

    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language", ["ar", "en"], key="doc_lang")
    with col2:
        analyze_content = st.checkbox("AI analysis", value=True, key="doc_analysis")

    if uploaded_file and st.button("📄 Upload & Analyze", key="doc_analyze"):
        with st.spinner("Analyzing document..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/ppt-pdf-reader/upload-document",
                    files={"file": uploaded_file},
                    data={"language": language, "analyze_content": analyze_content},
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Document uploaded!")
                    st.session_state["doc_session_id"] = result.get("session_id")
                    st.json(result)
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def system_info_interface(api_info):
    """System information interface"""
    st.markdown(
        """
    <div class="service-header">
        <h2>ℹ️ System Information</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if api_info:
        st.subheader("🏥 Service Health")
        services = api_info.get("services", {})

        for service_name, service_status in services.items():
            status = service_status.get("status", "unknown")
            if status == "healthy":
                st.success(f"✅ {service_name.replace('_', ' ').title()}")
            else:
                st.error(f"❌ {service_name.replace('_', ' ').title()}")

        st.subheader("📊 System Status")
        st.write(f"**API Version:** {api_info.get('api_version', 'Unknown')}")
        st.write(f"**Total Sessions:** {api_info.get('total_sessions', 0)}")
        st.write(f"**Overall Status:** {api_info.get('status', 'Unknown')}")


if __name__ == "__main__":
    main()
