# Tạo key riêng tư
openssl genpkey -algorithm RSA -out key.pem

# Tạo chứng chỉ tự ký bằng key riêng tư
openssl req -new -x509 -key key.pem -out cert.pem -days 365 -config openssl.cnf

