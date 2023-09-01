from rest_framework.views import APIView
from rest_framework.request import Request


class BaseAPIView(APIView):
    serializer_class = None

    def _prepare_validated_data(self, request: Request) -> dict:
        if self.serializer_class is None:
            raise NotImplementedError("serializer_class must be defined")

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            serializer = self.serializer_class(data=request.query_params)
            serializer.is_valid(raise_exception=True)

        return serializer.validated_data
