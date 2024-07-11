# Test_HH_INITI
## Тестовое задание фирмы ИНИТИ
## Вакансия: Инженер-программист
### Тестовое задание
Рассмотрим перекресток на рисунке. 
![image](https://github.com/Fga4643/Test_HH_INITI/assets/45387631/5fb37796-0318-45da-8b70-7cd90b71ac99)
На нем находится несколько светофоров, регулирующих
движение автомобилей (4 шт), и несколько - движение пешеходов по переходам (8 шт):
У пешеходных светофоров 2 состояния, у автомобильных - 3 В каждый светофор встроена
камера, которая фиксирует количество автомобилей/пешеходов в той очереди, для которых
светофор установлен. Это очередь на противоположной стороне пешехода/перекрестка (см
рисунок). Автомобили при проезде перекрестка едут либо прямо, либо направо. Люди и
автомобили осуществляют переход или проезд перекрестка по одному, уменьшая размер
соответствующей очереди на 1
Каждый светофор имеет уникальный id. Светофоры могут общаться при помощи событий, отсылая
события друг другу по id. Пересылаемые события - это некоторые контейнеры с данными
(например, там может лежать количество людей/автомобилей в очереди, id отправителя, текущее
состояние светофора). Светофор может взводить таймер, который через заданное время
отсылают заданное событие на заданный id. Отправка события - это помещение контейнера в
очередь событий для светофора, у каждого светофора очередь своя собственная. Светофоры
обрабатывают события параллельно, независимо от друг от друга. При этом каждый светофор
обрабатывает свои события последовательно, в том порядке, в каком они помещаются в очередь.
Светофор может получить информацию о текущем состоянии любого другого светофора
синхронно (не через событие).
Задача: придумать и описать адаптивный алгоритм работы светофоров для
оптимизации общей пропускной способности перекрестка в зависимости от ситуации
на перекрестке.
