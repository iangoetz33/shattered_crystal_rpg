from colorama import Fore, Style


# # is a wall. Dots are walkable floor.
MAPS = {
    "forest": [
        "#########",
        "#.......#",
        "#.#.....#",
        "#...##..#",
        "#.......#",
        "#..#....#",
        "#######.#",
    ],
    "castle": [
        "##########",
        "#........#",
        "#..##....#",
        "#.....#..#",
        "##.......#",
        "#...##...#",
        "#........#",
        "##########",
    ],
}


class GameMap:
    def __init__(self, map_name, player_x, player_y):
        self.map_name = map_name
        self.player_x = player_x
        self.player_y = player_y

    def can_move(self, x, y):
        layout = MAPS[self.map_name]
        if y < 0 or y >= len(layout):
            return False
        if x < 0 or x >= len(layout[y]):
            return False
        return layout[y][x] != "#"

    def draw(self):
        print(Fore.CYAN + f"\n--- {self.map_name.upper()} ---")
        layout = MAPS[self.map_name]

        for y, line in enumerate(layout):
            row = ""
            for x, tile in enumerate(line):
                if (x, y) == (self.player_x, self.player_y):
                    row += Fore.YELLOW + "@ " + Style.RESET_ALL
                elif tile == "#":
                    row += Fore.WHITE + "█ " + Style.RESET_ALL
                elif self.map_name == "forest" and (x, y) == (7, 5):
                    row += Fore.MAGENTA + "P " + Style.RESET_ALL
                elif self.map_name == "castle" and (x, y) == (8, 6):
                    row += Fore.RED + "B " + Style.RESET_ALL
                else:
                    row += ". "
            print(row)

        print("@ = You | P = Portal | B = Boss room | █ = Wall")
