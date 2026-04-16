"""
cert_manager.py
Geração automática de PKI interna para mTLS do Apollo IAM Engine.

Estrutura gerada em <certs_dir>/:
  ca/
    ca.key      — chave privada da CA (RSA-2048)
    ca.crt      — certificado auto-assinado da CA
  server/
    server.key  — chave privada do servidor
    server.crt  — certificado do servidor assinado pela CA
  client/
    client.key  — chave privada do cliente
    client.crt  — certificado do cliente assinado pela CA
    client.p12  — bundle PKCS#12 (para importar em browsers/ferramentas)

Todos os certs usam RSA-2048 + SHA-256.
O2 Data Solutions
"""
from __future__ import annotations

import ipaddress
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from src.infrastructure.logging.console_logger import info, success, warning


# ── helpers ───────────────────────────────────────────────────────────────────

def _gen_rsa_key(key_size: int = 2048) -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=key_size)


def _save_key(key: rsa.RSAPrivateKey, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    # permissão restrita — somente dono lê/escreve
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


def _save_cert(cert: x509.Certificate, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


def _subject(cn: str, org: str = "O2 Data Solutions", country: str = "BR") -> x509.Name:
    return x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])


def _validity(days: int):
    now = datetime.now(timezone.utc)
    return now, now + timedelta(days=days)


# ── CA ────────────────────────────────────────────────────────────────────────

def _gen_ca(certs_dir: Path, cfg: dict) -> tuple[rsa.RSAPrivateKey, x509.Certificate]:
    ca_dir  = certs_dir / "ca"
    key_path = ca_dir / "ca.key"
    crt_path = ca_dir / "ca.crt"

    if key_path.exists() and crt_path.exists():
        info("mTLS: CA já existe — reutilizando.")
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        ca_key  = load_pem_private_key(key_path.read_bytes(), password=None)
        ca_cert = x509.load_pem_x509_certificate(crt_path.read_bytes())
        return ca_key, ca_cert

    info("mTLS: Gerando CA interna RSA-2048...")
    ca_key = _gen_rsa_key(2048)
    not_before, not_after = _validity(cfg.get("validity_days", 3650))

    subject = _subject(
        cn=cfg.get("common_name", "Apollo IAM Internal CA"),
        org=cfg.get("organization", "O2 Data Solutions"),
        country=cfg.get("country", "BR"),
    )

    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before)
        .not_valid_after(not_after)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True, key_cert_sign=True, crl_sign=True,
                content_commitment=False, key_encipherment=False,
                data_encipherment=False, key_agreement=False,
                encipher_only=False, decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    _save_key(ca_key, key_path)
    _save_cert(ca_cert, crt_path)
    success(f"mTLS: CA gerada → {crt_path}")
    return ca_key, ca_cert


# ── Server cert ───────────────────────────────────────────────────────────────

def _gen_server_cert(
    certs_dir: Path,
    ca_key: rsa.RSAPrivateKey,
    ca_cert: x509.Certificate,
    cfg: dict,
) -> tuple[Path, Path, Path]:
    srv_dir  = certs_dir / "server"
    key_path = srv_dir / "server.key"
    crt_path = srv_dir / "server.crt"

    if key_path.exists() and crt_path.exists():
        info("mTLS: Certificado do servidor já existe — reutilizando.")
        return key_path, crt_path, certs_dir / "ca" / "ca.crt"

    info("mTLS: Gerando certificado do servidor RSA-2048...")
    srv_key = _gen_rsa_key(cfg.get("key_size", 2048))
    not_before, not_after = _validity(cfg.get("validity_days", 825))

    # SANs
    san_list: list[x509.GeneralName] = []
    for dns in cfg.get("san_dns", ["localhost"]):
        san_list.append(x509.DNSName(dns))
    for ip_str in cfg.get("san_ip", ["127.0.0.1"]):
        try:
            san_list.append(x509.IPAddress(ipaddress.ip_address(ip_str)))
        except ValueError:
            pass

    subject = _subject(cn=cfg.get("common_name", "apollo-iam-server"))

    srv_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(srv_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before)
        .not_valid_after(not_after)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True, key_encipherment=True,
                content_commitment=False, data_encipherment=False,
                key_agreement=False, key_cert_sign=False,
                crl_sign=False, encipher_only=False, decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([x509.ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
        .add_extension(x509.SubjectAlternativeName(san_list), critical=False)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(srv_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    _save_key(srv_key, key_path)
    _save_cert(srv_cert, crt_path)
    success(f"mTLS: Certificado servidor gerado → {crt_path}")
    return key_path, crt_path, certs_dir / "ca" / "ca.crt"


# ── Client cert ───────────────────────────────────────────────────────────────

def _gen_client_cert(
    certs_dir: Path,
    ca_key: rsa.RSAPrivateKey,
    ca_cert: x509.Certificate,
    cfg: dict,
) -> tuple[Path, Path, Path]:
    cli_dir  = certs_dir / "client"
    key_path = cli_dir / "client.key"
    crt_path = cli_dir / "client.crt"
    p12_path = cli_dir / "client.p12"

    if key_path.exists() and crt_path.exists():
        info("mTLS: Certificado do cliente já existe — reutilizando.")
        return key_path, crt_path, p12_path

    info("mTLS: Gerando certificado do cliente RSA-2048...")
    cli_key = _gen_rsa_key(cfg.get("key_size", 2048))
    not_before, not_after = _validity(cfg.get("validity_days", 825))

    subject = _subject(
        cn=cfg.get("common_name", "apollo-iam-client"),
        org=cfg.get("organization", "O2 Data Solutions"),
    )

    cli_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(cli_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before)
        .not_valid_after(not_after)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True, key_encipherment=True,
                content_commitment=False, data_encipherment=False,
                key_agreement=False, key_cert_sign=False,
                crl_sign=False, encipher_only=False, decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([x509.ExtendedKeyUsageOID.CLIENT_AUTH]),
            critical=False,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(cli_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    _save_key(cli_key, key_path)
    _save_cert(cli_cert, crt_path)

    # PKCS#12 bundle (sem senha — para facilitar import em ferramentas)
    from cryptography.hazmat.primitives.serialization import pkcs12
    p12_data = pkcs12.serialize_key_and_certificates(
        name=b"apollo-iam-client",
        key=cli_key,
        cert=cli_cert,
        cas=[ca_cert],
        encryption_algorithm=serialization.NoEncryption(),
    )
    p12_path.parent.mkdir(parents=True, exist_ok=True)
    p12_path.write_bytes(p12_data)

    success(f"mTLS: Certificado cliente gerado → {crt_path}")
    success(f"mTLS: Bundle PKCS#12 → {p12_path}")
    return key_path, crt_path, p12_path


# ── Ponto de entrada público ──────────────────────────────────────────────────

class CertPaths:
    """Caminhos dos certificados gerados."""
    def __init__(
        self,
        ca_crt: Path,
        server_key: Path,
        server_crt: Path,
        client_key: Path,
        client_crt: Path,
        client_p12: Path,
    ):
        self.ca_crt     = ca_crt
        self.server_key = server_key
        self.server_crt = server_crt
        self.client_key = client_key
        self.client_crt = client_crt
        self.client_p12 = client_p12

    def as_dict(self) -> dict:
        return {k: str(v) for k, v in self.__dict__.items()}


def ensure_certs(certs_dir: str | Path | None = None, security_cfg: dict | None = None) -> CertPaths:
    """
    Garante que todos os certificados existam.
    Gera automaticamente se ausentes.
    Retorna CertPaths com os caminhos absolutos.
    """
    cfg = security_cfg or {}
    tls_cfg = cfg.get("tls", {})

    if certs_dir is None:
        certs_dir = tls_cfg.get("certs_dir", "certs")

    base = Path(certs_dir).resolve()
    base.mkdir(parents=True, exist_ok=True)

    ca_cfg  = tls_cfg.get("ca",     {})
    srv_cfg = tls_cfg.get("server", {})
    cli_cfg = tls_cfg.get("client", {})

    ca_key, ca_cert = _gen_ca(base, ca_cfg)
    srv_key, srv_crt, ca_crt = _gen_server_cert(base, ca_key, ca_cert, srv_cfg)
    cli_key, cli_crt, cli_p12 = _gen_client_cert(base, ca_key, ca_cert, cli_cfg)

    return CertPaths(
        ca_crt=ca_crt,
        server_key=srv_key,
        server_crt=srv_crt,
        client_key=cli_key,
        client_crt=cli_crt,
        client_p12=cli_p12,
    )
