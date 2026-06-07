import flet as ft
from gui.gui import gui


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    page.title = "Handwriting Dec."
    
    await gui(page)
 


if __name__ == "__main__":
    ft.run(main)
