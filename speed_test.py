
import flet as ft
import speedtest
import threading


def speed_page(page: ft.Page):
    page.assets_dir = "assets"


    # ================== قيم السرعة ==================
    ping_txt = ft.Text("0 ms", size=20, weight="bold")
    down_txt = ft.Text("0 Mbps", size=20, weight="bold", color="green")
    up_txt = ft.Text("0 Mbps", size=20, weight="bold", color="blue")
    status_txt = ft.Text("اضغط زر بدء الاختبار", size=12)

    # ================== بوكس عرض البيانات ==================
    info_box = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#E3F2FD",
        content=ft.Row(
            alignment="spaceAround",
            controls=[
                ft.Column([ft.Text("Ping"), ping_txt]),
                ft.Column([ft.Text("التنزيل"), down_txt]),
                ft.Column([ft.Text("اتحميل"), up_txt]),
            ]
        )
    )

    # ================== نافذة التحميل (Dialog + GIF) ==================
    loading_gif = ft.Image(
        src="doa2.gif",  # يمكنك تغيير الرابط
        width=120
    )

    loading_text = ft.Text(" جاري اختبار السرعة...", size=14)

    cancel_flag = {"stop": False}

    def cancel_test(e):
        cancel_flag["stop"] = True
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            padding=5,
            border_radius=20,
            height=200,
            bgcolor="white",
            content=ft.Column(
                horizontal_alignment="center",
                controls=[
                    loading_gif,
                    loading_text,
                    ft.ProgressBar(width=200),
                    ft.ElevatedButton("❌ إلغاء", bgcolor="red", color="white", on_click=cancel_test)
                ]
            )
        )
    )

    # ================== تشغيل الاختبار ==================
    def run_speed_test():
        cancel_flag["stop"] = False

        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            if cancel_flag["stop"]:
                return

            ping = st.results.ping
            down = st.download() / 1_000_000
            up = st.upload() / 1_000_000

            if cancel_flag["stop"]:
                return

            ping_txt.value = f"{int(ping)}ms"
            down_txt.value = f"{down:.2f}Mbps"
            up_txt.value = f"{up:.2f}Mbps"
            status_txt.value = "✅ تم الانتهاء من الاختبار"

        except Exception as e:
            status_txt.value = f"❌ خطأ: {e}"

        # إغلاق النافذة عند الانتهاء
        dlg.open = False
        page.update()

    # تشغيل في Thread حتى لا يتجمد التطبيق
    def start_test(e):
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

        threading.Thread(target=run_speed_test).start()

    # ================== زر الاختبار ==================
    start_btn = ft.ElevatedButton(
        "🚀 بدء اختبار السرعة",
        icon=ft.icons.SPEED,
        bgcolor="green",
        color="white",
        on_click=start_test
    )

    # ================== الرجوع ==================
    def go_home(e):
        page.clean()
        page.appbar = None
        from main import main
        main(page)

    page.appbar = ft.AppBar(
        title=ft.Text("📡 اختبار سرعة الشبكة"),
        bgcolor="#3F51B5",
        center_title=True,
        leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=go_home)
    )

    # ================== الصفحة ==================
    return ft.Column(
        expand=True,
        alignment="center",
        horizontal_alignment="center",
        controls=[
            info_box,
            ft.Container(height=20),
            start_btn,
            ft.Container(height=10),
            status_txt
        ]
    )
