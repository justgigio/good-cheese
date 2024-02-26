from src.server import app
from fastapi.testclient import TestClient

from tests.fixtures import session

from tests.factories.boleto_factory import BoletoFactory
from tests.factories.boleto_file_factory import BoletoFileFactory

client = TestClient(app)

def test_list_boletos(session):
    bf1 = BoletoFileFactory.build()
    bf2 = BoletoFileFactory.build()

    session.add_all([bf1, bf2])
    session.commit()

    response = client.get("/boletos/")

    bf_list = response.json()

    assert response.status_code == 200
    assert len(bf_list) == 2
    assert bf_list[0]["name"] == bf1.name
    assert bf_list[1]["checksum"] == bf2.checksum


def test_check_upload_boleto(session):
    bf = BoletoFileFactory.build(size=4)

    not_found_response = client.get(f"/boletos/upload/{bf.id}")
    assert not_found_response.status_code == 404

    session.add(bf)
    session.commit()

    response = client.get(f"/boletos/upload/{bf.id}")

    upload_status = response.json()

    assert response.status_code == 200
    assert upload_status["id"] == bf.id
    assert upload_status["size"] == bf.size
    assert upload_status["inserted"] == 0
    assert upload_status["completed"] == False
    assert upload_status["percent"] == 0

    b1 = BoletoFactory.build(boleto_file=bf)

    session.add(b1)
    session.commit()

    response = client.get(f"/boletos/upload/{bf.id}")

    upload_status = response.json()

    assert response.status_code == 200
    assert upload_status["id"] == bf.id
    assert upload_status["size"] == bf.size
    assert upload_status["inserted"] == 1
    assert upload_status["completed"] == False
    assert upload_status["percent"] == 25.0

    b2 = BoletoFactory.build(boleto_file=bf)
    b3 = BoletoFactory.build(boleto_file=bf)

    session.add_all([b2, b3])
    session.commit()

    response = client.get(f"/boletos/upload/{bf.id}")

    upload_status = response.json()

    assert response.status_code == 200
    assert upload_status["id"] == bf.id
    assert upload_status["size"] == bf.size
    assert upload_status["inserted"] == 3
    assert upload_status["completed"] == False
    assert upload_status["percent"] == 75.0

    b4 = BoletoFactory.build(boleto_file=bf)

    session.add(b4)
    session.commit()

    response = client.get(f"/boletos/upload/{bf.id}")

    upload_status = response.json()

    assert response.status_code == 200
    assert upload_status["id"] == bf.id
    assert upload_status["size"] == bf.size
    assert upload_status["inserted"] == 4
    assert upload_status["completed"] == True
    assert upload_status["percent"] == 100.0
