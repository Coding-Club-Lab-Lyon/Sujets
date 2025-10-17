{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.markdown
    pkgs.python312Packages.reportlab
    pkgs.python312Packages.selenium
    pkgs.python312Packages.pypdf2
    pkgs.python312Packages.weasyprint
    pkgs.firefox
    pkgs.geckodriver
    pkgs.cairo
    pkgs.pango
    pkgs.gdk-pixbuf
    pkgs.glib
    pkgs.gobject-introspection
    pkgs.gtk3
    pkgs.fontconfig
    pkgs.freetype
    pkgs.harfbuzz
    pkgs.libffi
    pkgs.libxml2
    pkgs.libxslt
    pkgs.lcms2
    pkgs.zlib
  ];

  shellHook = ''
    export PYTHONPATH=$PWD/.github/workflows/parser/venv/lib/python3.12/site-packages:$PYTHONPATH
    export MOZ_HEADLESS=1
    export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts
  '';
}
