import yagmail
import flet as ft
from environs import Env

class SendError:
    def __init__(self, page: ft.Page, email: str):
        env = Env()
        env.read_env(".env")

        self.page=page
        self.email_to=email
        self.smtp_key=env("SMTP_KEY")

    async def dialog_saful(self, error: bool):
        self.page.pop_dialog()
        dialog_end = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    icon=ft.Icons.CHECK_ROUNDED,
                                    size=140,
                                    color=ft.Colors.GREEN,
                                    visible=False if error else True
                                ),
                                ft.Icon(
                                    icon=ft.Icons.CLOSE_ROUNDED,
                                    size=140,
                                    color=ft.Colors.RED,
                                    visible=error
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            controls=ft.Text(
                                value="Мы успешно отправили отчет об ошибке на почту: rycode.support@gmail.com" if not error else "Не удалось отправить отчет об ошибке, проверьте подключение к интернету",
                                opacity=0.8,
                                overflow=ft.TextOverflow.CLIP,
                                expand=True
                            ),
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                ),
                alignment=ft.Alignment.CENTER,
                height=200
            ),
            actions=[
                ft.TextButton(
                    content="Закрыть",
                    on_click=lambda e: self.page.pop_dialog()
                )
            ]
        )

        self.page.show_dialog(dialog_end)

    async def send_to_email(self, your_email, subject, content_msg):

        try:
            ygm = yagmail.AsyncSMTP(self.email_to, self.smtp_key)

            await ygm.send(self.email_to, subject, f"{content_msg} \n\nот: {your_email}")
            await self.dialog_saful(False)
        except Exception:
            await self.dialog_saful(True)

    async def send_window(self, title: str, content: str):

        async def send(e):
            await self.send_to_email(your_email.value, subject.value, content_msg.value)
            print("отправить")

        sender_window = ft.AlertDialog(
            modal=True,
            title="Отправить ошибку",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        your_email := ft.TextField(
                            label="Ваш email"
                        ),
                        subject := ft.TextField(
                            label="Заголовок",
                            value=title
                        ),
                        content_msg := ft.TextField(
                            label="Сообщение",
                            value=content,
                            multiline=True,
                            min_lines=1,
                            max_lines=2
                        )
                    ],
                ),
                height=200,
                alignment=ft.Alignment.CENTER
            ),
            actions=[
                ft.TextButton(
                    content="Отправить",
                    on_click=send
                ),
                ft.TextButton(
                    content="Отмена",
                    on_click=lambda e: self.page.pop_dialog() 
                )
            ]
        )


        self.page.show_dialog(sender_window)
