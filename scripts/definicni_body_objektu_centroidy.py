import psycopg2


ALTER TABLE vyska_stavebnich_objektu
ADD COLUMN novy_def_bod DOUBLE PRECISION;


conn = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
conn_insert = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur = conn.cursor()
cur.execute('''
    SELECT ST_asEWKB(so.definicni_bod), ST_asEWKB(centroid.geom), so.kod
    FROM rn_stavebni_objekt so LEFT JOIN
        (SELECT kod, ST_centroid(hranice) as geom
        FROM rn_stavebni_objekt
        WHERE NOT ST_within(definicni_bod, hranice)) as centroid
        ON so.kod = centroid.kod
                     ;''')

definicni_body = cur.fetchall()

for zaznam in definicni_body:
    if zaznam[1] is None:
        geometry = zaznam[0]
    else:
        geometry = zaznam[1]
    cur.execute('UPDATE vyska_stavebnich_objektu SET novy_def_bod = ST_GeomFromEWKB(%s) WHERE id_stavebni_objekt = %s;',(geometry,zaznam[2]))
    conn.commit()
print('done')


