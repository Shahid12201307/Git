import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from st_aggrid import AgGrid
from streamlit_option_menu import option_menu

# Set up the app's theme and layout
st.set_page_config(page_title="Expense Tracker", layout="wide")

# Set custom CSS for header and button styling
st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .custom-button {
        background-color: #FF6347;
        border-radius: 12px;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Initialize session state for expenses if not already done
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# Function to add an expense
def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

# Function to load expenses from a file
def load_expenses():
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        try:
            # Load and update session state
            st.session_state.expenses = pd.read_csv(uploaded_file)
            st.success('Expenses loaded successfully!')

            # Display the uploaded expenses in the main content area
            st.write(st.session_state.expenses)

        except Exception as e:
            st.error(f"Error loading the file: {e}")

# Function to save expenses to a CSV file
def save_expenses():
    st.session_state.expenses.to_csv('expenses.csv', index=False)
    st.success("Expenses saved successfully!")

# Function to visualize expenses
def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

# Sidebar navigation menu
selected = option_menu(
    menu_title="Main Menu",  # required
    options=["Home", "Add Expense", "Reports"],  # required
    icons=["house", "plus-circle", "bar-chart"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="vertical",
)

# Title and main content based on the menu selection
st.markdown('<h1 class="title">Expense Tracker</h1>', unsafe_allow_html=True)

if selected == "Home":
    st.write("Welcome to the Expense Tracker! You can manage your expenses and visualize them.")
    
elif selected == "Add Expense":
    st.subheader('Add a New Expense 🧾')

    # Create form to add new expenses
    date = st.date_input('📅 Date')
    category = st.selectbox('🛍️ Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input('💵 Amount', min_value=0.0, format="%.2f")
    description = st.text_input('✍️ Description', placeholder="Enter a brief description")
    
    if st.button('Add Expense'):
        add_expense(date, category, amount, description)
        with st.spinner('Adding expense...'):
            time.sleep(1)
        st.success('Expense added successfully! ✅')

    st.subheader('File Operations')
    if st.button('Save Expenses 💾'):
        save_expenses()
    if st.button('Load Expenses 📂'):
        load_expenses()

elif selected == "Reports":
    st.subheader('Expense Reports 📊')
    
    # Two-column layout for showing expenses and visualizations
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header('Expense List')
        if not st.session_state.expenses.empty:
            AgGrid(st.session_state.expenses)
        else:
            st.write("No expenses available.")

    with col2:
        st.header('Expense Visualization')
        if st.button('Visualize Expenses'):
            visualize_expenses()

# Footer
st.markdown(
    """
    <hr style="border:1px solid #4CAF50">
    <p style="text-align: center;">Built with 💻 and Streamlit</p>
    """, 
    unsafe_allow_html=True
)
