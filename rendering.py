import dash
from dash import Dash, html,dcc, callback 
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import dash_table
import pandas as pd 
import dash
from dash.dependencies import Input, Output, State

# get data
climate=pd.read_csv('../data/climate.csv',parse_dates=['date']) # climate data
iso=pd.read_csv('../data/iso_codes.csv') # iso data to make it plotable on the map

# merge climate and iso data
df=pd.merge(climate,iso, on='country', how='left')
df.head()

# sort by time
df = df.sort_values('date', ascending=True)

df['month']=df['date'].dt.month_name()
df['month_num']=df['date'].dt.month
df.head()

# data for one place
tirana=df[df['city']=='Tirana']
tirana = tirana[['avg_max_temp', 'avg_min_temp','avg_temp','month','month_num']]
tirana= tirana.groupby(['month','month_num'],as_index=False).mean()
tirana=tirana.sort_values('month_num')
tirana = tirana.drop('month_num', axis=1)

# make a table
d_table = dash_table.DataTable(tirana.to_dict('records'),
                                  [{"name": i, "id": i} for i in tirana.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                             style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })

# make a bar graph (from two days ago)
fig = px.bar(df, 
             x='city', 
             y='avg_temp', 
             height=300,
             animation_frame="date",
             #color_discrete_sequence=px.colors.sequential.Rainbow,
             color="region_y",
             barmode='group',
            title = "Contient Temperatures")   
    
#fig.show()

fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

graph = dcc.Graph(figure=fig)

# make a line graph
fig2 = px.line(tirana, x='month', y='avg_temp', height=300, title="Tirana Temperatures", markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)

# make a map (from one day ago)

fig3 = px.choropleth(df, locations='alpha-3', 
                    projection='natural earth',
                    scope='world',
                    color='avg_temp',
                    animation_frame='date',
                    color_continuous_scale=px.colors.sequential.Plotly3,
                    #range_color=(-34.6, 43.9)
                    range_color=(-10, 40)
)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )

# here we needed to change the geo color also to make the world black

graph3 = dcc.Graph(figure=fig3)


app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
#app =dash.Dash(external_stylesheets=[dbc.themes.VAPOR])
#app =dash.Dash(external_stylesheets=[dbc.themes.PULSE])

#dropdown = dcc.Dropdown(['Europe', 'Oceania', 'Asia', 'Africa','Americas'], "Europe", clearable=False)

# set app layout
#app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div([html.H1('My First Spicy Dash', style={'textAlign': 'center', 'color': 'green'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                      #html.Div(d_table)])
                       html.Div([html.Div('Tirana', style={'backgroundColor': 'blue', 'color': 'white', 'width': "Tirana"}),
                                 d_table,graph,graph2, graph3])
                    #    html.Div([html.Div('Tirana', style={'backgroundColor': 'blue', 'color': 'white', 'width': "Tirana"}),
                    #              d_table,dropdown,dcc.Graph(id='my-output')])
                    #    #,graph2, graph3])
])



# @callback(
#     #Output(graph, "figure"), 
#     #Input(dropdown, "value"))

# Output(component_id='my-output', component_property='figure'),
# Input(component_id='my-input', component_property='value')
# )

# def update_bar_chart(region_y): 
#     mask=df["region_y"]==region_y # coming from the function parameter
#     fig =px.bar(df[mask], 
#              x='city', 
#              y='avg_temp',  
#              color='region_y',
#              barmode='group',
#              height=300, title = "Contient Temperatures")
#     fig = fig.update_layout(
#         plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
#     )

 #   return fig # whatever you are returning here is connected to the component property of
                       #the output which is figure

if __name__ == "__main__":
    app.run_server(port=8081)