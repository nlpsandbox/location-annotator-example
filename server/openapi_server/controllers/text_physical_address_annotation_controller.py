import connexion
import pandas as pd
import re

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server.models.text_physical_address_annotation_request import TextPhysicalAddressAnnotationRequest  # noqa: E501
from openapi_server.models.text_physical_address_annotation import TextPhysicalAddressAnnotation  # noqa: E501
from openapi_server.models.text_physical_address_annotations import TextPhysicalAddressAnnotations  # noqa: E501


class Data:
    def __init__(self):
        df = pd.read_csv("data/street_list.csv")
        self._streets = df['Street'].str.lower().unique().tolist()

        df = pd.read_csv("data/city_list.csv")
        self._cities = df['City'].str.lower().unique().tolist()

        df = pd.read_csv("data/state_list.csv")
        self._states = df['State'].str.lower().unique().tolist()

        df = pd.read_csv("data/country_list.csv")
        self._countries = df['Name'].str.lower().unique().tolist()

        df = pd.read_csv("data/other_list.csv")
        self._others = df['Other'].str.lower().unique().tolist()


data = Data()


def create_text_physical_address_annotations(note=None):  # noqa: E501
    """Annotate physical addresses in a clinical note

    Return the physical addresse annotations found in a clinical note # noqa: E501

    :param note:
    :type note: dict | bytes

    :rtype: TextPhysicalAddressAnnotations
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextPhysicalAddressAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            note = annotation_request._note
            annotations = []

            for street in data._streets:
                matches = re.finditer(
                    r'\b({})\b'.format(street), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'street')

            for city in data._cities:
                matches = re.finditer(
                    r'\b({})\b'.format(city), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'city')

            for state in data._states:
                matches = re.finditer(
                    r'\b({})\b'.format(state), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'state')

            for country in data._countries:
                matches = re.finditer(
                    r'\b({})\b'.format(country), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'country')

            for other in data._others:
                matches = re.finditer(
                    r'\b({})\b'.format(other), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'other')

            res = TextPhysicalAddressAnnotations(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))

    return res, status


def add_annotations(annotations, matches, address_type):
    """
    Converts matches to TextPhysicalAddressAnnotation objects and adds them
    to the annotations array specified.
    """
    for match in matches:
        annotations.append(
            TextPhysicalAddressAnnotation(
                start=match.start(),
                length=len(match[0]),
                text=match[0],
                address_type=address_type
            ))
