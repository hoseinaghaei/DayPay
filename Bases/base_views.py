from rest_framework.views import APIView
from rest_framework.serializers import Serializer


class BaseAPIView(APIView):
    serializer_class = None

    def _prepare_validated_data(self, request):
        if self.serializer_class is None:
            raise NotImplementedError("serializer_class must be defined")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
