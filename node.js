// Installeer Node.js en de Replicate npm package
// Voer de volgende commando's uit in de terminal:
// mkdir replicate-nodejs
// cd replicate-nodejs
// echo "{\"type\": \"module\"}" > package.json
// npm install replicate

// Maak een bestand aan genaamd index.js en voeg de volgende code toe:
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,  // Zorg ervoor dat uw token is ingesteld als een omgevingsvariabele
});

const model = "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf";
const input = { prompt: "an astronaut riding a horse on mars, hd, dramatic lighting, detailed" };
const output = await replicate.run(model, { input });

console.log(output);

// Voer de code uit met:
// node index.js
