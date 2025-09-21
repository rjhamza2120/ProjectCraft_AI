import streamlit as st

def add_custom_css():
    """Add custom CSS for enhanced UI"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 2rem;
    }
    
    /* Custom Title Styling */
    .title-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: fadeInDown 1s ease-out;
    }
    
    .main-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: rgba(255,255,255,0.9);
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
    }
    
    /* Stage Progress Styling */
    .stage-progress {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    /* Category Cards */
    .category-card {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        border: none;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .category-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Project Details Cards */
    .project-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    /* Animated Icons */
    .animated-icon {
        display: inline-block;
        animation: bounce 2s infinite;
    }
    
    .pulse-icon {
        animation: pulse 2s infinite;
    }
    
    /* Chat Messages */
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e0e0e0;
        border-radius: 25px;
        padding: 3px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        height: 20px;
        border-radius: 25px;
        transition: width 0.3s ease;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
        }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Success/Info Boxes */
    .stSuccess {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        border-radius: 10px;
    }
    
    .stInfo {
        background: linear-gradient(45deg, #2196F3, #1976D2);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def create_animated_title():
    """Create an animated title section"""
    st.markdown("""
    <div class="title-container">
        <h1 class="main-title">
            <span class="animated-icon">🚀</span> 
            ProjectCraft AI
            <span class="pulse-icon">✨</span>
        </h1>
        <p class="subtitle">
            Transform Ideas into Reality • Build • Learn • Innovate
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_progress_indicator(current_stage):
    """Create an animated progress indicator"""
    stages = ["idea_input", "project_suggestions", "project_type_selection", "refinement", "details", "resources", "export"]
    
    # Find current stage index safely
    try:
        current_index = stages.index(current_stage)
    except ValueError:
        # If stage not found, default to 0
        current_index = 0
    
    progress = ((current_index + 1) / len(stages)) * 100
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%"></div>
    </div>
    <p style="text-align: center; font-weight: 600; color: #667eea;">
        Step {current_index + 1} of {len(stages)}: {progress:.0f}% Complete
    </p>
    """, unsafe_allow_html=True)

def create_interactive_assistant(current_stage):
    """Create an interactive AI assistant avatar"""
    assistant_states = {
        "idea_input": {"emoji": "💡", "message": "I'm here to help you discover amazing project ideas!"},
        "project_suggestions": {"emoji": "🔥", "message": "Check out these trending projects in your field!"},
        "project_type_selection": {"emoji": "🎯", "message": "Let's define your project details!"},
        "refinement": {"emoji": "🔍", "message": "Let's refine your idea to make it perfect!"},
        "details": {"emoji": "📋", "message": "Generating your comprehensive project guide..."},
        "resources": {"emoji": "🔗", "message": "Finding the best resources for your project!"},
        "export": {"emoji": "📄", "message": "Your project guide is ready to download!"}
    }
    
    assistant = assistant_states.get(current_stage, assistant_states["idea_input"])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; padding: 1rem; margin: 1rem 0; 
                text-align: center; color: white; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;" class="pulse-icon">
            {assistant['emoji']}
        </div>
        <p style="margin: 0; font-weight: 500; font-size: 1.1rem;">
            {assistant['message']}
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_stages(current_stage):
    """Create enhanced sidebar with stage tracking"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: #667eea; margin-bottom: 1rem;">🎯 Your Journey</h2>
    </div>
    """, unsafe_allow_html=True)
    
    stages = [
        {"name": "💡 Field Selection", "key": "idea_input", "desc": "Choose your domain"},
        {"name": "🔥 Project Ideas", "key": "project_suggestions", "desc": "Trending projects"},
        {"name": "� Project Details", "key": "project_type_selection", "desc": "Define your project"},
        {"name": "🔍 Refinement", "key": "refinement", "desc": "Perfect your concept"},
        {"name": "� Project Guide", "key": "details", "desc": "Detailed blueprint"},
        {"name": "🔧 Resources", "key": "resources", "desc": "Tools & tutorials"},
        {"name": "📄 Export", "key": "export", "desc": "Download guide"}
    ]
    
    # Find current stage index
    current_stage_index = -1
    for i, stage in enumerate(stages):
        if stage["key"] == current_stage:
            current_stage_index = i
            break
    
    # Show user selections in sidebar
    if hasattr(st.session_state, 'selected_field') and st.session_state.selected_field:
        st.markdown(f"""
        <div style="background: #e8f5e8; border-radius: 10px; padding: 0.75rem; margin: 1rem 0; border-left: 4px solid #4CAF50;">
            <strong>🎓 Field:</strong><br>
            <small>{st.session_state.selected_field}</small>
        </div>
        """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'selected_subdomain') and st.session_state.selected_subdomain:
            st.markdown(f"""
            <div style="background: #e3f2fd; border-radius: 10px; padding: 0.75rem; margin: 1rem 0; border-left: 4px solid #2196F3;">
                <strong>🎯 Specialization:</strong><br>
                <small>{st.session_state.selected_subdomain}</small>
            </div>
            """, unsafe_allow_html=True)
    
    if hasattr(st.session_state, 'selected_project') and st.session_state.selected_project:
        project = st.session_state.selected_project
        st.markdown(f"""
        <div style="background: #fff3e0; border-radius: 10px; padding: 0.75rem; margin: 1rem 0; border-left: 4px solid #FF9800;">
            <strong>🚀 Project:</strong><br>
            <small>{project['title']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'project_type') and st.session_state.project_type:
            st.markdown(f"""
            <div style="background: #f3e5f5; border-radius: 10px; padding: 0.75rem; margin: 1rem 0; border-left: 4px solid #9C27B0;">
                <strong>📚 Type:</strong><br>
                <small>{st.session_state.project_type}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Show refinement progress
    if hasattr(st.session_state, 'user_responses') and st.session_state.user_responses:
        response_count = len(st.session_state.user_responses)
        st.markdown(f"""
        <div style="background: #e1f5fe; border-radius: 10px; padding: 0.75rem; margin: 1rem 0; border-left: 4px solid #00BCD4;">
            <strong>🔍 Refinement:</strong><br>
            <small>{response_count} questions answered</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show stage progress
    for i, stage in enumerate(stages):
        if current_stage_index >= 0:
            if i < current_stage_index:
                # Completed stages
                st.markdown(f"""
                <div class="stage-progress" style="background: linear-gradient(45deg, #4CAF50, #45a049); color: white;">
                    <strong>{stage['name']}</strong><br>
                    <small>✅ {stage['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_stage_index:
                # Current stage
                st.markdown(f"""
                <div class="stage-progress" style="background: linear-gradient(45deg, #FF9800, #F57C00); color: white;">
                    <strong>{stage['name']}</strong><br>
                    <small>🔄 {stage['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Future stages
                st.markdown(f"""
                <div class="stage-progress" style="background: #f8f9fa; color: #6c757d;">
                    <strong>{stage['name']}</strong><br>
                    <small>⏳ {stage['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            # If current stage not found, show all as future
            st.markdown(f"""
            <div class="stage-progress" style="background: #f8f9fa; color: #6c757d;">
                <strong>{stage['name']}</strong><br>
                <small>⏳ {stage['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
