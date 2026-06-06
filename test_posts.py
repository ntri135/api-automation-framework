# =============================================
# TEST POSTS - Test CRUD cho Posts API
# =============================================

import time
import pytest
import requests
from config import BASE_URL, TIMEOUT, MAX_RESPONSE_TIME


# =============================================
# NHOM 1: Lay bai viet
# =============================================

def test_get_all_posts():
    response = requests.get(
        BASE_URL + "/posts",
        timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100, \
        "JSONPlaceholder co dung 100 posts"

    print("\nLay duoc " + str(len(data)) + " posts: PASS")


def test_get_single_post():
    response = requests.get(
        BASE_URL + "/posts/1",
        timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert "title" in data
    assert "body" in data
    assert "userId" in data
    assert len(data["title"]) > 0, "Title khong duoc rong"
    assert len(data["body"]) > 0, "Body khong duoc rong"

    print("\nPost 1: " + data["title"][:30] + "...")


def test_get_posts_by_user():
    """
    Lay tat ca posts cua user 1.
    """
    response = requests.get(
        BASE_URL + "/posts",
        params={"userId": 1},
        timeout=TIMEOUT
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    for post in data:
        assert post["userId"] == 1, \
            "Tat ca posts phai thuoc user 1"

    print("\nUser 1 co " + str(len(data)) + " posts")


def test_post_has_required_fields():
    response = requests.get(
        BASE_URL + "/posts",
        timeout=TIMEOUT
    )

    posts = response.json()
    bat_buoc = ["id", "userId", "title", "body"]

    for post in posts[:5]:
        for truong in bat_buoc:
            assert truong in post, \
                "Post thieu truong: " + truong

    print("\nKiem tra 5 posts dau: tat ca co du truong")


# =============================================
# NHOM 2: Tao va sua bai viet
# =============================================

def test_create_post():
    payload = {
        "title": "Bai viet test tu dong",
        "body": "Day la noi dung bai viet duoc tao tu script test",
        "userId": 1
    }

    start = time.time()
    response = requests.post(
        BASE_URL + "/posts",
        json=payload,
        timeout=TIMEOUT
    )
    response_time = time.time() - start

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data
    assert response_time < MAX_RESPONSE_TIME

    print("\nTao post thanh cong!")
    print("ID moi: " + str(data["id"]))
    print("Title: " + data["title"])


def test_create_post_with_empty_title():
    """
    Tao post voi title rong.
    Ghi nhan hanh vi cua server.
    """
    payload = {
        "title": "",
        "body": "Body binh thuong",
        "userId": 1
    }

    response = requests.post(
        BASE_URL + "/posts",
        json=payload,
        timeout=TIMEOUT
    )

    if response.status_code == 400:
        print("\nServer tu choi title rong: DUNG")
    else:
        print("\n[GHI NHAN] Server chap nhan title rong")
        print("Day co the la bug trong he thong that")

    assert response.status_code in [200, 201, 400]


def test_update_post():
    payload = {
        "id": 1,
        "title": "Title da cap nhat",
        "body": "Body da cap nhat",
        "userId": 1
    }

    response = requests.put(
        BASE_URL + "/posts/1",
        json=payload,
        timeout=TIMEOUT
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]

    print("\nUpdate post thanh cong!")
    print("Title moi: " + data["title"])


def test_delete_post():
    response = requests.delete(
        BASE_URL + "/posts/1",
        timeout=TIMEOUT
    )

    assert response.status_code == 200

    print("\nXoa post thanh cong!")


# =============================================
# NHOM 3: Test Comments
# =============================================

def test_get_comments_of_post():
    """
    Lay tat ca comments cua post 1.
    """
    response = requests.get(
        BASE_URL + "/posts/1/comments",
        timeout=TIMEOUT
    )

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0

    print("\nPost 1 co " + str(len(comments)) + " comments")


def test_comment_email_is_valid():
    """
    Kiem tra email trong comments phai dung format.
    """
    response = requests.get(
        BASE_URL + "/posts/1/comments",
        timeout=TIMEOUT
    )

    comments = response.json()
    loi = []

    for comment in comments:
        email = comment["email"]
        if "@" not in email:
            loi.append(email)

    assert len(loi) == 0, \
        "Co email sai format trong comments: " + str(loi)

    print("\nTat ca " + str(len(comments)) + " comment emails deu hop le")


def test_response_time_posts():
    """
    Kiem tra toc do cua Posts API.
    """
    start = time.time()
    response = requests.get(
        BASE_URL + "/posts",
        timeout=TIMEOUT
    )
    response_time = time.time() - start

    assert response.status_code == 200
    assert response_time < MAX_RESPONSE_TIME, \
        "API qua cham: " + str(round(response_time, 2)) + "s"

    print("\nToc do Posts API: " + str(round(response_time, 2)) + "s")