import flet as ft
import flet_camera as fc
import flet_ads as fta
import asyncio
from dataclasses import dataclass, field
from base64 import b64encode
from gui.page_result import page_result
from exceptions.error_gui import show_error

# Тестовые ключи для рекламы
ids = {
    ft.PagePlatform.ANDROID: {
        "banner": "ca-app-pub-3940256099942544/9214589741",
        "interstitial": "ca-app-pub-3940256099942544/1033173712",
    },
    ft.PagePlatform.IOS: {
        "banner": "ca-app-pub-3940256099942544/2435281174",
        "interstitial": "ca-app-pub-3940256099942544/3986624511",
    },
}

async def gui(page: ft.Page):

    # Рекламный баннер
    def get_new_banner_ad() -> fta.BannerAd:
        return fta.BannerAd(
            unit_id=ids[page.platform]["banner"],
            width=320,
            height=50,
            on_click=lambda e: print("BannerAd clicked"),
            on_load=lambda e: print("BannerAd loaded"),
            on_error=lambda e: print("BannerAd error", e.data),
            on_open=lambda e: print("BannerAd opened"),
            on_close=lambda e: print("BannerAd closed"),
            on_impression=lambda e: print("BannerAd impression"),
            on_will_dismiss=lambda e: print("BannerAd will dismiss"),
        )

    # Функция с инициализацией камеры
    async def init_back_camera():
        try:
            # Получаем список доступных камер
            cameras = await camera.get_available_cameras()

            # Сохраняем значение задней камеры
            back_cam = next(
                (c for c in cameras if c.lens_direction == fc.CameraLensDirection.BACK),
                None,
            )
            
            raise Exception("ошибка1")

            if back_cam:
                # Инициализируем камеру
                await camera.initialize(
                    description=back_cam,
                    resolution_preset=fc.ResolutionPreset.HIGH,
                    enable_audio=False,  # при необходимости включите
                )
                print(f"✅ Задняя камера: {back_cam.name}")
                button_camera.disabled = False
                page.update()
            else:
                await show_error("❌ Задняя камера не найдена", page)
                page.update()
        except Exception as e:
            await show_error(f"⚠️ Ошибка: {e}", page)
            page.update()

    # сделать фото
    async def do_picture(e):
        try :
            res = await camera.take_picture()
            await preview_picture(b64encode(res).decode(encoding="utf-8"))
            
        except Exception as e:
            await show_error(str(e), page)
    
    # Показать фото
    async def preview_picture(image: str):
        # Сменить страницу
        async def change_page(e):
            page.controls.clear()
            page.pop_dialog()
            await page_result(page, image)
        


        try :
            preview_image = ft.AlertDialog(
                content=ft.Image(
                    src=image,
                    border_radius=20
                ),
                modal=True,
                actions=[
                    ft.TextButton("Продолжить", on_click=change_page),
                    ft.TextButton("переснять", on_click=lambda e: page.pop_dialog()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )

            page.show_dialog(preview_image)
        except Exception as e:
            await show_error(str(e), page)


    # Кнопка камеры
    button_camera = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT_ROUNDED,
        icon_size=50,
        disabled=True,
        on_click=do_picture
    )

    # Объект с камерой
    camera = fc.Camera(
        expand=True,
        preview_enabled=True,
        content=ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.CENTER_FOCUS_STRONG,
                color=ft.Colors.WHITE_70,
                size=48,
            ),
        )
    )
    


    page.add(
        ft.SafeArea(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=camera,
                            expand=True,
                            height=620,
                            alignment=ft.Alignment.CENTER,
                            border_radius=20

                        ),
                        ft.Row(
                            controls=[
                                button_camera
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            )
        ),
    )

    await init_back_camera()