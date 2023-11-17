pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'vmt_manager_gtk'
gnome = import('gnome')

gnome.compile_resources('vmt_manager_gtk',
  'vmt_manager_gtk.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'vmt_manager_gtk.in',
  output: 'vmt_manager_gtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

vmt_manager_gtk_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'osc_manager.py',
]

install_data(vmt_manager_gtk_sources, install_dir: moduledir)
