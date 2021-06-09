from functools import lru_cache
from PIL import Image, ImageFont, ImageDraw
from ..models import Job


font_header = ImageFont.truetype("fonts/Inter-SemiBold.ttf", 100, 0)
font = ImageFont.truetype("fonts/Inter-Regular.ttf", 35, 0)
success_font = ImageFont.truetype("fonts/Inter-Regular.ttf", 64, 0)


success_icon = Image.open("images/icons/done.png")

text_color = "#2e3440"
success_color = "#88c0d0"
failure_color = "#d08770"


# TODO: add error handling if a funny user uses a exotic OS or messes wiht the
# service.
@lru_cache()
def load_os_logo(os: str) -> Image:
    os_logo = Image.open(f"images/os/{os}.png")  # TODO os agnostic
    os_logo.thumbnail((250, 250))
    return os_logo


def render_job(job: Job):
    img = Image.new("RGB", (1200, 600), "#FFFFFFFF")
    draw = ImageDraw.Draw(img, "RGBA")

    padding = 80

    draw.text(
        (padding, padding), job.command, font=font_header, fill=text_color
    )

    # Draw the bottom color bar
    rect_color = success_color
    if job.exit_code != 0:
        rect_color = failure_color
    draw.rectangle([0, 600 - 48, 1200, 600], fill=rect_color)

    # OS logo
    os_logo = load_os_logo(job.os)
    img.paste(os_logo, (1200 - 250 - padding, padding))

    # username and host
    draw.text(
        ((1200 - padding - (250 / 2)), padding + 250 + 24),
        job.prompt,
        font=font,
        fill=text_color,
        anchor="mt",
    )

    # time spend
    draw.text(
        (1200 - padding - (250 / 2), 300 + 150),
        f"{job.seconds}s",
        font=font,
        fill=text_color,
        anchor="mt",
    )

    # success icon
    success_size = 64
    success_icon.thumbnail((success_size, success_size))
    img.paste(success_icon, (padding, 300), success_icon)

    # Success text
    draw.text(
        (padding + success_size + 24, 300 - 8),
        "Success",
        font=success_font,
        fill=text_color,
    )
    draw.text((padding, 380), "exit code: 0", font=font, fill=text_color)

    return img
