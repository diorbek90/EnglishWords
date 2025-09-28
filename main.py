import flet as ft
from db.db_words import *
from add_elem import *
import pyttsx3
import threading
from random import choice

MAX_ITEMS_IN_COLUMN = 9
random_word = ft.Text()
current_translated = ""
guess_field = None
result_icon = ft.Icon()

def main(page: ft.Page):
    global current_translated, guess_field, result_icon
    page.title = "English words"
    page.theme_mode = ft.ThemeMode.DARK

    create_table_themes()
    create_table_words()

    field_theme = ft.TextField(label="Enter Theme:")
    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column([
                field_theme,
                ft.ElevatedButton(text="Add Theme", on_click=lambda e: add_new_theme(field_theme.value)),
            ]),
            padding=20,
        )
    )

    def make_bottom_sheet_word():
        fw = ft.TextField(label="Enter the word")
        ft_trans = ft.TextField(label="Enter the translated")
        add_btn = ft.ElevatedButton(text="Add word", on_click=lambda e: add_new_word(fw.value, ft_trans.value))
        fw.on_submit = lambda e: ft_trans.focus()
        ft_trans.on_submit = lambda e: add_new_word(fw.value, ft_trans.value)
        return ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([fw, ft_trans, add_btn]),
                padding=20,
            )
        ), fw, ft_trans

    bottom_sheet_word, field_word, field_translated = make_bottom_sheet_word()
    page.overlay.append(bottom_sheet)
    page.overlay.append(bottom_sheet_word)

    def open_sheet(e=None):
        bottom_sheet.open = True
        field_theme.focus()
        page.update()

    def close_sheet(e=None):
        bottom_sheet.open = False
        page.update()

    def open_sheet_word(e=None):
        nonlocal bottom_sheet_word, field_word, field_translated
        try:
            page.overlay.remove(bottom_sheet_word)
        except Exception:
            pass
        bottom_sheet_word, field_word, field_translated = make_bottom_sheet_word()
        page.overlay.append(bottom_sheet_word)
        bottom_sheet_word.open = True
        field_word.focus()
        page.update()

    def close_sheet_word(e=None):
        bottom_sheet_word.open = False
        page.update()

    rows = ft.Row(scroll=ft.ScrollMode.ALWAYS)

    def update_page():
        themes = get_theme()
        rows.controls.clear()
        for theme in themes:
            theme_id, theme_name = theme
            word_count = len(get_words_by_theme(theme_id))
            rows.controls.append(
                ft.ElevatedButton(
                    text=f"{theme_name} ({word_count})",
                    style=button_for_theme,
                    on_click=lambda e, id=theme_id: page.go(f"/{id}"),
                )
            )
        page.update()

    def add_new_theme(theme_name):
        if not theme_name.strip():
            return
        insert_theme(theme_name)
        update_page()
        close_sheet()
        field_theme.value = ""

    words_row = ft.Row(scroll=ft.ScrollMode.AUTO)

    def update_word_page(theme_id):
        words = get_words_by_theme(theme_id)
        words_row.controls.clear()
        for i in range(0, len(words), MAX_ITEMS_IN_COLUMN):
            chunk = words[i:i + MAX_ITEMS_IN_COLUMN]
            col = ft.Column()
            for word_id, word, translated in chunk:
                col.controls.append(
                    ft.Row([
                        ft.Text(f"{word} - {translated}"),
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.HEARING, on_click=lambda e, w=word: hear_word(w)),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, wid=word_id, tid=theme_id: delete_word(wid, tid)),
                        ])
                    ], spacing=10)
                )
            words_row.controls.append(col)
        page.update()

    def hear_word(word):
        def run():
            engine = pyttsx3.init()
            engine.setProperty("rate", 125)
            engine.setProperty("volume", 1.0)
            voices = engine.getProperty("voices")
            if len(voices) > 1:
                engine.setProperty("voice", voices[1].id)
            engine.say(word)
            engine.runAndWait()
            engine.stop()
            del engine
        threading.Thread(target=run, daemon=True).start()

    def add_new_word(word, translated):
        if not word.strip() or not translated.strip():
            return
        route_path = page.route
        if route_path.startswith("/"):
            theme_id = int(route_path.strip("/"))
            insert_word_with_theme_id(word, translated, theme_id)
            field_word.value = ""
            field_translated.value = ""
            update_word_page(theme_id)
            close_sheet_word()
            page.update()

    def delete_word(word_id, theme_id):
        delete_word_by_id(word_id)
        update_word_page(theme_id)

    def delete_theme(theme_id):
        delete_theme_by_id(theme_id)
        update_page()
        page.go("/")

    def random_words():
        global current_translated
        r_th = choice(get_only_exist_id())
        r_w_id = choice(get_only_exist_words_id(r_th))
        word, translated = get_word_by_id(r_w_id)
        random_word.value = word
        current_translated = translated
        result_icon.icon = None
        page.update()

    def check_word(word_translated):
        global current_translated
        if word_translated.strip().lower() == current_translated.strip().lower():
            result_icon.icon = ft.Icons.CHECK
            random_words()
        else:
            result_icon.icon = ft.Icons.CLOSE
        guess_field.value = ""
        guess_field.focus()
        page.update()

    def route_change(route):
        global guess_field, result_icon
        page.views.clear()
        route_path = page.route

        if route_path == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.ADD, icon_size=30, on_click=open_sheet),
                            ft.ElevatedButton(text="Играть", color=ft.Colors.GREEN_300, bgcolor=ft.Colors.BLUE_50, on_click=lambda e: page.go('game')),
                        ]),
                        rows,
                    ],
                )
            )
            update_page()

        elif route_path.startswith("/"):
            try:
                theme_id = int(route_path.strip("/"))
                theme_name = get_theme_by_id(theme_id)[0]
                update_word_page(theme_id)
                page.views.append(
                    ft.View(
                        route=f"/{theme_id}",
                        controls=[
                            ft.Container(
                                content=ft.Row([
                                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/")),
                                    ft.IconButton(icon=ft.Icons.ADD, icon_size=30, on_click=open_sheet_word),
                                    ft.IconButton(icon=ft.Icons.DELETE_FOREVER, icon_size=30, on_click=lambda e, id=theme_id: delete_theme(id))
                                ]),
                                alignment=ft.alignment.center,
                            ),
                            words_row,
                        ],
                    )
                )
            except ValueError:
                print("Invalid route!")

        elif route_path == "game":
            random_words()
            guess_field = ft.TextField(width=250)
            result_icon = ft.Icon()
            guess_field.on_submit = lambda e: check_word(guess_field.value)
            input_row = ft.Row(controls=[guess_field, result_icon], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            page.views.append(
                ft.View(
                    route="game",
                    controls=[
                        ft.ElevatedButton("Назад", on_click=lambda _: page.go("/")),
                        ft.Container(
                            content=ft.Column([random_word, input_row],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                )
            )
            page.update()
            guess_field.focus()
            page.update()

    def on_key(e: ft.KeyboardEvent):
        route_path = page.route
        if e.key == "Enter" and route_path.startswith("/") and route_path != "/" and not bottom_sheet_word.open:
            open_sheet_word()

    page.on_keyboard_event = on_key
    page.on_route_change = route_change
    page.go(page.route)

ft.app(main)
