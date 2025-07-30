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
