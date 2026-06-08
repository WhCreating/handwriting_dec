import flet as ft

# Результат от модели
async def page_result(page: ft.Page, image: str):

    # Назад
    async def back(e):
        from gui.gui import gui
        page.controls.clear()
        await gui(page)


    page.add(
        ft.SafeArea(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                back := ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                    on_click=back
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.SelectionArea(
                            ft.Text(
                                value="Привет, тут будет результат",
                                text_align=ft.TextAlign.CENTER
                            )
                        )
                    ]
                ),
                expand=True
            )
        )
    )