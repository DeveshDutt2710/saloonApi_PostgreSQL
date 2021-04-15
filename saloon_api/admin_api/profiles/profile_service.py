from django.db.models import Q
from utility.pagination_utilities import PaginationUtilities
from .serializers import ProfileSerializer
from ..serializers import BsonSerializer
from .models import Profiles, Contact, Address, PrivacySettings

class ProfileService():
    profile_id = None
    page = 1
    page_size = 10

    def __init__(self, profile_id: str = None, page: int = 1, page_size: int = 10):
        self.set_profile_id(profile_id)
        self.page = page
        self.page_size = page_size

    def set_profile_id(self, profile_id):
        self.profile_id = profile_id

    def get_profile_id(self):
        return self.profile_id
     
    def _create_user_contact_details(self, contact_details, profile):
        return Contact.create_contact(profile = profile, **contact_details)

    def _create_user_address_details(self, address_details):
        return Address.create_address(address_details)

    def _create_user_privacy_settings(self, privacy_settings):
        return PrivacySettings.create_privacy_setting(privacy_settings)


    def _save_profile(self, profile):
        saved_profile = profile.save()
        return saved_profile
        

    def _update_profile_details(self, profile, data):
        profile.name = data['name']
        profile.account = data['account']
        profile.profile_type = data['profile_type']
        profile.vendor_description = data['vendor_description']
        profile.dob = data['dob']
        profile.gender = data['gender']
        profile.image = data['image']
        profile.last_app_activity = data['last_app_activity']
        profile.is_admin_verified = data['is_admin_verified']

        self._save_profile(profile)

    def fetch_all_profiles(self) -> dict:
        profiles = Profiles.objects.all()  # .filter(is_deleted=False)

        profiles = PaginationUtilities.paginate_results(profiles,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        profile_data = ProfileSerializer(profiles, many=True)

        response = {
            'success': True,
            'profiles': profile_data.data
        }

        return response

    def fetch_profile_by_id(self) -> dict:
        profiles = Profiles.get_object_or_raise_exception(self.get_profile_id())

        profile_data = ProfileSerializer(profiles)

        response = {
            'success': True,
            'profile': profile_data.data
        }

        return response

    def create_profile(self, data) -> dict:
        saved_profile = self._save_profile(Profiles(**data))

        
        if 'contact' in data:
            contacts = data.pop('contact')
            print(type(contacts))
            print("\nCONTACTS : "+(str)(contacts))
            for contact in contacts:
                contact = self._create_user_contact_details(contact, profile = saved_profile)
            

        # if 'address' in data:
        #     address = self._create_user_address_details(data.pop('address'))
        #     data['address'] = address

        # if 'privacy_setting' in data:
        #     privacy_setting = self._create_user_privacy_settings(data.pop('privacy_setting'))
        #     data['privacy_setting'] = privacy_setting

        
        response = {
            'success': True,
            'profile_id' : saved_profile.id
        }

        return response

    def update_profile(self, data) -> dict:

        profile = Profiles.get_object_or_raise_exception(self.get_profile_id())

        if 'contact' in data:
            profile.contact.update_contact(data.pop('contact'))

        if 'address' in data:
            profile.address.update_address(data.pop('address'))

        if 'privacy_setting' in data:
            profile.privacy_setting.update_privacy_setting(data.pop('privacy_setting'))

        self._update_profile_details(profile, data)

        response = {
            'success': True,
        }

        return response

    def delete_profile(self) -> dict:
        profile = Profiles.get_object_or_raise_exception(self.get_profile_id())

        profile.delete_profile()

        response = {
            'success': True,
        }

        return response

    def search_profile(self, query):

        profiles = Profiles.objects.filter(Q(name__icontains=query) |
                                           Q(contact__email__icontains=query) |
                                           Q(contact__phone__icontains=query))

        profiles = PaginationUtilities.paginate_results(profiles,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        data = ProfileSerializer(profiles, many=True).data

        response = {
            'success': True,
            'profiles': data
        }

        return response
