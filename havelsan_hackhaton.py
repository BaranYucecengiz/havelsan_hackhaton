from tabulate import tabulate


class train:

	def __init__(self, tip, anlıkKonum, maksHız, genelBakımKm, genelBakımSüre, minBakımAralık, kazanç, toplamYol,
	             güzergah, kod, güzergahKontrol, time, durakTime):
		self._tip = tip
		self._anlıkKonum = anlıkKonum
		self._maksHız = maksHız
		self._genelBakımKm = genelBakımKm
		self._genelBakımSüre = genelBakımSüre
		self._minBakımAralık = minBakımAralık
		self._kazanç = kazanç
		self._toplamYol = toplamYol
		self._güzergah = güzergah
		self._kod = kod
		self._güzergahKontrol = güzergahKontrol
		self._time = time
		self._durakTime = durakTime

	# -----Setters-----
	def set_anlıkKonum(self, anlıkKonum):
		self._anlıkKonum = anlıkKonum

	def set_toplamYol(self, toplamYol):
		self._toplamYol = toplamYol

	def set_güzergah(self, güzergah):
		self._güzergah = güzergah

	def set_güzergahKontrol(self, güzergahKontrol):
		self._güzergahKontrol = güzergahKontrol

	def set_time(self, time):
		self._time = time

	def set_durakTime(self, durakTime):
		self._durakTime = durakTime

	# -----Getters-----
	def get_tip(self):
		return self._tip

	def get_anlıkKonum(self):
		return self._anlıkKonum

	def get_maksHız(self):
		return self._maksHız

	def get_genelBakımKm(self):
		return self._genelBakımKm

	def get_genelBakımSüre(self):
		return self._genelBakımSüre

	def get_minBakımAralık(self):
		return self._minBakımAralık

	def get_kazanç(self):
		return self._kazanç

	def get_toplamYol(self):
		return self._toplamYol

	def get_güzergah(self):
		return self._güzergah

	def get_kod(self):
		return self._kod

	def get_güzergahKontrol(self):
		return self._güzergahKontrol

	def get_time(self):
		return self._time

	def get_durakTime(self):
		return self._durakTime


düz_güzergah = {"ROTA_1": {"A": 0, "B": 100, "C": 75, "D": 100, "E": 75, "F": 75, "O": 25},
                "ROTA_2": {"N": 0, "K": 100, "P": 100, "R": 75, "D": 50, "S": 50, "P_": 75},
                "ROTA_3": {"G": 0, "H": 77, "I": 82, "F": 50, "J": 97, "K": 100, "L": 112}
                }

ters_güzergah = {"ROTA_1": {"O": 0, "F": 25, "E": 75, "D": 75, "C": 100, "B": 75, "A": 100},
                 "ROTA_2": {"P_": 0, "S": 75, "D": 50, "R": 50, "P": 75, "K": 100, "N": 100},
                 "ROTA_3": {"L": 0, "K": 112, "J": 100, "F": 97, "I": 50, "H": 82, "G": 77}
                 }


def CreateTrains(val, tip, başKonum, güzergah, maksHız, genelBakımKm, genelBakımSüre, minBakımAralık, kazanç, time,
                 durakTime):
	tren = []
	for i in range(val):

		if i < 10:
			kod = tip + "-0" + str(i)
			tren.append(train(tip, başKonum, maksHız, genelBakımKm, genelBakımSüre, minBakımAralık, kazanç,
			                  0, düz_güzergah[güzergah], kod, True, time, durakTime=durakTime))
		else:
			kod = tip + "-" + str(i)
			tren.append(
				train(tip, başKonum, genelBakımKm, genelBakımSüre, minBakımAralık, kazanç, 0, düz_güzergah[güzergah],
				      kod, True, time, durakTime=durakTime))
	return tren


def dkToSaat(dk):
	day = dk // 1440
	hour = (dk - (1440 * day)) // 60
	min = (dk - (1440 * day)) - hour * 60

	return day, hour, min


def start(trains, güzerIsim, time, gün):
	listTrainSaatKonum = []
	trains.set_time(trains.get_time() + time)
	while trains.get_time() < gün * 24 * 60:  ##Gün kadar ilerleyecek while total Time(saat) < girilen gün(saat)
		if trains.get_genelBakımKm() - trains.get_toplamYol() < sum(trains.get_güzergah().values()):
			trains.set_time(trains.get_time() + 60 * trains.get_genelBakımSüre())
			trains.set_toplamYol(0)
		else:

			count = 0
			maksHız = trains.get_maksHız()
			toplamYol = trains.get_toplamYol()
			for anlıkKonum, güzergahMesafe in trains.get_güzergah().items():
				trains.set_anlıkKonum(anlıkKonum)
				toplamYol += güzergahMesafe
				trains.set_toplamYol(toplamYol)
				trains.set_time(trains.get_time() + 60 * (güzergahMesafe / maksHız))

				varis = trains.get_time()

				if count == 0:
					trains.set_time(trains.get_time() + 5)
				if count == len(trains.get_güzergah()) - 1:
					trains.set_time(trains.get_time() + trains.get_durakTime())
				if count != 0 and count != len(trains.get_güzergah()) - 1:
					trains.set_time(trains.get_time() + trains.get_durakTime() + 5)

				listTrainSaatKonum.append(
					[trains.get_kod(), trains.get_güzergah(), trains.get_toplamYol(), anlıkKonum, güzergahMesafe,
					 trains.get_maksHız(), varis, trains.get_time(), trains.get_durakTime(), trains.get_güzergahKontrol()])
				count += 1

			if trains.get_güzergahKontrol():
				trains.set_güzergah(ters_güzergah[güzerIsim])
				trains.set_güzergahKontrol(False)
			else:
				trains.set_güzergah(düz_güzergah[güzerIsim])
				trains.set_güzergahKontrol(True)
			trains.set_time(trains.get_time() + 60 * trains.get_minBakımAralık())

	return listTrainSaatKonum


def tablo(trains, rota, time, gün):
	listTrainSaatKonum = []
	for i in range(len(trains)):
		#print(i + 1, trains[i].get_kod(), ".", 80 * "-")
		listTrainSaatKonum.append(start(trains[i], rota, time, gün))
		trains[i].set_time(trains[i].get_time())
		time += time
	return listTrainSaatKonum

def graph(liste):
	for i in range(len(liste)):
		print(tabulate(liste[i], headers=["KodAdı", "Güzergah", "ToplamYol", "İstasyon", "GüzergahMesafe",
		                                               "Ortalama Hız", "Varış", "Çıkış", "Bekleme Süresi",
		                                               "Güzergah Yönü"]))
def karsilastir(list1):
	for i in range(len(list1)):
		for j in range(i,len(list1)):
			if i != j:
				if list1[i][3] == list1[j][3] and list1[i][2] > list1[j][2]:
					print("List1",list1[i], "List2", list1[j])

def tablo4Bastir(liste, allList):
	temp = liste[0][0]
	tempList = []
	for i in range(len(liste)):
		if temp == liste[i][0]:
			tempList.append(liste[i])
			allList.append(liste[i])
		else:
			#print(tempList)
			karsilastir(tempList)

			temp = liste[i][0]
			tempList = []

	return allList

val = int(input("Anahat Treni adedi giriniz"))
anahatTreni =CreateTrains(val,"AT", list(düz_güzergah["ROTA_2"].keys())[0], "ROTA_2", 100, 2500, 24, 4, 50000, time=0, durakTime=15)

val = int(input("Yük Treni adedi giriniz"))
yükTreni = CreateTrains(val, "YT", list(düz_güzergah["ROTA_3"].keys())[0], "ROTA_3", 75, 3000, 36, 3, 45000, time=0,
                        durakTime=0)
val = int(input("Hızlı Tren adedi giriniz"))
hızlıTren = CreateTrains(val, "HT", list(düz_güzergah["ROTA_1"].keys())[0], "ROTA_1", 75, 3000, 36, 3, 45000, time=0,
                        durakTime=20)

gün = int(input("Gün gir"))
listTrainSaatKonumYT = tablo(yükTreni, "ROTA_3", time=5, gün=gün)
listTrainSaatKonumAT = tablo(anahatTreni, "ROTA_2", time = 5, gün=gün)
listTrainSaatKonumHT = tablo(hızlıTren, "ROTA_1", time = 5, gün=gün)

graph(listTrainSaatKonumYT)
graph(listTrainSaatKonumAT)
graph(listTrainSaatKonumHT)

def karsilastirList(listTrainSaatKonum):
	karsilastirList = []
	for i in range(len(listTrainSaatKonum)):
		for j in range(len(listTrainSaatKonum[i])):
			karsilastirList.append([listTrainSaatKonum[i][j][3], listTrainSaatKonum[i][j][6], listTrainSaatKonum[i][j][7], listTrainSaatKonum[i][j][9],
			                        listTrainSaatKonum[i][j][0],
			                        str(list(listTrainSaatKonum[i][j][1].keys())[0]) + str(list(listTrainSaatKonum[i][j][1].keys())[len(listTrainSaatKonum[i][j][1]) - 1])])
			# print(listTrainSaatKonumYT[i][j][3], dkToSaat(listTrainSaatKonumYT[i][j][6]), dkToSaat(listTrainSaatKonumYT[i][j][7]), listTrainSaatKonumYT[i][j][9],
			#       listTrainSaatKonumYT[i][j][0],
			#       str(list(listTrainSaatKonumYT[i][j][1].keys())[0]) + str(list(listTrainSaatKonumYT[i][j][1].keys())[len(listTrainSaatKonumYT[i][j][1]) - 1]))
	return karsilastirList
karsilastirListYT = karsilastirList(listTrainSaatKonumYT)
karsilastirListAT = karsilastirList(listTrainSaatKonumAT)
karsilastirListHT = karsilastirList(listTrainSaatKonumHT)

karsilastirListYT.sort()
karsilastirListAT.sort()
karsilastirListHT.sort()

allList = list()
tablo4Bastir(karsilastirListYT, allList)
tablo4Bastir(karsilastirListAT, allList)
tablo4Bastir(karsilastirListHT, allList)
print(tabulate(allList, headers=["İstasyon", "Varış(Dk)", "Kalkış(Dk)", "Güzergah Yönü(True : Düz, False : Ters)", "Tip",
	                            "Güzergah"]))