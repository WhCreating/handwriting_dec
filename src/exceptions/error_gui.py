import flet as ft
from back.send_error import SendError

# Окно ошибки
async def show_error(text: str, page: ft.Page):
    async def send_error_func(e):
        error_window_send = SendError(page, "rycode.support@gmail.com")

        await error_window_send.send_window(error_window.title.value, error_window.content.value)


    error_window = ft.AlertDialog(
        title=ft.Text("Ошибка"),
        modal=True,
        content=ft.Text(str(text)),
        alignment=ft.Alignment.CENTER,
        title_padding=ft.Padding.all(25),
        actions=[
            ft.TextButton(
                content="Отправить ошибку",
                on_click=send_error_func
            ),
            ft.TextButton(
                content="Закрыть",
                on_click=lambda e: page.pop_dialog()
            )
        ]
    )

    page.show_dialog(error_window)

