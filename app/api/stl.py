from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/stl/{scan_id}")
def download_stl(scan_id: int):

    stl_path = f"results/scan_{scan_id}.stl"

    return FileResponse(
        path=stl_path,
        media_type="application/octet-stream",
        filename=f"scan_{scan_id}.stl"
    )