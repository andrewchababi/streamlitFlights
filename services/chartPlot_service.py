import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

def plot_flights_by_hour(df, time_col="updatedTime"):
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

def plot_passengers_by_hour(df, time_col="updatedTime", passenger_col="Passengers"):
    
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
    ax.set_xlim(3,24)
    ax.set_xticks(range(3, 24))
    ax.set_xticklabels(range(3, 24), fontsize=10)
    
    plt.tight_layout()
    return fig, ax


def create_passenger_dist_chart(passenger_dist: pd.DataFrame):
    p_chart = alt.Chart(passenger_dist).mark_bar().encode(
        x=alt.X('updatedTime:N', title="Time Slots", sort=list(passenger_dist['updatedTime'])),  
        y=alt.Y('passengers:Q', title="Number of Passengers"),
        tooltip=[
                    alt.Tooltip('updatedTime:N', title="Time "),
                    alt.Tooltip('passengers:Q', title="Total Passengers", format=',d')  # Comma format for numbers
                ]
            ).properties(
                width=700,
                height=400
            )
    return p_chart

def create_passenger_dist_monthly_chart(passenger_dist: pd.DataFrame):
    p_chart = alt.Chart(passenger_dist).mark_bar().encode(
        x=alt.X('time:N', title="Time Slots", sort=list(passenger_dist['time'])),  
        y=alt.Y('passengers:Q', title="Number of Passengers"),
        tooltip=[
                    alt.Tooltip('time:N', title="Time "),
                    alt.Tooltip('passengers:Q', title="Total Passengers", format=',d')  # Comma format for numbers
                ]
            ).properties(
                width=700,
                height=400
            )
    return p_chart

def create_flights_chart(flight_count: pd.DataFrame):
    f_chart = alt.Chart(flight_count).mark_bar().encode(
        x=alt.X('rounded_hour:N', title="Time Slots", sort=list(flight_count['rounded_hour']), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('flight_counts:Q', title="Number of Flights"),
        tooltip=[
            alt.Tooltip('rounded_hour:N', title="Hour"),
            alt.Tooltip('flight_counts:Q', title="Flights Count", format=',d')  # Ensures readable number format
        ]
    ).properties(
        width=700,
        height=400
    )
    
    return f_chart

def create_half_flights_chart(flight_half_count:pd.DataFrame):
    f_chart = alt.Chart(flight_half_count).mark_bar().encode(
            x=alt.X('rounded_half_hour_time:N', title="Time Slots", sort=list(flight_half_count['rounded_half_hour_time']), axis=alt.Axis(labelAngle=0)),
            y=alt.Y('flights_count:Q', title="Number of Flights"),
            tooltip=[
                alt.Tooltip('rounded_half_hour_time:N', title="Time"),
                alt.Tooltip('flights_count:Q', title="Flights Count", format=',d')
            ]
        ).properties(
            width=700,
            height=400
        )

    return f_chart