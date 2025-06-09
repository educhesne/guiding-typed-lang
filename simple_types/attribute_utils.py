from simple_types.type_inference import app_type, Var, Arr, Pair, lambda_type, vars_in_type
from unification import reify

__all__ =['init_ctx', 'ctx_vars', 'ctx_app', 'ctx_pair', 'ctx_lambda', 
          'ctx_is_applicable', 'add_vars', 'exclude_vars', 'fresh_pair_types']


def init_ctx(gv):
    gv.ctx = {}
    gv.sub = {}
    gv.counter = 0


def ctx_vars(gv):
    return '|'.join([v for v in gv.ctx]) if gv.ctx else ''


def add_vars(gv, var_list):
    gv.ctx.update({v: Var(v) for v in var_list})


def exclude_vars(gv, var_list):
    exclude_list = var_list + list(gv.ctx.keys())
    if len(exclude_list) > 0:
        return "(?!(" + '|'.join([w for w in exclude_list]) + "))"
    else:
        return "(.*?)"


def ctx_app(t, u, gv):
    app_t_u, gv.ctx, gv.sub =  app_type(t, u, gv.ctx, gv.sub)
    return app_t_u

def ctx_pair(t, u, gv):
    return Pair(reify(t, gv.sub), u)


def ctx_is_applicable(t, u, gv):
    try:
        ctx_app(t, u, gv)
    except TypeError:
        return False
    return True


def ctx_lambda(var_list, t, gv):
    lambda_v_t, gv.ctx = lambda_type(var_list, t, gv.ctx)
    free_var_types = set().union(*[vars_in_type(a) for a in gv.ctx.values()])
    gv.sub = {k:v for k,v in gv.sub.items() if k in free_var_types}
    return lambda_v_t


def fresh_pair_types(gv):
    i = gv.counter
    gv.counter += 2
    a = Var(f't#{i}')
    b = Var(f't#{i+1}')
    return (Arr(a, Arr(b, Pair(a, b))), Arr(Pair(a, b), a), Arr(Pair(a, b), b))