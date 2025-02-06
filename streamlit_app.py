import streamlit as st
import numpy as np
import pandas as pd
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_distribution(mean, std, size=1000):
    return np.random.normal(mean, std, size)

def calculate_metrics(not_risk_scores, at_risk_scores, threshold):
    # Calculate confusion matrix elements
    true_negatives = np.sum(not_risk_scores < threshold)
    false_positives = np.sum(not_risk_scores >= threshold)
    false_negatives = np.sum(at_risk_scores < threshold)
    true_positives = np.sum(at_risk_scores >= threshold)
    
    # Calculate metrics
    total_negatives = len(not_risk_scores)
    total_positives = len(at_risk_scores)
    
    specificity = true_negatives / total_negatives
    sensitivity = true_positives / total_positives
    accuracy = (true_positives + true_negatives) / (total_positives + total_negatives)
    
    return {
        'False Positive Rate': (false_positives / total_negatives) * 100,
        'False Negative Rate': (false_negatives / total_positives) * 100,
        'Accuracy': accuracy * 100,
        'Sensitivity': sensitivity * 100,
        'Specificity': specificity * 100
    }

def main():
    st.title('Medical Risk Score Analysis')
    
    # # Sidebar controls
    # st.sidebar.header('Distribution Parameters')
    
    # Distribution parameters
    # not_risk_mean = st.sidebar.slider('Not At-Risk Mean', 0.0, 100.0, 35.0)
    # at_risk_mean = st.sidebar.slider('At-Risk Mean', 0.0, 100.0, 65.0)
    # std_dev = st.sidebar.slider('Standard Deviation', 1.0, 20.0, 12.0)
    
    # Reset button for distributions
    if st.button('Reset Distributions'):
        low_mean = random.randint(10, 60)
        high_mean = random.randint(40, 80)
        std_dev_low = random.randint(1,20)
        std_dev_high = random.randint(1,20)
        size_first = random.randint(300,1500)
        size_second = random.randint(300,1500)
        st.session_state.not_risk_scores = generate_distribution(low_mean, std_dev_low, size=size_first)
        st.session_state.at_risk_scores = generate_distribution(high_mean, std_dev_high, size=size_second)
        st.session_state.distribution_reset = True
    
    # Initialize distributions if not already in session state
    if 'not_risk_scores' not in st.session_state:
        st.session_state.not_risk_scores = generate_distribution(35.0, 12.0)
        st.session_state.at_risk_scores = generate_distribution(65.0, 12.0, size=300)
    
    # Main threshold slider
    threshold = st.slider('Number of Risk Words', 
                         min_value=0, 
                         max_value=100, 
                         value=5,
                         step=1)
    
    # Create visualization
    fig = make_subplots(rows=1, cols=1)
    
    # Add distributions
    fig.add_trace(
        go.Histogram(
            x=st.session_state.not_risk_scores,
            name='Not At-Risk Messages',
            opacity=0.75,
            nbinsx=50,
            marker_color='#1b3a6f'
        )
    )
    
    fig.add_trace(
        go.Histogram(
            x=st.session_state.at_risk_scores,
            name='At-Risk Messages',
            opacity=0.75,
            nbinsx=50,
            marker_color='#c5a46d'
        )
    )
    
    # Add threshold line
    fig.add_vline(
        x=threshold,
        line_dash="dash",
        line_color="#5ab9ea",
        annotation_text=f"Threshold ({threshold})",
        annotation_position="top"
    )
    
    # Update layout
    fig.update_layout(
        title='Risk Score Distribution',
        xaxis_title='Risk Score',
        yaxis_title='Count',
        barmode='overlay',
        showlegend=True,
        height=500
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate and display metrics
    metrics = calculate_metrics(
        st.session_state.not_risk_scores,
        st.session_state.at_risk_scores,
        threshold
    )
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("False Alerts (Type I)", f"{metrics['False Positive Rate']:.1f}%")
    with col2:
        st.metric("Missed Alerts (Type II)", f"{metrics['False Negative Rate']:.1f}%")
    with col3:
        st.metric("Overall Accuracy", f"{metrics['Accuracy']:.1f}%")
    
    # Additional metrics in an expander
    with st.expander("Detailed Metrics"):
        st.write(f"Sensitivity (True Positive Rate): {metrics['Sensitivity']:.1f}%")
        st.write(f"Specificity (True Negative Rate): {metrics['Specificity']:.1f}%")

if __name__ == "__main__":
    main()