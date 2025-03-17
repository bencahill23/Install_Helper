import pprint
import folium
import streamlit as st
import xml.etree.ElementTree as ET

from pyproj import Transformer
from lxml import etree
from bs4 import BeautifulSoup

from streamlit_folium import st_folium
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
from folium.plugins import GroupedLayerControl
from streamlit_folium import folium_static

@st.cache_data
def GMLtoLonLat(gmlCoords):
	transformer = Transformer.from_crs("EPSG:25832", "EPSG:4326") #25832 is the source format - found in header
	tc = transformer.transform(gmlCoords[0], gmlCoords[1])
	return tc

@st.cache_resource
def getData(xmlfile):
	with open(xmlfile) as fp:
		xmldata = BeautifulSoup(fp, 'lxml')
	print("Importing Data")
	return xmldata


def create_map():
    if 'map' not in st.session_state or st.session_state.map is None:
        m = folium.Map(location=[55.681181, 12.381820], zoom_start=15)
        
        marker_cluster = MarkerCluster().add_to(m)
        folium.Marker(location=[45.372, -121.6972], popup="Mt. Hood Meadows").add_to(marker_cluster)
        for (i,loc) in enumerate(crds):
        	folium.CircleMarker(location = [loc[0], loc[1]], radius = 5, fill = True, fill_color = 'blue', popup=crds[i] , tooltip = sources[i]).add_to(m) 
        #fmc = FastMarkerCluster(data=crds,callback=callback, control=True).add_to(m)

        st.session_state.map = m  # Save the map in the session state
    return st.session_state.map


def show_map():
    m = create_map()  # Get or create the map
    folium_static(m, width=1000, height=800)



callback = """\
function (row) {
	var icon, marker;
	icon = L.AwesomeMarkers.icon({
		icon: "map-marker", markerColor: "red"});
	marker = L.marker(new L.LatLng(row[0], row[1]));
	marker.setIcon(icon);
	return marker;
};
"""


vendorName = ''

xmlfile = 'DOLL_lys.gml'
xmldata = getData(xmlfile)

coords = 'gml:coordinates'
road_names = 'ogr:vej'
source = 'ogr:kilde'
item = 'ogr:styklist'

raw_coords = []
road_names = []
sources = []
items = []

list_of_road_names = xmldata.find_all(road_names) 
list_of_coords = xmldata.find_all(coords)
list_of_sources = xmldata.find_all(source)
list_of_items = xmldata.find_all(item)



for (i,it) in enumerate(list_of_coords):
	coord_data = it.text
	raw_coords.append(coord_data)

	#roadname_data = list_of_road_names[i].text
	#road_names.append(roadname_data)

	sources_data = list_of_sources[i].text
	sources.append(sources_data)

	items_data = list_of_items[i].text
	items.append(items_data)


# coords come back as a list of pairs and must be seperated at the comma and added to a new list
crds = []
for point in raw_coords:
	floatdata = [float(item) for item in point.split(',')]
	crds.append(GMLtoLonLat(floatdata.copy()))

#####################
#  GUI
#####################

show_map()


#vendorName = st.text_input('Vendor Name', 'Vendor Name', label_visibility="collapsed")
#st_data = st_folium(m, width=700)
