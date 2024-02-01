class CommonGeneration:
    """
    This class contains the common code for the generation, including multistart, save, main, ...
    """

    @classmethod
    def main_function(cls, data: dict) -> str:
        return f"""
def main():
    \"""
    If this file is run, then it will perform the optimization
    \"""

    # --- Prepare the ocp --- #
    ocp = prepare_ocp()

    # --- Solve the ocp --- #
    sol = ocp.solve(solver=Solver.IPOPT())
    sol.animate()
"""

    @classmethod
    def name_eq_main(cls) -> str:
        return """
if __name__ == "__main__":
    main()
"""

    @classmethod
    def generate_common(cls, data: dict) -> str:
        ret = cls.main_function(data)
        ret += cls.name_eq_main()
        return ret
