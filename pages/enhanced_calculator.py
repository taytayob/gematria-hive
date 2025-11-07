"""
Enhanced Gematria Calculator with Step-by-Step Breakdown
Purpose: Show calculation process and find all related values like gematrix.org
- Step-by-step calculation breakdown
- Visual representation of process
- Search across ALL methods simultaneously
- Educational insights and tooltips

Author: Gematria Hive Team
Date: January 6, 2025
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Enhanced Gematria Calculator",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .calculation-step {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        border-left: 3px solid #1f77b4;
    }
    .step-char {
        font-weight: bold;
        color: #1f77b4;
        font-size: 1.2em;
    }
    .step-value {
        color: #2ca02c;
        font-weight: bold;
    }
    .step-total {
        color: #d62728;
        font-weight: bold;
    }
    .method-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .related-word {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        border-left: 3px solid #2ca02c;
    }
</style>
""", unsafe_allow_html=True)

# Try to import required modules
try:
    from core.gematria_engine import get_gematria_engine
    HAS_ENGINE = True
except ImportError:
    HAS_ENGINE = False

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
except ImportError:
    HAS_SUPABASE = False
    supabase = None

st.title("🔢 Enhanced Gematria Calculator")
st.markdown("**Calculate with step-by-step breakdown • Find all related values across all methods • Learn how it works**")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📝 Calculate with Breakdown", "🔍 Search All Methods", "📚 Learn & Explore"])

with tab1:
    st.header("Calculate with Step-by-Step Breakdown")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input = st.text_input(
            "Enter text to calculate:",
            placeholder="e.g., 'LOVE', 'HELLO', Hebrew text, etc.",
            help="Calculate gematria with detailed step-by-step breakdown",
            key="enhanced_calc_text"
        )
        
        # Method selector
        method = st.selectbox(
            "Select method for breakdown:",
            [
                'english_gematria',
                'simple_gematria',
                'jewish_gematria',
                'latin_gematria',
                'greek_gematria',
                'hebrew_full',
                'hebrew_musafi',
                'hebrew_katan',
                'hebrew_ordinal',
                'hebrew_atbash',
                'hebrew_kidmi',
                'hebrew_perati',
                'hebrew_shemi'
            ],
            index=0,
            help="Select which gematria method to show step-by-step breakdown"
        )
    
    with col2:
        st.markdown("### 💡 How It Works")
        st.markdown("""
        **Step-by-Step Breakdown:**
        1. Each letter is processed
        2. Letter value is looked up
        3. Running total is calculated
        4. Final value is displayed
        
        **Visual Process:**
        - See each letter's contribution
        - Watch the total accumulate
        - Understand the calculation
        """)
    
    if st.button("🔢 Calculate with Breakdown", type="primary", use_container_width=True):
        if text_input:
            if HAS_ENGINE:
                try:
                    engine = get_gematria_engine()
                    
                    # Get step-by-step breakdown
                    breakdown = engine.calculate_with_breakdown(text_input, method)
                    
                    # Display results
                    st.success(f"✅ Calculated {method.replace('_', ' ').title()} for: **{text_input}**")
                    
                    # Show formula
                    st.info(f"**Formula:** {breakdown['formula']}")
                    
                    # Main result
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Input Text", text_input)
                    with col2:
                        st.metric("Method", method.replace('_', ' ').title())
                    with col3:
                        st.metric("Total Value", breakdown['total'])
                    
                    st.divider()
                    
                    # Step-by-step breakdown
                    st.subheader("📊 Step-by-Step Calculation")
                    
                    # Create visual breakdown
                    steps_html = "<div style='font-family: monospace;'>"
                    steps_html += "<div style='display: grid; grid-template-columns: 1fr 2fr 2fr 2fr; gap: 0.5rem; padding: 0.5rem; background: #f8f9fa; border-radius: 0.25rem; margin-bottom: 0.5rem;'>"
                    steps_html += "<strong>Step</strong><strong>Character</strong><strong>Value</strong><strong>Running Total</strong>"
                    steps_html += "</div>"
                    
                    for i, step in enumerate(breakdown['steps'], 1):
                        char = step['char']
                        value = step.get('value', 0)
                        running_total = step.get('running_total', breakdown['total'])
                        note = step.get('note', '')
                        
                        steps_html += f"<div class='calculation-step'>"
                        steps_html += f"<div style='display: grid; grid-template-columns: 1fr 2fr 2fr 2fr; gap: 0.5rem;'>"
                        steps_html += f"<span>{i}</span>"
                        steps_html += f"<span class='step-char'>{char}</span>"
                        steps_html += f"<span class='step-value'>{value}</span>"
                        steps_html += f"<span class='step-total'>{running_total}</span>"
                        steps_html += f"</div>"
                        if note:
                            steps_html += f"<small style='color: #666;'>{note}</small>"
                        steps_html += f"</div>"
                    
                    steps_html += "</div>"
                    st.markdown(steps_html, unsafe_allow_html=True)
                    
                    # Show calculation summary
                    st.divider()
                    st.subheader("📝 Calculation Summary")
                    
                    # Create summary
                    summary_text = f"**{text_input}** = "
                    summary_parts = []
                    for step in breakdown['steps']:
                        if step.get('value', 0) > 0:
                            summary_parts.append(f"{step['char']}({step['value']})")
                    
                    if summary_parts:
                        summary_text += " + ".join(summary_parts)
                        summary_text += f" = **{breakdown['total']}**"
                        st.markdown(summary_text)
                    
                    # Show all methods
                    st.divider()
                    st.subheader("📊 All Methods Results")
                    
                    all_results = engine.calculate_all(text_input)
                    
                    # Display in columns
                    methods_list = [
                        'jewish_gematria', 'english_gematria', 'simple_gematria',
                        'latin_gematria', 'greek_gematria', 'hebrew_full',
                        'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal',
                        'hebrew_atbash', 'hebrew_kidmi', 'hebrew_perati', 'hebrew_shemi'
                    ]
                    
                    cols = st.columns(4)
                    for i, method_name in enumerate(methods_list):
                        with cols[i % 4]:
                            value = all_results.get(method_name, 0)
                            st.metric(
                                label=method_name.replace('_', ' ').title(),
                                value=value
                            )
                    
                    # Find related terms across ALL methods
                    if HAS_SUPABASE and supabase:
                        st.divider()
                        st.subheader("🔗 Related Terms (All Methods)")
                        
                        related_all = {}
                        
                        # Search across all methods
                        for method_name in methods_list:
                            value = all_results.get(method_name)
                            if value:
                                try:
                                    result = supabase.table('gematria_words')\
                                        .select('phrase, jewish_gematria, english_gematria, simple_gematria')\
                                        .eq(method_name, int(value))\
                                        .neq('phrase', text_input.upper())\
                                        .limit(20)\
                                        .execute()
                                    
                                    if result.data:
                                        related_all[method_name] = {
                                            'value': value,
                                            'count': len(result.data),
                                            'words': result.data[:10]  # Show first 10
                                        }
                                except Exception as e:
                                    st.warning(f"Error searching {method_name}: {e}")
                        
                        if related_all:
                            # Display in expandable sections
                            for method_name, data in related_all.items():
                                with st.expander(f"🔍 {method_name.replace('_', ' ').title()} (Value: {data['value']}) - {data['count']} matches"):
                                    df = pd.DataFrame(data['words'])
                                    st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.info("No related terms found in database. Try ingesting more data!")
                    
                except Exception as e:
                    st.error(f"Error calculating: {e}")
                    st.exception(e)
            else:
                st.warning("⚠️ Gematria engine not available")
        else:
            st.info("👆 Enter text above to calculate")

with tab2:
    st.header("🔍 Search All Methods (Like Gematrix.org)")
    st.markdown("**Enter a value and find all words/phrases with that value across ALL methods simultaneously**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        search_value = st.number_input(
            "Enter gematria value to search:",
            min_value=0,
            value=54,
            help="Find all words/phrases with this value across all methods"
        )
    
    with col2:
        limit = st.slider("Maximum results per method:", 10, 100, 20)
    
    if st.button("🔍 Search All Methods", type="primary", use_container_width=True):
        if HAS_SUPABASE and supabase:
            try:
                # Search across all methods
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
                    
                    # Display results by method
                    for method, words in results_all.items():
                        with st.expander(f"🔍 {method.replace('_', ' ').title()} - {len(words)} matches"):
                            df = pd.DataFrame(words)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            # Show sample phrases
                            sample_phrases = [w.get('phrase', 'N/A') for w in words[:5]]
                            st.caption(f"Sample phrases: {', '.join(sample_phrases)}")
                else:
                    st.info(f"No words found with value {search_value} in any method")
                    
            except Exception as e:
                st.error(f"Error searching: {e}")
                st.exception(e)
        else:
            st.warning("⚠️ Database not connected. Cannot search words.")

with tab3:
    st.header("📚 Learn & Explore")
    st.markdown("**Educational resources and insights about gematria calculations**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📖 How Gematria Works")
        st.markdown("""
        **Gematria** is a system of assigning numerical values to letters.
        
        **Basic Process:**
        1. Each letter has a numerical value
        2. Values are summed for the word/phrase
        3. Words with same value are considered related
        
        **Common Methods:**
        - **English Gematria:** A=1, B=2, ..., Z=26
        - **Jewish Gematria:** Hebrew alphabet values
        - **Simple Gematria:** Same as English
        - **Latin Gematria:** Qabala Simplex system
        - **Greek Gematria:** Classical Greek alphabet
        
        **Hebrew Variants:**
        - **Full:** Standard Hebrew values
        - **Musafi:** Adds 1000 per letter
        - **Katan:** Reduced values
        - **Ordinal:** Position in alphabet
        - **Atbash:** Reversed alphabet
        - **Kidmi:** Cumulative values
        - **Perati:** Product of values
        - **Shemi:** Name-based values
        """)
    
    with col2:
        st.subheader("💡 Tips for Learning")
        st.markdown("""
        **Understanding Calculations:**
        1. Use step-by-step breakdown to see each letter's contribution
        2. Compare different methods to see how values differ
        3. Search across all methods to find related terms
        4. Explore the database to discover patterns
        
        **Finding Related Terms:**
        - Words with same gematria value are considered related
        - Search across all methods to find connections
        - Use the calculator to explore relationships
        
        **Best Practices:**
        - Start with simple words like "LOVE" (54 in English)
        - Compare results across methods
        - Explore the database for patterns
        - Use step-by-step breakdown to understand
        """)
    
    # Example calculations
    st.divider()
    st.subheader("📝 Example Calculations")
    
    examples = [
        ("LOVE", "english_gematria", "L=12, O=15, V=22, E=5 → 12+15+22+5 = 54"),
        ("HELLO", "english_gematria", "H=8, E=5, L=12, L=12, O=15 → 8+5+12+12+15 = 52"),
        ("GOD", "english_gematria", "G=7, O=15, D=4 → 7+15+4 = 26"),
    ]
    
    for word, method, explanation in examples:
        with st.expander(f"**{word}** ({method.replace('_', ' ').title()})"):
            st.markdown(f"**Calculation:** {explanation}")
            if HAS_ENGINE:
                try:
                    engine = get_gematria_engine()
                    result = engine.calculate_all(word)
                    st.metric("Value", result.get(method, 0))
                except:
                    pass

