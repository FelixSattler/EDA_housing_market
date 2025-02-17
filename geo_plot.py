import plotly.graph_objs as go


# Visualizes houses with their respective price and number of bedrooms on a scatter mapbox plot.


def plotting_houses(df, fig, price_col='price', quality_col='house_quality', bedrooms_col='bedrooms', lat_col='lat', long_col='long', legend_entry = 'Houses <br>cheap (small) to expensive (large)'):
    """
    Visualizes houses with their repsective price and number of bedrooms on a scatter mapbox plot.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing house data.
    fig (go.Figure): Plotly figure to add the houses to.
    price_col (str): Column name for house prices. Default is 'price'.
    quality_col (str):  Column name for house quality. Default is 'house_quality'.
    bedrooms_col (str): Column name for the number of bedrooms. Default is 'bedrooms'.
    lat_col (str): Column name for latitude. Default is 'lat'.
    long_col (str): Column name for longitude. Default is 'long'.
    legend_entry (str): legend entry name for the scatter plot. Default is 'Houses'.

    Raises:
    ValueError: If any of the required columns are missing in the input DataFrame.

    Returns:
    None 

    Example:
    >>> df = pd.read_csv('your_dataset.csv')
    >>> plotting_houses(df)
    """

    # Ensure required columns are present
    required_columns = [price_col, quality_col, bedrooms_col, lat_col, long_col]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f'Missing required column: {col}')

    
    # Create hover text
    df['hover_text'] = 'Price: ' + df[price_col].astype(int).astype(str) + '$' + \
        '<br>Quality: ' + df[quality_col].astype(str) + \
        '<br>Bedrooms: ' + df[bedrooms_col].astype(str)

    # Normalize column for marker size
    def normalize_column(column):
        return (column - column.min()) / (column.max() - column.min())


    fig.add_trace(go.Scattermapbox(
        lat=df[lat_col],
        lon=df[long_col],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=(normalize_column(df[price_col]) + 1) * 10,  # Normalize sizes, +1 to avoid the cheapest price being =0 after normalization
            color='blue'
        ),
        text=df['hover_text'],
        hoverinfo='text',
        name= legend_entry,  # Legend entry
        showlegend=True
    ))

#----------------------------------------------------------------------------------------------------------

def add_choropleth_map(df, fig, counties, zipcode_col='zipcode', house_quality_col='house_quality', legend_entry='Average house quality <br>low (dark red) to high (bright yellow)'):
    """
    Adds a choropleth map of average house quality to a Plotly figure.

    Parameters:
    fig (go.Figure): Plotly figure to add the choropleth map to.
    df (pd.DataFrame): Input DataFrame containing house data.
    counties (dict): GeoJSON data for the counties.
    zipcode_col (str): Column name for zip codes. Default is 'zipcode'.
    house_quality_col (str): Column name for house quality. Default is average 'house_quality'.
    legend_entry (str): Legend entry name for the choropleth map. Default is 'Average house quality'.

    Raises:
    ValueError: If any of the required columns are missing in the input DataFrame.

    Returns:
    None

    Example:
    >>> fig = go.Figure()
    >>> df = pd.read_csv('your_dataset.csv')
    >>> add_choropleth_map(fig, df, counties, legend_entry='Average House Quality')
    """
    # Ensure required columns are present
    required_columns = [zipcode_col, house_quality_col]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f'Missing required column: {col}')

    # Create hover text
    df['hover_text'] = 'Zipcode: ' + df[zipcode_col].astype(str) + '<br>Quality: ' + df[house_quality_col].astype(str)

    # Add the choropleth map
    fig.add_trace(go.Choroplethmapbox(
        geojson=counties,
        locations=df[zipcode_col],
        z=df[house_quality_col],
        colorscale='Hot',
        showscale=False,  # Remove color scale
        marker_opacity=0.4,  # Reduce opacity so clicks and hover can pass through
        featureidkey='properties.ZCTA5CE10',
        name=legend_entry,  # Legend entry
        text=df['hover_text'],
        hoverinfo='text',
        showlegend=True  # Ensure it appears in the legend
    ))

#----------------------------------------------------------------------------------------------------------

def add_park_outlines_layer(fig, parks, legend_entry='Park outlines'):
    """
    Adds a scattermapbox dummy point for the legend and a geojson layer for park outlines to a Plotly figure.

    Parameters:
    fig (go.Figure): Plotly figure to add the layers to.
    parks (dict): GeoJSON data for the parks.
    legend_entry (str): Legend entry name for the scattermapbox. Default is 'Park outlines'.

    Returns:
    None

    Example:
    >>> fig = go.Figure()
    >>> parks = ...  # Load your GeoJSON data for parks
    >>> add_park_outlines_layer(fig, parks, legend_entry='Park outlines')
    """
    # Add scattermapbox dummy point for the legend
    fig.add_trace(go.Scattermapbox(
        lat=[None],  # Dummy point, so legend displays
        lon=[None],
        mode='lines',
        line=dict(width=3, color='green'),
        name=legend_entry,  # Legend entry
        showlegend=True
    ))

    # Add geojson layer for the actual lines
    fig.update_layout(
        mapbox_layers=[
            {
                'sourcetype': 'geojson',
                'source': parks,
                'type': 'line',
                'color': 'green',
                'line': {'width': 1.5}
            }
        ]
    )


#----------------------------------------------------------------------------------------------------------

def add_schools_layer(fig, gdf_schools, lat_col='LAT_CEN', lon_col='LONG_CEN', name_col='ABB_NAME', desc_col='FEATUREDES', legend_entry='Schools'):
    """
    Adds a Scattermapbox layer for schools in King County to a Plotly figure.

    Parameters:
    gdf_schools (pd.DataFrame): The GeoDataFrame containing school data.
    fig (go.Figure): The Plotly figure to add the layer to.
    lat_col (str): Column name for latitude. Default is 'LAT_CEN'.
    lon_col (str): Column name for longitude. Default is 'LONG_CEN'.
    name_col (str): Column name for school name. Default is 'ABB_NAME'.
    desc_col (str): Column name for school description. Default is 'FEATUREDES'.
    legend_entry (str): The name to display in the legend. Default is 'Schools'.
    
    Returns:
    None
    """
    # Create hover text
    gdf_schools['hover_text'] = gdf_schools[name_col].astype(str) + '<br>' + gdf_schools[desc_col].str.replace('School-', '', case=False).str.strip().astype(str)
    

    # Add the schools layer
    fig.add_trace(go.Scattermapbox(
        lat=gdf_schools[lat_col],
        lon=gdf_schools[lon_col],
        mode='markers',
        marker=dict(  # use dict to force chosen color and avoid interference with other layers
            size=4,  # Increased size for better visibility
            color='darkred',  # Force color to stay dark red
            opacity=0.8,  # Adjust opacity for contrast
            symbol="circle"  # Explicitly set symbol type to avoid color inheritance
        ),
        text=gdf_schools['hover_text'],
        hoverinfo='text',
        name=legend_entry,
        showlegend=True
    ))


#----------------------------------------------------------------------------------------------------------


def update_map_layout(fig, lat, lon, mapbox_style='open-street-map'):
    """
    Updates the layout of a Plotly figure with specific map and legend settings.

    Parameters:
    fig (go.Figure): Plotly figure to update.
    lat (float): Latitude for the map center.
    lon (float): Longitude for the map center.
    mapbox_style (str): Style of the mapbox. Default is 'open-street-map'.

    Returns:
    None

    Example:
    >>> fig = go.Figure()
    >>> update_map_layout(fig, lat=47.5864, lon=-121.9861)
    """
    fig.update_layout(
        mapbox_style=mapbox_style,
        mapbox_zoom=9,
        mapbox_center={"lat": lat, "lon": lon},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            title="Legend",
            orientation="v",  # Vertical legend
            yanchor="top",
            y=0.99,  # Position it near the top
            xanchor="left",
            x=0.01  # Move it to the left
        ), 
        width=1000,  # Change the width as needed
        height=1000  # Change the height as needed
    )
    
#----------------------------------------------------------------------------------------------------------

def vizualize_findings(
    df_houses=None, df_schools=None, df_county=None, parks=None, county=None, save_png=None,
    lat=47.3464, lon=-121.9861, mapbox_style='open-street-map'    
):
    """
    Generates an interactive map with optional layers for houses, schools, county data, and park outlines.
    
    Parameters:
    df_houses (DataFrame, optional): DataFrame containing house data to be plotted on the map.
    df_schools (DataFrame, optional): DataFrame containing school data to be plotted on the map.
    df_county (DataFrame, optional): DataFrame containing county data to be plotted as a choropleth map.
    parks (GeoDataFrame, optional): GeoDataFrame containing park outlines to be plotted on the map.
    county (str, optional): The specific county to be visualized in the choropleth map.
    save_png (str, optional): File path to save the generated map as a .png image.
    lat (float, optional): Latitude coordinate for centering the map. Default is 47.6003.
    lon (float, optional): Longitude coordinate for centering the map. Default is -122.1755.
    mapbox_style (str, optional): Mapbox style to be used for the base map. Default is 'open-street-map'.

    Returns:
    None

    This function generates an interactive map using Plotly and displays various spatial datasets
    such as houses, schools, parks, and county choropleth maps. The map is centered on the specified
    latitude and longitude coordinates. If `save_png` is provided, the map is saved as a .png file
    at the specified path.
    """
    fig = go.Figure()
  
    if df_county is not None and county is not None:
        add_choropleth_map(df_county, fig, county)
    
    if parks is not None:
        add_park_outlines_layer(fig, parks)
    
    if df_schools is not None:
        add_schools_layer(fig, df_schools)

    if df_houses is not None:
        plotting_houses(df_houses, fig)

    update_map_layout(fig, lat, lon, mapbox_style)
    fig.show()

    if save_png is not None:
        fig.write_image(save_png)
