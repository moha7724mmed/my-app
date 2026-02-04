import pandas as pd
from PyPDF2 import PdfReader
from datetime import datetime
from db import add_card_to_table,print_all_user_card,count_cards,get_total
import os ,re
import shutil
import flet as ft

"""def open_upload_dialog(page: ft.Page,balance_card,show_open_dialogs):
    
    selected_amount = None
    uploaded_pdf_path = None
    def on_cancel(e):
        sad_dialog.open = False
        page.update()
    # ================= إعداد مجلد الحفظ =================
    UPLOAD_DIR = "uploaded_pdfs"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # ================= دالة إغلاق النوافذ =================
    def close_dialog(dialog):
        dialog.open=False
        page.update()
        show_open_dialo()


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
            print("❌ فئة غير معروفة")
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
            "فئة 1000":count_cards("User_card1000"),
            "فئة 500": count_cards("User_card500"),
            "فئة 300": count_cards("User_card300"),
            "فئة 200":count_cards("User_card200"),
        }
    )
        page.dialog=category_dialo
        category_dialo.open = False
        page.update()
        sad_dialog.open = True
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
        

        '''else:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"تم اختيار فئة {value}")
            )
            page.snack_bar.open = True
            page.update()'''

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
    

    sad_dialog = ft.AlertDialog(
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
            ft.Text(
                "تم التعبئة مخزن فئة 1000 بنجاح",
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

   
    page.dialog=category_dialo    
    category_dialo.open = True
    
    show_open_dialo()
    page.update()
    print('ok')"""
   

    


def sales_summary_card(nodebtor, debtor, categories):

    # القيم الافتراضية للفئات
    def get_zero(value,max_value):
        if max_value <= 0:
            return 0
        return min(value / 66, 1.0)


    # تحديد لون الدائرة حسب النسبة
    def get_progress_color(percent):
        if percent >= 0.75:
            return ft.colors.GREEN
        elif percent >= 0.5:
            return ft.colors.ORANGE
        elif percent >= 0.25:
            return ft.colors.AMBER
        return ft.colors.RED

    # دالة رسم دائرة لكل فئة
    def circle(title, value):
        p = get_zero(value,60)
        percent_text = int(p * 100)
        color = get_progress_color(p)

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Stack(
                    alignment=ft.alignment.center,
                    controls=[
                        ft.ProgressRing(
                            value=p,
                            width=60,
                            height=60,
                            stroke_width=6,
                            color=color,
                        ),
                        ft.Text(f"{percent_text}%", size=12, weight=ft.FontWeight.BOLD),
                    ],
                ),
                ft.Text(title, size=11, color=ft.colors.WHITE),
            ],
        )

    # إنشاء الدوائر
    circles = [circle(name, value) for name, value in categories.items()]

    # الكارد النهائي
    return ft.Container(
        width=350,
        padding=16,
        border_radius=20,
        bgcolor="#5E4B87",
        content=ft.Column(
            spacing=15,
            controls=[
                # الصف العلوي
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("مبيعات نقد", color=ft.colors.WHITE70, size=12),
                                ft.Text(str(debtor)+"ريال", color=ft.colors.WHITE, size=19, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                        ft.Container(
                            height=2,
                            bgcolor=ft.colors.AMBER_400,
                            border_radius=10,
                        ),


                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Text("المبيعات دين", color=ft.colors.WHITE70, size=12),
                                ft.Text(str(nodebtor)+"ريال", color=ft.colors.WHITE, size=19, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                    ],
                ),

                # الدوائر
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=circles,
                ),
            ],
        ),
    )





"""

    def convert(pdf):
        pdf_path = "1000.pdf"

        reader = PdfReader(pdf_path)
        users = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                # استخراج الأرقام فقط
                numbers = re.findall(r"\d+", text)

                for num in numbers:
                    # إذا الرقم أطول من 12 → نقسمه
                    if len(num) > 12:
                        chunks = [num[i:i+12] for i in range(0, len(num), 12)]
                        users.extend(chunks)
                    else:
                        users.append(num)

        # حفظ في Excel
        df = pd.DataFrame(users, columns=["Username"])
        df.to_excel("use.xlsx", index=False)

        print("تم الإصلاح وإنشاء ملف users.xlsx بنجاح")

ft.app(tarrget=)"""
