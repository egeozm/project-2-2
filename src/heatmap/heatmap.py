import plotly.graph_objects as go
import json
import requests
import plotly.colors

class EuropeanHeatmap:
    """
    A class to generate an interactive choropleth heatmap of Europe with annotations.
    """

    def __init__(self, geojson_url="https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"):
        self.geojson_url = geojson_url
        self.country_id_property = 'ISO3'
        self.geojson_data = self._load_geojson()
        self.country_data = {}
        self.fig = None

    def _fetch_geojson_from_url(self):
        """Fetches GeoJSON data from the specified URL."""
        try:
            response = requests.get(self.geojson_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"ERROR: Could not fetch GeoJSON. {e}")
            return None

    def _load_geojson(self):
        """Loads and validates the GeoJSON data."""
        if not self.geojson_url:
            return None
        data = self._fetch_geojson_from_url()
        if data and data.get('features'):
            return data
        return None

    def _calculate_centroid(self, geometry):
        """
        Calculates the centroid of a GeoJSON geometry.
        For MultiPolygons, it finds the centroid of the largest polygon.
        """
        if geometry['type'] == 'Polygon':
            coords = geometry['coordinates'][0]
        elif geometry['type'] == 'MultiPolygon':
            largest_polygon = max(geometry['coordinates'], key=lambda polygon: len(polygon[0]))
            coords = largest_polygon[0]
        else:
            return 0, 0

        lon, lat = 0, 0
        for point in coords:
            lon += point[0]
            lat += point[1]
        return lon / len(coords), lat / len(coords)

    def update_data(self, data):
        """Updates the country data for the map."""
        self.country_data = data

    def display_map(self, title="European Energy Map", colorscale_data="Viridis", colorbar_title_data="Value"):
        """
        Generates and displays a choropleth map with country annotations.
        """
        if not self.geojson_data:
            print("ERROR: GeoJSON data not loaded. Cannot display map.")
            return

        all_geojson_locations = [
            feature['properties'][self.country_id_property]
            for feature in self.geojson_data['features']
            if self.country_id_property in feature.get('properties', {})
        ]

        locations, values, hover_text = [], [], []
        for loc in all_geojson_locations:
            locations.append(loc)
            value = self.country_data.get(loc)
            if value is not None:
                values.append(value)
                hover_text.append(f"{loc}: {value:.2f}")
            else:
                values.append(0)
                hover_text.append(f"{loc}: No Data")

        custom_colorscale = [
            [0, 'rgba(255, 255, 255, 0)'],
            [0.001, 'rgb(217, 217, 217)'],
            [0.25, 'rgb(68, 1, 84)'],
            [0.5, 'rgb(255, 102, 102)'],
            [1.0, 'rgb(255, 255, 0)']
        ]

        choropleth_trace = go.Choropleth(
            geojson=self.geojson_data,
            locations=locations,
            z=values,
            featureidkey=f"properties.{self.country_id_property}",
            colorscale=custom_colorscale,
            colorbar_title=colorbar_title_data,
            colorbar_dtick=0.25,
            hovertext=hover_text,
            hoverinfo="text",
            marker_line_color='black',
            marker_line_width=0.7,
            zmin=0,
            zmax=2,
            autocolorscale=False,
            marker_opacity=1,
            zauto=False
        )

        lons, lats, texts = [], [], []
        for feature in self.geojson_data['features']:
            iso_code = feature['properties'].get(self.country_id_property)
            
            
            if iso_code and self.country_data.get(iso_code, 0) > 0:
                if feature.get('geometry'):
                    lon, lat = self._calculate_centroid(feature['geometry'])
                    
                    if iso_code == 'FRA': lat += 1.5
                    if iso_code == 'SWE': lat -= 1.5
                    if iso_code == 'FIN': lat -= 1
                    if iso_code == 'GRC': lon -= 1.5; lat += 1
                    if iso_code == 'ITA': lat += 1

                    lons.append(lon)
                    lats.append(lat)
                    texts.append(iso_code)

        annotation_trace = go.Scattergeo(
            lon=lons,
            lat=lats,
            text=texts,
            mode='text',
            textfont=dict(
                family="Arial, sans-serif",
                size=10,
                color="black"
            ),
            hoverinfo='none',
            showlegend=False
        )

        self.fig = go.Figure(data=[choropleth_trace, annotation_trace])

        self.fig.update_layout(
            title_text=title,
            geo=dict(
                scope='europe',
                center=dict(lon=12, lat=53),
                projection_scale=4,
                bgcolor='rgba(0,0,0,0)',
                visible=False,
                showframe=False,
                showcoastlines=False,
                showcountries=False,
                showland=True,
                landcolor='rgba(255, 255, 255, 0)'
            ),
            margin={"r":10, "t":50, "l":10, "b":10},
            dragmode='zoom',
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        self.fig.show()

if __name__ == "__main__":
    european_map = EuropeanHeatmap()

    country_code_mapping = {
        'EE': 'EST', 'ES': 'ESP', 'GR': 'GRC', 'FR': 'FRA', 'RO': 'ROU'
    }

    solar_reliability_scores = { 
        'EE': 1.97,
        'ES': 0.85,
        'GR': 0.72,
        'FR': 0.71,
        'RO': 0.68
    }

    solar_reliability_data = {
        country_code_mapping[code]: score
        for code, score in solar_reliability_scores.items()
    }

    european_map.update_data(solar_reliability_data)
    european_map.display_map(
        title="European Solar Energy Reliability",
        colorbar_title_data="Solar Reliability Score"
    )