from earley_parser import matches, Rule
from typing import Dict, List, Union

Grammar = Dict[int, List[List[Union[int, str]]]]
def get_grammar_rules(input_str: str) -> Grammar:
    return {
        int(splitrule[0]): [
            [int(c) if not c.startswith('"') else c[1] for c in rules.split()] for rules in splitrule[1].split(" | ")
        ]
        for splitrule in (ruletext.split(": ") for ruletext in input_str.split("\n"))
    }

def get_rule(n: int):
    seen_rules = {}
    if n in seen_rules.keys():
        return seen_rules[n]
    current_rule = grammar_rules[n]
    if isinstance(current_rule[0][0], int):
        rule = Rule(str(n))
        for and_rules in current_rule:
            individual_rules = []
            for individual_rule in and_rules:
                if individual_rule == n:
                    individual_rules.append(rule)
                else:
                    individual_rules.append(get_rule(individual_rule))
            rule.add((*individual_rules,))
        seen_rules[n] = rule
        return rule
    else:
        return current_rule[0][0]

with open("input") as f:
    textinput = f.read().split("\n\n")

grammar_rules = get_grammar_rules(textinput[0])
words = textinput[1].split("\n")

rule = get_rule(0)
positives = sum(1 for word in words if matches(rule, word))
print("Task 1:", positives)

with open("input2") as f:
    textinput = f.read().split("\n\n")

grammar_rules = get_grammar_rules(textinput[0])
words = textinput[1].split("\n")

rule = get_rule(0)
positives = sum(1 for word in words if matches(rule, word))
print("Task 2:", positives)
