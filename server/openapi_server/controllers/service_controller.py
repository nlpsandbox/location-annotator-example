from openapi_server.models.service import Service  # noqa: E501


def service():  # noqa: E501
    """Get service information

    Get information about the service # noqa: E501


    :rtype: Service
    """
    service = Service(
        name="physical-address-annotator-example",
        version="0.2.1",
        license="apache-2.0",
        repository="github:nlpsandbox/physical-address-annotator-example",
        description="An example implementation of the NLP Sandbox " +
                    "Physical Address Annotator API",
        author="The NLP Sandbox Team",
        author_email="thomas.schaffter@sagebionetworks.org",
        url="https://github.com/nlpsandbox/physical-address-annotator-example"
    )

    return service, 200
