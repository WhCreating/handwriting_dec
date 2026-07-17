import flet as ft
from back.result_get import ModelEdgeImpulse
import threading
from exceptions.error_gui import show_error
import requests
import asyncio

# Результат от модели
async def page_result(page: ft.Page, image: str):

    async def apply_result():
        try :
            
            def blocking():
                model = ModelEdgeImpulse()
                samp = model.upload_image_base64(image)
                model.classify(samp)
                return model.get_result()

            results = await asyncio.to_thread(blocking)


            prgrs_bar.visible = False
            area.visible = True
            area.content.value = result

            page.update()
        except Exception as ex:
            prgrs_bar.visible = False
            area.visible = True
            area.content.value = "Ошибка подключения"
            await show_error(str(ex), page)

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


    #threading.Thread(target=apply_result, daemon=True).start()
    await apply_result()
    
