from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


async def create_certificate(full_name: str):
    img = Image.open("certificate.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf", 80)
    date_font = ImageFont.truetype("/usr/share/fonts/truetype/montserrat/Montserrat-Regular.ttf", 40)
    date_text = datetime.today().strftime("%d - %B %Y")
    draw.text((650, 750), full_name, font=font, fill=(32, 45, 76))
    draw.text((1000, 1480), date_text, font=date_font, fill=(32, 45, 76))
    img.save("output.png")
    img.show()
