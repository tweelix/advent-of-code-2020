class Bag:
    def __init__(self, name, parents=None, children=None):
        self.name = name
        self.parents = [] if parents is None else parents
        self.children = [] if children is None else children

    def get_number_of_distinct_final_parents_containing(self):
        return len(self.get_all_final_parents_containing())

    def get_all_final_parents_containing(self):
        return self.get_all_attached_nodes().difference({self.name})

    def get_all_attached_nodes(self):
        final_parents_containing = {self.name}
        for parent in self.parents:
            final_parents_containing.update(parent.get_all_attached_nodes())
        return final_parents_containing

    def count_children_and_yourself(self):
        return 1 + sum([n * child.count_children_and_yourself() for n, child in self.children])

    def get_number_of_bags_contained(self):
        return self.count_children_and_yourself() - 1
        

all_bags = {}
with open("input") as f:
    for line in f.readlines():
        parent_bag_name, contents = line.split(" bags contain ")
        if parent_bag_name not in all_bags.keys():
            all_bags[parent_bag_name] = Bag(parent_bag_name)
        if contents.startswith("no"):
            continue
        for child in contents.split(","):
            number_in_parent = int(child.split()[0])
            child_name = " ".join(child.split()[1:-1])
            if child_name in all_bags.keys():
                all_bags[child_name].parents.append(all_bags[parent_bag_name])
            else:
                all_bags[child_name] = Bag(child_name, parents=[all_bags[parent_bag_name]])
            all_bags[parent_bag_name].children.append((number_in_parent, all_bags[child_name]))


print("Task 1: ", all_bags["shiny gold"].get_number_of_distinct_final_parents_containing())
print("Task 2: ", all_bags["shiny gold"].get_number_of_bags_contained())
