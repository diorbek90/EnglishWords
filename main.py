import flet as ft
from db.db_words import *
from add_elem import *

def main(page: ft.Page):
    page.title = 'English words'
    page.theme_mode = ft.ThemeMode.DARK
    create_table_themes()


    def open_sheet(e=None):
        bottom_sheet.open = True
        page.update()

    def close_sheet(e=None):
        bottom_sheet.open = False
        page.update()

    def update_page():
        themes = get_theme()
        rows.controls.clear()
        for theme in themes:
            theme_name = theme[1]
            rows.controls.append(
                ft.ElevatedButton(
                    text=theme_name,
                    style=button_for_theme,
                    on_click=lambda e, name=theme_name: click_theme(name)
                )
            )
        page.update()

    def add_new_theme(theme_name):
        create_table_themes()
        insert_theme(theme_name)
        update_page()
        close_sheet()

    def click_theme(theme_name):
        id = get_theme_id(theme_name)
        page.go(f'/{id[0]}')

    rows = ft.Row()

    field_theme = ft.TextField(label="Enter Theme:")
    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column([
                field_theme,
                ft.ElevatedButton(text="Add Theme", on_click=lambda e: add_new_theme(field_theme.value))
            ]),
            padding=20
        )
    )

    page.bottom_sheet = bottom_sheet
    page.overlay.append(bottom_sheet)


    # Диалоговое окно для слов


    def open_sheet_word(e=None):
        bottom_sheet_word.open = True
        page.update()

    def close_sheet_word(e=None):
        bottom_sheet_word.open = False
        page.update()

    def update_word_page(id):
        print(get_words_by_theme(id))

    def add_new_word(word, translated):
        
        route_path = page.route

        if route_path.startswith("/"):
            
            theme_id = int(route_path.strip('/'))
            create_table_words()
            insert_word_with_theme_id(word, translated, theme_id)
            update_word_page(theme_id)
            close_sheet_word()

            

    row_for_word = ft.Row()

    field_word = ft.TextField(label="Enter the word")
    field_translated = ft.TextField(label="Enter the translated")

    bottom_sheet_word = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column([
                field_word,
                field_translated,
                ft.ElevatedButton(text="Add word", on_click=lambda e: add_new_word(field_word.value, field_translated.value))
            ]),
            padding=20
        )
    )

    page.bottom_sheet_word = bottom_sheet_word
    page.overlay.append(bottom_sheet_word)

    def route_change(route):
        page.views.clear()
        route_path = page.route

        if route_path == '/':
            page.views.append(
                ft.View(
                    route='/',
                    controls=[
                        ft.IconButton(icon=ft.Icons.ADD, icon_size=30, on_click=open_sheet),
                        rows
                    ]
                )
            )
            update_page()

        elif route_path.startswith('/'):
            try:
                theme_id = int(route_path.strip('/'))
                theme_name = get_theme_by_id(theme_id)[0]
                page.views.append(
                    ft.View(
                        route=f"/{theme_id}",
                        controls=[
                            ft.IconButton(icon=ft.Icons.ADD, icon_size=30, on_click=open_sheet_word),
                            ft.ElevatedButton(text=str(theme_name), on_click=lambda e: page.go('/'))
                        ]
                    )
                )
            except ValueError:
                print("Invalid route!")

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main)
