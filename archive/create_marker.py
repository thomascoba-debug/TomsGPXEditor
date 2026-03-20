import folium


def create_marker(lat, lon, text):

    marker = folium.Marker(
        location=(lat, lon),
        popup=text
    )

    return marker