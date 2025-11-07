"""
Gematria Hive - Comprehensive Dashboard
Purpose: Rebuild Streamlit UI with comprehensive dashboard showing all data and perspectives
- All analysis types run simultaneously (no dropdowns)
- All perspectives visible
- Real-time updates
- Interactive visualizations
- Beautiful, fluid UI/UX

Author: Gematria Hive Team
Date: January 6, 2025
"""

import streamlit as st
import pandas as pd
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Gematria Hive - Comprehensive Dashboard",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-active {
        background-color: #00ff00;
    }
    .status-pending {
        background-color: #ffaa00;
    }
    .status-error {
        background-color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.data_loaded = False

# Try to import agents and modules
try:
    from agents.orchestrator import get_orchestrator
    from core.gematria_engine import get_gematria_engine
    from core.visualization_engine import get_visualization_engine
    from agents.cost_manager import CostManagerAgent
    from agents.persona_manager import PersonaManagerAgent
    from agents.alphabet_manager import AlphabetManagerAgent
    from agents.validation_engine import ValidationEngineAgent
    from utils.floating_index import get_floating_index
    HAS_AGENTS = True
except ImportError as e:
    logger.warning(f"Some agents not available: {e}")
    HAS_AGENTS = False

# Try to import Supabase
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
        supabase = None
except Exception:
    HAS_SUPABASE = False
    supabase = None


def get_database_stats() -> Dict:
    """Get database statistics"""
    if not HAS_SUPABASE or not supabase:
        return {}
    
    try:
        stats = {}
        
        # Get counts from all tables
        tables = [
            'gematria_words', 'sources', 'authors', 'key_terms', 'patterns',
            'research_topics', 'proofs', 'personas', 'alphabets', 'validations',
            'cost_tracking', 'projects', 'synchronicities', 'observations'
        ]
        
        for table in tables:
            try:
                result = supabase.table(table).select('id', count='exact').limit(1).execute()
                stats[table] = result.count if hasattr(result, 'count') else 0
            except Exception as e:
                logger.warning(f"Error getting count for {table}: {e}")
                stats[table] = 0
        
        return stats
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {}


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🐝 Gematria Hive - Comprehensive Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Self-scaffolding MCP for gematria unification - All perspectives, all the time")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select a page:",
            ["Dashboard", "Gematria Calculator", "Data Tables", "Visualizations", 
             "Agents & Status", "Cost Management", "Patterns & Proofs", "Settings"]
        )
        
        st.divider()
        
        # Database status
        st.subheader("Database Status")
        if HAS_SUPABASE:
            st.success("✅ Connected")
            stats = get_database_stats()
            if stats:
                st.metric("Total Records", sum(stats.values()))
        else:
            st.warning("⚠️ Not connected")
        
        # Cost status
        if HAS_AGENTS:
            try:
                cost_manager = CostManagerAgent()
                cost_summary = cost_manager.get_cost_summary()
                st.divider()
                st.subheader("Cost Status")
                st.metric("Today's Cost", f"${cost_summary.get('total_today', 0):.2f}")
                st.metric("Remaining Budget", f"${cost_summary.get('remaining_budget', 10):.2f}")
                status = cost_summary.get('status', 'ok')
                if status == 'ok':
                    st.success("✅ Within budget")
                elif status == 'warning':
                    st.warning("⚠️ Approaching limit")
                else:
                    st.error("🚨 Limit exceeded")
            except Exception as e:
                logger.warning(f"Error getting cost status: {e}")
    
    # Main content based on page selection
    if page == "Dashboard":
        show_dashboard()
    elif page == "Gematria Calculator":
        show_gematria_calculator()
    elif page == "Data Tables":
        show_data_tables()
    elif page == "Visualizations":
        show_visualizations()
    elif page == "Agents & Status":
        show_agents_status()
    elif page == "Cost Management":
        show_cost_management()
    elif page == "Patterns & Proofs":
        show_patterns_proofs()
    elif page == "Settings":
        show_settings()


def show_dashboard():
    """Show main dashboard with all perspectives"""
    st.header("📊 Comprehensive Dashboard")
    st.markdown("**All data, all perspectives, all the time - No dropdowns, no silos**")
    
    # Get database stats
    stats = get_database_stats()
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Gematria Words", stats.get('gematria_words', 0))
    
    with col2:
        st.metric("Sources", stats.get('sources', 0))
    
    with col3:
        st.metric("Authors", stats.get('authors', 0))
    
    with col4:
        st.metric("Key Terms", stats.get('key_terms', 0))
    
    with col5:
        st.metric("Patterns", stats.get('patterns', 0))
    
    st.divider()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Recent Sources")
        if HAS_SUPABASE and supabase:
            try:
                result = supabase.table('sources')\
                    .select('*')\
                    .order('ingested_at', desc=True)\
                    .limit(10)\
                    .execute()
                
                if result.data:
                    df = pd.DataFrame(result.data)
                    st.dataframe(df[['url', 'source_type', 'title', 'ingested_at']], use_container_width=True)
                else:
                    st.info("No sources yet")
            except Exception as e:
                st.error(f"Error loading sources: {e}")
        else:
            st.info("Database not connected")
    
    with col2:
        st.subheader("🔍 Recent Patterns")
        if HAS_SUPABASE and supabase:
            try:
                result = supabase.table('patterns')\
                    .select('*')\
                    .order('created_at', desc=True)\
                    .limit(10)\
                    .execute()
                
                if result.data:
                    df = pd.DataFrame(result.data)
                    st.dataframe(df[['pattern_name', 'pattern_type', 'confidence_score', 'created_at']], use_container_width=True)
                else:
                    st.info("No patterns yet")
            except Exception as e:
                st.error(f"Error loading patterns: {e}")
        else:
            st.info("Database not connected")
    
    st.divider()
    
    # All analysis types running simultaneously
    st.subheader("🔄 All Analysis Types (Running Simultaneously)")
    
    if HAS_AGENTS:
        try:
            orchestrator = get_orchestrator()
            agents_list = list(orchestrator.agents.keys()) if hasattr(orchestrator, 'agents') else []
            
            if agents_list:
                cols = st.columns(min(len(agents_list), 4))
                for i, agent_name in enumerate(agents_list):
                    with cols[i % 4]:
                        st.markdown(f"**{agent_name}**")
                        st.markdown('<span class="status-indicator status-active"></span>Active', unsafe_allow_html=True)
            else:
                st.info("No agents available")
        except Exception as e:
            st.warning(f"Error loading agents: {e}")
    else:
        st.info("Agents not available")


def show_gematria_calculator():
    """Show enhanced gematria calculator with all methods"""
    st.header("🔢 Gematria Calculator & Integration")
    st.markdown("**Calculate gematria values using all methods - Find related terms - Search by value**")
    
    # Tabs for different calculator functions
    tab1, tab2, tab3 = st.tabs(["📝 Calculate Text", "🔍 Search by Value", "🔗 Find Related Terms"])
    
    with tab1:
        st.subheader("Calculate Gematria for Text")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            text_input = st.text_area(
                "Enter text to calculate:",
                height=150,
                placeholder="Type or paste text here (e.g., 'LOVE', 'HELLO', Hebrew text, etc.)...",
                help="Calculate gematria for any text using all methods simultaneously",
                key="calc_text_input"
            )
            
            # Auto-calculate option
            auto_calc = st.checkbox("Auto-calculate on change", value=False, 
                                   help="Automatically calculate when text changes (may be slower)")
        
        with col2:
            st.markdown("### 📊 Calculation Methods")
            st.markdown("""
            **Standard Methods:**
            - Jewish Gematria
            - English Gematria
            - Simple Gematria
            - Latin Gematria
            - Greek Gematria
            
            **Hebrew Variants:**
            - Full (Standard)
            - Musafi
            - Katan (Reduced)
            - Ordinal
            - Atbash
            - Kidmi
            - Perati
            - Shemi
            """)
        
        # Calculate button or auto-calculate
        should_calculate = False
        if auto_calc and text_input and text_input != st.session_state.get('last_calc_text', ''):
            should_calculate = True
            st.session_state['last_calc_text'] = text_input
        elif st.button("Calculate All Methods", type="primary", use_container_width=True):
            should_calculate = True
            st.session_state['last_calc_text'] = text_input
        
        if should_calculate and text_input:
            if HAS_AGENTS:
                try:
                    engine = get_gematria_engine()
                    results = engine.calculate_all(text_input)
                    
                    # Display results in a beautiful format
                    st.success(f"✅ Calculated gematria for: **{text_input}**")
                    
                    # Show step-by-step breakdown option
                    show_breakdown = st.checkbox("📊 Show Step-by-Step Breakdown", value=False,
                                                help="Show detailed calculation breakdown for selected method")
                    
                    if show_breakdown:
                        breakdown_method = st.selectbox(
                            "Select method for breakdown:",
                            ['english_gematria', 'simple_gematria', 'jewish_gematria', 'latin_gematria', 'greek_gematria'],
                            index=1,
                            help="Select which method to show step-by-step breakdown"
                        )
                        
                        breakdown = engine.calculate_with_breakdown(text_input, breakdown_method)
                        
                        st.divider()
                        st.subheader(f"📊 Step-by-Step Breakdown: {breakdown_method.replace('_', ' ').title()}")
                        st.info(f"**Formula:** {breakdown['formula']}")
                        
                        # Display breakdown in a table
                        breakdown_data = []
                        for i, step in enumerate(breakdown['steps'], 1):
                            breakdown_data.append({
                                'Step': i,
                                'Character': step['char'],
                                'Value': step.get('value', 0),
                                'Running Total': step.get('running_total', breakdown['total']),
                                'Note': step.get('note', '')
                            })
                        
                        breakdown_df = pd.DataFrame(breakdown_data)
                        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
                        
                        # Show calculation summary
                        summary_parts = [f"{step['char']}({step['value']})" for step in breakdown['steps'] if step.get('value', 0) > 0]
                        if summary_parts:
                            summary_text = f"**{text_input}** = " + " + ".join(summary_parts) + f" = **{breakdown['total']}**"
                            st.markdown(summary_text)
                        
                        st.divider()
                    
                    # Main results in columns
                    st.subheader("📊 Results by Method")
                    
                    # Group results
                    standard_methods = ['jewish_gematria', 'english_gematria', 'simple_gematria', 'latin_gematria', 'greek_gematria']
                    hebrew_methods = ['hebrew_full', 'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal', 
                                     'hebrew_atbash', 'hebrew_kidmi', 'hebrew_perati', 'hebrew_shemi']
                    
                    # Standard methods in columns
                    cols = st.columns(len(standard_methods))
                    for i, method in enumerate(standard_methods):
                        with cols[i]:
                            value = results.get(method, 0)
                            st.metric(
                                label=method.replace('_', ' ').title(),
                                value=value
                            )
                    
                    st.divider()
                    
                    # Hebrew variants
                    st.subheader("🔤 Hebrew Variants")
                    cols = st.columns(4)
                    for i, method in enumerate(hebrew_methods):
                        with cols[i % 4]:
                            value = results.get(method, 0)
                            st.metric(
                                label=method.replace('hebrew_', '').replace('_', ' ').title(),
                                value=value
                            )
                    
                    # Detailed table
                    st.divider()
                    st.subheader("📋 Detailed Results")
                    results_data = []
                    for method, value in results.items():
                        if method != 'search_num':  # Skip search_num in main display
                            results_data.append({
                                'Method': method.replace('_', ' ').title(),
                                'Value': value,
                                'Category': 'Standard' if method in standard_methods else 'Hebrew Variant'
                            })
                    
                    df = pd.DataFrame(results_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Show related terms
                    st.divider()
                    st.subheader("🔗 Related Terms (Same Gematria Value)")
                    
                    if HAS_SUPABASE and supabase:
                        try:
                            # Find related terms by multiple gematria values
                            related_all = {}
                            
                            # Search by Jewish Gematria (most common)
                            jewish_value = results.get('jewish_gematria')
                            if jewish_value:
                                related = supabase.table('gematria_words')\
                                    .select('phrase, jewish_gematria, english_gematria, simple_gematria')\
                                    .eq('jewish_gematria', jewish_value)\
                                    .neq('phrase', text_input.upper())\
                                    .limit(50)\
                                    .execute()
                                
                                if related.data:
                                    related_all['Jewish Gematria'] = related.data
                            
                            # Search by English Gematria
                            english_value = results.get('english_gematria')
                            if english_value:
                                related = supabase.table('gematria_words')\
                                    .select('phrase, jewish_gematria, english_gematria, simple_gematria')\
                                    .eq('english_gematria', english_value)\
                                    .neq('phrase', text_input.upper())\
                                    .limit(50)\
                                    .execute()
                                
                                if related.data:
                                    related_all['English Gematria'] = related.data
                            
                            if related_all:
                                # Display in tabs
                                method_tabs = st.tabs(list(related_all.keys()))
                                for i, (method_name, related_data) in enumerate(related_all.items()):
                                    with method_tabs[i]:
                                        related_df = pd.DataFrame(related_data)
                                        st.dataframe(
                                            related_df[['phrase', 'jewish_gematria', 'english_gematria', 'simple_gematria']],
                                            use_container_width=True,
                                            hide_index=True
                                        )
                                        st.caption(f"Found {len(related_data)} related terms with {method_name} value")
                            else:
                                st.info("No related terms found in database. Try ingesting more data!")
                        except Exception as e:
                            st.warning(f"Error finding related terms: {e}")
                            st.info("Database may not be connected or table may not exist yet.")
                    else:
                        st.info("💡 Connect to Supabase database to see related terms with matching gematria values")
                    
                    # Export option
                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        # Create JSON export
                        import json
                        export_data = {
                            'input_text': text_input,
                            'results': results,
                            'calculated_at': datetime.now().isoformat()
                        }
                        st.download_button(
                            label="📥 Download Results (JSON)",
                            data=json.dumps(export_data, indent=2),
                            file_name=f"gematria_{text_input.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    with col2:
                        # Create CSV export
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results (CSV)",
                            data=csv,
                            file_name=f"gematria_{text_input.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                        
                except Exception as e:
                    st.error(f"Error calculating gematria: {e}")
                    st.exception(e)
            else:
                st.warning("⚠️ Gematria engine not available. Please check that agents are properly initialized.")
        elif not text_input:
            st.info("👆 Enter text above to calculate gematria values")
    
    with tab2:
        st.subheader("🔍 Search Words by Gematria Value (Like Gematrix.org)")
        st.markdown("**Enter a value and find all words/phrases with that value across ALL methods simultaneously**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_value = st.number_input(
                "Enter gematria value to search:",
                min_value=0,
                value=54,
                help="Find all words/phrases with this gematria value across all methods"
            )
        
        with col2:
            search_all_methods = st.checkbox(
                "🔍 Search ALL methods (like gematrix.org)",
                value=True,
                help="Search across all methods simultaneously to find all related values"
            )
        
        if not search_all_methods:
            search_method = st.selectbox(
                "Gematria Method:",
                ['jewish_gematria', 'english_gematria', 'simple_gematria', 'latin_gematria', 'greek_gematria',
                 'hebrew_full', 'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal', 'hebrew_atbash',
                 'hebrew_kidmi', 'hebrew_perati', 'hebrew_shemi'],
                help="Select which gematria method to search by"
            )
        
        limit = st.slider("Maximum results per method:", 10, 200, 50)
        
        if st.button("🔍 Search", type="primary", use_container_width=True):
            if HAS_SUPABASE and supabase:
                try:
                    if search_all_methods:
                        # Search across ALL methods (like gematrix.org)
                        all_methods = [
                            'jewish_gematria', 'english_gematria', 'simple_gematria',
                            'latin_gematria', 'greek_gematria', 'hebrew_full',
                            'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal',
                            'hebrew_atbash', 'hebrew_kidmi', 'hebrew_perati', 'hebrew_shemi'
                        ]
                        
                        results_all = {}
                        
                        with st.spinner("Searching across all methods..."):
                            for method in all_methods:
                                try:
                                    result = supabase.table('gematria_words')\
                                        .select('phrase, jewish_gematria, english_gematria, simple_gematria, source')\
                                        .eq(method, int(search_value))\
                                        .limit(limit)\
                                        .execute()
                                    
                                    if result.data:
                                        results_all[method] = result.data
                                except Exception as e:
                                    st.warning(f"Error searching {method}: {e}")
                        
                        if results_all:
                            st.success(f"✅ Found matches in {len(results_all)} method(s) for value {search_value}")
                            
                            # Display results by method in expandable sections
                            for method, words in results_all.items():
                                with st.expander(f"🔍 {method.replace('_', ' ').title()} - {len(words)} matches"):
                                    df = pd.DataFrame(words)
                                    st.dataframe(df, use_container_width=True, hide_index=True)
                                    
                                    # Show sample phrases
                                    sample_phrases = [w.get('phrase', 'N/A') for w in words[:10]]
                                    st.caption(f"Sample phrases: {', '.join(sample_phrases)}")
                        else:
                            st.info(f"No words found with value {search_value} in any method")
                    else:
                        # Single method search
                        result = supabase.table('gematria_words')\
                            .select('*')\
                            .eq(search_method, int(search_value))\
                            .limit(limit)\
                            .execute()
                        
                        if result.data:
                            st.success(f"✅ Found {len(result.data)} words with {search_method} value of {search_value}")
                            df = pd.DataFrame(result.data)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.info(f"No words found with {search_method} value of {search_value}")
                except Exception as e:
                    st.error(f"Error searching: {e}")
                    st.exception(e)
            else:
                st.warning("⚠️ Database not connected. Cannot search words.")
    
    with tab3:
        st.subheader("Find Related Terms")
        
        related_text = st.text_input(
            "Enter a word or phrase:",
            placeholder="e.g., 'LOVE', 'HELLO', etc.",
            help="Find all words with the same gematria value as this text"
        )
        
        related_method = st.selectbox(
            "Gematria Method:",
            ['jewish_gematria', 'english_gematria', 'simple_gematria'],
            key="related_method"
        )
        
        if st.button("🔗 Find Related", type="primary", use_container_width=True):
            if related_text:
                if HAS_AGENTS:
                    try:
                        engine = get_gematria_engine()
                        results = engine.calculate_all(related_text)
                        target_value = results.get(related_method)
                        
                        if target_value:
                            st.success(f"✅ '{related_text}' has {related_method} value: **{target_value}**")
                            
                            if HAS_SUPABASE and supabase:
                                try:
                                    related = supabase.table('gematria_words')\
                                        .select('*')\
                                        .eq(related_method, target_value)\
                                        .neq('phrase', related_text.upper())\
                                        .limit(100)\
                                        .execute()
                                    
                                    if related.data:
                                        st.subheader(f"🔗 Related Terms (Value: {target_value})")
                                        df = pd.DataFrame(related.data)
                                        st.dataframe(df, use_container_width=True, hide_index=True)
                                    else:
                                        st.info(f"No related terms found with {related_method} value of {target_value}")
                                except Exception as e:
                                    st.warning(f"Error finding related terms: {e}")
                            else:
                                st.info("💡 Connect to database to see related terms")
                        else:
                            st.warning(f"Could not calculate {related_method} value for '{related_text}'")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("⚠️ Gematria engine not available")
            else:
                st.info("👆 Enter a word or phrase above")


def show_data_tables():
    """Show all data tables"""
    st.header("📋 Data Tables")
    st.markdown("**All tables, all data, all perspectives**")
    
    if not HAS_SUPABASE or not supabase:
        st.warning("Database not connected")
        return
    
    # Table selector
    tables = [
        'gematria_words', 'sources', 'authors', 'key_terms', 'patterns',
        'research_topics', 'proofs', 'personas', 'alphabets', 'validations',
        'cost_tracking', 'projects', 'synchronicities', 'observations'
    ]
    
    selected_table = st.selectbox("Select table:", tables)
    
    if selected_table:
        try:
            # Get data from table
            result = supabase.table(selected_table)\
                .select('*')\
                .limit(100)\
                .execute()
            
            if result.data:
                df = pd.DataFrame(result.data)
                st.dataframe(df, use_container_width=True)
                
                # Show statistics
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Table", selected_table)
            else:
                st.info(f"No data in {selected_table}")
        except Exception as e:
            st.error(f"Error loading table {selected_table}: {e}")


def show_visualizations():
    """Show visualizations"""
    st.header("📊 Visualizations")
    st.markdown("**Sacred geometry, waves, fields, harmonics - All perspectives**")
    
    if not HAS_AGENTS:
        st.warning("Visualization engine not available")
        return
    
    try:
        viz_engine = get_visualization_engine()
        
        # Visualization selector
        viz_type = st.selectbox(
            "Select visualization:",
            ["Metatron's Cube", "Tree of Life", "Wave Form", "Toroidal Field", 
             "Cymatics Pattern", "Harmonic Series", "Chakra Visualization"]
        )
        
        if viz_type == "Metatron's Cube":
            geometry = viz_engine.generate_metatrons_cube()
            fig = viz_engine.create_3d_plot(geometry, "Metatron's Cube")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Tree of Life":
            geometry = viz_engine.generate_tree_of_life()
            fig = viz_engine.create_3d_plot(geometry, "Tree of Life")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Wave Form":
            frequency = st.slider("Frequency (Hz)", 1.0, 100.0, 10.0)
            amplitude = st.slider("Amplitude", 0.1, 2.0, 1.0)
            wave_data = viz_engine.generate_wave_form(frequency, amplitude)
            fig = viz_engine.create_wave_plot(wave_data, "Wave Form")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Toroidal Field":
            radius = st.slider("Radius", 0.5, 3.0, 1.0)
            tube_radius = st.slider("Tube Radius", 0.1, 1.0, 0.3)
            geometry = viz_engine.generate_toroidal_field(radius, tube_radius)
            fig = viz_engine.create_3d_plot(geometry, "Toroidal Field")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Cymatics Pattern":
            frequency = st.slider("Frequency (Hz)", 100.0, 1000.0, 440.0)
            pattern_data = viz_engine.generate_cymatics_pattern(frequency)
            fig = viz_engine.create_cymatics_plot(pattern_data, "Cymatics Pattern")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Harmonic Series":
            fundamental = st.slider("Fundamental Frequency (Hz)", 100.0, 1000.0, 440.0)
            harmonics = st.slider("Number of Harmonics", 5, 20, 10)
            harmonic_data = viz_engine.generate_harmonic_series(fundamental, harmonics)
            fig = viz_engine.create_harmonic_plot(harmonic_data, "Harmonic Series")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Chakra Visualization":
            chakra_data = viz_engine.generate_chakra_visualization()
            fig = viz_engine.create_chakra_plot(chakra_data, "Chakra Visualization")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error creating visualization: {e}")


def show_agents_status():
    """Show agents status"""
    st.header("🤖 Agents & Status")
    st.markdown("**All agents running simultaneously - No dropdowns**")
    
    if not HAS_AGENTS:
        st.warning("Agents not available")
        return
    
    try:
        orchestrator = get_orchestrator()
        agents_list = list(orchestrator.agents.keys()) if hasattr(orchestrator, 'agents') else []
        
        if agents_list:
            # Display all agents
            cols = st.columns(3)
            for i, agent_name in enumerate(agents_list):
                with cols[i % 3]:
                    st.markdown(f"### {agent_name}")
                    st.markdown('<span class="status-indicator status-active"></span>Active', unsafe_allow_html=True)
                    st.markdown(f"**Type:** Agent")
                    st.markdown(f"**Status:** Running")
        else:
            st.info("No agents available")
    
    except Exception as e:
        st.error(f"Error loading agents: {e}")


def show_cost_management():
    """Show cost management"""
    st.header("💰 Cost Management")
    st.markdown("**$10 cap with alerts - All API costs tracked**")
    
    if not HAS_AGENTS:
        st.warning("Cost manager not available")
        return
    
    try:
        cost_manager = CostManagerAgent()
        cost_summary = cost_manager.get_cost_summary()
        
        # Display cost summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Today's Cost", f"${cost_summary.get('total_today', 0):.2f}")
        
        with col2:
            st.metric("Week's Cost", f"${cost_summary.get('total_week', 0):.2f}")
        
        with col3:
            st.metric("Month's Cost", f"${cost_summary.get('total_month', 0):.2f}")
        
        with col4:
            st.metric("Remaining Budget", f"${cost_summary.get('remaining_budget', 10):.2f}")
        
        st.divider()
        
        # Cost by API
        st.subheader("Cost by API")
        cost_by_api = cost_summary.get('cost_by_api', {})
        if cost_by_api:
            df = pd.DataFrame(list(cost_by_api.items()), columns=['API', 'Cost'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No API costs yet")
        
        # Status indicator
        status = cost_summary.get('status', 'ok')
        if status == 'ok':
            st.success("✅ Within budget")
        elif status == 'warning':
            st.warning("⚠️ Approaching $10 limit")
        else:
            st.error("🚨 Cost limit exceeded!")
    
    except Exception as e:
        st.error(f"Error loading cost management: {e}")


def show_patterns_proofs():
    """Show patterns and proofs"""
    st.header("🔍 Patterns & Proofs")
    st.markdown("**All patterns, all proofs, all perspectives**")
    
    if not HAS_SUPABASE or not supabase:
        st.warning("Database not connected")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Patterns")
        try:
            result = supabase.table('patterns')\
                .select('*')\
                .order('confidence_score', desc=True)\
                .limit(20)\
                .execute()
            
            if result.data:
                df = pd.DataFrame(result.data)
                st.dataframe(df[['pattern_name', 'pattern_type', 'confidence_score', 'created_at']], use_container_width=True)
            else:
                st.info("No patterns yet")
        except Exception as e:
            st.error(f"Error loading patterns: {e}")
    
    with col2:
        st.subheader("✅ Proofs")
        try:
            result = supabase.table('proofs')\
                .select('*')\
                .order('accuracy_metric', desc=True)\
                .limit(20)\
                .execute()
            
            if result.data:
                df = pd.DataFrame(result.data)
                st.dataframe(df[['proof_name', 'proof_type', 'accuracy_metric', 'efficiency_score', 'created_at']], use_container_width=True)
            else:
                st.info("No proofs yet")
        except Exception as e:
            st.error(f"Error loading proofs: {e}")


def show_settings():
    """Show settings"""
    st.header("⚙️ Settings")
    st.markdown("**Configuration and system settings**")
    
    st.subheader("Database Configuration")
    if HAS_SUPABASE:
        st.success("✅ Supabase connected")
        st.info(f"URL: {os.getenv('SUPABASE_URL', 'Not set')[:50]}...")
    else:
        st.warning("⚠️ Supabase not configured")
        st.info("Set SUPABASE_URL and SUPABASE_KEY in .env file")
    
    st.divider()
    
    st.subheader("API Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        grok_configured = bool(os.getenv('GROK_API_KEY'))
        if grok_configured:
            st.success("✅ Grok API configured")
        else:
            st.warning("⚠️ Grok API not configured")
    
    with col2:
        perplexity_configured = bool(os.getenv('PERPLEXITY_API_KEY'))
        if perplexity_configured:
            st.success("✅ Perplexity API configured")
        else:
            st.warning("⚠️ Perplexity API not configured")
    
    st.divider()
    
    st.subheader("System Information")
    st.info(f"Python version: {os.sys.version}")
    st.info(f"Streamlit version: {st.__version__}")


if __name__ == "__main__":
    main()
