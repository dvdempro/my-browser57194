from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    # Для перевода dp -> px
    DisplayMetrics = autoclass('android.util.DisplayMetrics')
else:
    from kivy.uix.label import Label


class MyBrowserApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        # ---------- Верхняя панель ----------
        top_layout = BoxLayout(size_hint_y=None, height=dp(50))

        self.url_input = TextInput(
            text='https://google.com',
            multiline=False,
            size_hint_x=0.8
        )
        self.url_input.bind(on_text_validate=self.open_url)

        btn = Button(text='Идти', size_hint_x=0.2)
        btn.bind(on_press=self.open_url)

        top_layout.add_widget(self.url_input)
        top_layout.add_widget(btn)
        root.add_widget(top_layout)

        # ---------- Контейнер под WebView ----------
        self.webview_container = Widget()
        root.add_widget(self.webview_container)

        if platform == 'android':
            # Ждём, пока Kivy отрисует layout, чтобы знать координаты контейнера
            Clock.schedule_once(self.setup_webview, 0.5)
        else:
            root.add_widget(Label(text='[Режим ПК] WebView работает только на Android!'))

        return root

    @run_on_ui_thread
    def setup_webview(self, dt):
        activity = PythonActivity.mActivity

        # Высота верхней панели в пикселях
        density = activity.getResources().getDisplayMetrics().density
        top_bar_px = int(dp(50) * density)

        # Создаём WebView
        self.webview = WebView(activity)
        self.webview.setWebViewClient(WebViewClient())
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)

        # Размещаем под верхней панелью, на всю ширину и высоту
        params = LayoutParams(
            LayoutParams.MATCH_PARENT,  # ширина
            LayoutParams.MATCH_PARENT   # высота
        )
        params.topMargin = top_bar_px

        # addContentView кладёт WebView ПОВЕРХ Activity, но с topMargin
        # верхняя панель Kivy остаётся видимой
        activity.addContentView(self.webview, params)

        self.webview.loadUrl(self.url_input.text)

    def open_url(self, instance):
        if platform != 'android':
            return
        if not hasattr(self, 'webview'):
            return

        url = self.url_input.text.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_input.text = url

        self.webview.loadUrl(url)


if __name__ == '__main__':
    MyBrowserApp().run()
