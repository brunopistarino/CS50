# def print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
def f(*args, **kwargs):
    print("Positional:", args)
    print("Named:", kwargs)


f(100, 50, 25, galleons=100, sickles=50, knuts=25)
