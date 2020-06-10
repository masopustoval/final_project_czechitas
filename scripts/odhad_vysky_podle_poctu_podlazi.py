import psycopg2


ALTER TABLE vyska_stavebnich_objektu
ADD COLUMN odhad_dle_poctu_pater DOUBLE PRECISION;


conn1 = psycopg2.connect(host="172.18.0.2", dbname="ruian", user="ruianuser", password='123456')
cur1 = conn1.cursor()

cur1.execute('''SELECT kod, vyska_rozdil, pocet_podlazi
                FROM vyska_stavebnich_objektu v JOIN rn_stavebni_objekt so on v.id_stavebni_objekt = so.kod
                WHERE vyska_rozdil > 1 and
                      pocet_podlazi IS NOT NULL and
                      pocet_podlazi != 0;''')
res = cur1.fetchall()
vysky_objektu = {}
for obj in res:
    if vysky_objektu.get(obj[2]) is None:
        vysky_objektu[obj[2]] = []
    vysky_objektu[obj[2]].append(obj[1])

median = {}
prumer = {}

for k in sorted(vysky_objektu.keys()):
    prumer[k] = sum(vysky_objektu[k]) / len(vysky_objektu[k])

cur1.execute('''SELECT kod, vyska_rozdil, pocet_podlazi
                FROM vyska_stavebnich_objektu v JOIN rn_stavebni_objekt so on v.id_stavebni_objekt = so.kod
                WHERE pocet_podlazi IS NOT NULL and
                      pocet_podlazi != 0;''')
res = cur1.fetchall()

for obj in res:
    prumer_vyska = prumer.get(obj[2])
    cur1.execute("UPDATE vyska_stavebnich_objektu SET odhad_dle_poctu_pater = %s WHERE id_stavebni_objekt = %s;", (prumer_vyska, obj[0]))
    conn1.commit()
print('done')
