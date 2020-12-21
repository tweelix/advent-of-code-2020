from collections import Counter
def parse_file(filename):
    possible_foods_per_allergen = {}
    all_food_names = []
    with open(filename) as f:
        for line in f.readlines():
            food_names = line.split(" (contains ")[0].split()
            allergens = line.split(" (contains ")[1].replace(")", "").replace("\n", "").split(", ")
            all_food_names.extend(food_names)
            for allergen in allergens:
                if allergen not in possible_foods_per_allergen.keys():
                    possible_foods_per_allergen[allergen] = set(food_names)
                else:
                    possible_foods_per_allergen[allergen] &= set(food_names)
    food_counter = Counter(all_food_names)

    good_allergens = set()
    while len(possible_foods_per_allergen.keys()) != len(good_allergens):
        for allergen, foods in possible_foods_per_allergen.items():
            if len(foods) == 1:
                good_allergens = good_allergens.union(foods)
            else:
                possible_foods_per_allergen[allergen] -= good_allergens

    for k, v in possible_foods_per_allergen.items():
        if len(v) == 1:
            possible_foods_per_allergen[k] = next(iter(v))
    return possible_foods_per_allergen, food_counter

possible_foods_per_allergen, food_counter = parse_file("input")
part_1 = sum(n for food, n in food_counter.items() if food not in set(possible_foods_per_allergen.values()))
print("Task 1:", part_1)
part_2 = ','.join(ingredient for allergen, ingredient in sorted(possible_foods_per_allergen.items()))
print("Task 2:", part_2)