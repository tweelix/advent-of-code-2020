function lines_from(file)
    lines = {}
    for line in io.lines(file) do 
        lines[#lines + 1] = line
    end
    return lines
end
local traversals = {
    {1, 1},
    {1, 3},
    {1, 5},
    {1, 7},
    {2, 1},
}

local lines = lines_from('input')
local total_trees = 1
for _,v in pairs(traversals) do
    local x = 1
    local y = 1
    local trees = 0
    local n_lines = #lines
    while y <= n_lines do
        if string.sub(lines[y], x, x) == "#" then
            trees = trees + 1
        end
        x = ( (x + v[2] - 1) % (#lines[y])) + 1
        y = y + v[1]
    end
    print("("..v[1]..", "..v[2].."): "..trees)
    total_trees = total_trees * trees
end
print(" total: "..total_trees)