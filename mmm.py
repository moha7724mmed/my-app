import flet as ft
from db import print_all_user_card,count_cards,delet_usercard,count_available_cards
import os
from datetime import datetime

def mmmm(page:ft.Page):
    def open_sheet(e=None):
        bottom_sheet.open = True
        page.update()

    def close_sheet():
        bottom_sheet.open = False
        page.update()


    def go_home(e):
        page.clean() 
        page.appbar = None
         # مهم جدًا
        from main import main
        main(page)             # يرجع للرئيسية


        # ================= زر جميل =================
    def service_button(text, color, on_click):
        return ft.Card(
            content=ft.Container(
                height=60,
                alignment=ft.alignment.center,
                bgcolor=color,
                border_radius=15,
                ink=True,
                on_click=lambda e: button_clicked(e, text),
                content=ft.Text(
                    text,
                    size=14,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER
                ),
            )
        )

    def copy_card(e, text):
        page.set_clipboard(text)
        page.snack_bar = ft.SnackBar(
            ft.Text("✅ تم نسخ الكرت")
        )
        page.snack_bar.open = True
        page.update()

    def card_item(card_number):
        return ft.Container(
            padding=10,
            border_radius=12,
            bgcolor="#F5F5F5",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(card_number, size=16, weight="bold"),

                    ft.IconButton(
                        icon=ft.icons.COPY,
                        tooltip="نسخ",
                        on_click=lambda e: copy_card(e, card_number)
                    )
                ]
            )
        )

    # ================= وظائف الأزرار =================

    def btn1(e,ty_user):
        cards = print_all_user_card(ty_user) or []

        sheet_content.controls.clear()

        sheet_content.controls.append(
            ft.Text("📌 الكروت", size=18, weight="bold")
        )

        for c in cards:
            sheet_content.controls.append(
                card_item(c[1])
            )

        bottom_sheet.open = True
        page.update()
    def close_banner(e):
        page.banner.open = False
        page.update()
    def show_banner(e,typ):
        total = count_available_cards(typ)  # 👈 تعريف المتغير أولًا

        page.banner = ft.Banner(
            content=ft.Text(f"عدد الكروت: {total}"),
            actions=[
                ft.TextButton("إغلاق", on_click=close_banner)
            ]
        )

        page.banner.open = True
        page.update()




    def button_clicked(e, name):
        print("تم الضغط على:", name)

        if name == "1000 عرض كروت":
            show_banner(e,"User_card1000")
            btn1(e,"User_card1000")

        elif name == "500 عرض كروت":
            show_banner(e,"User_card500")
            btn1(e,"User_card500")

        elif name == "300 عرض كروت":
            show_banner(e,"User_card300")
            btn1(e,"User_card300")

        elif name == "200 عرض كروت":
            show_banner(e,"User_card200")
            btn1(e,"User_card200")
        elif name == "dellet":
            listp=['debt_sales','cash_sales','User_card200','User_card300','User_card500','User_card1000','user_cards','debtor_sales']
            for i in listp:
                delet_usercard(i)
            


    def cou(e):
        total =count_cards("User_card1000")
        print("عدد الكروت:", total)
    def dell(e):
        delet_usercard("User_card1000")
    def btn(e):
        print("klkl")




    # ================= AppBar =================
    page.appbar = ft.AppBar(
        title=ft.Text("📊 لوحة التحكم"),
        bgcolor="#3F51B5",
        center_title=True,
        leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=go_home)
    )



    # ================= شبكة 12 زر =================
    buttons = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        controls=[
            service_button("1000 عرض كروت", "#3F51B5",button_clicked),
            service_button("500 عرض كروت", "#3F51B5", cou),
            service_button("300 عرض كروت", "#3F51B5", dell),
            service_button("200 عرض كروت", "#3F51B5",button_clicked ),

            service_button("dellet", "#E0F2F1", button_clicked),
            service_button("طباعة", "#FFFDE7", btn),
            service_button("تقارير", "#E1F5FE", btn),
            service_button("بحث", "#F3E5F5", btn),

            service_button("الإعدادات", "#ECEFF1", btn),
            service_button("نسخة احتياطية", "#E8EAF6", btn),
            service_button("إشعارات", "#FFF8E1", btn),
            service_button("مساعدة", "#E0F7FA", btn),
        ]
    )

    sheet_content = ft.Column(
    scroll=ft.ScrollMode.AUTO,
    controls=[]
)

    bottom_sheet = ft.BottomSheet(
        show_drag_handle=True,
        content=ft.Container(
            height=350,
            padding=20,
            content=sheet_content
        ),
        open=False
    )


    page.overlay.append(bottom_sheet)




        # ================= إضافة للصفحة =================
    page.add(
        ft.Column(
            expand=True,
            controls=[
                
                ft.Container(height=5),
                buttons
            ]
        )
    )




    # زر جميل
    """def service_button(icon, text, color, on_click):
        return ft.Container(
            width=150,
            height=120,
            bgcolor=color,
            border_radius=20,
            padding=10,
            ink=True,
            on_click=on_click,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, size=40, color=ft.colors.BLACK87),
                    ft.Text(text, size=14, weight=ft.FontWeight.BOLD)
                ]
            )
        )

    # وظائف الأزرار
    def btn1(e): print("زر 1")
    def btn2(e): print("زر 2")
    def btn3(e): print("زر 3")
    def btn4(e): print("زر 4")

    # رجوع
    def go_home(e):
        page.clean()
        from main import main
        main(page)

    # AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("📊 قائمة المدينين"),
        bgcolor="#3F51B5",
        center_title=True,
        leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=go_home)
    )

    # مجموعة الأزرار
    buttons = ft.GridView(
        expand=True,
        runs_count=2,
        spacing=10,
        run_spacing=10,
        controls=[
            service_button(ft.icons.CREDIT_CARD, "كبينه السداد", "#E3F2FD", btn1),
            service_button(ft.icons.PEOPLE, "المدينين", "#E8F5E9", btn2),
            service_button(ft.icons.PRINT, "طباعة", "#FFF3E0", btn3),
            service_button(ft.icons.SETTINGS, "الإعدادات", "#FCE4EC", btn4),
        ]
    )



    # إضافة للصفحة
    page.add(
        ft.Text("مرحبا بك في صفحة كبينة السداد", size=20),
        buttons
    )"""
