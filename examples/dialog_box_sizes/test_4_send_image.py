import pytest
from hardpy import DialogBox, ImageWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Image dialog box")


# def test_small_100():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/test.png",
#             width=100,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_100_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/test.png",
#             width=100,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_100():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=100,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_100_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=100,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_20():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/test.png",
#             width=20,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_20_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/test.png",
#             width=20,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_200():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/test.png",
#             width=200,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_200_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/test.png",
#             width=200,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_20():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=20,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_20_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=20,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_200():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=200,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_200_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=200,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_50():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=50,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_50_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/sample_1920x1280.gif",
#             width=50,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_5_mb_100():
#     dbx = DialogBox(
#         dialog_text="Test image",
#         widget=ImageWidget(
#             address="assets/test_5_mb.jpg",
#             width=100,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_5_mb_50_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/test_5_mb.jpg",
#             width=50,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_5_mb_200_long_text():
#     dbx = DialogBox(
#         dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
#         widget=ImageWidget(
#             address="assets/test_5_mb.jpg",
#             width=200,
#         ),
#     )
#     response = run_dialog_box(dbx)
#     assert response
