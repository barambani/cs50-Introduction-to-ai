from collections import deque
import random
from shutil import move
from xmlrpc.client import MAXINT


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __lt__(self, other):
        return tuple(self.cells) < tuple(other.cells)

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash((tuple(self.cells), self.count))

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if not cell in self.cells:
            return

        self.cells.remove(cell)

        if self.count > 0:
            self.count = self.count - 1
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if not cell in self.cells:
            return

        if self.count == len(self.cells):
            self.count = self.count - 1

        self.cells.remove(cell)
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()
        self.moves_made_cronology = deque()
        self.moves_remaining = set(
            [(i, j) for i in range(self.height) for j in range(self.width)]
        )

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def neighbours_of(self, cell):
        """
        Finds all the neighbours of a cell in the field.
        """
        neighbours = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i <= self.height - 1 and 0 <= j <= self.width - 1:
                    neighbours.append((i, j))
        return set(neighbours)

    def remove_mines(self, neighbours, mines_count):
        """
        Removes the known mines from a cell's neighbours set, updating the mines count with the info
        """
        no_mines_neighbours = set()
        no_mines_count = mines_count
        for cell in neighbours:
            if cell not in self.mines:
                no_mines_neighbours.add(cell)
            else:
                no_mines_count = no_mines_count - 1
        return no_mines_neighbours, no_mines_count

    def infer_new_knowledge(self):
        """
        Finds all the neighbours of a cell in the field.
        """
        non_empty = [s for s in self.knowledge if len(s.cells) > 0]
        new_knowledge = set(non_empty.copy())
        while True:
            inferred = set()
            for s1 in new_knowledge:
                for s2 in new_knowledge:
                    if s1 == s2:
                        continue
                    if len(s1.cells) > 0 and len(s2.cells) > 0 and s1.cells <= s2.cells:
                        new_sentence = Sentence(s2.cells - s1.cells, s2.count - s1.count)
                        if new_sentence not in new_knowledge:
                            inferred.add(new_sentence)

            new_knowledge.update(inferred)
            if len(inferred) == 0:
                break

        return sorted(list(new_knowledge))

    def mark_known(self):
        """
        Scans the knowldege and marks known safes and mines
        """
        while True:
            repeat = False
            for s in self.knowledge:
                if s.count == 0 and len(s.cells) > 0:
                    for c in set(s.cells):
                        self.mark_safe(c)
                    repeat = True
                elif s.count == len(s.cells) and len(s.cells) > 0:
                    for c in set(s.cells):
                        self.mark_mine(c)
                    repeat = True

            if not repeat:
                break

        self.knowledge = [s for s in set(self.knowledge) if len(s.cells) > 0]
        return

    def print_knowledge(self):
        """
        Prints a summary of the knowledge
        """
        print()
        print(f'Safe moves remianing: {len(self.safes - self.moves_made)}')
        print(f'Possible moves left: {len(self.moves_remaining - self.moves_made - self.mines)}')
        print()
        print(f'Known mines: {len(self.mines)}')
        print('Knowledge:')
        print("\n".join(map(lambda x: x.__str__(), self.knowledge)))
        print()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.moves_remaining.remove(cell)
        self.moves_made_cronology.append(cell)
        self.mark_safe(cell)

        neighbours = self.neighbours_of(cell)
        neighbours = neighbours - self.safes
        no_mines_neighbours, new_count = self.remove_mines(neighbours, count)

        self.knowledge.append(Sentence(no_mines_neighbours, new_count))

        self.knowledge = self.infer_new_knowledge()

        self.mark_known()

        # self.print_knowledge()
        return

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None

        candidates = [cell for cell in self.safes if cell not in self.moves_made and cell not in self.mines]

        if len(candidates) == 1:
            return candidates[0]

        if len(candidates) == 0:
            return None

        # tries to get the safe move closest to the latest move
        last_made_move_i, last_made_move_j = self.moves_made_cronology.pop()

        closest = None
        closest_distance = MAXINT
        for ci, cj in candidates:
            canidate_distance = abs(ci - last_made_move_i) + abs(cj - last_made_move_j)
            if canidate_distance < closest_distance:
                closest_distance = canidate_distance
                closest = (ci, cj)

        return closest

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # classifies the candidates by score and by mentions in the Knowledge
        scored_candidates = dict()
        mentioned_candidates = dict()
        for cell in self.moves_remaining:
            if cell not in self.moves_made and cell not in self.mines:
                scored_candidates[cell] = 0
                mentioned_candidates[cell] = 0
                for s in self.knowledge:
                    if cell in s.cells:
                        scored_candidates[cell] = scored_candidates[cell] + s.count
                        mentioned_candidates[cell] = mentioned_candidates[cell] + 1

        if len(scored_candidates) == 1:
            return list(scored_candidates.keys())[0]

        if len(scored_candidates) == 0:
            return None

        # picks the candidates with fewer mines around them in the knowledge and we fewer mentions
        sorted_candidates = dict(sorted(scored_candidates.items(), key = lambda c: c[1]))
        mentioned_candidates = dict(sorted(mentioned_candidates.items(), key = lambda c: c[1]))

        best_sorted_candidates = []
        for cell, value in list(sorted_candidates.items()):
            if value == sorted_candidates[list(sorted_candidates.keys())[0]]:
                best_sorted_candidates.append(cell)

        best_mentioned_candidates = []
        for cell, value in list(mentioned_candidates.items()):
            if value == mentioned_candidates[list(mentioned_candidates.keys())[0]]:
                best_mentioned_candidates.append(cell)

        best_candidates = list(set(best_sorted_candidates).intersection(set(best_mentioned_candidates)))

        if len(best_candidates) == 1:
            return best_candidates[0]

        if len(best_candidates) == 0:
            if len(best_sorted_candidates):
                return None

            best_candidates = best_sorted_candidates

        # in the remaining candidates picks those that are mentioned less in the knowledge
        return best_candidates[random.randrange(start = 0, stop = len(best_candidates) - 1)]