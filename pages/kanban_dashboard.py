"""
Kanban Dashboard Page

Purpose: Streamlit page for kanban-style task tracking and management.
Displays tasks/hunches in columns by status with drag-and-drop functionality,
cost tracking, and full CRUD operations.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from task_manager import (
    TaskManager,
    get_task_manager,
    STATUS_PENDING,
    STATUS_IN_PROGRESS,
    STATUS_COMPLETED,
    STATUS_ARCHIVED
)

# Page config
st.set_page_config(
    page_title="Kanban Dashboard - Gematria Hive",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize task manager
@st.cache_resource
def init_task_manager():
    """Initialize task manager singleton"""
    return get_task_manager(use_memory_fallback=True)


def format_cost(cost: float) -> str:
    """Format cost as currency"""
    if cost is None or cost == 0:
        return "$0.00"
    return f"${cost:.2f}"


def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return timestamp


def render_task_card(task: Dict, status: str) -> bool:
    """
    Render a task card and return True if status was changed
    
    Args:
        task: Task dictionary
        status: Current status column
        
    Returns:
        True if status was changed, False otherwise
    """
    task_id = task.get("id", "")
    content = task.get("content", "No content")
    cost = task.get("cost", 0.0) or 0.0
    timestamp = task.get("timestamp", "")
    links = task.get("links", []) or []
    
    # Create card container
    with st.container():
        # Card header with cost badge
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{content[:50]}{'...' if len(content) > 50 else ''}**")
        with col2:
            if cost > 0:
                st.caption(f"💰 {format_cost(cost)}")
        
        # Task details
        if timestamp:
            st.caption(f"📅 {format_timestamp(timestamp)}")
        
        if links:
            st.caption(f"🔗 {len(links)} link(s)")
        
        # Status change dropdown
        current_status = task.get("status", STATUS_PENDING)
        new_status = st.selectbox(
            "Status:",
            [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED],
            index=[STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED].index(current_status) if current_status in [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED] else 0,
            key=f"status_{task_id}",
            label_visibility="collapsed"
        )
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Edit", key=f"edit_{task_id}", use_container_width=True):
                st.session_state[f"edit_task_{task_id}"] = True
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{task_id}", use_container_width=True):
                st.session_state[f"delete_task_{task_id}"] = True
        
        # Check if status changed
        if new_status != current_status:
            return True
        
        return False


def main():
    """Main kanban dashboard"""
    st.title("📋 Kanban Dashboard")
    st.markdown("### Task Tracking & Management")
    
    # Initialize task manager
    task_manager = init_task_manager()
    
    # Sidebar for filters and actions
    with st.sidebar:
        st.header("Actions")
        
        # Create new task
        if st.button("➕ Create New Task", type="primary", use_container_width=True):
            st.session_state["create_task"] = True
        
        st.divider()
        
        # Filters
        st.header("Filters")
        filter_status = st.selectbox(
            "Filter by Status:",
            ["All", STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED]
        )
        
        filter_date_range = st.checkbox("Filter by Date Range")
        if filter_date_range:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=30))
            with col2:
                end_date = st.date_input("End Date", value=datetime.now().date())
        else:
            start_date = None
            end_date = None
        
        st.divider()
        
        # Statistics
        st.header("Statistics")
        try:
            stats = task_manager.get_task_statistics()
            st.metric("Total Tasks", stats.get("total", 0))
            st.metric("Total Cost", format_cost(stats.get("total_cost", 0.0)))
            st.metric("Avg Cost", format_cost(stats.get("avg_cost", 0.0)))
            
            st.subheader("By Status")
            for status, count in stats.get("by_status", {}).items():
                st.caption(f"{status.replace('_', ' ').title()}: {count}")
        except Exception as e:
            st.error(f"Error loading statistics: {e}")
    
    # Main content area
    # Handle create task
    if st.session_state.get("create_task", False):
        with st.expander("➕ Create New Task", expanded=True):
            with st.form("create_task_form"):
                content = st.text_area("Task Content:", height=100)
                status = st.selectbox(
                    "Status:",
                    [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED]
                )
                cost = st.number_input("Cost:", min_value=0.0, value=0.0, step=0.01)
                links_input = st.text_area("Links (one per line):", height=50)
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Create Task", type="primary")
                with col2:
                    cancel = st.form_submit_button("Cancel")
                
                if submit and content:
                    links = [link.strip() for link in links_input.split("\n") if link.strip()]
                    task = task_manager.create_task(
                        content=content,
                        status=status,
                        cost=cost,
                        links=links
                    )
                    if task:
                        st.success("Task created successfully!")
                        st.session_state["create_task"] = False
                        st.rerun()
                    else:
                        st.error("Failed to create task")
                elif cancel:
                    st.session_state["create_task"] = False
                    st.rerun()
    
    # Handle edit/delete tasks
    for key in list(st.session_state.keys()):
        if key.startswith("edit_task_"):
            task_id = key.replace("edit_task_", "")
            task = task_manager.get_task(task_id)
            if task:
                with st.expander(f"📝 Edit Task: {task.get('content', '')[:50]}", expanded=True):
                    with st.form(f"edit_task_form_{task_id}"):
                        content = st.text_area("Task Content:", value=task.get("content", ""), height=100)
                        status = st.selectbox(
                            "Status:",
                            [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED],
                            index=[STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED].index(task.get("status", STATUS_PENDING))
                        )
                        cost = st.number_input("Cost:", min_value=0.0, value=float(task.get("cost", 0.0) or 0.0), step=0.01)
                        links_input = st.text_area("Links (one per line):", value="\n".join(task.get("links", []) or []), height=50)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            submit = st.form_submit_button("Update Task", type="primary")
                        with col2:
                            cancel = st.form_submit_button("Cancel")
                        
                        if submit:
                            links = [link.strip() for link in links_input.split("\n") if link.strip()]
                            updated = task_manager.update_task(
                                task_id=task_id,
                                content=content,
                                status=status,
                                cost=cost,
                                links=links
                            )
                            if updated:
                                st.success("Task updated successfully!")
                                del st.session_state[key]
                                st.rerun()
                            else:
                                st.error("Failed to update task")
                        elif cancel:
                            del st.session_state[key]
                            st.rerun()
        
        elif key.startswith("delete_task_"):
            task_id = key.replace("delete_task_", "")
            task = task_manager.get_task(task_id)
            if task:
                st.warning(f"⚠️ Delete Task: {task.get('content', '')[:50]}...")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirm Delete", key=f"confirm_delete_{task_id}", use_container_width=True):
                        if task_manager.delete_task(task_id):
                            st.success("Task deleted successfully!")
                            del st.session_state[key]
                            st.rerun()
                        else:
                            st.error("Failed to delete task")
                with col2:
                    if st.button("❌ Cancel", key=f"cancel_delete_{task_id}", use_container_width=True):
                        del st.session_state[key]
                        st.rerun()
    
    # Kanban board columns
    st.divider()
    
    # Get tasks based on filter
    if filter_status == "All":
        all_tasks = task_manager.get_all_tasks(order_by="timestamp", ascending=False)
    else:
        all_tasks = task_manager.get_tasks_by_status(filter_status, order_by="timestamp", ascending=False)
    
    # Apply date filter if enabled
    if filter_date_range and start_date and end_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())
        all_tasks = [
            task for task in all_tasks
            if start_dt.isoformat() <= task.get("timestamp", "") <= end_dt.isoformat()
        ]
    
    # Group tasks by status
    tasks_by_status = {
        STATUS_PENDING: [t for t in all_tasks if t.get("status") == STATUS_PENDING],
        STATUS_IN_PROGRESS: [t for t in all_tasks if t.get("status") == STATUS_IN_PROGRESS],
        STATUS_COMPLETED: [t for t in all_tasks if t.get("status") == STATUS_COMPLETED],
        STATUS_ARCHIVED: [t for t in all_tasks if t.get("status") == STATUS_ARCHIVED]
    }
    
    # Display kanban columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader(f"📝 Pending ({len(tasks_by_status[STATUS_PENDING])})")
        for task in tasks_by_status[STATUS_PENDING]:
            if render_task_card(task, STATUS_PENDING):
                # Status changed, update task
                new_status = st.session_state.get(f"status_{task.get('id')}", STATUS_PENDING)
                task_manager.update_task(task.get("id"), status=new_status)
                st.rerun()
    
    with col2:
        st.subheader(f"🔄 In Progress ({len(tasks_by_status[STATUS_IN_PROGRESS])})")
        for task in tasks_by_status[STATUS_IN_PROGRESS]:
            if render_task_card(task, STATUS_IN_PROGRESS):
                new_status = st.session_state.get(f"status_{task.get('id')}", STATUS_IN_PROGRESS)
                task_manager.update_task(task.get("id"), status=new_status)
                st.rerun()
    
    with col3:
        st.subheader(f"✅ Completed ({len(tasks_by_status[STATUS_COMPLETED])})")
        for task in tasks_by_status[STATUS_COMPLETED]:
            if render_task_card(task, STATUS_COMPLETED):
                new_status = st.session_state.get(f"status_{task.get('id')}", STATUS_COMPLETED)
                task_manager.update_task(task.get("id"), status=new_status)
                st.rerun()
    
    with col4:
        st.subheader(f"📦 Archived ({len(tasks_by_status[STATUS_ARCHIVED])})")
        for task in tasks_by_status[STATUS_ARCHIVED]:
            if render_task_card(task, STATUS_ARCHIVED):
                new_status = st.session_state.get(f"status_{task.get('id')}", STATUS_ARCHIVED)
                task_manager.update_task(task.get("id"), status=new_status)
                st.rerun()
    
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()


if __name__ == "__main__":
    main()

