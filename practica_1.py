# -*- coding: utf-8 -*-
"""Practica_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TTxXlOJf441EoC2Ghp-ko5isO2rpMxcg

# Práctica 1: Clasificación

En esta práctica se ponen en práctica algunos de los sistemas de aprendizaje automático
vistos en la asignatura. En concreto se trabajan dos tareas de clasificación: un problema con datos
artificiales y otro con datos reales de imágenes de números manuscritos. Se trabaja tanto con una
implementación detallada de un sistema sencillo como desde el punto de vista de un toolkit.

## 1. Programación del algoritmo de un modelo Naive Bayes Gaussiano, GNB

En la primera parte de la práctica se estudia el modelo Naive Bayes Gaussiano paso a paso.
Para ello iremos elaborando la solución y visualizaremos los resultados

### 1.1. Datos Artificiales

Se importan las librerías necesarias
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
from scipy import stats
import pickle, gzip, matplotlib #Pickle sirve para manejar paquetes de datos
import matplotlib.pyplot as plt

# Descarga de datos 
!wget https://dihana.cps.unizar.es/~cadrete/mlbio/p1_data1.pkl.gz --no-check-certificate

"""Instrucción para abrir el fichero comprimido y volcarlo en las variables 
definidas (x_train, y_train, x_test, y_test)
"""

with gzip.open('p1_data1.pkl.gz', 'rb') as f:
 x_train, y_train, x_test, y_test = pickle.load(f)

"""Se imprime por pantalla tanto el tamaño como el tipo de dato"""

print(x_train.shape)
print(x_train.dtype)

"""## Funciones Apéndice"""

def find(x, value):
 return np.where(x == value)[0]

def view_data(x, y):
 k = 0
 for i in range(4):
  for j in range(4):
    plt.subplot(4, 4, k+1)
    plt.imshow( x[k].reshape(16, 16), interpolation='none', cmap='gray')
    plt.title(r'$y_{%d}$ = %d' % (k, y[k]))
    plt.gca().axis('off')
    k += 1
    
def view_model_decision(model, x_train, y_train):
 xrange1 = np.linspace(-1.2, 2.4, 50)
 xrange2 = np.linspace(-1.2, 1.2, 50)
 X1, X2 = np.meshgrid(xrange1, xrange2)
 x = np.array( [X1.flatten(), X2.flatten()] ).T
 y = model.predict(x)
 plt.figure()
 plt.clf()
 plt.imshow(y.reshape(50,50), extent=[-1.2, 2.4, -1.2, 1.2],
 origin='lower', cmap='jet')
 ind0 = find(y_train, 0)
 ind1 = find(y_train, 1)
 plt.plot(x_train[ind0,0], x_train[ind0,1],'bx', markersize=4)
 plt.plot(x_train[ind1,0], x_train[ind1,1],'rx', markersize=4)
 plt.grid(True)
 plt.gca().legend(['y_n=0', 'y_n=1'], loc='upper right',fontsize=8)

"""Separar en indices en funcion de la clase de los datos de y_train (0 o 1)

*   y_train es un vector de 1000 elementos cuyos valores son 0 o 1
*   x_train es un vector de 1000 elementos y cada elemento se compone de 2 numeros

Se buscan los indices para los que los valores en y_train son 0 y 1
"""

ind0 = find(y_train, 0)
ind1 = find(y_train, 1)

"""Se separan los valores de x_train cuya posicion coincide con y_train en 0 o 1

"""

x_train_0 = x_train[ind0]

x_train_1 = x_train[ind1]

"""Se dibujan los puntos cuyos indices y_train valen 0 y 1"""

plt.plot(x_train[ind0, 0], x_train[ind0, 1],'bx', markersize=4)

plt.plot(x_train[ind1, 0], x_train[ind1, 1],'rx', markersize=4)

"""Se pinta la distribución"""

# x = np.random.randn(4, 6)

plt.show()

"""Pintar media y desviacion típica de clase 0 y 1 para la dimension 0, que es donde se asignan los valores"""

m_0 = np.mean( x_train_0, 0, keepdims=True)
s_0 = np.std( x_train_0, 0, keepdims=True)

m_1 = np.mean(x_train_1, 0, keepdims=True)
s_1 = np.std(x_train_1, 0, keepdims=True)

"""Se define la funcion para evaluar un dato del espacio (se aplica la 
formula del guion)
"""

def evaluate_log_like( x, m, s):
  exponente = -1/2 * np.sum(((x-m)/s)**2, axis=1)
  d = x.shape[1]
  llk = -d/2 * np.log(2*np.pi) - 1/2 * np.sum(np.log(s**2)) + exponente
  return llk

like0 = evaluate_log_like( x_test, m_0, s_0 )
like1 = evaluate_log_like( x_test, m_1, s_1 )

"""El mayor de los dos valores de verosimilitud para cada ejemplo de test será la clase asignada. Si
la decisión coincide con la etiqueta se considera un acierto. En caso contrario contaríamos un
error. 

Se comprueba si el valor de y_test(0-1) es igual la condicion de que 
like1 > like0 (devuelve un boolean pero se convierte en un int(0-1))
Si es igual se almacena como acierto (acc) y sino en error (err)
"""

acc = np.mean( y_test == (like1 > like0).astype(int) )
err = np.mean( y_test != (like1 > like0).astype(int) )

# print(acc, err)

"""### Apartado 1.2: Datos Imagen

Se debe hacer el mismo procedimiento que en el apartado anterior, esta vez se
clasifican los pixeles de la imagen
Se sobreescriben las variables del apartado anterior

Se descarga, lee e imprime los tamaños de los datos y los tipos.
"""

!wget https://dihana.cps.unizar.es/~cadrete/mlbio/p1_data2.pkl.gz --no-check-certificate
with gzip.open('p1_data2.pkl.gz', 'rb') as f:
 x_train, y_train, x_test, y_test = pickle.load(f)

 viewdata_1 = view_data(x_train, y_train)

"""Volvemos a separar las posiciones de los indices de 0 (ind0) y 1 (ind1) en dos vectores distintos

"""

ind0 = find(y_train, 0)
ind1 = find(y_train, 1)

# Separar los elementos de x_train en funcion de su clase 0-1
x_train_0 = x_train[ind0]
x_train_1 = x_train[ind1]

"""Se calculan media y desviacion típica de los datos nuevos"""

m_0 = np.mean( x_train_0, 0, keepdims=True)
s_0 = np.std( x_train_0, 0, keepdims=True) + 1e-5

m_1 = np.mean( x_train_1, 0, keepdims=True)
s_1 = np.std( x_train_1, 0, keepdims=True) + 1e-5

"""Se evalúan los datos con la función 'evaluate_log_like' creada antes"""

like0 = evaluate_log_like(x_test, m_0, s_0)
like1 = evaluate_log_like(x_test, m_1, s_1)

acc = np.mean( y_test == (like1 > like0).astype(int) )
err = np.mean( y_test != (like1 > like0).astype(int) )

print(acc, err)

"""## 2. Estudio de clasificadores: librería scikit-learn

Separar el train en dos train de 800 ejemplos y dev de 200 ya que es posible que el modelo requiera del ajuste de hiperparámetros.
"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.10,
random_state=42)

"""Se importa la librería de árboles de decisión de scikit y se inicia modelo."""

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()

"""Se vuelven a cargar los datos en las mismas variables que antes, sobreescribiéndolas."""

with gzip.open('p1_data1.pkl.gz', 'rb') as f:
 x_train, y_train, x_test, y_test = pickle.load(f)

"""Se crea una función nueva para visualizar los datos con el fin de no repetir líneas de código en siguientes etapas de la práctica."""

def mostrarDatos(model, x_train, y_train):
# Se pasan datos de entrenamiento y etiquetas
  model.fit(x_train, y_train)

# Prediccion de datos de test y tasa de error
  y_pred_test = model.predict(x_test)
  err = np.sum( y_pred_test != y_test )
  print('error rate test: %f %%' % (err / len(y_test) * 100))

# Visualizar frontera de separacion de los datos
  view_model_decision(model,x_train,y_train)

"""Mostramos el mapa de valores para el modelo calculado"""

mostrarDatos(model, x_train, y_train)

"""En este caso se inicializa el árbol de decisión con el criterio de la entropía de los nodos como modelo de clasificación.
Además, se le añade una profundidad máxima al árbol de 2
"""

model = DecisionTreeClassifier(criterion='entropy', max_depth=2)

mostrarDatos(model, x_train, y_train)

"""Generamos otro árbol de decisión, con el mismo criterio de separación pero pasándole al programa el número mínimo de muestras que debe haber para poder volver a separar los nodos"""

model = DecisionTreeClassifier(criterion='entropy', min_samples_split=4)
mostrarDatos(model, x_train, y_train)

"""El siguiente modelo que se va a generar es un Naive-Bayes Gaussiano, igual que antes, mediante la librería scikit"""

from sklearn.naive_bayes import GaussianNB
model = GaussianNB()

"""Se muestra el mapa de features para el modelo seleccionado, con los datos de los que disponemos"""

mostrarDatos(model, x_train, y_train)

"""Se observa que el modelo de árbol de decisión es mejor ya que la separación de muestras es no lineal y, por tanto, ajusta mejor

Conjunto de modelos: Bagging

Se genera un modelo mediante Bagging, trabajando con 10 árboles de decisión conectados en paralelo.
Esta técnica ayuda a evitar el overfitting en el entreno
"""

from sklearn.ensemble import BaggingClassifier
model = BaggingClassifier(DecisionTreeClassifier(), n_estimators=10)

"""Se muestra la gráfica del modelo"""

mostrarDatos(model, x_train, y_train)

"""A continuación se hace un modelo similar pero mediante Boosting (conexión secuencial)"""

from sklearn.ensemble import AdaBoostClassifier
model = AdaBoostClassifier(DecisionTreeClassifier(), n_estimators=10)
mostrarDatos(model, x_train, y_train)

"""La siguiente librería que se utiliza es XGBoost, también con la librería scikit.
Lo iniciamos con todos los parámetros por defecto
"""

from xgboost import XGBClassifier
model = XGBClassifier()
mostrarDatos(model, x_train, y_train)

"""A continuación se inicializa la librería de scikit que nos permite generar Máquinas de Vectores de soporte (SVM)"""

from sklearn.svm import SVC
model = SVC()
mostrarDatos(model, x_train, y_train)

model = SVC(C=1., kernel='rbf')
mostrarDatos(model, x_train, y_train)

model = SVC(C=1.0, kernel='linear')
mostrarDatos(model, x_train, y_train)

model = SVC(C=1.0, kernel='rbf', gamma=2.0)
mostrarDatos(model, x_train, y_train)

model = SVC(C=1.0, kernel='poly', degree=2)
mostrarDatos(model, x_train, y_train)