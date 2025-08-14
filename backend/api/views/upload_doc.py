from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from ai.utils.vector_store import vectorstore


@api_view(["POST"])
def upload_doc(request):
    file = request.FILES.get("file")
    user_id = request.data.get("userId") # Get userId from request data

    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    if not user_id:
        return Response({"error": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.name)

    # Save the uploaded file to disk
    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Read the full content of the file for manual indexing
    with open(file_path, "r") as f:
        full_text = f.read()

    # Load and split the text file (without add_start_index)
    loader = TextLoader(file_path)
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=300, chunk_overlap=100)
    docs = loader.load_and_split(text_splitter=text_splitter)

    # Add metadata to each document
    for doc in docs:
        doc.metadata["document_name"] = file.name
        doc.metadata["user_id"] = user_id # Add userId to metadata
        doc.metadata["type"] = "customer-agent-docs" # Add new metadata type

    # Vectorize and store
    vectorstore.add_documents(documents=docs)

    return Response({"message": f"{file.name} uploaded and processed successfully!"}, status=status.HTTP_200_OK)
