"""
Chart generation utilities
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio
from fasthtml.common import NotStr


def generate_plot_html(fig):
    """Convert Plotly figure to HTML"""
    return NotStr(pio.to_html(fig, full_html=False, include_plotlyjs=False, config={'responsive': True}))


def create_status_pie_chart(df: pd.DataFrame, title: str = "Status Distribution"):
    """Create pie chart for status distribution"""
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig = px.pie(status_counts, values='Count', names='Status', hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title=title)
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig


def create_scraper_status_bar_chart(df: pd.DataFrame, title: str = "Scraper Status Breakdown"):
    """Create bar chart for scraper status"""
    scraper_status_counts = df['scraper_status'].value_counts().reset_index()
    scraper_status_counts.columns = ['Scraper Status', 'Count']
    fig = px.bar(scraper_status_counts, x='Scraper Status', y='Count',
                 color='Scraper Status', text='Count',
                 title=title)
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig


def create_infrastructure_chart(active: int, on_hold: int, workers: int):
    """Create infrastructure overview bar chart"""
    infra_data = pd.DataFrame({
        'Category': ['Active Accounts', 'Accounts On Hold', 'Active Workers'],
        'Count': [active, on_hold, workers]
    })
    fig = px.bar(infra_data, x='Category', y='Count',
                 color='Category', text='Count',
                 title="Infrastructure Overview",
                 color_discrete_sequence=['#28a745', '#ffc107', '#007bff'])
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), showlegend=False)
    return fig


def create_timeline_chart(df: pd.DataFrame, period_label: str = "All Time"):
    """Create timeline chart for daily activity"""
    df['date'] = df['compute_datetime'].dt.date
    daily_activity = df.groupby('date').size().reset_index(name='Count')
    fig = px.line(daily_activity, x='date', y='Count', markers=True,
                  title=f"Scraped Companies Over Time ({period_label})")
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig


def create_processing_time_histogram(df: pd.DataFrame):
    """Create histogram for processing time distribution"""
    fig = px.histogram(df, x='processing_time',
                      nbins=30,
                      title="Processing Time Distribution (Hours)",
                      labels={'processing_time': 'Hours'})
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig
