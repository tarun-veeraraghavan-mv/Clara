from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

@api_view(["POST"])
def upload_doc(request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.name)

    # Save the uploaded file to disk
    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return Response({"message": f"{file.name} uploaded and processed successfully!"}, status=status.HTTP_200_OK)
