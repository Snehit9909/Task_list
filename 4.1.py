# analyzer.py
import ast, sys

def analyze(file):
    with open(file) as f:
        tree = ast.parse(f.read())

    funcs = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            calls = [n.func.id for n in ast.walk(node)
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
            funcs[node.name] = calls
    return funcs

def show_graph(funcs):
    print("\nFunction Calls:")
    for f, c in funcs.items():
        print(f"{f} -> {', '.join(c) if c else '(none)'}")

def trace(func):
    def wrapper(*a, **kw):
        print(f"[TRACE] {func.__name__}")
        return func(*a, **kw)
    return wrapper

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <script.py> [--trace]")
        sys.exit()

    script = sys.argv[1]
    funcs = analyze(script)
    show_graph(funcs)

    if "--trace" in sys.argv:
        print("\nRunning with trace...\n")
        run_globals = {"trace": trace}
        exec(open(script).read(), run_globals)
