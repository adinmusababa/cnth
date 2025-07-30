https://vscode.dev/tunnel/msi/C:/Users/Musa/OneDrive - Universitas Teknologi Yogyakarta/chatbot

https://vscode.dev/tunnel/msi/C:/Users/Musa/OneDrive%20-%20Universitas%20Teknologi%20Yogyakarta/chatbot?vscode-lang=id

https://vscode.dev/tunnel/msi/C:/Users/Musa/OneDrive%20-%20Universitas%20Teknologi%20Yogyakarta/project%202025/chatbot?vscode-lang=id

https://bps3320.my.id/


PS C:\Users\BPS> docker pull qdrant/qdrant
Using default tag: latest
latest: Pulling from qdrant/qdrant
Digest: sha256:d122138f76868edba68d36cb0833139c1d1761f00f09e48e61f8314196e6a4c6
Status: Image is up to date for qdrant/qdrant:latest
docker.io/qdrant/qdrant:latest
PS C:\Users\BPS> docker run -p 6333:6333 -p 6334:6334 \
docker: invalid reference format

Run 'docker run --help' for more information
PS C:\Users\BPS>     -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
-v : The term '-v' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and 
try again.
At line:1 char:5
+     -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
+     ~~
    + CategoryInfo          : ObjectNotFound: (-v:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

PS C:\Users\BPS>     qdrant/qdrant



from pathlib import Path
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from qdrant_client import QdrantClient

# --- Qdrant Docker via Ngrok ---
qdrant_client = QdrantClient(
    url="http://20e7f39eb39d.ngrok-free.app",  # gunakan http
    prefer_grpc=False
)

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="chatbotdata3320"
)

# --- Load dokumen hasil ekstraksi ---
DATA_DIR = "/content/drive/MyDrive/extracted"
documents = SimpleDirectoryReader(DATA_DIR).load_data()

# --- Split dokumen jadi chunk agar embedding lebih optimal ---
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = splitter.get_nodes_from_documents(documents)

# --- Model embedding ---
embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large")

# --- Simpan embedding ke Qdrant Docker ---
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    nodes,
    storage_context=storage_context,
    embed_model=embed_model
)

print("✅ Index berhasil disimpan ke dalam Qdrant Docker via Ngrok")

