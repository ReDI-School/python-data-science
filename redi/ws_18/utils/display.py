from IPython.core.display import HTML

def display_side_by_side(display):
    def wrapped(*objects):
        css = HTML("""
        <style>
        .display_data {
            float: left;
            padding: 10px;
        }
        </style>
        """)
        display(css, *objects)
    return wrapped
