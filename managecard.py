import flet as ft
import db
import os
from datetime import datetime

# ================= صفحة المدينين =================
def manage(page: ft.Page):
    def go_home(e):
        page.clean() 
        page.appbar = None
         # مهم جدًا
        from main import main
        main(page)             # يرجع للرئيسية
   
        
    def open_delete_dialog(page, name):

        def delete_now(e):
            db.delete_debtor(name)
            dlg.open = False
            page.update()
            DebtorsPage()  # تحديث القائمة

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ تأكيد الحذف"),
            content=ft.Text(f"هل تريد حذف المدين: {name} ؟"),
            actions=[
                ft.TextButton("إلغاء", on_click=lambda e: close_dialog()),
                ft.ElevatedButton("حذف", bgcolor="red", color="white", on_click=delete_now),
            ],
        )

        def close_dialog():
            dlg.open = False
            page.update()

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # ================= إنشاء فاتورة HTML =================
    def create_invoice_html(debtor_name, data):
        folder = "invoices_html"
        os.makedirs(folder, exist_ok=True)

        file_name = os.path.join(folder, f"{debtor_name}_invoice.html")

        html = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>فاتورة {debtor_name}</title>
            <style>
            .footer{{
                text-align: center;
                margin-top: 40px;
                font-size: 15px;
                color: #777;
                border-top: 1px dashed #ccc;
                padding-top: 10px;
            }}

                body {{
                    font-family: Arial;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .invoice {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px #ccc;
                    max-width: 900px;
                    margin: auto;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background: #2196F3;
                    color: white;
                }}
                .total {{
                    font-size: 22px;
                    color: red;
                    font-weight: bold;
                    margin-top: 20px;
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <div class="invoice">
                <div style="text-align:center;">
                <img src="image.png" width="150" style="border-radius:50%">
                </div>
                <h1>فاتورة دين</h1>
                <hr style="width: 90%; height: 3px; background-color: black; border: none;">
                <p><b>اسم المدين:</b> {debtor_name}</p>
                <p><b>صدرت بتاريخ:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

                <table>
                    <tr>
                        
                        <th>الفئة</th>
                        <th>عدد الكروت</th>
                        <th>الإجمالي</th>
                        <th>التاريخ</th>
                    </tr>
        """

        total_sum = 0

        for id_, category, cards, total, date in data:
            html += f"""
            <tr>
                
                <td>{category}</td>
                <td>{cards}</td>
                <td style="color:red;">{total}</td>
                <td>{date}</td>
            </tr>
            """

            try:
                total_sum += int(category) * int(cards)
            except:
                pass

        html += f"""
                </table>
                <div class="total">إجمالي الدين: {total_sum} ريال</div>
                <img src="sing2.png" width="150">
            </div>
            <div class="footer">
                💻 برمجة وتصميم م/ محمد مغرم
            </div>

        </body>
        </html>
        """

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html)

        return file_name

    # ================= قائمة المدينين =================
    def DebtorsPage():
        page.appbar = ft.AppBar(
            title=ft.Text("📊 قائمة المدينين"),
            bgcolor="#3F51B5",
            center_title=True,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e:go_home(e))
        )   

        debtors = db.get_debtors_summary()
        cards = []

        for name, total in debtors:

            def open_details(e, debtor_name=name):
                page.session.set("debtor_name", debtor_name)
                DebtorDetailsPage()

            cards.append(
                ft.Container(
                    padding=15,
                    margin=8,
                    bgcolor=ft.colors.WHITE,
                    border_radius=18,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.BLACK12),
                    on_click=open_details,
                    content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # زر تفاصيل
                        ft.Icon(ft.icons.ARROW_BACK),
                        ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                        # المبلغ
                        ft.Text(f"{int(total):,} ريال", color=ft.colors.RED, size=18),

                        # الاسم + زر حذف
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color="red",
                                tooltip="حذف المدين",
                                on_click=lambda e, n=name: open_delete_dialog(page,n)
                            )
                        ]),
                    ]

                    )
                )
            )

        page.controls.clear()
        page.add(ft.Column(cards, scroll=ft.ScrollMode.AUTO, expand=True))

    # ================= تفاصيل المدين =================
    def DebtorDetailsPage():
        name = page.session.get("debtor_name")
        data = db.get_debtor_details(name)

        # حساب مجموع الدين الصحيح
        total_sum = 0
        for id_, category, cards, total, date in data:
            try:
                total_sum += int(category) * int(cards)
            except:
                pass
 

        # زر تصدير HTML
        def export_html(e):
            path = create_invoice_html(name, data)
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ تم إنشاء الملف: {path}"))
            page.snack_bar.open = True
            page.update()

        html_btn = ft.ElevatedButton(
            "🌐 تصدير فاتورة HTML",
            icon=ft.icons.LANGUAGE,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            on_click=export_html
        )

        # AppBar
        page.appbar = ft.AppBar(
            title=ft.Text(f"تفاصيل المدين: {name}"),
            bgcolor="#0D47A1",
            center_title=True,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: DebtorsPage())
        )

        # جدول البيانات
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(category))),
                    ft.DataCell(ft.Text(str(cards))),
                    ft.DataCell(ft.Text(f"{total} ريال", color=ft.colors.RED)),
                    ft.DataCell(ft.Text(date, size=11)),
                ]
            )
            for id_, category, cards, total, date in data
        ]

        table = ft.DataTable(
            heading_row_color="#E3F2FD",
            
            border=ft.border.all(1, ft.colors.BLACK12),
            columns=[
                
                ft.DataColumn(ft.Text("الفئة")),
                ft.DataColumn(ft.Text("الكروت")),
                ft.DataColumn(ft.Text("الإجمالي")),
                ft.DataColumn(ft.Text("بتاريخ")),
            ],
            rows=rows
        )

        # كرت علوي
        header_card = ft.Container(
            padding=15,
            border_radius=20,
            bgcolor="#E3F2FD",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(name, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"💰 {int(total_sum):,} ريال",
                    color=ft.colors.RED, size=20),
                     ]

            )
        )

        # تصميم الصفحة
        page.controls.clear()
        page.add(
            ft.Column(
                controls=[
                    header_card,
                    ft.Container(height=10),
                    html_btn,
                    ft.Container(height=10),
                    ft.Container(
                        padding=10,
                        border_radius=15,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(blur_radius=6, color=ft.colors.BLACK12),
                        content=ft.Column(
                                    [
                                        ft.Row(
                                            [table],
                                            scroll=ft.ScrollMode.AUTO
                                        )
                                    ],
                                    scroll=ft.ScrollMode.AUTO
                                ),

                        expand=True
                    )
                ],
                expand=True
            )
        )

    # تشغيل أول صفحة
    DebtorsPage()
