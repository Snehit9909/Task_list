x = "global_x"
print(f"[Global] Created x = '{x}' id={id(x)}")
print("[Global] globals:", {k: v for k, v in globals().items() if k == "x"})

def outer():
    x = "outer_x"
    print(f"[Outer] Created x = '{x}' id={id(x)}")
    print("[Outer] locals:", locals())

    def inner():
        nonlocal x
        print(f"[Inner] Accessed nonlocal x = '{x}' id={id(x)}")
        x = "inner_modified_x"
        print(f"[Inner] Modified nonlocal x = '{x}' id={id(x)}")
        print("[Inner] locals:", locals())

        def innermost():
            x = "innermost_x"
            print(f"[Innermost] Shadowed x = '{x}' id={id(x)}")
            print("[Innermost] locals:", locals())

        innermost()
        print(f"[Inner] After innermost x = '{x}' id={id(x)}")

    inner()
    print(f"[Outer] After inner x = '{x}' id={id(x)}")

outer()
