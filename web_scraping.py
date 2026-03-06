# IBM Python Project for Data Science - Final Assignment
# Analyzing Historical Stock/Revenue Data and Building a Dashboard
# Save this file as: assignment.py
# Requirements: pip install yfinance pandas requests beautifulsoup4 plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ────────────────────────────────────────────────
# Required graphing function (must keep this exact signature)
# ────────────────────────────────────────────────
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data["Date"], infer_datetime_format=True),
            y=stock_data["Close"].astype("float"),
            name="Share Price"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data["Date"], infer_datetime_format=True),
            y=revenue_data["Revenue"].astype("float"),
            name="Revenue"
        ),
        row=2, col=1
    )

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )

    fig.show()


# ────────────────────────────────────────────────
# Question 1 – Tesla Stock Data
# ────────────────────────────────────────────────
print("\nQuestion 1: Tesla Stock Data (last 5 rows)")
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data = tesla_data.reset_index()
print(tesla_data.tail())


# ────────────────────────────────────────────────
# Question 2 – Tesla Revenue Data (web scrape)
# ────────────────────────────────────────────────
print("\nQuestion 2: Tesla Revenue Data (last 5 rows)")
url_tesla = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
response = requests.get(url_tesla)
soup = BeautifulSoup(response.text, "html5lib")

# Find the table and read it
tables = soup.find_all("table")
for table in tables:
    if "Tesla Quarterly Revenue" in str(table) or "Quarterly Revenue" in str(table):
        tesla_revenue = pd.read_html(str(table))[0]
        break
else:
    # Fallback - sometimes class-based
    tesla_revenue = pd.read_html(response.text, match="Revenue")[0]

tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(",", "").str.replace("$", "", regex=False)
tesla_revenue = tesla_revenue[tesla_revenue["Revenue"].str.strip() != ""]
tesla_revenue.dropna(inplace=True)
print(tesla_revenue.tail())


# ────────────────────────────────────────────────
# Question 3 – GameStop (GME) Stock Data
# ────────────────────────────────────────────────
print("\nQuestion 3: GameStop Stock Data (last 5 rows)")
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data = gme_data.reset_index()
print(gme_data.tail())


# ────────────────────────────────────────────────
# Question 4 – GameStop Revenue Data (web scrape)
# ────────────────────────────────────────────────
print("\nQuestion 4: GameStop Revenue Data (last 5 rows)")
# IBM often provides this static page in the course
url_gme = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
response_gme = requests.get(url_gme)
soup_gme = BeautifulSoup(response_gme.text, "html5lib")

gme_revenue = pd.read_html(str(soup_gme), match="GameStop Quarterly Revenue")[0]
gme_revenue.columns = ["Date", "Revenue"]
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(",", "").str.replace("$", "", regex=False)
gme_revenue.dropna(inplace=True)
print(gme_revenue.tail())


# ────────────────────────────────────────────────
# Question 5 – Tesla Stock + Revenue Dashboard
# ────────────────────────────────────────────────
print("\nQuestion 5: Generating Tesla Dashboard...")
make_graph(tesla_data, tesla_revenue, "Tesla")


# ────────────────────────────────────────────────
# Question 6 – GameStop Stock + Revenue Dashboard
# ────────────────────────────────────────────────
print("\nQuestion 6: Generating GameStop Dashboard...")
make_graph(gme_data, gme_revenue, "GameStop")


print("\nAll 6 questions completed. You can now convert this .py file to .ipynb if needed, or run it directly.")
print("Note: Interactive Plotly graphs will open in your browser when running this script.")
