class SudokuBoard:
    def __init__(self, board_str: str, starting_boards: int = 20000):
        # save this so we can copy it later
        self.og = board_str.strip()

        # amount of random boards to start with
        self.starting_boards = starting_boards

        self.size = 9
        self.box_size = 3

        # the actual sudoku thing
        self.brd = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # numbers already given
        self.locked = set()

        # spots we can change
        self.empty = []

        # score thing, lower is better
        self.fit = float("inf")

        self.load(self.og)

    def load(self, s: str) -> None:
        # board has to be 81 long
        if len(s) != 81:
            raise ValueError("board needs 81 chars")

        blanks = {"*", "0", "."}

        for r in range(self.size):
            for c in range(self.size):
                ch = s[9 * r + c]

                if ch in blanks:
                    self.brd[r][c] = 0
                    self.empty.append((r, c))

                elif ch.isdigit() and 1 <= int(ch) <= 9:
                    self.brd[r][c] = int(ch)
                    self.locked.add((r, c))

                else:
                    raise ValueError("bad board char")

    def clone(self):
        # copy it bc python is annoying with lists
        x = SudokuBoard(self.og, self.starting_boards)
        x.brd = [row[:] for row in self.brd]
        x.locked = set(self.locked)
        x.empty = list(self.empty)
        x.fit = self.fit
        return x

    def row(self, r: int):
        return self.brd[r]

    def col(self, c: int):
        return [self.brd[r][c] for r in range(self.size)]

    def box(self, r: int, c: int):
        # find which little 3x3 box
        rr = (r // 3) * 3
        cc = (c // 3) * 3

        stuff = []
        for i in range(rr, rr + 3):
            for j in range(cc, cc + 3):
                stuff.append(self.brd[i][j])

        return stuff

    def opts(self, r: int, c: int):
        # locked spots dont get options
        if (r, c) in self.locked:
            return {self.brd[r][c]}

        used = set(self.row(r)) | set(self.col(c)) | set(self.box(r, c))
        used.discard(0)

        return set(range(1, 10)) - used

    def bad_if(self, r: int, c: int, num: int) -> int:
        # counts how many problems this num makes
        bad = 0

        # row
        for j in range(9):
            if j != c and self.brd[r][j] == num:
                bad += 1

        # col
        for i in range(9):
            if i != r and self.brd[i][c] == num:
                bad += 1

        # box
        rr = (r // 3) * 3
        cc = (c // 3) * 3

        for i in range(rr, rr + 3):
            for j in range(cc, cc + 3):
                if (i, j) != (r, c) and self.brd[i][j] == num:
                    bad += 1

        return bad

    def cell_bad(self, r: int, c: int) -> int:
        num = self.brd[r][c]

        # blank is bad
        if num == 0:
            return 3

        return self.bad_if(r, c, num)

    def put(self, r: int, c: int, num: int) -> None:
        # dont change the real clues
        if (r, c) in self.locked:
            return

        self.brd[r][c] = num

    def score(self) -> int:
        # smaller number = better board
        total = 0

        # check rows
        for r in range(9):
            cnt = [0] * 10

            for num in self.brd[r]:
                if num == 0:
                    total += 1
                else:
                    cnt[num] += 1

            for n in range(1, 10):
                if cnt[n] > 1:
                    total += cnt[n] - 1

        # check cols
        for c in range(9):
            cnt = [0] * 10

            for r in range(9):
                num = self.brd[r][c]

                if num == 0:
                    total += 1
                else:
                    cnt[num] += 1

            for n in range(1, 10):
                if cnt[n] > 1:
                    total += cnt[n] - 1

        # check boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                cnt = [0] * 10

                for r in range(br, br + 3):
                    for c in range(bc, bc + 3):
                        num = self.brd[r][c]

                        if num == 0:
                            total += 1
                        else:
                            cnt[num] += 1

                for n in range(1, 10):
                    if cnt[n] > 1:
                        total += cnt[n] - 1

        self.fit = total
        return total

    def solved(self) -> bool:
        return self.score() == 0

    def pretty(self) -> str:
        lines = []

        for r in range(9):
            if r != 0 and r % 3 == 0:
                lines.append("-" * 25)

            row = []
            for c in range(9):
                if c != 0 and c % 3 == 0:
                    row.append("|")

                row.append(str(self.brd[r][c]))

            lines.append(" ".join(row))

        return "\n".join(lines)

    def show(self) -> None:
        print(self.pretty())

    def line(self) -> str:
        ans = []

        for r in range(9):
            for c in range(9):
                num = self.brd[r][c]
                ans.append(str(num) if num != 0 else "*")

        return "".join(ans)