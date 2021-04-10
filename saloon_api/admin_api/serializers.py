import json
from bson import json_util
from .profiles.models import Profiles
from .profiles.serializers import BasicProfileSerializer


class BsonSerializer:

    @staticmethod
    def _fetch_basic_profile_details(profile_id):
        profile = Profiles.get_object_or_raise_exception(profile_id)
        return BasicProfileSerializer(profile).data

    @staticmethod
    def serialize_search_results(results, serialize_extra_data=False):

        data = []

        for result in results:
            result_obj = json.loads(json_util.dumps(result))

            if '_id' in result_obj:
                result_obj['_id'] = result_obj['_id']['$oid']

            if serialize_extra_data:

                if "vendorId" in result_obj:
                    result_obj['vendor'] = BsonSerializer._fetch_basic_profile_details(result_obj['vendorId'])
                    del result_obj['vendorId']

                if "customerId" in result_obj:
                    result_obj['customer'] = BsonSerializer._fetch_basic_profile_details(result_obj['customerId'])
                    del result_obj['customerId']


            data.append(result_obj)

        return data
