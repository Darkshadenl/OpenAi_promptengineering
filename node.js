import Replicate from "replicate";
import dotenv from 'dotenv';

console.log("started")
dotenv.config();

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const model = "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3";
const input = { prompt: "write me a joke" };
const output = await replicate.run(model, { input });

output.forEach(item => {
    process.stdout.write(item);
});

