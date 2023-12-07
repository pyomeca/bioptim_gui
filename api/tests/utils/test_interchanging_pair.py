from bioptim_gui_api.utils.interchanging_pair import InterchangingPair


def test_eq_interchanging_pair():
    assert InterchangingPair("a", "b") == InterchangingPair("b", "a")
