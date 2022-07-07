import streamlit as st
import SessionState

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

state = SessionState.get(table=data)


def doSqlQuery():
    # sql code here

    return state.table.append(len(state.table) + 1)


if st.button("Do SQL"):
    doSqlQuery()

st.table(state.table)