from io import BytesIO

from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from rest_framework import viewsets, authentication, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app_core.models import LangchainPgEmbedding
from api_embeddings.serializers import EmbeddingSerializer
from app_chatbot.utils.llm import get_embeddings


class EmbeddingViewSet(viewsets.ModelViewSet):
    """Manage embeddings in the database"""
    serializer_class = EmbeddingSerializer
    queryset = LangchainPgEmbedding.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Perform the creation of an embedding."""
        serializer.save(user=self.request.user)


class UploadDocumentView(APIView):
    """Ingest an uploaded .txt, .md or .pdf file into the vector store."""
    parser_classes = [MultiPartParser]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        name = file.name
        ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
        if ext == 'pdf':
            reader = PdfReader(BytesIO(file.read()))
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
        elif ext in ('txt', 'md'):
            text = file.read().decode('utf-8', errors='ignore')
        else:
            return Response({'detail': 'Only .pdf, .txt and .md are supported.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not text.strip():
            return Response({'detail': 'No text found in file.'},
                            status=status.HTTP_400_BAD_REQUEST)

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0)
        splits = splitter.split_documents(
            [Document(page_content=text, metadata={'source': name})])
        PGVector.from_documents(
            documents=splits,
            collection_name='rag-pgvector',
            embedding=get_embeddings(),
            use_jsonb=True,
        )
        return Response({'file': name, 'chunks': len(splits)},
                        status=status.HTTP_201_CREATED)
