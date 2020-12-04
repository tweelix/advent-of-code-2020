import re

with open("input") as f:
    input_data = f.read().split("\n\n")

colour_regex = re.compile(r"#[0-9a-f]{6}")
passport_no_regex = re.compile(r"[0-9]{9}")

required_fields = {
    "byr": lambda x: x.isnumeric() and 1920 <= int(x) <= 2002,
    "iyr": lambda x: x.isnumeric() and 2010 <= int(x) <= 2020,
    "eyr": lambda x: x.isnumeric() and 2020 <= int(x) <= 2030,
    "hgt": lambda x: x[:-2].isnumeric()
    and ((x[-2:] == "cm" and 150 <= int(x[:-2]) <= 193) or (x[-2:] == "in" and 59 <= int(x[:-2]) <= 76)),
    "hcl": lambda x: colour_regex.fullmatch(x) is not None,
    "ecl": lambda x: x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
    "pid": lambda x: passport_no_regex.fullmatch(x) is not None,
    # "cid"
}

print(
    "part 1:",
    len(
        [
            passport
            for passport in input_data
            if all([required_field in passport for required_field in required_fields.keys()])
        ]
    ),
)

valid_records = 0
for passport in input_data:
    data_cleaned = passport.replace("\n", " ").split()
    data_dict = {f.split(":")[0]: f.split(":")[1] for f in data_cleaned}
    if set(data_dict.keys()) - {"cid"} == set(required_fields.keys()) and all(
        [required_fields[k](v) for k, v in data_dict.items() if k != "cid"]
    ):
        valid_records += 1
print("part 2: ", valid_records)
