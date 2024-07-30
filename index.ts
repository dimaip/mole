import path from "path";

import { TextLoader } from "langchain/document_loaders/fs/text";
import * as fs from "fs";
import { ChromaClient } from "chromadb";
import crypto from "crypto";

import { OpenAIEmbeddingFunction } from "chromadb";

const collectionName = "mole-content-large";

const a: any[] = [];

const index = async () => {
  const embedder = new OpenAIEmbeddingFunction({
    openai_api_key: "",
    openai_model: "text-embedding-3-large",
  });
  const client = new ChromaClient();

  // await client.deleteCollection({ name: collectionName });
  const collection = await client.createCollection({
    name: collectionName,
    embeddingFunction: embedder,
  });

  async function indexFile(filePath: string) {
    console.log(`Processing file: ${filePath}`);
    const loader = new TextLoader(filePath);
    const docs = await loader.loadAndSplit();
    console.log(docs);

    a.push(...docs);

    await collection.add({
      ids: docs.map((doc, index) => `${filePath}-${index}`),
      documents: docs.map((doc) => doc.pageContent),
      metadatas: docs.map((doc) => doc.metadata),
    });
  }

  async function traverseDirectory(dir: string) {
    const files = fs.readdirSync(dir, { withFileTypes: true });

    for (const file of files) {
      if (file.isDirectory()) {
        await traverseDirectory(file.path + "/" + file.name);
      } else if (file.isFile() && file.name.endsWith(".txt")) {
        await indexFile(file.path + "/" + file.name);
      }
    }
  }

  await traverseDirectory(path.resolve("./scrape"));
  console.log(a.length, a[0], a[1]);
};

index();
