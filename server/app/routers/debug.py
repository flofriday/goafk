from ..database import insert_job, insert_user
from ..models import JobIn, UserIn
from fastapi import APIRouter


router = APIRouter(
    prefix="/debug",
    tags=["debug", "NOT-PRODUCTIOON"],
)

# TODO: write a middleware that disables the debug routes in productin


@router.get("/add/user", status_code=201)
async def add_user():
    user = UserIn(platform="telegram", user_name="flofriday", token="super")
    await insert_user(user)


@router.get("/add/job", status_code=201)
async def add_job():
    job = JobIn(
        command="brew upgrade",
        exit_code=0,
        os="darwin",
        prompt="flo@MBP",
        seconds=3.21,
        user_id=1,
    )
    await insert_job(job)
