from rest_framework.views import APIView
from rest_framework import status as status_codes
from django.http import JsonResponse
from .profile_service import ProfileService
from ..mixins import TransactionMixin


class AllProfileView(APIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        page_no = query_params.get('page', 1)
        page_size = query_params.get("page_size", 10)

        profile_manager = ProfileService(page=page_no, page_size=page_size)
        response = profile_manager.fetch_all_profiles()

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class GetProfileView(APIView):

    def get(self, request, profile_id, *args, **kwargs):

        profile_manager = ProfileService(profile_id)
        response = profile_manager.fetch_profile_by_id()

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class CreateProfileView(TransactionMixin, APIView):

    def post(self, request, *args, **kwargs):

        profile_manager = ProfileService()
        response = profile_manager.create_profile(request.data)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class UpdateProfileView(TransactionMixin, APIView):

    def post(self, request, profile_id, *args, **kwargs):

        profile_manager = ProfileService(profile_id)
        response = profile_manager.update_profile(request.data)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class DeleteProfileView(TransactionMixin, APIView):

    def post(self, request, profile_id, *args, **kwargs):

        profile_manager = ProfileService(profile_id)
        response = profile_manager.delete_profile()

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class SearchProfileView(APIView):

    def post(self, request, query, *args, **kwargs):
        query_params = request.query_params

        page_no = query_params.get('page', 1)
        page_size = query_params.get("page_size", 10)

        profile_manager = ProfileService(page=page_no, page_size=page_size)
        response = profile_manager.search_profile(query)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)
