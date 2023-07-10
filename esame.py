class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    
    def __init__(self, nome):
        self.nome = nome

    def apri_mio_file(self):
        try:
            mio_file_aperto = open(self.nome)
        except:
            raise ExamException("Impossibile aprire il file")        
        return mio_file_aperto

    def leggi_mio_file(self, mio_file_aperto):
        try:
            dati = mio_file_aperto.read()
        except:
            raise ExamException("Impossibile leggere il file")
        return dati.split("\n")

    def get_data(self):
        lettore_mio_file = self.apri_mio_file()
        dati_mio_file = self.leggi_mio_file(lettore_mio_file)
        dati_mio_file = [linea for linea in dati_mio_file if linea and not linea.startswith("d")]
        return [linea.split(",") for linea in dati_mio_file if linea]

def compute_avg_monthly_difference(serie_temporale, primo_anno, ultimo_anno):
    if int(primo_anno) >= int(ultimo_anno):
        raise ExamException("Errore: dati non conformi")

    dati_annuali = {}

    for riga in serie_temporale:
        
        anno_mese = riga[0].split('-')
        anno = int(anno_mese[0])
        mese = int(anno_mese[1])
        numero_passeggeri = int(riga[1])
 
        if primo_anno <= anno <= ultimo_anno:
            if anno not in dati_annuali:
                dati_annuali[anno] = [0]*12
            dati_annuali[anno][mese-1] = numero_passeggeri

    differenza_mensile = []
    for mese in range(12):
        diffs = []
        for anno in range(int(primo_anno), int(ultimo_anno)):
            if dati_annuali[anno+1][mese] and dati_annuali[anno][mese]:
                diffs.append(dati_annuali[anno+1][mese] - dati_annuali[anno][mese])
        if diffs:
            differenza_mensile.append(sum(diffs)/len(diffs))
        else:
            differenza_mensile.append(0)
    
    return differenza_mensile
