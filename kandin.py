import kandinsky
import key

pipe = andinsky(auth_token={'X-Key': f'Key {key.api_key}', 'X-Secret': f'Secret {key.secret_key}'})

job = pipe.create(prompt="cat")
result = pipe.wait(job) #b64 string
image = pipe.load(result) #BytesIO object