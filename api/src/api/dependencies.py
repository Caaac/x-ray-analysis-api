from typing import Annotated
from fastapi import Depends

from src.services.request import RequestService
from src.repositories.request import XRayRequestRepository

from src.services.brocker import BrokerService
from src.rabbitmq.producer import producer_connection


def get_request_service():
    return RequestService(XRayRequestRepository)


def get_broker_producer():
    return BrokerService(producer_connection)


request_service = Annotated[RequestService, Depends(get_request_service)]
producer_dep = Annotated[BrokerService, Depends(get_broker_producer)]
