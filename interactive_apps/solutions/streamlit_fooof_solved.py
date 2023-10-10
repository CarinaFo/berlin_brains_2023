"""
This file contains an exercise/tutorial on developing a Streamlit app, 
which allows exploring different parameters of the FOOOF method.

The script is structured into several steps with comments and `st.stop()`
instructions, which stop the execution of Streamlit at a certain line.
Comment or delete the `st.stop()` lines to proceed with further steps.

Author: Nikolai Kapralov
"""

import numpy as np
import matplotlib.pyplot as plt
import mne
import streamlit as st

from fooof import FOOOF
from fooof.plts.annotate import plot_annotated_model
from pathlib import Path
from mne_bids import print_dir_tree


# Title
st.title("FOOOF")
with st.expander("Learn more about FOOOF:"):
    st.markdown("[Documentation](https://fooof-tools.github.io/fooof/index.html)")
    st.markdown("[Tutorials](https://fooof-tools.github.io/fooof/auto_tutorials/index.html)")
    st.markdown("[Paper](https://doi.org/10.1038/s41593-020-00744-x)")


# STEP 0: Set up the location of the dataset
#
# * Provide the full path to the dataset in the variable `path_to_data` below.
# * Save the file and use the 'Always rerun' option in the upper right corner
#   of the app webpage to update the Streamlit app on every save.
# * If the correct path is provided, you should see the list of files and folders 
#   contained in the dataset (first level only, e.g., `sub-XX` folders) in the app.
# * After that, comment or delete lines 39-43 to remove this output and proceed

path_to_data = None
if path_to_data is None:
    st.warning('Please specify the full path to the dataset in the variable `path_to_data` (line XXX)')


# st.code(print_dir_tree(path_to_data, 
#                        max_depth=1, return_str=True),
#         language=None)

# st.stop()


# Helper functions
@st.cache_data    # 👈 Add the caching decorator
def load_data(path_to_data):
    path_to_file = Path(path_to_data) / 'sub-01' / 'sub-01-raw.fif'
    return mne.io.read_raw_fif(path_to_file)


@st.cache_data    # 👈 Add the caching decorator
def get_spectrum():
    return raw.compute_psd(fmin=0, fmax=250)


# STEP 1: Load the data, select M/EEG channels, and calculate the spectrum
#
# * Once the app is updated, you should see the list of M/EEG channels
#   (output is split into elements 0-100, 100-200, and so on)
# * After that, comment lines 71-73 to remove this output and proceed further

raw = load_data(path_to_data)
meeg_idx = mne.pick_types(raw.info, meg=True, eeg=True)
meeg_ch_names = mne.pick_info(raw.info, meeg_idx)['ch_names']
spec = get_spectrum()

# st.write is a universal function that will try to use the most suitable
# output format depending on the data type (string, array, pandas DataFrame)
# st.write(meeg_ch_names)

# st.stop()


# STEP 2: Adding widgets and a debug output
#
# * The updated app should contain a sidebar with three widgets
# * The main panel contains a string, which is updated based on the values
#   of the widgets. This output is helpful for debugging to ensure that
#   the input is stored correctly
# * Comment or delete line 97 to proceed

with st.sidebar:
    # Select a channel to fit FOOOF
    channel = st.selectbox('Channel', meeg_ch_names)

    f_range = st.slider("Frequency range (Hz)", value=[1, 45],
                        min_value=0, max_value=250, step=1)

    peak_width = st.slider("Peak width limits (Hz)", value=[0.5, 12.0],
                           min_value=0., max_value=40., step=0.5)
    
    max_n_peaks = st.slider("Maximal number of peaks", value=3,
                            min_value=1, max_value=10)
    
    aperiodic_mode = st.radio("Aperiodic mode",
                              options=['fixed', 'knee'],
                              horizontal=True)

    # Control the annotations to the FOOOF plots
    annotate_peaks = st.checkbox('Annotate peaks', value=False)
    annotate_aperiodic = st.checkbox('Annotate aperiodic', value=False)

# Show the values as text in the app for debugging purposes
# st.write(f'''
# Channel: {channel}, frequency range: {f_range},
# peak width: {peak_width}, max number of peaks: {max_n_peaks}, aperiodic_mode: {aperiodic_mode},
# annotate_peaks: {annotate_peaks}, annotate_aperiodic: {annotate_aperiodic}
# ''')

# st.stop()


# STEP 3: Reduce the amount of unnecessary computations
#
# As you may have noticed, after adding the widgets in the step 2,
# every manipulation of the widget leads to calculations that take
# noticeable time even though there is no meaningful output yet.
#
# This is caused by the workflow of Streamlit - every time the user
# manipulates the widget, this script is re-run as a whole, and 
# spectra are calculated for all channels (see step 1).
#
# Since the spectra do not really depend on the values of the widgets,
# it would make a lot of sense to calculate them only once and then 
# re-use the calculated values on the next re-run of the script. This
# mechanism is called caching, and in Streamlit caching is achieved through
# decorators.
#
# Decorators are wrapper functions that add some functionality (in this case,
# caching of the results) to existing functions. To add the decorator to a 
# function, you need to use the following syntax:
#
# @name_of_the_decorator   # Added the decorator
# def my_function(arg1, arg2):
#     pass
#
# `st.cache_data` decorator should be used to cache the results of the function.
# To speed up the computations, go back to the helper functions `load_data` and
# `get_spectrum` (lines 48-55) and add the decorator to both of them.
#
# Update the browser page. Notice that there is a delay while the application
# is starting (functions `load_data` and `get_spectrum` are launched for the
# first time), but manipulations of the widgets don't take so long anymore. This
# is important for the future steps to work faster! :)
#
# * Now remove or comment the stop instruction below
# st.stop()


# STEP 4: Run FOOOF and prepare the output
#
# In step 2, we created a widget to select one of the channels.
# Now, we run the FOOOF algorithm to split the spectra of the selected
# channel into aperiodic and periodic components and visualize the
# FOOOF fit with the `plot_annotated_model` method of the FOOOF object.
#
# This figure will be added to the app in step 5 and updated 
# automatically depending on the values of the widgets.

# Extract the spectra for the given channel
psd, freqs = spec.get_data(picks=channel, return_freqs=True)

# Initialize the FOOOF object and fit it to the spectra
fm = FOOOF(peak_width_limits=peak_width,
           max_n_peaks=max_n_peaks,
           aperiodic_mode=aperiodic_mode)
fm.fit(freqs, np.squeeze(psd), freq_range=f_range)

# Plot the FOOOF fits (upper subplot is in the linear scale,
# lower subplot is log-scaled)
fig_fit, (ax_linear, ax_log) = plt.subplots(2, 1, figsize=(7, 6))
plot_annotated_model(fm, annotate_peaks=annotate_peaks, 
                     annotate_aperiodic=annotate_aperiodic,
                     ax=ax_linear)
ax_linear.set_title('Linear axes')

plot_annotated_model(fm, annotate_peaks=annotate_peaks, 
                     annotate_aperiodic=annotate_aperiodic,
                     plt_log=True, ax=ax_log)
ax_log.set_title('Log-scaled axes')


# STEP 5: Arrange the output in the app
#
# Finally, we add the output to the main panel of the app.
# We split the panel into two columns that take 80% and 20% of
# the available width, respectively.
#
# 80% column contains the FOOOF plots, while the 20% shows some
# of the key FOOOF parameters: offset and exponent (aperiodic
# part of the spectra) and peak frequency for the left-most peak.

col_left, col_right = st.columns([0.8, 0.2])

# with statement is used to pack widgets in the column
with col_left:
    st.pyplot(fig_fit)

# with statement is used to pack widgets in the column
with col_right:
    st.metric('Offset',
              round(fm.aperiodic_params_[0], 2))
    st.metric('Exponent',
              round(fm.aperiodic_params_[-1], 2))
    if fm.peak_params_.shape[0]:
        st.metric('Peak frequency (Hz)\n\n[first peak only]',
                  round(fm.peak_params_[0, 0], 2))
    

"""
Exercise:

Use checkboxes 'Annotate peaks' and 'Annotate aperiodic' (e.g.,
for channel EEG039) to highlight the estimated parameters of the
spectra.

Add more FOOOF parameters to the app to explore their influence
on the resulting fit, in particular:

1. Frequency range (provided to the `fm.fit` function)
2. FOOOF settings (provided to `FOOOF`):
  * `peak_width_limits`
  * `max_n_peaks`
  * `aperiodic_mode`
"""