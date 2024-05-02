from numpy import square, where


def f_free_style_full(x, a0, b0, db_v, x0, x_p, dxt):
    """
    the function of 2 phase transitions:
    solid+liquid: linear 1
    vapour: linear 2
    plasma: parabola
    :param x:
    coordinate
    :param a0:
    tilt of before image
    :param b0:
    shift of before image
    :param db_v:
    difference between b_v (shift of vapour state) and b0
    :param x0:
    the center of plasmas parabola
    :param x_p:
    coordinate of the plasma phase transition
    :param dxt:
    difference between x_p and x_v ( coordinate of the vapour phase transition)
    :return:
    the coordinate of the approximated front
    """
    x_v = x_p + dxt
    a_s = a0
    b_s = b0
    b_v = b0 + db_v
    a_v = (a_s * x_v + b_s - b_v) / x_v
    c = a_v * 0.5 / (x_p - x0)
    d = a_v * x_p + b_v - c * square(x_p - x0)
    ret = where(
        x < x_p,
        c * square(x - x0) + d,
        where(
            x < x_v,
            a_v * x + b_v,
            a_s * x + b_s
        )
    )
    return ret
