import flet as ft
from gui.gui import gui


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    page.title = "Handwriting Dec."
    page.set_allowed_device_orientations(ft.Orientation.PORTRAIT)
    page.update()

    await gui(page)
 


if __name__ == "__main__":
    ft.run(main)
