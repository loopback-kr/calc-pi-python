from common import *

def calc_pi(i):
    q,r,t,k,m,x=1,0,1,1,3,3
    for _ in range(i):
        if 4*q+r-t<m*t:
            yield m
            q,r,t,k,m,x=10*q,10*(r-m*t),t,k,(10*(3*q+r))//t-10*m,x
        else:
            q,r,t,k,m,x=q*k,(2*q+r)*x,t*x,k+1,(q*(7*k+2)+r*x)//(t*x),x+2

def get_pi(point):
    pi_stack = []
    for i in calc_pi(point):
        pi_stack.append(str(i))
    return "".join(pi_stack[:1] + ['.'] + pi_stack[1:])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--places', type=int, default=11)
    parser.add_argument('--num_processes', type=int, default=1)
    args = parser.parse_args()

    ret = run_multiproc(
        get_pi,
        [args.places] * args.num_processes,
    )
    for i, r in enumerate(ret):
        print(f'CPU{i}: {r}')