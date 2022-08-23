# Action-Object Recognition

Esse repositório contém duas abordagens distintas para o reconhecimento das ações de um cliente dentro de uma loja de conveniência, assim como a identificação do produto o qual este está interagindo.


A abordagem principal faz uso do [YOLO](https://github.com/pjreddie/darknet) para reconhecer a ação que o sujeito realiza e o produto com o qual ele está interagindo.

<img src='https://i.imgur.com/uk22sOR.png'>

Enquanto a abordagem secundária utiliza uma rede neural para realizar apenas o reconhecimento dos gestos do cliente baseando-se no esqueleto geométrico do KinectV2.

<img src='https://i.imgur.com/K32Cnqy.png'>


[DOWNLOAD DAS CONFIGURAÇÕES E DOS PESOS DAS REDES](https://mega.nz/#F!QkERWCyJ!nS2D_Qv9bKdwrOeWy4FQsg)

# Dataset

Para a utilização nas abordagens citadas, foi criada uma base de dados que possui 10.855 imagens de objetos divididas em seis classes:

* 1.475 Imagens de Pepsi 600ml;
* 1.925 Imagens de Latas de Bebida, em sua maioria de Coca-Cola;
* 2.600 Imagens de Long Neck de Cerveja, em sua maioria da Heineken;
* 1.475 Imagens de Pacotes de Bolachas;
* 1.580 de Suco de Caixinha;
* 1.800 de Ruffles;


A base também possui 2.700 imagens de ações separadas em duas classes:

* 1.385 Imagens da ação de pegar um produto;
* 1.385 Imagens da ação de consumir um produto;

O dataset ainda conta com 620 vídeos gravados utilizando o esqueleto geométrico do KinectV2, sendo:

* 310 Vídeos da ação de pegar um produto;
* 310 Vídeos da ação de consumir um produto;

[DOWNLOAD DO DATASET](https://mega.nz/folder/ggcH2ACB#4m5lwqc3BagGheNcU-nEaA)

<img src='https://i.imgur.com/gcIAUtP.png'>


### Bounding Box

Para cada imagem presente no dataset há um respectivo arquivo de extensão `.txt` que indica a bounding box do objeto existente naquela imagem.

Todas as bounding boxes foram criadas pelos autores utilizando o [YOLO_Mark](https://github.com/AlexeyAB/Yolo_mark), sendo assim o formato do arquivo `.txt` gerado segue o padrão da própria ferramenta, que possui o seguinte formato:
```sql
<classe_objeto> <x_centro> <y_centro> <largura> <altura>
```
Onde:

`<classe_objeto>` -  Número inteiro representando a classe do objeto (de 0 a classes-1)

`<x_centro> <y_centro> <largura> <altura>` - Valores relativos a largura e a altura da imagem que podem ser de `[0.0 à 1.0]`

<b>Exemplo: </b> `<x> = <x_absoluto> / <largura_imagem>` ou `<altura> = <altura_absoluta> / <altura_imagem>`

OBS: `<x_centro> <y_centro>` são os centros do retângulo (não se referem ao canto superior esquerdo)













## Referências

Em torno de 75% das imagens presentes na base de dados foram criadas pelos próprios autores.  A quantidade restante de imagens foi retirada, principalmente, da base de dados do [ImageNET](http://www.image-net.org/) e do [COCO Dataset](http://cocodataset.org/). 




## Autores

* **Gustavo Diniz**
* **Leonardo Iglesias Castabelli**
* **Nicholas Bergmann Lupifieris**

