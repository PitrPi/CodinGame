import sys

# 0 = empty cell
# 2 = X cell
# 1 = [] cell

class NonogramGeneral:
    def __init__(self, width=0, height=0, vclues=[], hclues=[]):
        # To be overwritten
        self.pic = [[0]*width for _ in range(height)]
        self.width = width
        self.height = height

    def transposed_pic(self):
        for i in range(len(self.pic[0])):
            yield [x[i] for x in self.pic]

    def create_target(self, transpose=False):
        if transpose:
            target = enumerate(self.transposed_pic())
        else:
            target = enumerate(self.pic)
        return target

class Nonogram(NonogramGeneral):
    def __init__(self, width, height, vclues, hclues):
        self.pic = [[0]*width for _ in range(height)]
        self.width = width
        self.height = height
        self.vclues = vclues
        self.hclues = hclues
        self.vclues_to_be_solved = self.vclues.copy()
        self.hclues_to_be_solved = self.hclues.copy()

    @staticmethod
    def yield_one():
        yield 1

    @staticmethod
    def clue_size(hints: list):
        return max(sum(hints)+len(hints)-1, 0) # Solves empty clues

    @staticmethod
    def line_size(line: list):
        try:
            size = len(line)
            last = size - line[::-1].index(0)
            while last+1 < size and line[last+1] != 1:
                last += 1
            first = line.index(0)
            while first-1 >= 0 and line[first-1] == 1:
                first -= 1
        except ValueError:
            return 0, 0
        return first, last


    def solve_shifting(self, transpose=False):
        target = self.create_target(transpose)
        for line_idx, line in target:
            if transpose:
                clue = self.vclues_to_be_solved[line_idx]
            else:
                clue = self.hclues_to_be_solved[line_idx]
            first, last = self.line_size(line)
            ls = last - first
            cs = self.clue_size(clue)
            df = ls - cs
            for idx, single in enumerate(clue):
                if single > df:
                    start = self.clue_size(clue[:idx]) + df + first
                    stop = start - df + single
                    if idx > 0: #Not first hint so add extra X
                        start += 1
                        stop += 1
                    for updated_idx in range(start, stop):
                        if transpose:
                            self.pic[updated_idx][line_idx] = 1
                        else:
                            self.pic[line_idx][updated_idx] = 1
        return self

    def insert_breaks(self, transpose=False):
        target = self.create_target(transpose)
        for line_idx, line in target:
            if transpose:
                clue = self.vclues[line_idx]
            else:
                clue = self.hclues[line_idx]
            for idx, single in enumerate(clue):
                try:
                    if line.index(0) == self.clue_size(clue[:(idx+1)]):
                        if transpose:
                            self.pic[line.index(0)][line_idx] = 2
                        else:
                            self.pic[line_idx][line.index(0)] = 2
                except ValueError:
                    continue
        return self

    def insert_stops(self, transpose=False):
        target = self.create_target(transpose)
        for line_idx, line in target:
            if transpose:
                clue = self.vclues[line_idx]
            else:
                clue = self.hclues[line_idx]
            clue_idx = 0
            full_count = 0
            empty_count = 0
            for sq_idx, sq in enumerate(line):
                if sq == 0:
                    empty_count += 1
                elif sq == 1:
                    full_count += 1
                else:
                    if empty_count < clue[clue_idx]:
                        for updated_idx in range(sq_idx-empty_count, sq_idx):
                            if transpose:
                                self.pic[line.index(0)][line_idx] = 2
                            else:
                                self.pic[line_idx][line.index(0)] = 2
                    empty_count = 0
                    full_count = 0
        return self

    def crossout_finished(self, transpose=False):
        target = self.create_target(transpose)
        for line_idx, line in target:
            if transpose:
                clue = vclues[line_idx]
            else:
                clue = hclues[line_idx]
            if sum(clue) == line.count(1):
                for updated_idx in range(len(line)):
                    if transpose:
                        if self.pic[updated_idx][line_idx] != 1:
                            self.pic[updated_idx][line_idx] = 2
                    else:
                        if self.pic[line_idx][updated_idx] != 1:
                            self.pic[line_idx][updated_idx] = 2
        return self

    def find_finished_clues(self, transpose=False):
        target = self.create_target(transpose)
        for line_idx, line in target:
            if transpose:
                clue = self.vclues[line_idx]
                clue_found = self.vclues_to_be_solved
            else:
                clue = self.hclues[line_idx]
                clue_found = self.hclues_to_be_solved
            clue_idx = 0
            full_count = 0
            for sq_idx, sq in enumerate(line):
                if sq != 1 and full_count > 0:
                    if full_count == clue[clue_idx]:
                        clue_idx += 1
                        clue_found[line_idx] = clue_found[line_idx][1:]
                        full_count = 0
                    else:
                        break
                elif sq == 1:
                    full_count += 1
            if full_count > 0 and full_count == clue[clue_idx]: # solves full line
                clue_found[line_idx] = clue_found[line_idx][1:]
        return self

    def printer(self):
        print(" ", file=sys.stderr, flush=True)
        max_hclues = max([len(x) for x in self.hclues])
        max_vclues = max([len(x) for x in self.vclues])
        max_hclues *= 3
        for vclue_idx in reversed(range(max_vclues)):
            vclue_out = " "*max_hclues + " "
            for vclue in self.vclues:
                if vclue_idx >= len(vclue):
                    vclue_out += " "
                else:
                    vclue_out += str(vclue[vclue_idx])
            print(vclue_out, file=sys.stderr, flush=True)
        print(" "*(max_hclues+1) + "_"*self.width, file=sys.stderr, flush=True)
        for line_idx, line in enumerate(self.pic):
            out = " ".join([str(x) for x in self.hclues[line_idx]]).rjust(max_hclues)
            out_line = "".join([str(x) for x in line])
            out_line = out_line.replace('0', ' ')
            out_line = out_line.replace('1', '#')
            out_line = out_line.replace('2', '.')
            print(out+"|"+out_line, file=sys.stderr, flush=True)


class NonogramInverter(NonogramGeneral):
    def __init__(self, nonogram):
        self.pic = nonogram.pic

    def count_blank(self, transpose=True):
        out = []
        target = self.create_target(transpose)
        for _, line in target:
            full_count = 0
            out_line = []
            for px in line + [1]:
                if px != 1:
                    full_count += 1
                elif full_count > 0:
                    out_line.append(full_count)
                    full_count = 0
            if len(out_line) == 0 :
                out.append([0])
            else:
                out.append(out_line)
        return out

    @staticmethod
    def printer(out):
        for line in out:
            print(" ".join([str(x) for x in line]))

    def step(self):
        out = self.count_blank(transpose=True)
        self.printer(out)
        out = self.count_blank(transpose=False)
        self.printer(out)


def main():
    width, height = [int(i) for i in input().split()]
    vclues = []
    hclues = []
    for i in range(width):
        vclues.append([int(i) for i in input().split()])
    for i in range(height):
        hclues.append([int(i) for i in input().split()])
    sum_of_hints = sum([sum(x) for x in vclues])
    sum_of_solved = 0
    sum_of_solved_new = -1
    nonogram = Nonogram(width, height, vclues, hclues)
    while sum_of_solved != sum_of_hints and sum_of_solved != sum_of_solved_new:
        sum_of_solved = sum_of_solved_new
        print(nonogram.hclues_to_be_solved, file=sys.stderr, flush=True)
        print(nonogram.vclues_to_be_solved, file=sys.stderr, flush=True)
        nonogram = nonogram.solve_shifting(transpose=True)
        nonogram = nonogram.insert_breaks(transpose=True)
        nonogram.printer()
        nonogram = nonogram.solve_shifting(transpose=False)
        nonogram = nonogram.insert_breaks(transpose=False)
        nonogram.printer()
        nonogram = nonogram.insert_stops(transpose=False)
        nonogram = nonogram.insert_stops(transpose=True)
        nonogram.printer()
        nonogram.find_finished_clues(transpose=False)
        nonogram.find_finished_clues(transpose=True)
        sum_of_solved_new = sum([x.count(1) for x in nonogram.pic])
        print(sum_of_solved, file=sys.stderr, flush=True)
        print(sum_of_solved_new, file=sys.stderr, flush=True)
    nonogram.printer()
    ni = NonogramInverter(nonogram)
    ni.step()

main()