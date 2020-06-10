import psycopg2
from multiprocessing import Pool
import requests


CREATE TABLE vyska_stavebnich_objektu (
    id_stavebni_objekt INTEGER REFERENCES rn_stavebni_objekt(kod),
    vyska_dmp1g DOUBLE PRECISION,
    vyska_dmr5g DOUBLE PRECISION,
    vyska_rozdil DOUBLE PRECISION
);


def get_height(x, y):
    point1g = {
        "surface_model": "DMP1G", 
           "geometry": { 
               "type": "Point", 
               "coordinates": [x, y]
           }, 
        "epsg_srid": 5514 
    }
    point5g = {
        "surface_model": "DMR5G", 
           "geometry": { 
               "type": "Point", 
               "coordinates": [x, y]
           }, 
        "epsg_srid": 5514 
    }
    r1 = requests.post("http://172.17.0.2/height", json=point1g)
    r5 = requests.post("http://172.17.0.2/height", json=point5g)
    return r1.json()["height"], r5.json()["height"]

def get_height_multi(points):
    with Pool(20) as p:
        return p.starmap(get_height, points)

conn = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
conn_insert = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur = conn.cursor()
cur.execute("SELECT kod, ST_astext(definicni_bod) FROM rn_stavebni_objekt WHERE definicni_bod IS NOT NULL;")
seznam_bodu = 0
while seznam_bodu != []:
    seznam_bodu = cur.fetchmany(100)
    upraveny_seznam_bodu = {}
    for body in seznam_bodu:
        kod = str(body[0])
        bod_x,bod_y = body[1].split(' ')
        bod_x = bod_x.strip('POINT(')
        bod_y = bod_y.strip(')')
        upraveny_seznam_bodu[kod] = (bod_x, bod_y)
    
    klice = []
    for klic in upraveny_seznam_bodu.keys():
        klice.append(klic)
    points = []
    for hodnota in upraveny_seznam_bodu.values():
        points.append(hodnota)
    heights = get_height_multi(points)

    x = 0
    while x < len(klice):
        k = int(klice[x])
        vyska_DMP1G = heights[x][0]
        vyska_DMR5G = heights[x][1]
        rozdil = round((vyska_DMP1G - vyska_DMR5G),2)
        x += 1
        cur1 = conn_insert.cursor()
        cur1.execute("INSERT INTO vyska_stavebnich_objektu (id_stavebni_objekt, vyska_dmp1g, vyska_dmr5g, vyska_rozdil) VALUES (%s, %s, %s, %s)",(k, vyska_DMP1G, vyska_DMR5G, rozdil))
        conn_insert.commit()
        print(rozdil)
print('done')



