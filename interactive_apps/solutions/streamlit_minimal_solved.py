"""
Solution to the exercise from `streamlit_minimal.py`

Author: Nikolai Kapralov
"""

import streamlit as st


def string_creator(symbol, length, prefix, make_square):
    result = symbol * length
    if make_square:
        result = '\n'.join([symbol * length] * length)
    
    if prefix:
        return f'{prefix}:\n{result}'
    else:
        return result


st.title('Minimal Example :sunglasses:')

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

    prefix = st.text_input(label='Prefix')

    make_square = st.checkbox(label='Make square',
                              value=False)


# Now we just generate output based on the provided values
st.text(string_creator(symbol, length, prefix, make_square))


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