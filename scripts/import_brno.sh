mkdir -p vdp_import	# tvorim slozku pro stazene data z vdp
cd vdp_import

BRNO="582786"		# vytvarim  promenne
DATUM="20200331"
for OBEC in "${BRNO}"; do	# $NAZEV_PROMENNE pri pouziti
    FILENAME="${DATUM}_OB_${OBEC}_UKSH.xml"
    wget https://vdp.cuzk.cz/vymenny_format/soucasna/${FILENAME}.zip	# stahuju soubor z http
    # -p posila soubor do stdoutu, ten cte ze stdinu gzip a uklada
    unzip -p ${FILENAME}.zip | gzip --stdout - > ${FILENAME}.gz
done
rm *.zip

cd ../
# https://github.com/fordfrog/ruian2pgsql
java -cp target/ruian2pgsql-1.6.1-jar-with-dependencies.jar:jdbc-driver.jar com.fordfrog.ruian2pgsql.App --convert-to-ewkt --linearize-ewkt --create-tables --db-connection-url 'jdbc:postgresql://172.18.0.2/ruian?user=ruianuser&password=123456' --input-dir vdp_import
