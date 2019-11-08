import math
import numpy as np

# x:0=5f1+6f2+7f3+22
# y:0=4f1+7f2+1f3+9
# m=0=20f1+21f2+80f3+50
# f(key,[(key,)])
f1v=np.array([5,4,20])
f2v=np.array([5,8,20])
f3v=np.array([7,1,80])
f4v=np.array([4,8,16])
fcv=np.array([22,9,50])
eqs1 = {'f1': [0, f1v], 'f2': [0, f2v], 'f3': [0, f3v],'f4': [0, f3v], 'c': [1, fcv]}


def iter_to_range(bias_range, eqs):
    def eval_d(eqs):
        x = 0
        y = 0
        z = 0
        v = np.array([0,0,0])
        for eq in eqs:
            # value eqs[eq][0]
            # vector eqs[eq][1]
            # v = v +eqs[eq][0] * eqs[eq][1]
            # print(v)
            # print(np.linalg.norm(v))
            # print(math.sqrt(27*27+13*13+70*70))
            x = x + eqs[eq][0] * eqs[eq][1][0]
            y = y + eqs[eq][0] * eqs[eq][1][1]
            z = z + eqs[eq][0] * eqs[eq][1][2]
        d = math.sqrt(x * x + y * y + z * z)
        return d

    def eval_minimize_d(variable, eqs, value_step):

        value_step = value_step

        d_before = eval_d(eqs)
        eqs[variable][0] = eqs[variable][0] + value_step
        d_after = eval_d(eqs)

        # to right way
        if d_after > d_before:
            value_step = -value_step

        d_before = eval_d(eqs)
        eqs[variable][0] = eqs[variable][0] + value_step
        d_after = eval_d(eqs)

        # over the lowest
        while d_after < d_before:
            d_before = eval_d(eqs)
            eqs[variable][0] = eqs[variable][0] + value_step
            d_after = eval_d(eqs)

        # roll back
        d_before = eval_d(eqs)
        eqs[variable][0] = eqs[variable][0] - value_step
        d_after = eval_d(eqs)
        return d_after

    bias = eval_d(eqs)
    bias_before = bias
    bias_after = bias
    value_step = bias
    while bias > bias_range:
        if bias_before - bias_after < value_step:
            value_step = value_step * 0.99


        bias_before = bias
        for eq in eqs1:
            if eq is not 'c':
                bias = eval_minimize_d(eq, eqs1, value_step)
        bias_after = bias
        print(bias)



print(eqs1)
iter_to_range(0.1, eqs1)
print(eqs1)

# dic={'f1': [-13.216462265697926, [5, 4, 20]], 'f2': [6.106545425660019, [6, 7, 21]], 'f3': [1.0759962888960246, [7, 1, 80]], 'c': [1, [22, 9, 50]]}
# f1=-13.216462265697926
# f2=6.106545425660019
# f3=1.0759962888960246
# c=1
# import numpy as np
# f1v=np.array([[5,4,20]])
# f2v=np.array([[6,7,21]])
# f3v=np.array([[7,1,80]])
# fcv=np.array([[22,9,50]])
# print(f1*f1v+f2*f2v+f3*f3v+c*fcv)