import sys

from crossword import *
from collections import deque

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, domain in self.domains.items():
            for word in domain.copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)
        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False        
        if self.crossword.overlaps[x, y] is not None:
            xi, yi = self.crossword.overlaps[x, y]
            for x_value in self.domains[x].copy():
                if not any(
                    [possible_value for possible_value in self.domains[y] if x_value[xi] == possible_value[yi]]
                ):
                    self.domains[x].remove(x_value)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = self.crossword.overlaps.keys()
        q = deque(arcs)
        while len(q) > 0:
            x, y = q.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False

                for n in self.crossword.neighbors(x):
                    q.appendleft((n, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment.keys()) == len(self.crossword.variables) == len(assignment.values())

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # if the values assigned to the variables are not all different
        # the assignment is not consistent
        if len(set(assignment.values())) != len(assignment.values()):
            return False

        arc_checked = set()        
        for variable, assigned_value in assignment.items():
            # if the value assigned to a variable is not of the length
            # set in the variable the assignment is not consistent
            if len(assigned_value) != variable.length:
                return False

            var_neighbors = { 
                (var, other): overlaps 
                for ((var, other), overlaps) 
                in self.crossword.overlaps.items() 
                if var == variable and overlaps is not None
            }

            # if the values letters don't overlap correctly with all
            # its neighbors the assignment is not consistent
            for (_, neighbor), (var_i, n_i)  in var_neighbors.items():
                if (variable, neighbor) not in arc_checked and neighbor in assignment.keys():
                    if assigned_value[var_i] != assignment[neighbor][n_i]:
                        return False
                    arc_checked.add((variable, neighbor))
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def get_eliminated_choices(value):
            unassigned_neighbours = list(
                self.crossword.neighbors(var) - set(assignment.keys())
            )
            eliminated = 0
            for neighbour in unassigned_neighbours:
                if self.crossword.overlaps[var, neighbour] is not None:
                    var_i, neigh_i = self.crossword.overlaps[var, neighbour]
                    allowed_values_in_neighbour = [ allowed_neighbour_value for allowed_neighbour_value in self.domains[neighbour]
                        if value[var_i] == allowed_neighbour_value[neigh_i] ]
                    if len(allowed_values_in_neighbour) == 0:
                        eliminated += 1

            return eliminated

        sorted_values = [
            val for val in self.domains[var]
            if val not in assignment.values()
        ]
        sorted_values.sort(key = get_eliminated_choices)
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        sorted_variables = [
            unassigned for unassigned in self.crossword.variables
            if unassigned not in assignment
        ]
        sorted_variables.sort(
            key = lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x)))
        )
        return sorted_variables[0] if len(sorted_variables) > 0 else None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            print(assignment)
            return assignment

        next_unassigned = self.select_unassigned_variable(assignment)
        for domain_value in self.order_domain_values(next_unassigned, assignment):
            assignment[next_unassigned] = domain_value
            if self.consistent(assignment):
                backtrack_result = self.backtrack(assignment)
                if backtrack_result is not None:
                    return assignment
                assignment.pop(next_unassigned)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
