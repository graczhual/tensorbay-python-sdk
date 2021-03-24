import pytest

from ...utility import NameOrderedDict
from .. import CategoryInfo, KeypointsInfo
from ..supports import (
    AttributesMixin,
    CategoriesMixin,
    IsTrackingMixin,
    SubcatalogMixin,
    _VisibleType,
)

_CATEGORYINFO_DATA = {"name": "test", "description": "This is an exmaple of test"}

_KEYPOINTSINFO_DATA = {
    "number": 5,
    "names": ["1", "2", "3", "4", "5"],
    "skeleton": [(1, 2), (1, 5)],
    "visible": "TERNARY",
    "parentCategories": ["string"],
    "description": "Testing",
}

_ISTRACKINGMIXIN_DATA = {"isTracking": True}
_CATEGORIESMIXIN_DATA = {
    "categories": [
        {
            "name": "Test",
            "description": "This is an exmaple of test",
        },
        {
            "name": "Test2",
            "description": "This is an exmaple of test",
        },
    ],
    "categoryDelimiter": ".",
}
_CATEGORIESMIXIN_DATA_OTHER = {
    "categories": [
        {
            "name": "Test1",
            "description": "This is an exmaple of test",
        },
        {
            "name": "Test2",
            "description": "This is an exmaple of test",
        },
    ],
    "categoryDelimiter": "-",
}

_ATTRIBUTESMIXIN_DATA = {
    "attributes": [
        {"name": "Test", "enum": [1, 2, 3, 4, 5], "type": "integer", "minimum": 1, "maximum": 5}
    ]
}
_ATTRIBUTESMIXIN_DATA_OTHER = {
    "attributes": [{"name": "Test", "enum": ["1", "2", "3", "4", "5"], "type": "integer"}]
}


class TestCategoryInfo:
    def test_loads(self):
        category_info = CategoryInfo.loads(_CATEGORYINFO_DATA)
        assert category_info.name == _CATEGORYINFO_DATA["name"]
        assert category_info.description == _CATEGORYINFO_DATA["description"]

    def test_eq(self):
        category_info1 = CategoryInfo(name="cat", description="This is a cat")
        category_info2 = CategoryInfo(name="cat", description="This is a cat")
        category_info3 = CategoryInfo(name="dog", description="This is a dog")
        assert category_info1 == category_info2
        assert category_info1 != category_info3

    def test_dumps(self):
        name = _CATEGORYINFO_DATA["name"]
        description = _CATEGORYINFO_DATA["description"]
        category_info = CategoryInfo(name=name, description=description)
        assert category_info.dumps() == _CATEGORYINFO_DATA


class TestKeypointsInfo:
    @pytest.mark.parametrize("visible", ["TERNARY", "BINARY"])
    def test_init(self, visible):
        number = 4
        names = ["1", "2", "3", "4"]
        skeleton = [(1, 2), (1, 4)]
        parent_categories = "string"
        description = "Testing"

        with pytest.raises(ValueError):
            KeypointsInfo(
                number=number,
                names=names,
                skeleton=skeleton,
                visible="1",
                parent_categories=parent_categories,
                description=description,
            )

        keypoints_info = KeypointsInfo(
            number=number,
            names=names,
            skeleton=skeleton,
            visible=visible,
            parent_categories=parent_categories,
            description=description,
        )

        assert keypoints_info.number == number
        assert keypoints_info.names == names
        assert keypoints_info.skeleton == skeleton
        assert keypoints_info.visible == visible
        assert keypoints_info.parent_categories == [parent_categories]
        assert keypoints_info.description == description

    def test_eq(self):
        keypoints_info1 = KeypointsInfo(
            number=3,
            names=["a", "b", "c"],
            skeleton=[[1, 2], [2, 3]],
            visible="binary",
            parent_categories=["c1", "c2"],
        )
        keypoints_info2 = KeypointsInfo(
            number=3,
            names=["a", "b", "c"],
            skeleton=[[1, 2], [2, 3]],
            visible="binary",
            parent_categories=["c1", "c2"],
        )
        keypoints_info3 = KeypointsInfo(
            number=3,
            names=["a", "b", "c"],
            skeleton=[[2, 3], [1, 2]],
            visible="binary",
            parent_categories=["c2", "c1"],
        )

        assert keypoints_info1 == keypoints_info2
        assert keypoints_info1 != keypoints_info3

    def test_loads(self):
        keypoints_info = KeypointsInfo.loads(_KEYPOINTSINFO_DATA)

        assert keypoints_info.number == _KEYPOINTSINFO_DATA["number"]
        assert keypoints_info.names == _KEYPOINTSINFO_DATA["names"]
        assert keypoints_info.skeleton == _KEYPOINTSINFO_DATA["skeleton"]
        assert keypoints_info.visible == _KEYPOINTSINFO_DATA["visible"]
        assert keypoints_info.parent_categories == _KEYPOINTSINFO_DATA["parentCategories"]
        assert keypoints_info.description == _KEYPOINTSINFO_DATA["description"]

    def test_number(self):
        keypoints_info = KeypointsInfo(number=5)
        assert keypoints_info.number == 5

    def test_dumps(self):
        number = _KEYPOINTSINFO_DATA["number"]
        names = _KEYPOINTSINFO_DATA["names"]
        skeleton = _KEYPOINTSINFO_DATA["skeleton"]
        visible = _KEYPOINTSINFO_DATA["visible"]
        parent_categories = _KEYPOINTSINFO_DATA["parentCategories"]
        description = _KEYPOINTSINFO_DATA["description"]

        keypoints_info = KeypointsInfo(
            number=number,
            names=names,
            skeleton=skeleton,
            visible=visible,
            parent_categories=parent_categories,
            description=description,
        )

        assert keypoints_info.dumps() == _KEYPOINTSINFO_DATA


class TestSubcatalogMixin:
    def test_loads(self):
        with pytest.raises(NotImplementedError):
            SubcatalogMixin._loads(1, {"test": 1})

    def test_dumps(self):
        with pytest.raises(NotImplementedError):
            SubcatalogMixin._dumps(2)


class TestIsTrackingMixin:
    def test_init(self):
        assert IsTrackingMixin().is_tracking == False
        assert IsTrackingMixin(True).is_tracking == True

    def test_eq(self):
        support_is_tracking1 = IsTrackingMixin()
        support_is_tracking2 = IsTrackingMixin()
        support_is_tracking3 = IsTrackingMixin(True)

        assert support_is_tracking1 == support_is_tracking2
        assert support_is_tracking1 != support_is_tracking3

    def test_loads(self):
        support_is_tracking = IsTrackingMixin()
        support_is_tracking._loads(contents=_ISTRACKINGMIXIN_DATA)
        assert support_is_tracking.is_tracking == True

    def test_dumps(self):
        is_tracking = _ISTRACKINGMIXIN_DATA["isTracking"]
        support_is_tracking = IsTrackingMixin(is_tracking)
        assert support_is_tracking._dumps() == _ISTRACKINGMIXIN_DATA


class TestCategoriesMixin:
    def test_loads(self):
        support_categories = CategoriesMixin()
        support_categories._loads(contents=_CATEGORIESMIXIN_DATA)
        assert support_categories.category_delimiter == _CATEGORIESMIXIN_DATA["categoryDelimiter"]

        support_categories_data = _CATEGORIESMIXIN_DATA["categories"]
        support_categorie_1 = support_categories.categories["Test"]
        assert support_categorie_1.name == support_categories_data[0]["name"]
        assert support_categorie_1.description == support_categories_data[0]["description"]

        support_categorie_2 = support_categories.categories["Test2"]
        assert support_categorie_2.name == support_categories_data[1]["name"]
        assert support_categorie_2.description == support_categories_data[1]["description"]

    def test_eq(self):
        support_categories_1 = CategoriesMixin()
        support_categories_1._loads(_CATEGORIESMIXIN_DATA)

        support_categories_2 = CategoriesMixin()
        support_categories_2._loads(_CATEGORIESMIXIN_DATA)

        support_categories_3 = CategoriesMixin()
        support_categories_3._loads(_CATEGORIESMIXIN_DATA_OTHER)

        assert support_categories_1 == support_categories_2
        assert support_categories_1 != support_categories_3

    def test_add_category(self):
        support_categories = CategoriesMixin()
        name = "Test"
        description = "This is a test"
        support_categories.add_category(name=name, description=description)

        assert support_categories.categories["Test"].name == name
        assert support_categories.categories["Test"].description == description

    def test_dumps(self):
        support_categories = CategoriesMixin()
        name_1 = _CATEGORIESMIXIN_DATA["categories"][0]["name"]
        name_2 = _CATEGORIESMIXIN_DATA["categories"][1]["name"]
        description = _CATEGORIESMIXIN_DATA["categories"][0]["description"]
        support_categories.add_category(name=name_1, description=description)
        support_categories.add_category(name=name_2, description=description)
        support_categories.category_delimiter = "."

        assert support_categories._dumps() == _CATEGORIESMIXIN_DATA


class TestAttributesMixin:
    def test_loads(self):
        support_attributes = AttributesMixin()
        support_attributes._loads(contents=_ATTRIBUTESMIXIN_DATA)
        support_attributes_test = support_attributes.attributes["Test"]
        support_attributes_data = _ATTRIBUTESMIXIN_DATA["attributes"][0]

        assert support_attributes_test.name == support_attributes_data["name"]
        assert support_attributes_test.type == support_attributes_data["type"]
        assert support_attributes_test.enum == support_attributes_data["enum"]
        assert support_attributes_test.minimum == support_attributes_data["minimum"]
        assert support_attributes_test.maximum == support_attributes_data["maximum"]

    def test_eq(self):
        support_attributes_1 = AttributesMixin()
        support_attributes_1._loads(contents=_ATTRIBUTESMIXIN_DATA)

        support_attributes_2 = AttributesMixin()
        support_attributes_2._loads(contents=_ATTRIBUTESMIXIN_DATA)

        support_attributes_3 = AttributesMixin()
        support_attributes_3._loads(contents=_ATTRIBUTESMIXIN_DATA_OTHER)

        assert support_attributes_1 == support_attributes_2
        assert support_attributes_1 != support_attributes_3

    def test_add_attribute(self):
        name = "Test"
        type_ = "number"
        enum = [1.1, 2.2, 3.3]
        minimum = 1.1
        maximum = 3.3

        support_attributes = AttributesMixin()
        support_attributes.add_attribute(
            name=name, type_=type_, enum=enum, minimum=minimum, maximum=maximum
        )

        assert support_attributes.attributes["Test"].name == name
        assert support_attributes.attributes["Test"].type == type_
        assert support_attributes.attributes["Test"].enum == enum
        assert support_attributes.attributes["Test"].minimum == minimum
        assert support_attributes.attributes["Test"].maximum == maximum

    def test_dumps(self):
        support_attributes_data = _ATTRIBUTESMIXIN_DATA["attributes"][0]
        name = support_attributes_data["name"]
        type_ = support_attributes_data["type"]
        enum = support_attributes_data["enum"]
        minimum = support_attributes_data["minimum"]
        maximum = support_attributes_data["maximum"]

        support_attributes = AttributesMixin()
        support_attributes.add_attribute(
            name=name, type_=type_, enum=enum, minimum=minimum, maximum=maximum
        )
        assert support_attributes._dumps() == _ATTRIBUTESMIXIN_DATA
