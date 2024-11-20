from unification import unify, Var, unifiable, reify
from typing import Tuple


@unifiable
class Arr():
    def __init__(self, arg, val):
        self.arg = arg 
        self.val = val

@unifiable
class Pair():
    def __init__(self, left, right):
        self.right= right
        self.left = left   

SimpleType = Arr | Pair | Var


def repr_type(t: SimpleType) -> str:
    if isinstance(t, Arr):
        if isinstance(t.arg, Arr):
            return f"({repr_type(t.arg)}) -> {repr_type(t.val)}"
        else:
            return f"{repr_type(t.arg)} -> {repr_type(t.val)}"
    elif isinstance(t, Pair):
        return f"({repr_type(t.left)}, {repr_type(t.right)})"
    elif isinstance(t, Var):
        return f"{t}"
    else:
        raise TypeError


def vars_in_type(t: SimpleType) -> set[Var]:
    if isinstance(t, Pair):
        return vars_in_type(t.left) | vars_in_type(t.right)
    elif isinstance(t, Arr):
        return vars_in_type(t.arg) | vars_in_type(t.val)
    elif isinstance(t, Var):
        return set([t])
    else:
        raise TypeError(t)


def has_loops(sub: dict):
    def _has_loops(v, s):
        if v in s:
            return True
        ext_s = set().union(*[vars_in_type(sub[a]) for a in s if a in sub])
        if ext_s.issubset(s) and v not in ext_s:
            return False
        else:
            return _has_loops(v, s | ext_s)
       
    for v in sub:
        if _has_loops(v, vars_in_type(sub[v])):
            return True
    return False


def reify_dict(ctx, sub):
    return {k: reify(v, sub) for k, v in ctx.items()}


def app_type(t: SimpleType, u: SimpleType, ctx: dict[str, SimpleType], sub_cstr: dict[Var: SimpleType]
             ) -> Tuple[SimpleType, dict[str, SimpleType], dict[Var, SimpleType]]:
    
    t = reify(t, sub_cstr)

    # Rename the type variables which don't appear in the type of a free term variable
    free_var_types = set().union(*[vars_in_type(a) for a in ctx.values()])
    left_vars_sub = {v: Var(f"{v.token}#l") for v in vars_in_type(t) - free_var_types}
    right_vars_sub = {v: Var(f"{v.token}#r") for v in vars_in_type(u) - free_var_types}

    t = reify(t, left_vars_sub)
    u = reify(u, right_vars_sub)

    if isinstance(t, Var):
        if t in vars_in_type(u):
            raise TypeError(f"Cannot apply term of type {repr_type(u)} to a variable of type {repr_type(t)} as {repr_type(t)} appears in it")
        else:
            assert t not in sub_cstr
            sub_cstr = {t: Arr(u, Var(f"{t.token}#r")), **sub_cstr}
            if not has_loops(sub_cstr):
                    return Var(f"{t.token}#r"), reify_dict(ctx, sub_cstr), sub_cstr
            else:
                raise TypeError(f"Cannot apply term of type {repr_type(u)} to a term of type {repr_type(t)}")        
    elif isinstance(t, Pair):
        raise TypeError(f"Cannot apply term of type {repr_type(u)} to a term of type {repr_type(t)}")
    elif isinstance(t, Arr):
        sub = unify(t.arg, u)
        if sub != False and not has_loops({**sub, **sub_cstr}):
            assert set(sub.keys()).intersection(sub_cstr.keys()) == set()
            sub_cstr = {**sub, **sub_cstr}
            return reify(t.val, sub_cstr), reify_dict(ctx, sub_cstr), sub_cstr
        else:
            raise TypeError(f"Types {repr_type(t)} and {repr_type(u)} are not unifiable")
    else:
        raise TypeError


def lambda_type(var_list: list[str], t: SimpleType, ctx: dict[str, SimpleType]) -> tuple[SimpleType, dict[str, SimpleType]]:
    if var_list:
        x = var_list[-1]
        type_x = ctx[x]
        del ctx[x]
        return lambda_type(var_list[:-1], Arr(type_x, t), ctx)
    else:
        return t, ctx