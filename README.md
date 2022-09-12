# ngram-model
Генерация текстов с помощью N-граммной модели для отбора на Tinkoff Generation ML 2022, Денисьев Илья 

```
$ python train.py -h
usage: train.py [-h] [--input INPUT_FILE_PATH] --model OUTPUT_FILE_PATH [-n NGRAM_LEN]

Тренировка N-граммной модели

options:
  -h, --help            show this help message and exit
  --input INPUT_FILE_PATH
                        путь к файлу с текстом для обучения (по умолчанию stdin)
  --model OUTPUT_FILE_PATH
                        путь к файлу, в который сохраняется модель (если он уже существует, то модель
                        будет обновлена)
  -n NGRAM_LEN          размер N-грамм (по умолчанию 3)
```

```
$ python generate.py -h
usage: generate.py [-h] --model INPUT_FILE_PATH [--prefix PREFIX] --length LENGTH

Генератор текстов с помощью N-граммной модели

options:
  -h, --help            show this help message and exit
  --model INPUT_FILE_PATH
                        путь к файлу с моделью
  --prefix PREFIX       начало текста
  --length LENGTH       длина генерируемой последовательности (в словах)
```

Можно запускать `train.py` несколько раз на одной и той же модели, чтобы её доучивать. При первом
запуске `generate.py` на модели, создаётся оптимизированная версия с расширением `.opt`. После доучивания модели 
следует удалить этот файл, чтобы она соптимизировалась заново.

В `/models` лежат модели, обученные на романе "Война и мир" с размерами N-грамм 2, 3, 4. Текст романа лежит в `/data`.
