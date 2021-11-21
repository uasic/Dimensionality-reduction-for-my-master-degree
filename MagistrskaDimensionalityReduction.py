# python.exe .\MagistrskaDimensionalityReduction.py .\Analiza.csv
# Naložitev in prikaz datoteke s podatki (Analiza.csv)
import sys
import pandas as pd

datoteka = "Analiza.csv"

if (len(sys.argv) > 1):
    datoteka = sys.argv[1]
    
if (len(datoteka) == 0):
    print("Podaj datoteko kot prvi argument programa!")
    exit(1)

Tabela = pd.read_csv(datoteka)
print("Originalni podatki: \n")
print (Tabela)

# Iz tabele izločimo stolpec z zaporedno številko testiranca in novonastalo datoteko prikažemo. 
# Vsaka vrstica predstavlja posameznega preiskovanca s podatki za posamezne polimorfizme in podatki o
# pripadajoči skupini

Tabela.drop(['id'], axis = 1, inplace=True)
print("Brez id stolpca: \n")
print(Tabela)

Tabela.shape #izpiše število stolpcev in število vrstic


# Reduciranje dimenzij (Dimensionality reduction) s PCA metodo (Principal Component Analysis)


from sklearn.preprocessing import StandardScaler

# TODO: znacilke preberi iz command line parametrov
features = ['rs677830', 'rs2296616', 'rs1011784', 'rs1799971']#, 'starost', 'stan', 'izobrazba', 'okolje', 'kajenje', 'obsession', 'compulsion', 'Total BSPS', 'T AUDIT', 'T OCDS', 'T DEPRESS', 'T ANXIOUS', 'T BDHI', 'T FRANGESTOM']
target = ['skupina_preiskovanca']

# Feature: Features are individual independent variables that act as the input in your system.
# Target: The target is whatever the output of the input variables.


# Separating out the features
x = Tabela.loc[:, features].values

# Separating out the target
y = Tabela.loc[:,['skupina_preiskovanca']].values

# Standardizing the features
x = StandardScaler().fit_transform(x)

print("Po standarizaciji: \n")
print(x)  

# Izpiše se array:
# [[-0.85363641 -1.08899437 -0.86360086  1.80404634]
#  [-0.85363641  0.2918954  -0.86360086 -0.48355881]...]


from sklearn.decomposition import PCA

pca = PCA(n_components=2)   # Zmanjšaš 4 dimenzije na 2 dimenziji

principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

print("2D tabela: \n")
print(principalDf)

# Izpiše se tabela, ki ima 4 spremenljivke združene v 2 spremenljivki

# Prenos podatkov z dvema spremenljivkama v Excelovo tabelo

principalDf.to_excel(r'C:/Users/urska/Desktop/Analiza2D.xlsx', index = False)  


# Grafični prikaz podatkov

from matplotlib import pyplot as plt

fig = plt.figure(figsize = (15,15))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('Razvrstitev v skupine', fontsize = 20)
targets = ['K', 'A', 'H']
colors = ['r', 'g', 'b']

finalDf = pd.concat([principalDf, Tabela[['skupina_preiskovanca']]], axis = 1)


for target, color in zip(targets,colors):
    indicesToKeep = finalDf['skupina_preiskovanca'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()

plt.show()

# prikaže se scatter plot















