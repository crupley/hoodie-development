from shapely.ops import cascaded_union, polygonize
import shapely.geometry as geometry
from scipy.spatial import Delaunay
from fastkml import kml
import numpy as np
import math
 
def alpha_shape(points, alpha):
    """

    ** function from
    http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/ **
    
    Compute the alpha shape (concave hull) of a set
    of points.
 
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
 
    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])
 
    coords = np.array([point.coords[0]
                       for point in points])
 
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
 
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
 
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
 
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c)) + 1e-10
        circum_r = a*b*c/(4.0*area)
 
        # Here's the radius filter.
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
 
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points

def make_polys(df):
    '''
    df: lat, lon, cnum
    returns: list of polygons
    '''

    gs = df.cnum.unique()

    polys = []
    for g in gs:
        groupn = df[df.cnum == g]
        points = geometry.MultiPoint(zip(groupn.lon, groupn.lat))
        if len(points) > 2:
            polygon, edge_points = alpha_shape(points, alpha=300)
        else:
            polygon = points
        polys.append(polygon)
    return polys

def make_kml(polys, filename):
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns, 'docid', 'doc name', 'doc description')
    f = kml.Folder(ns, 'fid', 'f name', 'f description')
    k.append(d)
    d.append(f)
    nf = kml.Folder(ns, 'nested-fid', 'nested f name', 'nested f description')
    f.append(nf)
    f2 = kml.Folder(ns, 'id2', 'name2', 'description2')
    d.append(f2)
    for poly in polys:
        p = kml.Placemark(ns, 'id', 'name', 'description')
        p.geometry = poly
        f2.append(p)
    # print k.to_string(prettyprint=True)
    with open(filename, 'wb') as f:
        f.write(k.to_string())