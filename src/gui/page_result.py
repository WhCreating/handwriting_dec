import flet as ft
from back.result_get import ModelEdgeImpulse
import threading
import requests

# Результат от модели
async def page_result(page: ft.Page, image: str):

    def apply_result():
        try :
            model = ModelEdgeImpulse()
            samp = model.upload_image_base64(image)
            model.classify(samp)


            prgrs_bar.visible = False
            area.visible = True
            area.content.value = model.get_result()

            page.update()
        except Exception:
            prgrs_bar.visible = False
            area.visible = True
            area.content.value = "Ошибка подключения"

            page.update()

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
                        prgrs_bar := ft.ProgressRing(visible=False),
                        area := ft.SelectionArea(
                            ft.Text(
                                size=20
                            ),
                            visible=False
                        )
                    ]
                ),
                expand=True
            )
        )
    )

    prgrs_bar.visible = True
    page.update()


    threading.Thread(target=apply_result, daemon=True).start()
    
