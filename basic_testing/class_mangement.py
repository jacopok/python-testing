# %%
from __future__ import annotations
from abc import ABC, abstractmethod


class BinaryBlackHole():
    def __init__(self, environment: Environment, m: float) -> None:

        self.m = m
        self._environment = environment

    @property
    def environment(self) -> Environment:
        return self._environment

    @environment.setter
    def environment(self, environment) -> None:
        print('Changing environment to {environment}')
        self._environment = environment

    def derivatives(self):
        return self.environment.derivatives(self)


class Environment(ABC):
    @abstractmethod
    def derivatives(self, bbh: BinaryBlackHole) -> None:
        pass


class VacuumEnvironment(Environment):
    def __init__(self, v):
        self.v = v

    def derivatives(self, bbh: BinaryBlackHole) -> None:
        print(f'bbh has {bbh.m}')
        print(f'env has {self.v}')


# %%
