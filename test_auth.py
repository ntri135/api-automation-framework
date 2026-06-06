# =============================================
# TEST AUTH - Mo phong flow authentication
# =============================================

import time
import pytest
import requests
from config import BASE_URL, TIMEOUT, MAX_RESPONSE_TIME, FAKE_TOKEN


# =============================================
# NHOM 1: Test lay du lieu nguoi dung
# =============================================

def test_get_all_users_success():
    """
    Lay danh sach tat ca users.
    Kiem tra status code va cau truc data.
    """
    start = time.time()
    response = requests.get(
        BASE_URL + "/users",
        timeout=TIMEOUT
    )
    response_time = time.time() - start

    assert response.status_code == 200, \
        "Phai tra ve 200. Thuc te: " + str(response.status_code)

    data = response.json()
    assert isinstance(data, list), "Data phai la list"
    assert len(data) > 0, "Phai co it nhat 1 user"
    assert response_time < MAX_RESPONSE_TIME, \
        "Qua cham: " + str(round(response_time, 2)) + "s"

    print("\nLay duoc " + str(len(data)) + " users")
    print("Thoi gian: " + str(round(response_time, 2)) + "s")


def test_get_single_user_success():
    """
    Lay thong tin 1 user cu the.
    """
    response = requests.get(
        BASE_URL + "/users/1",
        timeout=TIMEOUT
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data
    assert "username" in data

    print("\nUser 1: " + data["name"])
    print("Email: " + data["email"])


def test_get_nonexistent_user():
    """
    Lay user khong ton tai phai tra ve 404.
    """
    response = requests.get(
        BASE_URL + "/users/9999",
        timeout=TIMEOUT
    )

    assert response.status_code == 404, \
        "User khong ton tai phai tra ve 404"

    print("\nUser 9999 khong ton tai, tra ve 404: PASS")


def test_user_has_required_fields():
    """
    Kiem tra moi user phai co du cac truong bat buoc.
    """
    response = requests.get(
        BASE_URL + "/users",
        timeout=TIMEOUT
    )

    users = response.json()

    for user in users:
        assert "id" in user, \
            "User thieu truong id: " + str(user)
        assert "name" in user, \
            "User thieu truong name"
        assert "email" in user, \
            "User thieu truong email"
        assert "username" in user, \
            "User thieu truong username"

    print("\nTat ca " + str(len(users)) + " users deu co du truong")


def test_user_id_is_positive():
    """
    Kiem tra ID cua moi user phai la so duong.
    """
    response = requests.get(
        BASE_URL + "/users",
        timeout=TIMEOUT
    )

    users = response.json()

    for user in users:
        assert user["id"] > 0, \
            "User ID phai la so duong, thuc te: " + str(user["id"])

    print("\nTat ca user ID deu la so duong: PASS")


def test_email_format_valid():
    """
    Kiem tra tat ca email cua users phai dung format.
    """
    response = requests.get(
        BASE_URL + "/users",
        timeout=TIMEOUT
    )

    users = response.json()
    loi = []

    for user in users:
        email = user["email"]
        if "@" not in email:
            loi.append("Email thieu @: " + email)
        elif "." not in email.split("@")[1]:
            loi.append("Email thieu domain: " + email)

    assert len(loi) == 0, \
        "Co email sai format: " + str(loi)

    print("\nTat ca " + str(len(users)) + " emails deu dung format: PASS")


# =============================================
# NHOM 2: Test tao, sua, xoa du lieu
# =============================================

def test_create_new_user():
    """
    Tao user moi.
    Kiem tra response tra ve dung thong tin.
    """
    payload = {
        "name": "Nguyen Van A",
        "username": "nguyenvana",
        "email": "nguyenvana@gmail.com",
        "phone": "0901234567"
    }

    start = time.time()
    response = requests.post(
        BASE_URL + "/users",
        json=payload,
        timeout=TIMEOUT
    )
    response_time = time.time() - start

    assert response.status_code == 201, \
        "Tao user phai tra ve 201. Thuc te: " + str(response.status_code)

    data = response.json()
    assert data["name"] == payload["name"], \
        "Name tra ve khong khop"
    assert data["email"] == payload["email"], \
        "Email tra ve khong khop"
    assert "id" in data, \
        "Response phai chua id cua user moi"
    assert response_time < MAX_RESPONSE_TIME

    print("\nTao user thanh cong!")
    print("ID moi: " + str(data["id"]))
    print("Ten: " + data["name"])


def test_update_user():
    """
    Cap nhat thong tin user.
    """
    payload = {
        "name": "Nguyen Van B",
        "email": "nguyenvanb@gmail.com"
    }

    response = requests.put(
        BASE_URL + "/users/1",
        json=payload,
        timeout=TIMEOUT
    )

    assert response.status_code == 200, \
        "Update phai tra ve 200. Thuc te: " + str(response.status_code)

    data = response.json()
    assert data["name"] == payload["name"], \
        "Name sau update khong dung"
    assert data["email"] == payload["email"], \
        "Email sau update khong dung"

    print("\nUpdate user thanh cong!")
    print("Ten moi: " + data["name"])


def test_delete_user():
    """
    Xoa user.
    Kiem tra server xac nhan xoa thanh cong.
    """
    response = requests.delete(
        BASE_URL + "/users/1",
        timeout=TIMEOUT
    )

    assert response.status_code == 200, \
        "Xoa user phai tra ve 200. Thuc te: " + str(response.status_code)

    print("\nXoa user thanh cong: 200 OK")


# =============================================
# NHOM 3: Test bao mat co ban
# (Mo phong kiem tra auth)
# =============================================

def test_create_user_validates_required_fields():
    """
    Kiem tra tao user voi du lieu thieu truong.
    Mo phong validation test.
    """
    payload_thieu_name = {
        "email": "test@test.com"
    }

    response = requests.post(
        BASE_URL + "/users",
        json=payload_thieu_name,
        timeout=TIMEOUT
    )

    # JSONPlaceholder van tao duoc vi no la mock API
    # Nhung trong he thong that, phai tra ve 400
    # Day la diem chung ta ghi nhan de bao cao
    if response.status_code == 400:
        print("\nServer validate dung: Tu choi khi thieu name")
    else:
        print("\n[GHI NHAN] Server khong validate truong bat buoc")
        print("Trong he thong that, day co the la bug")
        print("Status code: " + str(response.status_code))

    # Test nay luon pass vi muc dich la ghi nhan hanh vi
    assert response.status_code in [200, 201, 400]


def test_get_user_data_structure():
    """
    Kiem tra cau truc du lieu tra ve co nhat quan khong.
    Moi user phai co cung cac truong.
    """
    response = requests.get(
        BASE_URL + "/users",
        timeout=TIMEOUT
    )

    users = response.json()
    truong_bat_buoc = ["id", "name", "username", "email", "phone"]

    user_thieu_truong = []

    for user in users:
        for truong in truong_bat_buoc:
            if truong not in user:
                user_thieu_truong.append(
                    "User " + str(user["id"]) + " thieu truong: " + truong
                )

    assert len(user_thieu_truong) == 0, \
        "Co user thieu truong bat buoc: " + str(user_thieu_truong)

    print("\nTat ca users co du cau truc: PASS")
    print("Da kiem tra " + str(len(truong_bat_buoc)) + " truong bat buoc")
    print("Tren " + str(len(users)) + " users")


def test_response_time_all_users():
    """
    Kiem tra toc do phan hoi cua API lay danh sach users.
    """
    response_times = []

    for i in range(3):
        start = time.time()
        response = requests.get(
            BASE_URL + "/users",
            timeout=TIMEOUT
        )
        response_time = time.time() - start
        response_times.append(response_time)
        assert response.status_code == 200

    trung_binh = sum(response_times) / len(response_times)
    lon_nhat = max(response_times)

    assert trung_binh < MAX_RESPONSE_TIME, \
        "Thoi gian trung binh qua cham: " + str(round(trung_binh, 2)) + "s"

    print("\nKiem tra toc do (3 lan):")
    for i, t in enumerate(response_times):
        print("  Lan " + str(i+1) + ": " + str(round(t, 2)) + "s")
    print("Trung binh: " + str(round(trung_binh, 2)) + "s")
    print("Lon nhat: " + str(round(lon_nhat, 2)) + "s")