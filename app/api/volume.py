from fastapi import APIRouter

from app.services.volume_loader import (
    load_dicom_series,
    get_volume_info
)

router = APIRouter()


@router.get("/volume-test")
def volume_test():

    volume = load_dicom_series("uploads")

    return get_volume_info(volume)