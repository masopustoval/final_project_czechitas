import psycopg2

conn = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
conn_insert = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur = conn.cursor()
cur.execute('''
    SELECT
        id_stavebni_objekt,
        vyska_rozdil,
        odhad_dle_poctu_bytu,
        odhad_dle_poctu_pater,
        zpusob_vyuziti,
        ST_x(ST_transform(novy_def_bod,4326)),
        ST_y(ST_transform(novy_def_bod,4326)),
        vyska_kompletni
    FROM vyska_stavebnich_objektu;
''')
res = cur.fetchall()

f = open('import_clevermaps.csv', 'w+')
f.write('kod,vyska_zmerena,vyska_odhad_pocty_bytu,vyska_odhad_pocty_pater,zpusob_vyuziti,lng,lat,vyska_kompletni,zaznacene\n')
for i in res:
    zaznacene = 0 if i[1] < 1 else 1
    if i[2] is None:
        vyska_odhad_kombinace = i[3]
    else:
        vyska_odhad_kombinace = i[2]
    line = ','.join([str(a) for a in i]) + f',{zaznacene}\n'
    line = line.replace('None','')
    f.write(line)
f.close()