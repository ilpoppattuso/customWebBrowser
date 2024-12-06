from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSvg import QSvgWidget
import os
import sys
import json

class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon
        self.setWindowIcon(QIcon("icons/browser.svg"))
        
        # Create the browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)
        
        # Navigation bar
        navbar = QToolBar()
        navbar.setIconSize(QSize(24, 24))
        navbar.setMovable(False)
        self.addToolBar(navbar)
        
        # Style the toolbar
        navbar.setStyleSheet("""
            QToolBar {
                background: #f0f0f0;
                spacing: 5px;
                border: none;
                padding: 5px;
            }
            QToolButton {
                border: none;
                padding: 6px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background: #e0e0e0;
            }
        """)
        
        # Back button
        back_btn = QAction(QIcon.fromTheme("go-previous", QIcon("icons/arrow-left.svg")), "Back", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)
        
        # Forward button
        forward_btn = QAction(QIcon.fromTheme("go-next", QIcon("icons/arrow-right.svg")), "Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)
        
        # Reload button
        reload_btn = QAction(QIcon.fromTheme("view-refresh", QIcon("icons/refresh.svg")), "Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)
        
        # Home button
        home_btn = QAction(QIcon.fromTheme("go-home", QIcon("icons/home.svg")), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                padding: 5px 10px;
                background: white;
                selection-background-color: #3874ff;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3874ff;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        # Bookmarks button
        bookmark_btn = QAction(QIcon.fromTheme("bookmark-new", QIcon("icons/bookmark.svg")), "Bookmark", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_btn)

        self.bookmark_toolbar = QToolBar()
        self.bookmark_toolbar.setIconSize(QSize(16, 16))
        self.bookmark_toolbar.setMovable(False)
        self.addToolBar(self.bookmark_toolbar)
        
        # Style bookmark toolbar
        self.bookmark_toolbar.setStyleSheet("""
            QToolBar {
                background: #f8f9fa;
                border-top: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
                spacing: 5px;
                padding: 2px 5px;
            }
            QToolButton {
                color: #444;
                background: transparent;
                border: none;
                border-radius: 2px;
                padding: 4px 8px;
                text-align: left;
            }
            QToolButton:hover {
                background: #e8e8e8;
            }
        """)

        # Load bookmarks
        self.load_bookmarks()
        
        # Initialize bookmarks menu
        self.bookmarks_menu = QMenu(self)
        self.bookmarks_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #3874ff;
                color: white;
            }
        """)
        
        # Connect signals
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.update_title)
        
        # Apply window styling
        self.setStyleSheet("""
            QMainWindow {
                background: white;
            }
        """)
        
        self.show()
        
    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))
        
    def update_url(self, q):
        self.url_bar.setText(q.toString())
        
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Custom Browser")

    def add_bookmark(self):
        url = self.browser.url().toString()
        title = self.browser.page().title()
        
        # Create QToolButton instead of QAction for better context menu support
        button = QToolButton(self.bookmark_toolbar)
        button.setText(title)
        button.setIcon(QIcon("icons/bookmark.svg"))
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.clicked.connect(lambda: self.browser.setUrl(QUrl(url)))
        
        # Store URL as property
        button.setProperty("url", url)
        
        # Setup context menu
        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda pos: self.bookmark_context_menu(pos, button))
        
        self.bookmark_toolbar.addWidget(button)
        self.save_bookmarks()

    def bookmark_context_menu(self, pos, button):
        menu = QMenu()
        remove_action = menu.addAction("Remove Bookmark")
        remove_action.triggered.connect(lambda: self.remove_bookmark(button))
        menu.exec_(button.mapToGlobal(pos))

    def remove_bookmark(self, button):
        self.bookmark_toolbar.removeWidget(button)
        button.deleteLater()
        self.save_bookmarks()

    def save_bookmarks(self):
        bookmarks = []
        for i in range(self.bookmark_toolbar.layout().count()):
            widget = self.bookmark_toolbar.layout().itemAt(i).widget()
            if isinstance(widget, QToolButton):
                bookmarks.append({
                    'title': widget.text(),
                    'url': widget.property("url")
                })
        
        with open('bookmarks.json', 'w') as f:
            json.dump(bookmarks, f)

    def load_bookmarks(self):
        try:
            with open('bookmarks.json', 'r') as f:
                bookmarks = json.load(f)
                
            for bookmark in bookmarks:
                button = QToolButton(self.bookmark_toolbar)
                button.setText(bookmark['title'])
                button.setIcon(QIcon("icons/bookmark.svg"))
                button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                button.setProperty("url", bookmark['url'])
                button.clicked.connect(
                    lambda _, url=bookmark['url']: self.browser.setUrl(QUrl(url)))
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(
                    lambda pos, b=button: self.bookmark_context_menu(pos, b))
                self.bookmark_toolbar.addWidget(button)
                
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont('Segoe UI', 10))
    
    # Create and show browser
    window = CustomBrowser()
    
    # Start the event loop
    sys.exit(app.exec_())