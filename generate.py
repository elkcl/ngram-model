from __future__ import annotations

import dataclasses
import sys
from typing import Callable
from collections import defaultdict
import argparse
import pickle
import string
import random
# import bisect
import os
from dataclasses import dataclass
from train import Model


@dataclass
class Candidate:
    word: str
    count: int
    pref: int = 0


@dataclass
class CandidateList:
    candidates: list[Candidate] = dataclasses.field(default_factory=list)
    count_sum: int = 0


# оптимизация выбора слова до O(log n)
# не знаю зачем, но пусть будет
class OptimisedModel:
    n: int
    ngrams: list[defaultdict[tuple[str, ...], CandidateList]]

    def __init__(self: OptimisedModel, model: Model) -> None:
        self.n = model.n
        self.ngrams = [defaultdict(CandidateList) for _ in range(self.n)]
        for i in range(self.n):
            for k, v in model.ngrams[i].items():
                self.ngrams[i][k].candidates = []
                for word, count in v.items():
                    self.ngrams[i][k].candidates.append(Candidate(word, count))
                self.ngrams[i][k].candidates.sort(key=lambda x: x.count, reverse=True)
                self.ngrams[i][k].count_sum += self.ngrams[i][k].candidates[0].count
                self.ngrams[i][k].candidates[0].pref = self.ngrams[i][k].candidates[0].count
                for j in range(1, len(self.ngrams[i][k].candidates)):
                    self.ngrams[i][k].candidates[j].pref = self.ngrams[i][k].candidates[j - 1].pref + \
                                                           self.ngrams[i][k].candidates[j].count
                    self.ngrams[i][k].count_sum += self.ngrams[i][k].candidates[j].count


def bin_search(lo: int, hi: int, func: Callable[[int], bool]):
    lo -= 1
    hi += 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if func(mid):
            lo = mid
        else:
            hi = mid
    return hi


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Генератор текстов с помощью N-граммной модели')
    parser.add_argument('--model', dest='input_file_path', required=True,
                        help='путь к файлу с моделью')
    parser.add_argument('--prefix', dest='prefix', help='начало текста')
    parser.add_argument('--length', dest='length', required=True, type=int, help='длина генерируемой '
                                                                                 'последовательности (в словах)')
    args: argparse.Namespace = parser.parse_args()
    model: OptimisedModel
    if os.path.isfile(args.input_file_path + '.opt'):
        with open(args.input_file_path + '.opt', 'rb') as f:
            model = pickle.load(f, encoding='utf-8')
    else:
        print('Оптимизация модели...', file=sys.stderr)
        with open(args.input_file_path, 'rb') as f:
            raw_model: Model = pickle.load(f, encoding='utf-8')
            model = OptimisedModel(raw_model)
        with open(args.input_file_path + '.opt', 'wb') as f:
            pickle.dump(model, f)

    text: list[str]
    curr: list[str]
    if args.prefix is None:
        text = []
        curr = ['<BEGIN>'] * (model.n - 1)
    else:
        text = args.prefix.casefold().translate(str.maketrans('', '', string.punctuation)).split()
        curr = text.copy()
        if len(curr) > (model.n - 1):
            curr = curr[-model.n + 1:]
        elif len(curr) < (model.n - 1):
            curr = ['<BEGIN>'] * (model.n - 1 - len(curr)) + curr

    for _ in range(args.length):
        for i in range(model.n - 1, -1, -1):
            ctx: tuple[str, ...] = tuple(curr[model.n - i - 1:])
            if len(model.ngrams[i][ctx].candidates) < 1:
                continue
            curr_sum = model.ngrams[i][ctx].count_sum
            rand = random.randrange(0, curr_sum)
            # print(model.ngrams[i][ctx].candidates)
            # curr_index = bisect.bisect(model.ngrams[i][ctx].candidates, rand, key=lambda x: x.pref)
            curr_index = bin_search(0, len(model.ngrams[i][ctx].candidates) - 1,
                                    lambda x: model.ngrams[i][ctx].candidates[x].pref <= rand)
            word = model.ngrams[i][ctx].candidates[curr_index].word
            text.append(word)
            curr.append(word)
            curr.pop(0)
            break

    print(' '.join(text))


if __name__ == '__main__':
    main()
