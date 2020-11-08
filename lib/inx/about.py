from .utils import build_environment, write_inx_file


def generate_about_inx_file():
    env = build_environment()
    template = env.get_template('about.xml')
    write_inx_file("about", template.render())
