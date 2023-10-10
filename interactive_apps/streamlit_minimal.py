"""
This file contains an toy example of a Streamlit app, showing
how to create and arrange widgets in Streamlit.

The main difference between Streamlit and Panel is the workflow.
In Panel, one binds inputs and functions that generate output.
In Streamlit, the whole file is re-run every time a change is
detected.

Author: Nikolai Kapralov
"""

import streamlit as st


def string_creator(symbol, length):
    """Toy function for testing input-output interaction"""
    return symbol * length
    

# Streamlit supports Markdown
st.title('_Minimal_ Example :sunglasses:')

# One of the ways to set up the layout in Streamlit 
# is to use `with` statements like the one below:
with st.sidebar:
    symbol = st.selectbox(label='Symbol',
                          options=['🌊', '🐘'])
    # From this line on the variable `symbol` contains
    # the value selected by the user, updated automatically

    length = st.slider(label='Length',
                       min_value=1, max_value=10, 
                       value=5, step=1)
    # From this line on the variable `length` contains
    # the value selected by the user, updated automatically


# Now we just generate output based on the provided values
st.text(string_creator(symbol, length))


# By default, multi-line text will also be displayed in the app
"""
Exercise: 
1. Add one or more widgets to the app
2. Update the `string_creator` function to use the value from the new widget somehow

Here is the list of widgets available in Streamlit:
https://docs.streamlit.io/library/api-reference/widgets

Some ideas (feel free to follow your own ones):

- TextInput: add custom prefix in the beginning of the string
- Checkbox: generate a square of symbols (`length` lines of `length` symbols) 
    if the checkbox is activated
"""