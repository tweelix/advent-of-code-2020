from itertools import product

def parse_file(file):
    for textline in open(file, "r"):
        line = textline.replace("\n", "").split(" = ")
        command = line[0]
        if command == "mask":
            yield (command, None, line[1])
        else: 
            yield (command.split("[")[0], int(command.split("[")[1][:-1]), int(line[1]))


memory = {}
current_masks = (1, 0)   

for command, param, value in parse_file("input"):
    if command == "mask":
        current_masks = int(value.replace("X", "1"), base=2), int(value.replace("X", "0"), base=2)
    if command == "mem":
        memory[param] = (value & current_masks[0]) | current_masks[1]
print("Task 1:", sum(memory.values()))

memory = {}
current_masks = []
current_base_mask = 0

for command, param, value in parse_file("input"):
    if command == "mask":
        print(value.count("X"))
        current_base_mask = int(value.replace("X", "0"), base=2)
        a = [i for i, c in enumerate(value) if c == "X"]
        replacements = [{l: i[j] for j, l in enumerate(a)} for i in product("10", repeat=len(a))]
        print(replacements)
        current_masks = []
        for replacement in replacements:
            mask_list_0 = []
            mask_list_1 = []
            for i in range(len(value)):
                if i in replacement.keys():
                    mask_list_0.append(replacement[i])
                    mask_list_1.append(replacement[i])
                else:
                    mask_list_0.append("1")
                    mask_list_1.append("0")
            new_mask_0 = "".join(mask_list_0)
            new_mask_1 = "".join(mask_list_1)
            current_masks.append((int(new_mask_0, base=2), int(new_mask_1, base=2)))
    if command == "mem":
        base_addr = param | current_base_mask
        for current_mask in current_masks:
            addr = (base_addr & current_mask[0]) | current_mask[1]
            print(bin(addr), addr, value)
            memory[addr] = value
print(memory)
print("Task 2:", sum(memory.values()))
