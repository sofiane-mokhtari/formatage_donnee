import csv, json
import unicodedata
import requests

def remove_accents(input_str):
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def create_json_discours() :
	i = 0;
	with open('data.json', 'w', encoding='utf8') as outfile:
		with open('03_le_politique_parle_au_citoyen\Rocard - Allocutions - Inventaire\FRAN_IR_050330_Rocard_allocutions.csv', newline='') as csvfile:
			spamreader  = csv.reader(csvfile, delimiter=';')
			try:
				for row in spamreader:
					if (i != 0) :
						lieux = remove_accents((row[5].split(","))[0])
						if (lieux != "S. l."):
							departement = lieux.split('(')
							if (len(departement) == 2) :
								lieux = departement[0][:-1]
							try :
								r = requests.get("https://geo.api.gouv.fr/communes?nom="+lieux+"&fields=centre&format=json&geometry=centre")
							except Exception as e:
								print (e)
							ret = r.json()
							if not ret :
								coo = -888
							else :
								coo = ret[0]['centre']['coordinates']
								my_row ={
									"id": row[0],
									"uni-id": row[1],
									"date": row[7],
									"lieux": lieux,
									"cooo": coo,
									"typologie": remove_accents(row[6])
									"path": row[:]
									}
								out = json.dumps(my_row, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
								outfile.write(out)
								outfile.write("\n")
					else :
						i = 1
			except Exception as e:
				print (e)

def main():
	create_json_discours()

main()