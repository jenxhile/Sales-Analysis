# -*- coding: utf-8 -*-
"""Teht1_osa2.ipynb

## Analysoidaan aineistoa sales_data_sample.csv ja haetaan vastauksia mm. seuraaviin kysymyksiin:
1. Onko yksittäisen tilauksen arvon (SALES) ja tilausmäärän (QUANTITYORDERED) välillä yhteyttä, ja kuinka suuri vaihtelu on myynnin määrässä eri asiakassegmenteissä (DEALSIZE)?

2. Onko myynnissä (SALES) tilastollisesti merkittävä ero sesonkien välillä (MONTH_ID)?

3. Onko parhaiten myyvien tuotekategorioiden keskimääräisissä hinnoissa merkitsevää eroa?
"""

# yhdistetään Google Driveen
from google.colab import drive
drive.mount('/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# valitaan työskentelykansio
# %cd /gdrive/MyDrive/data

# tuodaan kirjastot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# tuodaan data
df = pd.read_csv('sales_data_sample.csv', encoding = 'ISO-8859-1')
df.head()

# Tarkistetaan rivien ja sarakkeiden lukumäärä
df.shape

# Tarkastellaan muuttujien sisältämiä tietoja tarkemmin
df.info()

"""Huomioita:

Puuttuvat tiedot:

ADDRESSLINE2: Vain 302 riviä 2823 rivistä sisältää tietoa (puuttuvaa tietoa paljon). Tämä on lisäosoitekenttä, joka ei ole kaikilla asiakkailla käytössä.

STATE: Vain 1337 riviä 2823 rivistä sisältää tietoa. Tämä tarkoittaa, että osavaltioiden tieto puuttuu monelta asiakkaalta, todennäköisesti koska tämä sarake koskee vain USA
asiakkaita.

POSTALCODE: Puuttuu joiltain riveiltä (2747 riviä 2823
sisältää tietoa), mikä voi aiheuttaa haasteita maantieteellisen analyysin tekemisessä.

TERRITORY: Tämä sarake on tyhjä 1074 riviltä. Tämä tarkoittaa, että osalta asiakkaita ei ole määritelty myyntialuetta.

Merkittävimmät sarakkeet:

ORDERNUMBER, QUANTITYORDERED, PRICEEACH, SALES, ORDERDATE: Nämä sarakkeet liittyvät suoraan tilausten määrään, hintoihin ja myyntiin.

PRODUCTLINE, MSRP, PRODUCTCODE: Nämä sarakkeet liittyvät tuotteiden ryhmiin, suositeltuun hintaan ja yksilölliseen tunnisteeseen.

CUSTOMERNAME, PHONE, ADDRESSLINE1, CITY, COUNTRY: Näissä sarakkeissa on asiakkaan yhteystiedot, jotka voivat olla tärkeitä asiakasanalyysin ja kohdentamisen kannalta.

DEALSIZE: Tämä sarake kertoo tilauksen koon ("Small", "Medium", "Large"), mikä on hyödyllinen segmentoinnissa.
"""

# Tarkastellaan tilastollisia tunnuslukuja
df1 = df.describe()

# tunnuslukujen suomenkieliset nimet
tunnusluvut = ['lukumäärä', 'keskiarvo', 'keskihajonta', 'pienin', 'alakvartiili', 'mediaani', 'yläkvartiili', 'suurin']

df1.index = tunnusluvut

# desimaalit
df1 = df1.round(2)

df1

"""Huomioita:

Tilausten määrä (QUANTITYORDERED): Tilausmäärät vaihtelevat merkittävästi, mutta suurin osa tilauksista on välillä 27–43 tuotetta.

Tuotteiden hinnat (PRICEEACH): Hintojen hajonta on kohtuullinen, ja keskihinta on noin 83,66. Maksimihinta (100) vastaa suositeltua vähittäismyyntihintaa (MSRP).

Myynnin arvo (SALES): Myynnin arvo vaihtelee erittäin paljon, mikä voi johtua tuotteiden vaihtelevista hinnoista ja tilausmääristä.
"""

# lasketaan tunnuslukuja tietyille muuttujille
df_tunnuslukuja = df1[['PRICEEACH','SALES','MSRP']]
df_tunnuslukuja

"""PRICEEACH (Yksikköhinta)
Keskiarvo: 83.66 – Keskimääräinen tuotteen yksikköhinta on noin 83.66.
Keskihajonta: 20.17 – Yksikköhintojen vaihtelu on melko suurta, mikä tarkoittaa, että hinnoissa on merkittävää vaihtelua tuotteiden välillä.

SALES (Myynti)
Keskiarvo: 3553.89 – Keskimääräinen myynti tilausta kohti on noin 3554.
Keskihajonta: 1841.87 – Myynnissä on huomattavaa vaihtelua, mikä tarkoittaa, että jotkut tilaukset ovat huomattavasti suurempia kuin toiset.
Myynnin vaihtelu on huomattavaa. Tämä voi johtua siitä, että osa asiakkaista tekee suuria tilauksia, kun taas toiset tilaavat pienempiä määriä tuotteita. Keskimäärin tilaukset ovat kuitenkin kohtuullisen suuria, mikä on hyvä merkki liiketoiminnan kannalta.

Suositeltu vähittäismyyntihinta (MSRP): 100.72 €
Todellinen myyntihinta (PRICEEACH): 83.66 €
→ Tulkinta: Keskimäärin tuotteita myydään noin 17% halvemmalla kuin suositeltu vähittäismyyntihinta. Tämä viittaa siihen, että alennuksia annetaan yleisesti tai että todellinen markkinahinta on suositeltua hintaa alempi.
Suositeltujen hintojen vaihtelu on suurempaa kuin todellisten myyntihintojen, mikä viittaa siihen, että markkinat tasoittavat hintoja alennuksilla.
Erityisesti korkeammissa hintaluokissa tuotteet myydään merkittävästi alle suositellun hinnan, mikä voi johtua kilpailusta, alennuksista tai markkinatilanteesta.
"""

# Tutkitaan kaikkia korrelaatioita

# Jätetään pois kaikki kategoriset sarakkeet
df_numerical = df.select_dtypes(include=['float64', 'int64'])

# Lasketaan korrelaatio numeerisille muuttujille
correlation_matrix = df_numerical.corr()
correlation_matrix

"""Myynnin kokonaisarvon (SALES) ja tilausmäärän (QUANTITYORDERED) välillä on melko vahva positiivinen korrelaatio. Tämä tarkoittaa, että mitä enemmän tuotteita tilataan, sitä suurempi on myynnin arvo, mikä on loogista ja odotettavissa.

Myynnin kokonaisarvon (SALES) ja yksikköhinnan (PRICEEACH) välillä on vahva positiivinen korrelaatio. Tämä viittaa siihen, että korkeampi yksikköhinta liittyy suurempaan myynnin arvoon, mikä on myös loogista.

Yksikköhinnan (PRICEEACH) ja suositellun vähittäismyyntihinnan (MSRP) välillä on vahva positiivinen korrelaatio. Tämä tarkoittaa, että tuotteiden hinnat noudattavat pitkälti suositeltuja vähittäismyyntihintoja, mikä viittaa siihen, että hinnoittelu on johdonmukaista.

Myynnin kokonaisarvon (SALES) ja suositellun vähittäismyyntihinnan (MSRP) välillä on myös vahva positiivinen korrelaatio. Tämä viittaa siihen, että korkeammalla suositellulla hinnalla olevat tuotteet tuottavat enemmän myyntiä.

Näiden tietojen perusteella kannattaa keskittyä analyysissa ensisijaisesti muuttujien SALES, QUANTITYORDERED, PRICEEACH ja MSRP välisiin yhteyksiin. Myös sesonkivaihteluiden tarkastelu (MONTH_ID, QTR_ID) myynnin yhteydessä voi olla suositeltavaa.
"""

# Tehdään uusi df ja otetaan mukaan vain tarvittavat sarakkeet
selected_columns = ['SALES', 'QUANTITYORDERED', 'PRICEEACH', 'MSRP', 'QTR_ID']

# Lasketaan korrelaatiomatriisi vain näille sarakkeille
correlation_matrix1 = df[selected_columns].corr().style.format('{:.2f}')
correlation_matrix1

# valikoidaan tärkeimmiksi havaitut muuttujat ja niiden hajontakaaviot
sns.pairplot(data=df[selected_columns])

"""## 1. Onko yksittäisen tilauksen arvon (SALES) ja tilausmäärän (QUANTITYORDERED) välillä yhteyttä, ja kuinka suuri vaihtelu on myynnin määrässä eri asiakassegmenteissä (DEALSIZE)?"""

# valikoidaan SALES ja QUANTITYORDERED matriisit ja lisätään hue argumentti
sns.pairplot(data=df, x_vars=['QUANTITYORDERED'], y_vars=['SALES'],hue='DEALSIZE')

# Lasketaan tilauksen arvon ja tilausmäärän välinen korrelaatiokerroin
df['SALES'].corr(df['QUANTITYORDERED'])

"""Korrelaatiokerroin näiden kahden muuttujan välillä on 0.5514. Tämä viittaa siihen, että tilausmäärän ja tilauksen arvon välillä on kohtalaisen vahva positiivinen yhteys. Käytännössä tämä tarkoittaa, että suurempi tilausmäärä johtaa yleensä suurempaan tilauksen arvoon, mutta yhteys ei ole täysin lineaarinen. Toisin sanoen tilausmäärän kasvu ei aina johda suhteessa vastaavaan kasvavaan tilausarvoon.

Asiakassegmenttien värityksen perusteella voimme päätellä, että noin 0 - 2500 eurolla ostavat segmentoidaan ryhmään Small, 2500 - 7500 eurolla ostavat ryhmään Medium ja tätä enemmän ostavat ryhmään Large.

## 2. Onko myynnissä (SALES) tilastollisesti merkittävä ero sesonkien välillä (MONTH_ID)?
"""

# Tarkistetaan SALES-sarakkeen minimi ja maksimiarvot
print("SALES min:", df['SALES'].min())
print("SALES max:", df['SALES'].max())

# Luodaan uusi luokiteltu muuttuja
rajat = [0, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 16000]

# lisätään df-taulukkoon uusi muuttuja 'ikäjakauma'
df['MYYNTIJAKAUMA'] = pd.cut(df['SALES'], bins=rajat, right=False)

df.head()

df.groupby('QTR_ID')['SALES'].describe().style.format('{:.2f}')

sns.boxplot(data= df, x='QTR_ID', y='SALES', showmeans=True)

"""Jokaisella neljänneksellä on useita poikkeavia arvoja, mikä viittaa siihen, että vaikka suurin osa tilauksista on melko samanlaisia, on myös erittäin suuria tilauksia, jotka vaikuttavat keskiarvoon.

 Tilausten keskiarvot ovat lähellä toisiaan kaikilla neljänneksillä, mikä tarkoittaa, että myynnin keskimääräinen arvo ei vaihtele merkittävästi eri vuosineljännesten välillä.

Toinen vuosineljännes: Korkein keskiarvo ja suurin vaihtelu. Tämä voi viitata siihen, että toisella neljänneksellä on ollut erityisiä tilauksia tai kampanjoita, jotka ovat nostaneet tilausarvoa ja lisänneet vaihtelua.

Selvitetään merkitsevyys F-testillä:
"""

# tuodaan sopiva testi
from scipy.stats import f_oneway

# tiputetaan pois puuttuvat tiedot
df_filtered = df.dropna

# muodostetaan vertailtavat ryhmät
group1 = df[df['QTR_ID'] == 1]['SALES']
group2 = df[df['QTR_ID'] == 2]['SALES']
group3 = df[df['QTR_ID'] == 3]['SALES']
group4 = df[df['QTR_ID'] == 4]['SALES']

# tehdään testi eli lasketaan p-arvo
f_statistic, p_value = f_oneway(group1, group2, group3, group4)
print(f"P-arvo: {p_value}")

"""Vastaus: Arvo 0.54 on selvästi suurempi kuin yleisesti käytetty merkitsevyystaso, kuten 0.05.

Tämä tarkoittaa, että havaittu ero vuosineljännesten välillä on hyvin todennäköisesti sattumanvarainen, eikä tilastollisesti merkitsevä.

# 3. Onko parhaiten myyvien tuotekategorioiden keskimääräisissä hinnoissa merkitsevää eroa?
"""

# Lasketaan myyntien summa (SALES) tuotelinjoittain ja järjestetään laskevaan järjestykseen
top_selling_product_lines = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)
top_selling_product_lines

top_product_lines_data = df[df['PRODUCTLINE'].isin(['Classic Cars', 'Vintage Cars'])]

# Lasketaan keskimääräinen myyntihinta kummallekin tuotelinjalle
average_price_each = top_product_lines_data.groupby('PRODUCTLINE')['PRICEEACH'].mean()
average_price_each

# Tehdään t-testi
from scipy import stats

# Erotetaan hinnat kahdelle tuotelinjalle
classic_cars_prices = top_product_lines_data[top_product_lines_data['PRODUCTLINE'] == 'Classic Cars']['PRICEEACH']
vintage_cars_prices = top_product_lines_data[top_product_lines_data['PRODUCTLINE'] == 'Vintage Cars']['PRICEEACH']

# Suoritetaan t-testi
t_test_result = stats.ttest_ind(classic_cars_prices, vintage_cars_prices, equal_var=False)

t_test_result

"""T-testin tulokset:

t-arvo: 8.20
p-arvo: 6.60e-16 (eli erittäin pieni)
Näiden tulosten perusteella voimme sanoa, että keskimääräisissä myyntihinnoissa on tilastollisesti merkitsevä ero Classic Cars ja Vintage Cars -tuotelinjojen välillä. P-arvo on huomattavasti pienempi kuin tyypillinen merkitsevyystaso (esim. 0.05), mikä tarkoittaa, että ero on erittäin merkittävä.

Käytännön merkitys:

Classic Cars -tuotelinjan myyntihinnat ovat keskimäärin korkeampia (87.34) kuin Vintage Cars -tuotelinjan hinnat (78.15). Tämä voi viitata siihen, että Classic Cars -tuotteilla on korkeampi arvo markkinoilla, tai niistä voidaan pyytää korkeampaa hintaa esimerkiksi niiden kysynnän tai laadun vuoksi.
Tämä ero voi olla hyödyllinen tieto esimerkiksi markkinoinnissa tai hinnoittelustrategioiden suunnittelussa. Voidaan esimerkiksi pyrkiä tuomaan Vintage Cars -tuotteita lähemmäs Classic Cars -hintatasoa, jos se on mahdollista laadusta tinkimättä.

## Yhteenveto

Tehdyssä analyysissä tutkittiin sales_data_sample.csv-aineistoa kolmen keskeisen kysymyksen kautta:

*Tilausarvon ja tilausmäärän välinen yhteys:*

Analyysissa havaittiin, että tilausarvon (SALES) ja tilausmäärän (QUANTITYORDERED) välillä on positiivinen yhteys. Tämä tarkoittaa, että suurempi tilausmäärä johtaa korkeampaan tilausarvoon. Lisäksi eri asiakassegmenttien (DEALSIZE) välillä esiintyi merkittävää vaihtelua, jossa suurten tilausten (Large) segmentti dominoi myynnin arvoa.

*Myynnin sesonkivaihtelut:*

Kun tutkittiin myynnin vaihtelua eri sesonkien välillä (MONTH_ID), ei havaittu tilastollisesti merkitsevää eroa vuosineljännesten keskiarvoissa. Toisen vuosineljänneksen aikana havaittiin kuitenkin enemmän vaihtelua, mikä saattaa viitata kampanjoihin tai erityisiin tapahtumiin. F-testin tulokset osoittivat, että sesonkien välinen ero ei ole tilastollisesti merkitsevä (p-arvo > 0.05).

*Tuotekategorioiden hintavertailu:*

T-testi osoitti, että parhaiten myyvien tuotekategorioiden, Classic Cars ja Vintage Cars, keskimääräisissä hinnoissa on merkittävä ero. Classic Cars -tuotteilla on korkeampi keskimääräinen myyntihinta kuin Vintage Cars -tuotteilla, ja tämä ero on tilastollisesti erittäin merkitsevä (p-arvo < 0.05).
"""

