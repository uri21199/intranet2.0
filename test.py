from werkzeug.security import check_password_hash

hashed_password = "scrypt:32768:8:1$33JSUtB2xoFt7zz9$50309db8f65097cd37932085f9a843288281b2c35b3c424ffa1af61901b21a65fef9b23b19cc835954a92869af27de6f772bc0d6a56a723c371868ca8727c4ce"
input_password = "20365521132"

if check_password_hash(hashed_password, input_password):
    print("✅ Contraseña correcta")
else:
    print("❌ Contraseña incorrecta")
