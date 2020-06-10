import psycopg2


ALTER TABLE vyska_stavebnich_objektu
ADD COLUMN zpusob_vyuziti DOUBLE PRECISION;


conn = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
conn_insert = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur = conn.cursor()
cur.execute("SELECT kod, zpusob_vyuziti_kod FROM rn_stavebni_objekt;")
seznam_datumu = cur.fetchall()
for i in seznam_datumu:
    kod = i[0]
    zpusob_vyuziti =i[1]
    if zpusob_vyuziti != None:
        cur1 = conn_insert.cursor()
        cur1.execute("UPDATE vyska_stavebnich_objektu SET zpusob_vyuziti = {} WHERE id_stavebni_objekt = {}".format(zpusob_vyuziti, kod))
        conn_insert.commit()
print('done')
