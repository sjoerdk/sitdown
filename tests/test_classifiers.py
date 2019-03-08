from collections import OrderedDict

import pytest

from sitdown.classifiers import Category, StringMatchClassifier
from tests.factories import MutationFactory


@pytest.fixture()
def some_categories():
    sports = Category(name="sports")
    pool = Category(name="pool", container=sports)
    gym = Category(name="gym", container=sports)
    pool_a = Category(name="pool_a", container=pool)
    pool_b = Category(name="pool_b", container=pool)

    return {
        "gym": gym,
        "pool": pool,
        "pool_a": pool_a,
        "pool_b": pool_b,
        "sports": sports,
    }


def test_categories(some_categories):
    cat = some_categories
    assert cat["pool_a"].is_contained_by(cat["pool"])
    assert cat["pool_a"].is_contained_by(cat["pool"])
    assert cat["pool_a"].is_contained_by(cat["sports"])

    assert not cat["pool_a"].is_contained_by(cat["gym"])
    assert not cat["sports"].is_contained_by(cat["gym"])
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
        == cat["sports"]
    )
    assert (
        matcher.classify(MutationFactory(description="mega pool counter 1#45"))
        == cat["pool_a"]
    )

    assert (
        matcher.classify(MutationFactory(description="something else"))
        is None
    )

    assert len(matcher.categories()) == 4
