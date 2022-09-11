from __future__ import annotations
from typing import TextIO
from collections import Counter, defaultdict
import argparse
import pickle
import sys
import string
import os


# класс модели
class Model:
    n: int
    ngrams: list[defaultdict[tuple[str, ...], Counter[str]]]

    def __init__(self: Model, n: int) -> None:
        self.n = n
        self.ngrams = [defaultdict(Counter) for _ in range(n)]

    # добавить слово в модель
    def add_ngram(self: Model, ctx: tuple[str, ...], word: str) -> None:
        for i in range(self.n):
            self.ngrams[i][ctx[self.n - i - 1:]][word] += 1


def main() -> None:
    # парсим аргументы
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Тренировка N-граммной модели')
    parser.add_argument('--input', dest='input_file_path',
                        help='путь к файлу с текстом для обучения (по умолчанию stdin)')
    parser.add_argument('--model', dest='output_file_path', required=True,
                        help='путь к файлу, в который сохраняется модель (если он уже существует, то модель будет '
                             'обновлена)')
    parser.add_argument('-n', dest='ngram_len', type=int, default=3, help='размер N-грамм (по умолчанию 3)')
    args: argparse.Namespace = parser.parse_args()
    # читаем ввод
    input_file: TextIO
    if args.input_file_path is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input_file_path, 'r')
    content = input_file.read()
    input_file.close()
    # токенизация
    tokens: list[str] = content.casefold().translate(str.maketrans('', '', string.punctuation + '–«»…')).split()
    tokens = ['<BEGIN>'] * (args.ngram_len - 1) + tokens
    model: Model
    # загружаем модель, если она уже существует, чтобы дообучить
    if os.path.isfile(args.output_file_path):
        with open(args.output_file_path, 'rb') as f:
            model = pickle.load(f, encoding='utf-8')
            assert model.n == args.ngram_len
    else:
        model = Model(args.ngram_len)
    # добавляем слова
    for i in range(args.ngram_len - 1, len(tokens)):
        model.add_ngram(tuple(tokens[i - args.ngram_len + 1:i]), tokens[i])
    # сохраняем слова
    with open(args.output_file_path, 'wb') as output_file:
        pickle.dump(model, output_file)


if __name__ == '__main__':
    main()
