# Dataset

Essa base de dados que possui 10.855 imagens de objetos divididas em seis classes:

* 1.475 Imagens de Pepsi 600ml
* 1.925 Imagens de Latas de Bebida, em sua maioria de Coca-Cola
* 2.600 Imagens de Long Neck de Cerveja, em sua maioria da Heineken
* 1.475 Imagens de Pacotes de Bolachas
* 1.580 de Suco de Caixinha
* 1.800 de Ruffles

A base também possui 2.700 imagens de ações separadas em duas classes:

* 1.385 Imagens da ação de pegar um produto
* 1.385 Imagens da ação de consumir um produto

OBS: Cada imagem acompanha um respectivo arquivo de extensão .txt que indica a bounding box do objeto naquela imagem.


A base ainda conta com 620 vídeos gravados utilizando o esqueleto geométrico do KinectV2, sendo:

* 310 Vídeos da ação de pegar um produto
* 310 Vídeos da ação de consumir um produto


[DOWNLOAD DO DATASET](https://mega.nz/#F!VgEm0Qxa!oxIAStvvzWdwyC1HWId3fA)

## Referências

Em torno de 75% das imagens presentes na base de dados foram criadas pelos próprios autores.  A quantidade restante de imagens foi retirada, principalmente, da base de dados do [ImageNET](http://www.image-net.org/) e do [COCO Dataset](http://cocodataset.org/). 


### Bounding Box

Todas as bounding boxes foram criadas pelos autores utilizando o [YOLO_Mark](https://github.com/AlexeyAB/Yolo_mark), sendo assim o formato do arquivo .txt gerado segue o padrão da própria ferramenta, que possui o seguinte formato:

<classe_objeto> <x_centro> <y_centro> <largura> <altura>
  
Onde:

<classe_objeto> - número inteiro representando a classe do objeto (de 0 a classes-1)
<x_centro> <y_centro> <largura> <altura> - valores relativos a largura e altura da imagem
Exemplo: <x> = <x_absoluto> / <largura_imagem> or <altura> = <altura_absoluta> / <altura_imagem>
Atenção: <x_centro> <y_centro> - são os centros do retângulo


## Autores

* **Gustavo Diniz**
* **Leonardo Iglesias Castabelli**
* **Nicholas Bergmann Lupifieris**

