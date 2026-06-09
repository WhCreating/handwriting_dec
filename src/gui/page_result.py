import flet as ft
from back.result_get import ModelEdgeImpulse

# Результат от модели
async def page_result(page: ft.Page, image: str):

    model = ModelEdgeImpulse()
    samp = model.upload_image_base64(image)
    model.classify(samp)

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
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                    on_click=back
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.SelectionArea(
                            ft.Text(
                                value=model.get_result(),
                                size=20
                            )
                        )
                    ]
                ),
                expand=True
            )
        )
    )