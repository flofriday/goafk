from app.render.job import render_job
import io
from fastapi.params import Depends
from starlette.responses import HTMLResponse, StreamingResponse
from ..database import insert_job, select_job_by_uuid, select_user_by_token
from ..models import Job, JobIn
from fastapi import APIRouter, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

# from ..config import Settings

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")

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


@router.get("/{job_uuid}.json")
async def read_job(job_uuid: str, response_model=Job):
    job = await select_job_by_uuid(job_uuid)
    if job is None:
        raise HTTPException(status_code=404, detail="Job does not exist")

    # TODO: check that we don't leak anything here
    return job


# TODO id like it to be /{job_id}.png
@router.get("/{job_uuid}.png")
async def display_job(job_uuid: str):
    job = await select_job_by_uuid(job_uuid)
    if job is None:
        # TODO add job not found image
        raise HTTPException(status_code=404, detail="Job does not exist")

    img = render_job(job)

    bytes = io.BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)
    return StreamingResponse(bytes, media_type="image/png")


@router.get("/{job_uuid}")
async def document_job(
    request: Request, job_uuid: str, response_class=HTMLResponse
):
    job = await select_job_by_uuid(job_uuid)
    if job is None:
        # TODO return not found template
        raise HTTPException(status_code=404, detail="Job does not exist")

    # render the data
    return templates.TemplateResponse(
        "job.html", {"request": request, "job": job}
    )


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
