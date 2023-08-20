from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class GiftAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass


class CreditAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

    def get(self, request):
        pass


class WalletAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

    def get(self, request):
        pass
