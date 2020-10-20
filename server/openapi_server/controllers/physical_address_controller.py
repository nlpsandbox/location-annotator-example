import connexion
import six

from openapi_server.models.note import Note  # noqa: E501
from openapi_server.models.physical_address_annotation import PhysicalAddressAnnotation  # noqa: E501
from openapi_server import util


def physical_addresses_read_all(note=None):  # noqa: E501
    """Get all physical address annotations

    Returns the physical address annotations # noqa: E501

    :param note: 
    :type note: list | bytes

    :rtype: List[PhysicalAddressAnnotation]
    """
    if connexion.request.is_json:
        note = [Note.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
