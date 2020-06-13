import psycopg2
import collections


ALTER TABLE vyska_stavebnich_objektu
ADD COLUMN pocet_adres DOUBLE PRECISION;


conn = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur = conn.cursor()

objekt = collections.defaultdict(list)

for zpusob_vyuziti_kod in range(1,31):
    cur.execute("SELECT so.kod, cislo_domovni FROM rn_stavebni_objekt so JOIN rn_adresni_misto a ON so.kod = a.stavobj_kod WHERE so.zpusob_vyuziti_kod = {}".format(zpusob_vyuziti_kod))
    adresni_mista = cur.fetchall()
    for zaznam in adresni_mista:
        kod_objektu = zaznam[0]
        kod_objektu = str(kod_objektu)
        adresni_misto = zaznam[1]
        adresni_misto = str(adresni_misto)
        if kod_objektu in objekt:
            objekt[kod_objektu].append(adresni_misto)
        else:
            objekt[kod_objektu] = [adresni_misto]

for kod, pocet_adres in objekt.items():
    conn_insert = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
    cur1 = conn_insert.cursor()
    cur1.execute("UPDATE vyska_stavebnich_objektu SET pocet_adres = {} WHERE id_stavebni_objekt = {}".format(pocet_adres, kod))
    conn_insert.commit()
print('DONE')





