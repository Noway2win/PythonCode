from Path_create import build_path
from to_bytes import to_bytes


def test_normalize_path():
    dataset = {
        "":"/",
        "/":"/",
        "/hello":"hello/",
        "hello///":"hello///",
        "/hello":"/hello/",
    }

    for path, expected in dataset.items():
        got = build_path(path)
        assert got == expected, f"path {path} normalized to {got}, while {expected} expected"


def test_mypath():
    original=[
        "",
        "/",
        "hello",
        "hello/",
        "/congrats//",
    ]
    newname=[
        "/",
        "/",
        "hello/",
        "hello/",
        "/congrats//",
    ]

    for i in range(len(original)):
        got = build_path(original[i])
        expected = newname[i]
        assert got == expected, f"path{original[i]} normalized to {got}, while expected{expected}"


def test_encode():
    original = [
        " ",
        "/",
        "hello",
        "hello/",
        "/congrats//",
    ]
    for i in range(len(original)):
        result = to_bytes(original[i])
        assert type(result) == bytes, f"{original[i]} didn't convert"