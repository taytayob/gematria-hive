import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Gematria Hive",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

def calculate_gematria(text, method="standard"):
    """Calculate gematria value using different methods
    
    Methods:
    - standard: English Gematria (A=1, B=2, ..., Z=26)
    - ordinal: Simple Gematria (same as standard for compatibility)
    - reduced: Pythagorean reduction (A=1, B=2, ..., I=9, J=1, K=2, ...)
    """
    if method == 'standard' or method == 'ordinal':
        values = {chr(i + 96): i for i in range(1, 27)}
    elif method == 'reduced':
        values = {chr(i + 96): ((i - 1) % 9) + 1 for i in range(1, 27)}
    else:
        values = {chr(i + 96): i for i in range(1, 27)}
    
    total = 0
    text = text.lower()
    for char in text:
        if char in values:
            total += values[char]
    
    return total

def main():
    st.title("🐝 Gematria Hive")
    st.markdown("### Self-scaffolding MCP for gematria unification")
    
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select a page:",
            ["Calculator", "About", "Setup Guide"]
        )
    
    if page == "Calculator":
        st.header("Gematria Calculator")
        st.markdown("Enter text to calculate its gematria value.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            text_input = st.text_area(
                "Enter text:",
                height=100,
                placeholder="Type or paste text here..."
            )
        
        with col2:
            method = st.selectbox(
                "Calculation method:",
                ["standard", "reduced"],
                help="Standard: A=1, B=2...Z=26 | Reduced: Pythagorean (A=1...I=9, J=1...)"
            )
        
        if st.button("Calculate", type="primary"):
            if text_input:
                result = calculate_gematria(text_input, method)
                st.success(f"**Gematria Value:** {result}")
                
                st.divider()
                st.subheader("Character Breakdown")
                
                breakdown_data = []
                for char in text_input.lower():
                    if char.isalpha():
                        value = calculate_gematria(char, method)
                        breakdown_data.append({
                            "Character": char.upper(),
                            "Value": value
                        })
                
                if breakdown_data:
                    df = pd.DataFrame(breakdown_data)
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("Please enter some text to calculate.")
    
    elif page == "About":
        st.header("About Gematria Hive")
        st.markdown("""
        **Gematria Hive** is an expansive, self-scaffolding AI ecosystem engineered to unify:
        
        - 🔢 Gematria & Numerology
        - 📐 Sacred Geometry
        - 🔮 Esoteric Principles
        - 🧬 Ancient Knowledge
        - 🔬 Mathematics & Physics
        - ⚛️ Quantum Mechanics
        - 🤖 AI/ML Breakthroughs
        
        ### Vision
        
        At its foundation is a gematria calculator app, indexed with a 1M+ word CSV from gematrix.org,
        enhanced by notes, permutations, language histories, phonetic analyses, and etymological insights.
        
        The system constructs symmetrical mathematical models across dimensions (2D-5D), bridging vibration,
        oscillation, harmonics, wave functions, cymatics, and more.
        
        ### Current Status
        
        **Phase 1: Foundation** - Data foundation and basic calculator (v0.1)
        
        This is the initial prototype. Full features including MCP agents, database integration,
        and advanced proofs are planned for future phases.
        """)
    
    else:
        st.header("Setup Guide")
        st.markdown("""
        ### Getting Started
        
        This application is currently in Phase 1 (Foundation).
        
        #### Database Setup (Optional for Phase 1)
        
        To enable full features in future phases, you'll need to configure:
        
        1. **Supabase** - For relational data with pgvector embeddings
        2. **ClickHouse** - For OLAP analytics at scale
        
        #### Environment Variables
        
        Create a `.env` file with:
        
        ```
        SUPABASE_URL=your_supabase_url
        SUPABASE_KEY=your_supabase_key
        CLICKHOUSE_HOST=your_clickhouse_host
        CLICKHOUSE_USER=default
        CLICKHOUSE_PASSWORD=your_password
        ```
        
        #### Roadmap
        
        - ✅ Phase 1: Basic calculator (Current)
        - 🔄 Phase 2: Gematria app with 1M+ word database
        - 📋 Phase 3: Sacred geometry unifications
        - 📋 Phase 4: Full MCP/agents implementation
        - 📋 Phase 5: Generative media & expansion
        
        ### Contributions
        
        Contributions welcome! Focus on modular, proof-driven enhancements.
        """)
        
        st.divider()
        
        st.subheader("Environment Status")
        
        supabase_configured = bool(os.getenv("SUPABASE_URL"))
        clickhouse_configured = bool(os.getenv("CLICKHOUSE_HOST"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if supabase_configured:
                st.success("✅ Supabase configured")
            else:
                st.info("ℹ️ Supabase not configured (optional for v0.1)")
        
        with col2:
            if clickhouse_configured:
                st.success("✅ ClickHouse configured")
            else:
                st.info("ℹ️ ClickHouse not configured (optional for v0.1)")

if __name__ == "__main__":
    main()
