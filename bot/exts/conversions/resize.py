from bot.bot import Bot
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from bot.utils.images import download_image, image_to_file

Size = tuple[int, int]


class Resize(commands.Cog):
    """Commands for resizing images"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _new_size(
        size: Size,
        width: int = None,
        height: int = None,
        scale: int = None,
    ) -> Size:
        """Gets a new image size, given the new width, height or scale compared to the old image."""
        if width == height == scale == None:
            raise ValueError(
                "At least one of the arguments `width`, `height` and `scale` must be provided."
            )
        if (
            (width is not None and width <= 0)
            or (height is not None and height == 0)
            or (scale is not None and scale == 0)
        ):
            raise ValueError("Width, height and scale must be greater than 0.")
        if scale and (width or height):
            raise ValueError(
                "When `scale` is provided, please don't pass `width` or `height`."
            )

        if scale:
            return (size[0] * scale, size[1] * scale)
        if width and height:
            return (width, height)
        if width:
            f_scale = width / size[0]
        if height:
            f_scale = height / size[1]
        return (int(size[0] * f_scale), int(size[1] * f_scale))  # type: ignore

    @commands.slash_command()
    async def resize(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
        width: int = None,
        height: int = None,
        scale: int = None,
    ) -> None:
        """Resizes an image."""
        image = await download_image(image_url)
        try:
            size = Resize._new_size(image.size, width, height, scale)
        except ValueError as e:
            raise commands.BadArgument(str(e))

        image = image.resize(size)
        await inter.response.send_message(file=image_to_file(image))


def setup(bot: Bot) -> None:
    """Loads the Resize cog."""
    bot.add_cog(Resize(bot))
