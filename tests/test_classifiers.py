from collections import OrderedDict

import pytest

from sitdown.classifiers import Category, StringMatchClassifier
from tests.factories import MutationFactory


@pytest.fixture()
def some_categories():
    sports = Category(name="sports")
    pool = Category(name="pool", parent=sports)
    gym = Category(name="gym", parent=sports)
    pool_a = Category(name="pool_a", parent=pool)
    pool_b = Category(name="pool_b", parent=pool)

    return {
        "gym": gym,
        "pool": pool,
        "pool_a": pool_a,
        "pool_b": pool_b,
        "sports": sports,
    }


def test_categories(some_categories):
    cat = some_categories
    assert cat["pool_a"].is_in(cat["pool"])
    assert cat["pool_a"].is_in(cat["pool"])
    assert cat["pool_a"].is_in(cat["sports"])

    assert not cat["pool_a"].is_in(cat["gym"])
    assert not cat["sports"].is_in(cat["gym"])
    assert str(cat["sports"]) == 'sports'


def test_string_match_classifier(some_categories):
    cat = some_categories
    mapping = OrderedDict({
        "Hanky sports": cat["gym"],
        "mega pool": cat["pool_a"],
        "ultra pool": cat["pool_b"],
        "sports store alpha": cat["sports"],
    })

    matcher = StringMatchClassifier(mapping=mapping)
    assert (
        matcher.classify(
            MutationFactory(description="thank you for shopping at sports store alpha")
        )
        == {cat["sports"]}
    )
    assert (
        matcher.classify(MutationFactory(description="mega pool counter 1#45"))
        == {cat["pool_a"]}
    )

    assert (
        matcher.classify(MutationFactory(description="something else")) == set()
    )

    assert len(matcher.categories()) == 4
