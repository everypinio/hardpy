# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pathlib import Path

from hardpy.common.config import HardpyConfig

docker_compose_yaml = """version: "3.8"

services:
  couchserver:
    image: couchdb:3.4
    ports:
      - "{}:5984"
    environment:
      COUCHDB_USER: {}
      COUCHDB_PASSWORD: {}
    volumes:
      - ./database/dbdata:/opt/couchdb/data
      - ./database/couchdb.ini:/opt/couchdb/etc/local.ini
"""

couchdb_ini = """; CouchDB Configuration Settings

; Custom settings should be made in this file. They will override settings
; in default.ini, but unlike changes made to default.ini, this file won't be
; overwritten on server upgrade.

[couchdb]
;max_document_size = 4294967296 ; bytes
;os_process_timeout = 5000

[couch_peruser]
; If enabled, couch_peruser ensures that a private per-user database
; exists for each document in _users. These databases are writable only
; by the corresponding user. Databases are in the following form:
; userdb-{{hex encoded username}}
;enable = true

; If set to true and a user is deleted, the respective database gets
; deleted as well.
;delete_dbs = true

; Set a default q value for peruser-created databases that is different from
; cluster / q
;q = 1

[chttpd]
;port = {}
;bind_address = {}

; Options for the MochiWeb HTTP server.
;server_options = [{{backlog, 128}}, {{acceptor_pool_size, 16}}]

; For more socket options, consult Erlang's module 'inet' man page.
;socket_options = [{{sndbuf, 262144}}, {{nodelay, true}}]

enable_cors=true

[httpd]
; NOTE that this only configures the "backend" node-local port, not the
; "frontend" clustered port. You probably don't want to change anything in
; this section.
; Uncomment next line to trigger basic-auth popup on unauthorized requests.
;WWW-Authenticate = Basic realm="administrator"

; Uncomment next line to set the configuration modification whitelist. Only
; whitelisted values may be changed via the /_config URLs. To allow the admin
; to change this value over HTTP, remember to include {{httpd,config_whitelist}}
; itself. Excluding it from the list would require editing this file to update
; the whitelist.
;config_whitelist = [{{httpd,config_whitelist}}, {{log,level}}, {{etc,etc}}]

[cors]
origins = *
methods = GET, PUT, POST, HEAD, DELETE
credentials = true
headers = accept, authorization, content-type, origin, referer, x-csrf-token


[ssl]
;enable = true
;cert_file = /full/path/to/server_cert.pem
;key_file = /full/path/to/server_key.pem
;password = somepassword

; set to true to validate peer certificates
;verify_ssl_certificates = false

; Set to true to fail if the client does not send a certificate. Only used if verify_ssl_certificates is true.
;fail_if_no_peer_cert = false

; Path to file containing PEM encoded CA certificates (trusted
; certificates used for verifying a peer certificate). May be omitted if
; you do not want to verify the peer.
;cacert_file = /full/path/to/cacertf

; The verification fun (optional) if not specified, the default
; verification fun will be used.
;verify_fun = {{Module, VerifyFun}}

; maximum peer certificate depth
;ssl_certificate_max_depth = 1

; Reject renegotiations that do not live up to RFC 5746.
;secure_renegotiate = true

; The cipher suites that should be supported.
; Can be specified in erlang format "{{ecdhe_ecdsa,aes_128_cbc,sha256}}"
; or in OpenSSL format "ECDHE-ECDSA-AES128-SHA256".
;ciphers = ["ECDHE-ECDSA-AES128-SHA256", "ECDHE-ECDSA-AES128-SHA"]

; The SSL/TLS versions to support
;tls_versions = [tlsv1, 'tlsv1.1', 'tlsv1.2']

; To enable Virtual Hosts in CouchDB, add a vhost = path directive. All requests to
; the Virtual Host will be redirected to the path. In the example below all requests
; to http://example.com/ are redirected to /database.
; If you run CouchDB on a specific port, include the port number in the vhost:
; example.com:5984 = /database
[vhosts]
;example.com = /database/

; To create an admin account uncomment the '[admins]' section below and add a
; line in the format 'username = password'. When you next start CouchDB, it
; will change the password to a hash (so that your passwords don't linger
; around in plain-text files). You can add more admin accounts with more
; 'username = password' lines. Don't forget to restart CouchDB after
; changing this.
[admins]
;admin = mysecretpassword
"""  # noqa: E501

pytest_ini = """[pytest]
addopts = --hardpy-pt
          --hardpy-db-url http://{}:{}@{}:{}/
"""

test_1_py = """import pytest
import hardpy


pytestmark = pytest.mark.module_name("HardPy template")


@pytest.mark.case_name("Test 1")
def test_one():
    assert True
"""

conftest_py = """import pytest
import hardpy


def finish_executing():
    print("Testing completed")


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
"""


class TemplateGenerator:
    """HardPy template files generator."""

    def __init__(self, config: HardpyConfig) -> None:
        self._config = config

    def create_file(self, file_path: Path, content: str) -> None:
        """Create HardPy template file.

        Args:
            file_path (Path): file path
            content (str): file content
        """
        with Path.open(file_path, "w") as file:
            file.write(content)

    @property
    def docker_compose_yaml(self) -> str:
        return docker_compose_yaml.format(
            self._config.database.port,
            self._config.database.user,
            self._config.database.password,
        )

    @property
    def couchdb_ini(self) -> str:
        return couchdb_ini.format(
            self._config.database.port,
            self._config.database.host,
        )

    @property
    def pytest_ini(self) -> str:
        return pytest_ini.format(
            self._config.database.user,
            self._config.database.password,
            self._config.database.host,
            self._config.database.port,
        )

    @property
    def test_1_py(self) -> str:
        return test_1_py

    @property
    def conftest_py(self) -> str:
        return conftest_py
