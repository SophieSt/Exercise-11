## remember to set your working directory before executing!
from osgeo import ogr
## check, if driver is existent
driverName = "KML"
drv = ogr.GetDriverByName(driverName)
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

## make sure this layer does not exist in 'data' folder
fn = "points.kml"
layername = "anewlayer"


## Create kml file
ds = drv.CreateDataSource(fn)

from osgeo import osr
## Set spatial reference
spatialReference = osr.SpatialReference()

## you can also do the following
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

## Create Layer
layer = ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)


## Ste coordinates for points of interest
gaia_coords = [0, 5.666319, 51.987327]   # coordinates of GAIA entrance
busstop_coords = [0, 5.667111, 51.969378]  # coordinates of bus station in Wageningen

points_coords = [gaia_coords, busstop_coords]  # list of both coordinates
points = ogr.Geometry(ogr.wkbPoint)   # Create points

for point_coord in points_coords:
    points.SetPoint(point_coord[0], point_coord[1], point_coord[2])   # SetPoint(self, int point, double x, double y, double z = 0)
    layerDefinition = layer.GetLayerDefn()    
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(points)
    layer.CreateFeature(feature)

 
## Save by "closing"    
ds.Destroy()


import folium
centermap_y = (gaia_coords[1] + busstop_coords[1])/2   # center coordinate latitude
centermap_x = (gaia_coords[2] + busstop_coords[2])/2   # center coordinate longitude
map_osm = folium.Map(location=[centermap_x, centermap_y])  # center to middle of GAIA and busstop
folium.Marker([gaia_coords[2], gaia_coords[1]], popup='GAIA').add_to(map_osm)  # add GAIA to the map
folium.Marker([busstop_coords[2], busstop_coords[1]], popup='Busstop Wageningen').add_to(map_osm)  # add the busstop to the map
map_osm.save('gaia_busstop.html')

