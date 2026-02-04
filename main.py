import flet as ft
import pandas as pd
from PyPDF2 import PdfReader
from datetime import datetime
from db import add_card_to_table,print_all_user_card,count_cards,get_total,count_available_cards
import os ,re
import shutil
import os 
from upload_pdf import sales_summary_card
from managecard import manage
from datetime import datetime
import shutil
import db
def main(page: ft.Page):
    
    page.window_width = 360
    page.window_height = 640
    page.window_resizable = False
    db.init_db()
    error_text = ft.Text(color=ft.colors.RED)
    page.rtl = True
    cards_count = 1
    page.title = "الرئيسية"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    selected_amount = None
    uploaded_pdf_path = None
    # بيانات مدينين (كأنها من قاعدة بيانات)



    # بيانات نقد (كأنها من Excel)


    PRIMARY = "#5E4B87"
    card_buttons_row = ft.Row(
    spacing=10,
    alignment=ft.MainAxisAlignment.CENTER
    )
    
    def route_change(route):
        page.views.clear()

        page.views.append(ft.View("/", controls=[main(page)]))

        if page.route == "/manage":
            page.views.append(ft.View("/manage", controls=[manage_page(page)]))

        if page.route == "/mmmm":
            page.views.append(ft.View("/mmmm", controls=[mmmm(page)]))

        page.update()



    def card_count_btn(value):
        def select_count(e):
            nonlocal cards_count
            cards_count = value
            update_card_buttons()
            page.update()

        return ft.Container(
            content=ft.Text(str(value), size=14, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            width=44,
            height=44,
            border_radius=22,
            bgcolor=PRIMARY if cards_count == value else ft.colors.GREY_200,
            on_click=select_count,
        )

    def update_card_buttons():
        card_buttons_row.controls = [
            card_count_btn(1),
            card_count_btn(2),
            card_count_btn(3),
        ]
    update_card_buttons()


        # ---------- Dialog State ----------
    selected_category = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    def category_btn(value):
        return ft.ElevatedButton(
            value,
            width=200,
            height=44,
            on_click=lambda e: select_category(value),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=22),
                bgcolor=ft.colors.GREY_100,
                color=PRIMARY,
                elevation=0,
            ),
        )


    def on_confirm(e):
        sad_dialog.open = False
        page.snack_bar = ft.SnackBar(ft.Text("تم المتابعة 👍"))
        page.snack_bar.open = True
        page.update()

    def on_cancel(e):
        sad_dialog.open = False
        page.update()


 
    sad_dialog = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=20),

        title=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="face.gif",   # اسم الملف
                    width=120,
                    height=120,
                    repeat=True,
                ),
            ],
        ),

        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Text(
                    "عذرًا، لا توجد كروت كافية لإتمام العملية",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),

            ],
        ),

        actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        actions=[
    
            ft.OutlinedButton(
                "إلغاء",
                on_click=on_cancel,
            ),
        ],
    )
    page.dialog = sad_dialog

    actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    actions=[
        ft.ElevatedButton(
            "متابعة",
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            on_click=on_confirm,
        ),
        ft.OutlinedButton(
            "إلغاء",
            on_click=on_cancel,
        ),
    ],


    





        

    def close_dialog(dialog):
        dialog.open = False
        page.update()
    def copy_card(code):
        page.set_clipboard(code)
        page.snack_bar = ft.SnackBar(ft.Text("تم نسخ الكرت"))
        page.snack_bar.open = True
        page.update()
    def wifi_card_item(code):
        return ft.Container(
            padding=12,
            border_radius=14,
            bgcolor=ft.colors.GREY_100,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(code, size=14, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        icon=ft.icons.CONTENT_COPY,
                        tooltip="نسخ",
                        on_click=lambda e: copy_card(code),
                  ),
                ],
                        ),
        )
    def close_all_dialogs():
        for dlg in [category_dialog, payment_dialog, sad_dialog]:
            dlg.open = False
        page.update()


    def open_wifi_dialog(e):
        page.dialog = category_dialog
        category_dialog.open = True
        page.update()


    def select_category(value):
        category_dialog.open = False
        selected_category.value =value
       
        payment_dialog.open = True
        page.update()

    """def open_wifi_dialog(e):
        close_all_dialogs()
        category_dialog.open = True
        page.update()"""



    def finish_payment(method):
        global type_user
        type_user = method

        payment_dialog.open = False
        page.update()
        debt_dialog.open = True
        page.update()

    debtor_input = ft.TextField(
    label="اسم المدين",
    text_align=ft.TextAlign.RIGHT,   # النص من اليمين
    rtl=True,
    autofocus=True,
)

    debtor_list_view = ft.ListView(height=200)

    def filter_debtors(e):
        keyword = debtor_input.value.strip()
        debtor_list_view.controls.clear()

        if not keyword:
            page.update()
            return

        # 👇 جلب الأسماء من قاعدة البيانات
        results = db.search_debtors_by_name(keyword)

        for name in results:
            debtor_list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(name),
                    on_click=lambda ev, n=name: select_debtor(n)
                )
            )

        page.update()
    


    def open_upload(e):
        selected_amount = None
        uploaded_pdf_path = None
        success_text = ft.Text(
        "",
        size=16,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
        def on_cancel(e):
            sad_dialo.open = False
            page.update()
        # ================= إعداد مجلد الحفظ =================
        UPLOAD_DIR = "uploaded_pdfs"
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # ================= دالة إغلاق النوافذ =================
        def close_dialog(dialog):
            dialog.open=False
            page.update()


        # ================= تنفيذ العملية لفئة 1000 =================
        def process_1000_request(pdf_path):
            if not pdf_path:
                print("❌ لم يتم تمرير مسار ملف")
                return
        

            reader = PdfReader(pdf_path)
            
            if selected_amount == 1000:
                table_name = "User_card1000"
            elif selected_amount == 500:
                table_name = "User_card500"
            elif selected_amount == 300:
                table_name = "User_card300"
            elif selected_amount == 200:
                table_name = "User_card200"
            else:
                return

            for page in reader.pages:
                text = page.extract_text()
                if not text:
                    continue

                # استخراج الأرقام فقط
                numbers = re.findall(r"\d+", text)

                for num in numbers:
                    # تقسيم الأرقام الطويلة
                    if len(num) > 12:
                        chunks = [num[i:i+12] for i in range(0, len(num), 12)]
                        for chunk in chunks:
                            add_card_to_table(table_name, chunk)
                    else:
                        add_card_to_table(table_name, num)

                    
            _, ext = os.path.splitext(pdf_path)

            # إزالة التكرار مع الحفاظ على الترتيب
            '''users = list(dict.fromkeys(users))
            print(users)'''
            file_name = os.path.basename(pdf_path)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S--"+ str(selected_amount))
            new_file_name = f"pdf_{timestamp}{ext}"


            # المسار النهائي
            destination_path = os.path.join(UPLOAD_DIR, new_file_name)

            # نسخ الملف
            shutil.copy(pdf_path, destination_path)

            print("📄 تم حفظ الملف في:", destination_path)
            print("✅ تمت العملية")


            balance_card.content =sales_summary_card(
            get_total("debt_sales"),
            get_total("cash_sales"),
            categories={
                "فئة 1000":count_available_cards("User_card1000"),
                "فئة 500": count_available_cards("User_card500"),
                "فئة 300": count_available_cards("User_card300"),
                "فئة 200":count_available_cards("User_card200"),
            }
        )
            success_text.value = f"تم التعبئة مخزن فئة {selected_amount} بنجاح"
            category_dialo.open = False
            page.update()

            page.dialog = sad_dialo
            sad_dialo.open = True
            page.update()


            

        # ================= FilePicker =================
        def on_file_picked(e: ft.FilePickerResultEvent):
            nonlocal uploaded_pdf_path

            if not e.files:
                page.snack_bar = ft.SnackBar(
                    ft.Text("لم يتم اختيار أي ملف ❌")
                )
                page.snack_bar.open = True
                page.update()
                return

            uploaded_pdf_path = e.files[0].path
            print("📄 مسار الملف:", uploaded_pdf_path)

            # ✅ لا تتحقق من None
            process_1000_request(uploaded_pdf_path)



        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.append(file_picker)
        # ================= اختيار الفئة =================
        def select_amount(value):
            nonlocal selected_amount
            selected_amount = value
            category_dialo.open = False

            
                # فتح اختيار ملف PDF
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["pdf"])
            

        

        # ================= نافذة الفئات =================
        category_dialo = ft.AlertDialog(
            modal=True,
            title=ft.Text("اختر الفئة", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.ElevatedButton("200", on_click=lambda e: select_amount(200)),
                    ft.ElevatedButton("300", on_click=lambda e: select_amount(300)),
                    ft.ElevatedButton("500", on_click=lambda e: select_amount(500)),
                    ft.ElevatedButton("1000", on_click=lambda e: select_amount(1000)),
                ],
            ),
            actions=[
                ft.TextButton("إغلاق", on_click=lambda e: close_dialog(category_dialo))
            ],
        )
        

        sad_dialo = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=20),

        title=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="ok.gif",   # اسم الملف
                    width=120,
                    height=120,
                    repeat=True,
                ),
            ],
        ),
    

        content=ft.Column(
        tight=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            success_text
        ],
    ),


        actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        actions=[

            ft.OutlinedButton(
                "إلغاء",
                on_click=on_cancel,
            ),
        ],

    )
        page.dialog=sad_dialo

    
        page.dialog=category_dialo    
        category_dialo.open = True
        page.update()
    

        

        
    def copy_text(e, text):
        e.page.set_clipboard(text)
        e.page.snack_bar = ft.SnackBar(ft.Text("تم النسخ 📋"))
        e.page.snack_bar.open = True
        e.page.update()
    def create_ad_card(text):
        return ft.Container(
            padding=10,
            margin=5,
            border_radius=12,
            bgcolor=ft.colors.WHITE10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(text, size=14, expand=True),

                    ft.IconButton(
                        icon=ft.icons.COPY,
                        tooltip="نسخ",
                        on_click=lambda e, t=text: copy_text(e, t)
                    )
                ]
            )
        )






    def show_purchased_cards(type_user):

        # جلب عدد الكروت المختار
        count = cards_count
        select_card=[]

        if selected_category.value=="1000":
            if count > db.count_available_cards("User_card1000") :
                
                sad_dialog.open = True
                page.update()
                return
            else:
                select_card, msg =db.buy_cards("User_card1000", count)
                print(msg)
        elif selected_category.value=="500":
            if count > db.count_available_cards("User_card500") :
                #sad_dialog.open = True
                close_all_dialogs()
                sad_dialog.open = True
                page.update()
                return
            else:
                select_card, msg =db.buy_cards("User_card500", count)
                print(msg)
                
        elif selected_category.value=="300":
            if count > db.count_available_cards("User_card300"):
                sad_dialog.open = True
                page.update()
                
                return

            else:
                select_card, msg =db.buy_cards("User_card300", count)
                print(msg)
        elif selected_category.value=="200":
            if count > db.count_available_cards("User_card200"):
                sad_dialog.open = True
                page.update()
                return
            else:
                select_card, msg =db.buy_cards("User_card200", count)
                print(msg)

        # تفريغ العرض السابق
        cards_result_dialog.content.controls.clear()
        

        for card in select_card:
            
            # إضافة الكرت إلى نافذة النتائج
            cards_result_dialog.content.controls.append(
                wifi_card_item(card)
            )
            db.add_card(card)
        ads_panel.content.controls.clear()
        cards = db.get_cards_desc()
        for card in cards:
            ads_panel.content.controls.append(create_ad_card(card[0]))
        ads_panel.update()

        if type_user=="دين":
            db.add_amount(count* int(selected_category.value),"debt_sales")
            db.insert_debtor_sale(
            debtor_name=debtor_input.value,
            card_category=selected_category.value,
            cards_count=cards_count
        )
        
            
        elif type_user=="نقد":
            db.add_amount(count* int(selected_category.value),"cash_sales")
        
       
        balance_card.content =sales_summary_card(
            db.get_total("debt_sales"),
            db.get_total("cash_sales"),
            categories={
                "فئة 1000": db.count_available_cards("User_card1000"),
                "فئة 500": db.count_available_cards("User_card500"),
                "فئة 300": db.count_available_cards("User_card300"),
                "فئة 200": db.count_available_cards("User_card200"),
            }
        )            
  

        # فتح الناف

        cards_result_dialog.open = True

        page.update()


    def select_debtor(name):
        debtor_input.value = name
        debtor_list_view.controls.clear()
        page.update()
    cards_result_dialog = ft.AlertDialog(
    modal=True,
    shape=ft.RoundedRectangleBorder(radius=20),
    title=ft.Text("🎉 تم شراء الكروت", size=18, weight=ft.FontWeight.BOLD),
    content=ft.Column(
        width=320,
        spacing=12,
        controls=[],  # سيتم تعبئتها ديناميكيًا
    ),
    actions=[
        ft.TextButton("إغلاق", on_click=lambda e: close_dialog(cards_result_dialog))
    ],
)
    page.dialog=cards_result_dialog
        
    ads_panel = ft.Container(
        height=220,
        border_radius=18,
        bgcolor="#6A8C95",
        padding=12,
        content=ft.Column(
            controls=[],   # مهم جدًا
            scroll=ft.ScrollMode.AUTO
        )
    )
        
    cards = db.get_cards_desc()
    for card in cards:
        ads_panel.content.controls.append(create_ad_card(card[0]))
    
        

    """def confirm_cash():
        print("نقد")
        print("عدد الكروت:", cards_count)

        cash_dialog.open = False
        show_purchased_cards()"""



    
    def on_dlg_button_click(e):
        if e.control.text == "Yes":

            page.open=False
            page.update()
            page.dialog=debt_dialog
            debt_dialog.open=True
            page.update()
        page.close(dlg_modal)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation"),
        content=ft.Text("Do you want to exit?"),
        actions=[
            ft.TextButton("Ok", on_click=on_dlg_button_click),
            
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog=dlg_modal
    def on_confirm(e):
        
    
        if not debtor_input.value or debtor_input.value.strip() == "":
            print("اسم ")

            page.open(dlg_modal)
            page.update()
 # إيقاف التنفيذ
        else:
            show_purchased_cards("دين")



###########نافذة الدي
    debt_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("بيانات المدين"),
        content=ft.Column(
            width=30,
            spacing=14,
            controls=[
                debtor_input,
                debtor_list_view,
               
            ],
        ),
        actions=[
            ft.TextButton("تأكيد", on_click=lambda e: on_confirm(e)),
            ft.TextButton("إغلاق", on_click=lambda e: close_dialog(debt_dialog)),
        ],
    )
    page.dialog = debt_dialog

    def open_manage(e):
        page.clean()                 # يمسح الصفحة الحالية
        from managecard import manage
        manage(page)

        
          
    def manag__card(e):
        page.clean()                 # يمسح الصفحة الحالية
        from mmm import mmmm
        mmmm(page)               # يفتح صفحة الدفتر

    debtor_input.on_change = filter_debtors

    # ---------------- App Bar ----------------
    app_bar = ft.Container(
        bgcolor=PRIMARY,
        padding=ft.padding.symmetric(vertical=14),
        width=float("inf"),  # عرض كامل

        border_radius=ft.border_radius.only(
            bottom_left=20,
            bottom_right=20,
        ),

        # يبدأ خارج الشاشة للأعلى
        offset=ft.transform.Offset(0, -1),
        animate_offset=700,

        content=ft.Text(
            "✨ تطوير وبرمجة محمد مغرم ✨",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        ),
    )


    # تشغيل الانيميشن بعد العرض
    app_bar.offset = ft.transform.Offset(0, 0)


    # ---------------- Balance Card ----------------
    balance_card = ft.Container(
        bgcolor=PRIMARY,
        
        width=500,        # عرض الكارد
        height=200,
        border_radius=16,
        #padding=,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            sales_summary_card(
            db.get_total("debt_sales"),
            db.get_total("cash_sales"),
                categories={
                    "فئة 1000": db.count_available_cards("User_card1000"),
                    "فئة 500": db.count_available_cards("User_card500"),
                    "فئة 300": db.count_available_cards("User_card300"),
                    "فئة 200": db.count_available_cards("User_card200"),
                }
            )            ]
        )
    )


    balance_card.margin = ft.margin.only(right=-10,left=-10)

    # ---------------- Quick Action ---------------
 

    # ---------------- Services ----------------
    def service(icon, label, color, on_click=None):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=64,
                    height=64,
                    
                    border_radius=16,
                    bgcolor=color,
                    alignment=ft.alignment.center,
                    on_click=on_click,
                    content=ft.Icon(icon, size=32),
                ),
                ft.Text(label, size=13),
            ]
        )
    payment_dialog = ft.AlertDialog(
    modal=True,
    
    title=selected_category,
    content=ft.Column(
        tight=True,
        
        spacing=16,
        controls=[
            ft.Text("عدد الكروت", size=13, weight=ft.FontWeight.BOLD),
            card_buttons_row ,  # 👈 نفس الأزرار تمامًا
            ft.ElevatedButton("💳 دين", on_click=lambda e:finish_payment("دين")),
            ft.ElevatedButton("💵 نقد", on_click=lambda e: show_purchased_cards("نقد")),
           
         
        ],
    ),
    actions=[
        ft.TextButton("إغلاق", on_click=lambda e: close_dialog(payment_dialog))
    ],
)

    page.dialog=payment_dialog
    category_dialog = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=20),
        title=ft.Text(
            "اختر الفئة",
            size=18,
            
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Container(
            width=15,
            height=195,
            content=ft.Column(
                spacing=14,
                controls=[
                    category_btn("200"),
                    category_btn("300"),
                    category_btn("500"),
                    category_btn("1000"),
                ],
            ),
        ),
        actions=[
            ft.TextButton(
                "إغلاق",
                on_click=lambda e: close_dialog(category_dialog),
                
                style=ft.ButtonStyle(
                    color=ft.colors.BLUE,
                ),
            )
        ],
    )
    enter_card = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=20),
        title=ft.Text(
            "اختر الفئة",
            size=18,
            
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Container(
            width=15,
            height=195,
            content=ft.Column(
                spacing=14,
                controls=[
                    category_btn("100"),
                    category_btn("300"),
                    category_btn("500"),
                    category_btn("1000"),
                ],
            ),
        ),
        actions=[
            ft.TextButton(
                "إغلاق",
                on_click=lambda e: close_dialog(category_dialog),
                
                style=ft.ButtonStyle(
                    color=ft.colors.BLUE,
                ),
            )
        ],
    )


    services = ft.GridView(
        max_extent=100,
        child_aspect_ratio=0.9,
        spacing=12,
        run_spacing=20,

        controls=[
            service(ft.icons.WIFI, "كبينه WIFI", "#FFF3E0", on_click=open_wifi_dialog),
            service(ft.icons.CREDIT_CARD, "لوحة التحكم", "#EFEBE9",on_click=manag__card),
            service(ft.icons.CALCULATE, "الدفتر المحاسبي", "#F3E5F5",on_click=open_manage),
            service(ft.icons.ACCOUNT_BALANCE_WALLET, "غذي الكبائن", "#E3F2FD",on_click=open_upload),
        ]
    )

    # ---------------- Bottom Banner ----------------
    def nav_change(e):
        if e.control.selected_index == 0:
            page.go("/")   # الرئيسية
        elif e.control.selected_index == 1:
            open_speed(e)  # صفحة السرعة
        


    def open_speed(e):
        page.clean()
        from speed_test import speed_page
        page.add(speed_page(page))


    # ---------------- Bottom Navigation ----------------
    nav = ft.NavigationBar(
        selected_index=0,
        on_change=nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="الرئيسية"),
            ft.NavigationBarDestination(icon=ft.icons.SPEED, label="سرعة شبكتي"),
        ]
    )


    # ---------------- Layout ----------------
    page.add(
        ft.Column(
            expand=True,
            controls=[
                app_bar,
                ft.ListView(
                    expand=True,
                    padding=16,
                    controls=[
                        balance_card,
                        ft.Container(height=20),
                        
                        ft.Container(height=30),
                        ft.Text("الخدمات الأساسية", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(height=16),
                        services,
                        ft.Container(height=30),
                        ads_panel
                        
                    ]
                ),
                nav,
          ]
        )
    )

if __name__ == "__main__":
   ft.app(target=main, assets_dir="assets/")


