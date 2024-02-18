import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = dash.Dash(__name__)
data = pd.read_csv('Marketing campaign dataset.csv')
df = pd.DataFrame()
df['time'] = pd.to_datetime(data['time'])
df['ctr'] = (data['clicks'] / data['impressions']) * 100
df.index = df['time']
resampled = df["ctr"].resample("D").agg(["mean"]).rename(columns={"mean": "ctr"})

data['spent_budget_per_day'] = data['campaign_budget_usd'] / data['no_of_days']

fig = px.line(resampled, title='CTR Over Time', width=600,
              height=400)

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig2 = px.scatter(data, x=data["impressions"], y=data["clicks"], color=data["channel_name"],
                  title='Clicks vs. Impressions for Delivery Channels', width=600, height=400)

counts = data['advertiser_name'].value_counts().head(5)
fig3 = px.pie(counts, values=counts.values, names=counts.index, title='Top 5 Advertisers', width=600, height=400)

left_fig = html.Div(children=dcc.Graph(figure=fig))
right_fig = html.Div(children=dcc.Graph(figure=fig2))

upper_div = html.Div([left_fig, right_fig], style={"display": "flex"})
central_div = html.Div(
    children=dcc.Graph(figure=fig3),
    style={"display": "flex", "justify-content": "center"},
)
app.layout = html.Div([html.H1("Advertiser Analytics"), upper_div, central_div])

if __name__ == "__main__":
    app.run_server(debug=True)
