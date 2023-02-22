import pages.homepage.homepage_data as homepage_data

from app import app
from dash import Input, Output, State


@app.callback(
    [
      Output(component_id='subcategory-selector', component_property='options'),
    #   Output(component_id='subcategory-selector', component_property='value'),
      Output(component_id='subcategory-selector', component_property='disabled'),
    ],
    Input(component_id='category-selector', component_property='value'),
)
def on_category_selection(category):
    if category is None:
        return [], True

    print(category)
    return [], False
    
    
# * Affects
# * Timeline graph
# * Artwork dropdown
# * possibly add 2 color wheels (one for the selected artwork and one for the parent category of that artwork)
# @app.callback()
# def on_subcategory_selection(subcategory):
#     pass