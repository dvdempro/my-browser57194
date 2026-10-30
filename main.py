from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import platform

# Если запускаем на Андроиде, подтягиваем нативный системный WebView
if platform == 'android':
    from jnius import autoclass
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    from kivy.uix.label import Label

class MyBrowserApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        
        # Верхняя панель: строка ввода + кнопка
        top_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        self.url_input = TextInput(
            text='https://google.com',
            multiline=False
        )
        self.url_input.bind(on_text_validate=self.open_url)
        
        btn = Button(text='Идти', size_hint_x=None, width='80dp')
        btn.bind(on_press=self.open_url)
        
        top_layout.add_widget(self.url_input)
        top_layout.add_widget(btn)
        root.add_widget(top_layout)
        
        # Область браузера
        if platform == 'android':
            activity = PythonActivity.mActivity
            self.webview = WebView(activity)
            self.webview.setWebViewClient(WebViewClient())
            # Включаем JS, чтобы сайты вообще грузились
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.loadUrl(self.url_input.text)
            
            # В Kivy на Android нативный WebView добавляется через activity
            activity.addContentView(self.webview, self._get_layout_params())
        else:
            # Заглушка для ПК, чтобы код не падал при тестировании на компьютере
            root.add_widget(Label(text='[Режим ПК] WebView работает только на Android!'))
            
        return root

    def open_url(self, instance):
        url = self.url_input.text
        if not url.startswith('http'):
            url = 'https://' + url
        
        if platform == 'android':
            self.webview.loadUrl(url)

    def _get_layout_params(self, *args):
        from jnius import autoclass
        ViewGroup = autoclass('android.view.ViewGroup$LayoutParams')
        # Размещаем WebView под верхней панелью ввода
        params = ViewGroup(ViewGroup.MATCH_PARENT, ViewGroup.MATCH_PARENT)
        return params

if __name__ == '__main__':
    MyBrowserApp().run()
