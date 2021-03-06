"""Tests for the ORM bits"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from .. import orm


def test_server(db):
    server = orm.Server()
    db.add(server)
    db.commit()
    assert server.ip == 'localhost'
    assert server.base_url == '/'
    assert server.proto == 'http'
    assert isinstance(server.port, int)
    assert isinstance(server.cookie_name, str)
    assert server.url == 'http://localhost:%i/' % server.port


def test_proxy(db):
    proxy = orm.Proxy(
        auth_token='abc-123',
        public_server=orm.Server(
            ip='192.168.1.1',
            port=8000,
        ),
        api_server=orm.Server(
            ip='127.0.0.1',
            port=8001,
        ),
    )
    db.add(proxy)
    db.commit()
    assert proxy.public_server.ip == '192.168.1.1'
    assert proxy.api_server.ip == '127.0.0.1'
    assert proxy.auth_token == 'abc-123'


def test_hub(db):
    hub = orm.Hub(
        server=orm.Server(
            ip = '1.2.3.4',
            port = 1234,
            base_url='/hubtest/',
        ),
        
    )
    db.add(hub)
    db.commit()
    assert hub.server.ip == '1.2.3.4'
    hub.server.port == 1234
    assert hub.api_url == 'http://1.2.3.4:1234/hubtest/api'


def test_user(db):
    user = orm.User(name='kaylee',
        server=orm.Server(),
        state={'pid': 4234},
    )
    db.add(user)
    db.commit()
    assert user.name == 'kaylee'
    assert user.server.ip == 'localhost'
    assert user.state == {'pid': 4234}

    found = orm.User.find(db, 'kaylee')
    assert found.name == user.name
    found = orm.User.find(db, 'badger')
    assert found is None


def test_tokens(db):
    user = orm.User(name='inara')
    db.add(user)
    db.commit()
    token = user.new_api_token()
    assert any(t.match(token) for t in user.api_tokens)
    user.new_api_token()
    assert len(user.api_tokens) == 2
    found = orm.APIToken.find(db, token=token)
    assert found.match(token)
    found = orm.APIToken.find(db, 'something else')
    assert found is None
