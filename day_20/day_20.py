import numpy as np
from typing import List

class Tile:
    def __init__(self, tile_id, content):
        self.tile_id = tile_id
        _content = np.array([[c for c in line] for line in content])
        self.flipped_states = [
            _content,
            np.flip(_content, axis=0),
            np.flip(_content, axis=1),
            np.flip(_content),
            np.rot90(_content),
            np.flip(np.rot90(_content), axis=0),
            np.flip(np.rot90(_content), axis=1),
            np.flip(np.rot90(_content)),
        ]
        self._current_state = 0

    def get_current_content(self):
        return self.flipped_states[self._current_state]

    def __repr__(self):
        return "\n".join(("".join(line) for line in self.get_current_content()))

    def iterate_over_states(self):
        possible_states = len(self.flipped_states)
        for i in range(possible_states):
            self._current_state = (self._current_state + 1) % possible_states
            yield self


def iterate_over_edges(content):
    for edge in (content[0], content[-1], content[:, 0], content[:, -1]):
        yield edge


def find_starting_tile(tiles: List[Tile]) -> Tile:
    for i, tile in enumerate(tiles):
        for state in tile.iterate_over_states():
            if not any(
                np.array_equal(edge, _edge)
                for edge in (state.get_current_content()[0], state.get_current_content()[:, 0])
                for j, _tile in enumerate(tiles)
                if j != i
                for _state in _tile.iterate_over_states()
                for _edge in iterate_over_edges(_state.get_current_content())
            ):
                return tile


def get_tiles_in_correct_order(tiles: List[Tile]):
    all_placed_tiles = []
    st = find_starting_tile(tiles)
    used_tile_ids = {st.tile_id}
    current_tile = st
    current_row = [st]
    while len(used_tile_ids) < len(tiles):
        edge_to_find = (
            current_tile.get_current_content()[:, -1]
            if len(current_row) > 0
            else current_tile.get_current_content()[-1]
        )
        top_edge = lambda x: x[0]
        right_edge = lambda x: x[:, 0]
        check_corresponding_edge = right_edge if len(current_row) > 0 else top_edge
        found = next(
            (
                _state
                for _tile in tiles
                if _tile.tile_id not in used_tile_ids
                for _state in _tile.iterate_over_states()
                if np.array_equal(edge_to_find, check_corresponding_edge(_state.get_current_content()))
            ),
            None,
        )
        if found is not None:
            current_row.append(found)
            current_tile = found
            used_tile_ids.add(found.tile_id)
            continue
        current_tile = current_row[0]
        all_placed_tiles.append(current_row)
        current_row = []
    all_placed_tiles.append(current_row)
    return all_placed_tiles


def print_ordered_tiles(all_tiles: List[List[Tile]]):
    row_str = ""
    for row in all_tiles:
        for tilerow in range(len(row[0].get_current_content())):
            for tile in row:
                row_str += "".join(tile.get_current_content()[tilerow]) + " "
            row_str += "\n"
        row_str += "\n"
    print(row_str)


def get_full_image(ordered_tiles: List[List[Tile]]):
    all = []
    for row in ordered_tiles:
        for tilerow in range(1, len(row[0].get_current_content()) - 1):
            output_row = []
            for tile in row:
                output_row.extend(tile.get_current_content()[tilerow][1:-1])
            all.append(output_row)
    return np.array(all)


def find_monsters(image, monster_mask):
    monster_leny, monster_lenx = monster_mask.shape
    for image in (
        image,
        np.flip(image, axis=0),
        np.flip(image, axis=1),
        np.flip(image),
        np.rot90(image),
        np.flip(np.rot90(image), axis=0),
        np.flip(np.rot90(image), axis=1),
        np.flip(np.rot90(image)),
    ):
        n_monsters = 0
        leny, lenx = image.shape
        for i in range(lenx - monster_lenx):
            for j in range(leny - monster_leny):
                subarray = image[j : j + monster_leny, i : i + monster_lenx]
                if np.sum((subarray == "#") & monster_mask) == np.sum(monster_mask):
                    n_monsters += 1
        if n_monsters > 0:
            return n_monsters


tiles: List[Tile] = []

with open("input") as f:
    for tilestring in f.read().split("\n\n"):
        name_str = tilestring.split("\n")[0]
        content = tilestring.split("\n")[1:]
        tile_id = int(name_str.replace(":", "").split()[1])
        tiles.append(Tile(tile_id=tile_id, content=content))


ordered_tiles = get_tiles_in_correct_order(tiles)
print_ordered_tiles(ordered_tiles)

print(
    "Task 1:",
    ordered_tiles[0][0].tile_id
    * ordered_tiles[-1][0].tile_id
    * ordered_tiles[0][-1].tile_id
    * ordered_tiles[-1][-1].tile_id,
)


monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
monster_mask = np.array([[c == "#" for c in line] for line in monster.split("\n")])
image = get_full_image(ordered_tiles)

print("Task 2:", np.sum(image == "#") - find_monsters(image, monster_mask) * np.sum(monster_mask))
