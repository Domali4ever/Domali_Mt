import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Get today's date
today_date = datetime.date.today()
print(f"Today's date: {today_date}")

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Define certificate subject and issuer (customize as needed)
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Organization"),
])

# Set the current UTC time for consistency
current_time = datetime.datetime.now(datetime.timezone.utc)

# Create a self-signed certificate with validity starting now and lasting 1 year
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    current_time  # Use the same current time for consistency
).not_valid_after(
    current_time + datetime.timedelta(days=365)  # Valid for 1 year from the current time
).sign(
    private_key, hashes.SHA256()
)

# Save the private key to a PEM file
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save the certificate to a PEM file
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Certificate and private key have been saved successfully.")
