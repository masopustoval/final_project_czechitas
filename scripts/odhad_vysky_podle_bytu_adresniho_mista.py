import psycopg2


ALTER TABLE vyska_stavebnich_objektu
ADD COLUMN odhad_dle_poctu_bytu DOUBLE PRECISION;


conn1 = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur1 = conn1.cursor()

cur1.execute('''SELECT kod, vyska_rozdil, pocet_bytu, pocet_adres
                FROM vyska_stavebnich_objektu v JOIN rn_stavebni_objekt so on v.id_stavebni_objekt = so.kod
                WHERE vyska_rozdil > 1 and
                      pocet_adres IS NOT NULL and
                      pocet_adres != 0 and
                      pocet_bytu IS NOT NULL and
                      pocet_bytu != 0;''')
res = cur1.fetchall()
vysky_objektu = {}
for obj in res:
    prumer_bytu = round(obj[2]/obj[3])
    if vysky_objektu.get(prumer_bytu) is None:
        vysky_objektu[prumer_bytu] = []
    vysky_objektu[prumer_bytu].append(obj[1])

median = {}
prumer = {}

for k in sorted(vysky_objektu.keys()):
    prumer[k] = sum(vysky_objektu[k]) / len(vysky_objektu[k])

for k in sorted(vysky_objektu.keys()):
    index_prostredek = int(len(vysky_objektu[k])/2)         
    median[k] = sorted(vysky_objektu[k])[index_prostredek]

cur1.execute('''SELECT kod, vyska_rozdil, pocet_bytu, pocet_adres
                FROM vyska_stavebnich_objektu v JOIN rn_stavebni_objekt so on v.id_stavebni_objekt = so.kod
                WHERE pocet_adres IS NOT NULL and
                      pocet_adres != 0 and
                      pocet_bytu IS NOT NULL and
                      pocet_bytu != 0;''')
res = cur1.fetchall()

for obj in res:
    prumer_bytu = round(obj[2]/obj[3])
    prumer_vyska = prumer.get(prumer_bytu)
    cur1.execute("UPDATE vyska_stavebnich_objektu SET odhad_dle_poctu_bytu = %s WHERE id_stavebni_objekt = %s;", (prumer_vyska, obj[0]))
    conn1.commit()
print('done')
