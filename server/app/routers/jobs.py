from app.render.job import render_job
import io
from fastapi.params import Depends
from starlette.responses import StreamingResponse
from ..database import insert_job, select_job_by_id, select_user_by_token
from ..models import Job, JobIn
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# from ..config import Settings

security = HTTPBasic()

router = APIRouter(
    prefix="/jobs",
    tags=["cli", "jobs"],
)


# TODO: this doesn't really belong here
# TODO: do no leak the platform and id (privacy)
@router.get("/me", status_code=200)
async def read_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
):
    token = credentials.username
    user = await select_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return user


@router.get("/{job_id}")
async def read_job(job_id: int, response_model=Job):
    job = await select_job_by_id(job_id)
    return job


# TODO id like it to be /{job_id}.png
@router.get("/{job_id}/img")
async def display_job(job_id: int):
    job = await select_job_by_id(job_id)
    if job is None:
        # TODO add job not found image
        raise HTTPException(status_code=404, detail="Job does not exist")

    img = render_job(job)

    bytes = io.BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)
    return StreamingResponse(bytes, media_type="image/png")


@router.post("/")
async def create_job(
    job: JobIn,
    credentials: HTTPBasicCredentials = Depends(security),
    response_model=Job,
):
    # set the correct user
    token = credentials.username
    user = await select_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid Token")

    # create the job
    last_record_id = await insert_job(job)

    # TODO: notify user
    return {**job.dict(), "id": last_record_id}
