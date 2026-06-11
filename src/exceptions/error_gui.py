import flet as ft

# Окно ошибки
async def show_error(text: str, page: ft.Page):
    error_window = ft.AlertDialog(
        title=ft.Text("Ошибка"),
        content=ft.Text(str(text)),
        alignment=ft.Alignment.CENTER,
        title_padding=ft.Padding.all(25),
    )

    page.show_dialog(error_window)

