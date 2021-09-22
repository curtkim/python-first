import numpy as np

from manifpy import SE2, SE2Tangent


def test_constructor():
    state = SE2(4, 2, 1, 0)
    assert 4 == state.x()
    assert 2 == state.y()
    assert 1 == state.real()
    assert 0 == state.imag()
    assert 0 == state.angle()

    state = SE2(2, 4, 0.17)
    assert 2 == state.x()
    assert 4 == state.y()
    assert 0.17 == state.angle()

    state = SE2(4, 2, 1+0j)
    assert 4 == state.x()
    assert 2 == state.y()
    assert 0 == state.angle()

    state = SE2(np.array([2, 4]), 1+0j)
    assert 2 == state.x()
    assert 4 == state.y()
    assert 0 == state.angle()


def test_tangent_constructor():
    delta = SE2Tangent(4, 2, 0.17)
    assert 4 == delta.x()
    assert 2 == delta.y()
    assert 0.17 == delta.angle()


def test_accessors():
    state = SE2.Identity()

    assert 0 == state.x()
    assert 0 == state.y()
    assert 1 == state.real()
    assert 0 == state.imag()
    assert 0 == state.angle()

    delta = SE2Tangent.Zero()

    assert 0 == delta.x()
    assert 0 == delta.y()
    assert 0 == delta.angle()


def test_transform():
    state = SE2.Identity()
    transform = state.transform()

    assert (3, 3) == transform.shape
    assert (np.identity(3) == transform).all()


def test_rotation():
    state = SE2.Identity()
    rotation = state.rotation()

    assert (2, 2) == rotation.shape
    assert (np.identity(2) == rotation).all()


def test_translation():
    state = SE2.Identity()
    translation = state.translation()

    assert (2,) == translation.shape
    assert (np.zeros(2,) == translation).all()


def test_se2_tangent_coeffs():
    assert 3 == SE2Tangent.DoF
    data = np.random.rand(3)
    delta = SE2Tangent(data)
    assert (delta.coeffs() == data).all()


def test_plus():
    state = SE2.Random()
    delta = SE2Tangent.Random()

    assert state.plus(delta) == (state + delta)
    assert state.plus(delta) == state.rplus(delta)


def test_Compose():
    state = SE2.Random()
    other = SE2.Random()

    assert state.compose(other) == state * other
    assert state.compose(SE2.Identity()) == state
    assert SE2.Identity().compose(state) == state
    assert SE2.Identity() == state.compose(state.inverse())
    assert SE2.Identity() == state.inverse().compose(state)


def test_Exp():
    assert SE2.Identity() == SE2Tangent.Zero().exp()


def test_Log():
    assert SE2Tangent.Zero() == SE2.Identity().log()


def test_LogExp():
    state = SE2.Random()
    assert state == state.log().exp()


def test_Act():
    state = SE2.Identity()
    point = np.random.rand(SE2Tangent.Dim)
    pout = state.act(point)
    assert (point == pout).all()

