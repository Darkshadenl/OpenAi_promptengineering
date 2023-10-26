# Installeer de Replicate Python library met pip:
# pip install replicate

# Maak een bestand aan genaamd app.py en voeg de volgende code toe:
import replicate

# Zorg ervoor dat uw token is ingesteld als een omgevingsvariabele
replicate = replicate.Replicate(auth=os.environ['REPLICATE_API_TOKEN'])

model = "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"
input = { "prompt": "an astronaut riding a horse on mars, hd, dramatic lighting, detailed" }
output = replicate.run(model, { "input": input })

print(output)

# Voer de code uit met:
# python app.py
