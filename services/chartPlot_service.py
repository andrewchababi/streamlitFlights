import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

def plot_flights_by_hour(df, time_col="time"):
    # Ensure pyplot import is correct first
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df['rounded_time'] = df[time_col].dt.round("h")
    df['rounded_hour'] = df['rounded_time'].dt.hour
    
    flight_counts = df.groupby('rounded_hour').size().reindex(range(24), fill_value=0)
    
    # Set style using proper reference
    sns.set_theme(
        style='ticks',
        context="talk",
        palette="viridis",
        font="Arial"
    )
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(flight_counts.index, flight_counts.values, color='royalblue', alpha=0.7)
    
    # Customize labels and title with improved font sizes and weights
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_ylabel("Number of Flights", fontsize=12)
    ax.set_xlim(3,24)
    ax.set_xticks(range(3, 24))
    ax.set_xticklabels(range(3, 24), fontsize=10)
    
    plt.tight_layout()
    return fig, ax

def plot_passengers_by_hour(df, time_col="time", passenger_col="Passengers"):
    
    # Convert time column to datetime
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df['rounded_time'] = df[time_col].dt.round("h")
    df['rounded_hour'] = df['rounded_time'].dt.hour
    
    # Aggregate passengers per hour
    passenger_counts = df.groupby('rounded_hour')[passenger_col].sum().reindex(range(24), fill_value=0)
    
    # Set style using seaborn
    sns.set_theme(
        style='ticks',
        context="talk",
        palette="viridis",
        font="Arial"
    )
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(passenger_counts.index, passenger_counts.values, color='royalblue', alpha=0.7)
    
    # Customize labels and title
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_ylabel("Passengers", fontsize=12)
    ax.set_xlim(3,23)
    ax.set_xticks(range(3, 23))
    ax.set_xticklabels(range(3, 23), fontsize=10)
    
    plt.tight_layout()
    return fig, ax
