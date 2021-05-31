from PIL import Image, ImageFont, ImageDraw
from ..models import Job


def render_job(job: Job):
    img = Image.new("RGB", (1200, 600), "#FFFFFFFF")
    # img = Image.new('RGB', (1200, 600), "#eceff4")
    draw = ImageDraw.Draw(img, "RGBA")
    font_header = ImageFont.truetype("fonts/Inter-SemiBold.ttf", 100, 0)

    padding = 80

    draw.text(
        (padding, padding), job.command, font=font_header, fill="#2e3440"
    )

    draw.rectangle([0, 600 - 48, 1200, 600], fill="#88c0d0")

    # OS logo
    # TODO: move to function and cache
    os_logo = Image.open(f"images/os/{job.os}.png")  # TODO os agnostic
    os_logo.thumbnail((250, 250))
    img.paste(os_logo, (1200 - 250 - padding, padding))

    # username and host
    font = ImageFont.truetype("fonts/Inter-Regular.ttf", 35, 0)
    draw.text(
        ((1200 - padding - (250 / 2)), padding + 250 + 24),
        job.prompt,
        font=font,
        fill="#2e3440",
        anchor="mt",
    )

    # time spend
    draw.text(
        (1200 - padding - (250 / 2), 300 + 150),
        f"{job.seconds}s",
        font=font,
        fill="#2e3440",
        anchor="mt",
    )

    # success icon
    success_size = 64
    success_icon = Image.open("images/icons/done.png")
    success_icon.thumbnail((success_size, success_size))
    img.paste(success_icon, (padding, 300), success_icon)

    # Success text
    success_font = ImageFont.truetype("fonts/Inter-Regular.ttf", 64, 0)
    draw.text(
        (padding + success_size + 24, 300 - 8),
        "Success",
        font=success_font,
        fill="#2e3440",
    )
    draw.text((padding, 380), "exit code: 0", font=font, fill="#2e3440")

    return img
