import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, content_generator, analytics

st.set_page_config(
    page_title="Digital Content Generator",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home", "Content Generator", "Analytics"],
        icons=["house", "edit", "bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

# Navigation logic
if selected == "Home":
    home.render()
elif selected == "Content Generator":
    content_generator.render()
elif selected == "Analytics":
    analytics.render()
