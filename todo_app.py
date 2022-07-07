import streamlit as st
import pandas as pd
import plotly.express as px
import query as qu


def remainder(id):

    menu = ["Create Task", "Read Tasks", "Update Task", "Delete Task"]

    choice = st.sidebar.selectbox("Menu", menu)
    qu.create_todo_table(id)

    if choice == "Read Tasks":
        st.subheader("View Tasks")
        result = qu.read_todo_task(id)
        frame = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        with st.expander('View Tasks'):
            st.dataframe(frame)

        with st.expander('Task Status'):
            task_df = frame['Status'].value_counts().to_frame()

            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names='index', values='Status')
            st.plotly_chart(p1)

    elif choice == "Create Task":
        st.subheader("Add Task")

        # design
        col1, col2 = st.columns(2)
        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")
            print(task_due_date)

        if st.button("Add Task") and task != "" and task_status != "" and task_due_date != "":
            qu.add_todo_task(id, task, task_status, task_due_date)
            st.success("Successfully Added Task:{}".format(task))

        else:
            st.error("Fill all the details")

    elif choice == "Update Task":
        st.subheader("Edit/Update Items")
        result = qu.read_todo_task(id)
        frame = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        with st.expander('Current Tasks'):
            st.dataframe(frame)

        list_of_task = qu.view_unique_task(id)

        choice = st.selectbox("Task to Edit", list_of_task)

        check_present = qu.get_task(id, choice[0], choice[1])
        if check_present:
            task1 = check_present[0][0]
            task1_status = check_present[0][1]
            task1_due_date = check_present[0][2]

            st.subheader("Update Task "+choice[0])
            col1, col2 = st.columns(2)
            with col1:
                new_task = st.text_area("Task", task1)

            with col2:
                new_task_status = st.selectbox(
                    "Update "+task1_status, ["ToDo", "Doing", "Done"])
                new_task_due_date = st.date_input(
                    "Update date: "+task1_due_date)

            if st.button("Update Task") and new_task != "" and new_task_status != "" and new_task_due_date != "":
                qu.update_task(id, task1, task1_status, task1_due_date,
                               new_task, new_task_status, new_task_due_date)
                st.success("Successfully Updated Task:{}".format(new_task))

            else:
                st.error("Change the Details")

    else:

        st.subheader("Delete Item")
        list_of_task = qu.read_todo_task(id)
        frame = pd.DataFrame(list_of_task, columns=[
                             'Task', 'Status', 'Due Date'])
        st.dataframe(frame)

        choice = st.selectbox("Task to Delete", list_of_task)
        st.info('Do you want to delete this task {}'.format(choice))
        if st.button('Delete Task'):
            qu.delete_task(id, choice[0], choice[1], choice[2])
            st.warning("Task {} has successfully deleted!!".format(choice[0]))
