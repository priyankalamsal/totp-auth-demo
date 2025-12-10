import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

student_id = "23mh1a05s1"
repo_url = "https://github.com/priyankalamsal/totp-auth-demo"

public_key = open("student_public.pem").read()

payload = {
    "student_id": student_id,
    "github_repo_url": repo_url,
    "public_key": public_key
}

res = requests.post(API_URL, json=payload)
print("\nAPI RESPONSE:\n", res.json())

encrypted_seed = res.json()["encrypted_seed"]

with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_seed)

print("\nSaved NEW encrypted seed to encrypted_seed.txt\n")
