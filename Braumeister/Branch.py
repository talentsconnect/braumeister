class Branch:
    def __init__(self, branch, base_branches):
        self.branch = branch
        self.base_branches = base_branches.split()
