from __future__ import annotations
from typing import TextIO
from collections import Counter, defaultdict
import argparse
import pickle
import sys
import string
import os
from train import Model


class Candidate:
    word: str
    count: int
    pref: int

    def __init__(self: Candidate, word: str, count: int):
        self.word = word
        self.count = count
        self.pref = 0


class OptimisedModel:
    n: int
    ngrams: list[dict[tuple[str, ...], list[Candidate]]]

    def __init__(self: OptimisedModel, model: Model) -> None:
        self.n = model.n
        for i in range(self.n):
            for k, v in model.ngrams[i].items():
                self.ngrams[i][k] = []
                for word, count in v.items():
                    self.ngrams[i][k].append(Candidate(word, count))
                self.ngrams[i][k].sort(key=lambda x: x.count, reverse=True)
                for j in range(1, len(self.ngrams[i][k])):
                    self.ngrams[i][k][j].pref = self.ngrams[i][k][j - 1].pref + self.ngrams[i][k][j - 1].count


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Генератор текстов с помощью N-граммной модели')
    

if __name__ == '__main__':
    main()