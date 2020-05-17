import plotly.express as px
from htmlcreator import HTMLDocument

# Create new document with default CSS style
document = HTMLDocument()

# Set document title
document.set_title('my document with plotly figures')

# Embed plotly figure
document.add_header('plotly figure #1')
df = px.data.iris()
fig = px.scatter(df, x=df.sepal_length, y=df.sepal_width, color=df.species, size=df.petal_length)
fig.update_layout(title={'text': 'Iris Data Set', 'x': 0.5, 'xanchor': 'center'})
document.add_plotly_figure(fig)
# The first `add_plotly_figure` call includes `plotly.js` library in the document
# Including `plotly.js` makes HTML document self-contained but also heavier (+3 MB)

# Embed another plotly figure
document.add_header('plotly figure #2')
df = px.data.gapminder().query('continent=="Oceania"')
fig = px.line(df, x='year', y='lifeExp', color='country',
              color_discrete_sequence=px.colors.qualitative.Plotly[3:])
fig.update_layout(title={'text': 'Life expectancy: Oceania', 'x': 0.5, 'xanchor': 'center'})
document.add_plotly_figure(fig)

# Embed third plotly figure
document.add_header('plotly figure #3')
df = px.data.tips()
df['dayIndex'] = df['day'].map({'Thur': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7})
df = df.sort_values('dayIndex')
fig = px.histogram(df, x='day',
                   color_discrete_sequence=px.colors.qualitative.Plotly[5:], opacity=0.5)
fig.update_layout(title={'text': 'Tips', 'x': 0.5, 'xanchor': 'center'})
document.add_plotly_figure(fig)

# Write to file
output_filepath = '2_document_with_plotly.html'
document.write(output_filepath)
print(f'{output_filepath} has been saved successfully!')
