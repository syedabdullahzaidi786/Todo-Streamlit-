import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .todo-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = []

# Header
st.title("📝 Todo Application")
st.markdown("---")

# Add new todo
with st.form("add_todo"):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_todo = st.text_input("Add a new task", placeholder="Enter your task here...")
    with col2:
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    
    submitted = st.form_submit_button("Add Task")
    
    if submitted and new_todo:
        todo_item = {
            "task": new_todo,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.todos.append(todo_item)
        st.success("Task added successfully!")
        st.experimental_rerun()

# Display todos
st.subheader("Your Tasks")
if not st.session_state.todos:
    st.info("No tasks yet. Add some tasks to get started!")
else:
    # Convert todos to DataFrame for better display
    df = pd.DataFrame(st.session_state.todos)
    
    # Display each todo item
    for index, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Create a checkbox for completion status
                if st.checkbox(f"{row['task']}", key=f"check_{index}", value=row['completed']):
                    st.session_state.todos[index]['completed'] = True
                    st.experimental_rerun()
                
                # Show priority with color coding
                priority_color = {
                    "Low": "green",
                    "Medium": "orange",
                    "High": "red"
                }
                st.markdown(f"Priority: <span style='color: {priority_color[row['priority']]}'>{row['priority']}</span>", 
                          unsafe_allow_html=True)
                st.caption(f"Created: {row['created_at']}")
            
            with col2:
                # Edit button
                if st.button("Edit", key=f"edit_{index}"):
                    st.session_state.editing_index = index
                    st.experimental_rerun()
            
            with col3:
                # Delete button
                if st.button("Delete", key=f"delete_{index}"):
                    st.session_state.todos.pop(index)
                    st.experimental_rerun()
            
            st.markdown("---")

# Edit todo form
if 'editing_index' in st.session_state:
    with st.form("edit_todo"):
        st.subheader("Edit Task")
        index = st.session_state.editing_index
        edited_task = st.text_input("Edit task", value=st.session_state.todos[index]['task'])
        edited_priority = st.selectbox("Edit priority", 
                                     ["Low", "Medium", "High"],
                                     index=["Low", "Medium", "High"].index(st.session_state.todos[index]['priority']))
        
        if st.form_submit_button("Save Changes"):
            st.session_state.todos[index]['task'] = edited_task
            st.session_state.todos[index]['priority'] = edited_priority
            del st.session_state.editing_index
            st.success("Task updated successfully!")
            st.experimental_rerun()
        
        if st.form_submit_button("Cancel"):
            del st.session_state.editing_index
            st.experimental_rerun()

# Statistics
st.sidebar.subheader("Task Statistics")
if st.session_state.todos:
    total_tasks = len(st.session_state.todos)
    completed_tasks = sum(1 for todo in st.session_state.todos if todo['completed'])
    pending_tasks = total_tasks - completed_tasks
    
    st.sidebar.metric("Total Tasks", total_tasks)
    st.sidebar.metric("Completed Tasks", completed_tasks)
    st.sidebar.metric("Pending Tasks", pending_tasks)
    
    # Priority distribution
    priority_counts = pd.DataFrame(st.session_state.todos)['priority'].value_counts()
    st.sidebar.subheader("Priority Distribution")
    st.sidebar.bar_chart(priority_counts)
else:
    st.sidebar.info("No tasks to display statistics.")
