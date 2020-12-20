from __future__ import annotations
from typing import Tuple, List, Union, Optional, Iterable, Any, Set, Iterator
import itertools

Token = str
Production = Tuple[Union["Rule", Token], ...]


class Rule:
    def __init__(self: Rule, name: str, *productions: Production) -> None:
        self.name: str = name
        self.productions: List[Production] = list(productions)

    def add(self: Rule, *productions: Production) -> None:
        self.productions.extend(productions)


class State:
    def __init__(
        self, name: str, production: Production, dot_index: int, start_column: Column
    ) -> None:
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column: Optional[Column] = None
        self.dot_index = dot_index
        self.rules: List[Rule] = [t for t in production if isinstance(t, Rule)]

    def __eq__(self: State, other: Any) -> bool:
        return (self.name, self.production, self.dot_index, self.start_column) == (
            other.name,
            other.production,
            other.dot_index,
            other.start_column,
        )

    def __ne__(self: State, other: Any) -> bool:
        return not (self == other)

    def __hash__(self: State) -> int:
        return hash((self.name, self.production))

    def completed(self: State) -> bool:
        return self.dot_index >= len(self.production)

    def next_term(self: State) -> Optional[Union[Rule, str]]:
        if self.completed():
            return None
        return self.production[self.dot_index]


class Column:
    def __init__(self: Column, index: int, token: Optional[Token]) -> None:
        self.index = index
        self.token = token
        self.states: List[State] = []
        self._unique: Set[State] = set()

    def __iter__(self: Column) -> Iterator:
        return iter(self.states)

    def __getitem__(self: Column, index: Any) -> State:
        return self.states[index]

    def add(self: Column, state: State) -> bool:
        if state not in self._unique:
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False


def predict(col: Column, rule: Rule) -> None:
    for prod in rule.productions:
        col.add(State(rule.name, prod, 0, col))


def scan(col: Column, state: State, token: Token) -> None:
    if token != col.token:
        return
    col.add(
        State(state.name, state.production, state.dot_index + 1, state.start_column)
    )


def complete(col: Column, state: State) -> None:
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        if term.name == state.name:
            col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))


def matches(rule: Rule, text: Iterable[Token]) -> bool:
    token_list: List[Optional[Token]] = list(itertools.chain([None], text))
    table = [Column(i, tok) for i, tok in enumerate(token_list)]
    table[0].add(State("γ", (rule,), 0, table[0]))

    for i, col in enumerate(table):
        for state in col:
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule):
                    predict(col, term)
                elif i + 1 < len(table):
                    scan(table[i + 1], state, term)

    return any(st.name == "γ" and st.completed() for st in table[-1])
