
_pkgname=VCalculator
pkgname=vcalculator
pkgver=1.0.2
pkgrel=1
pkgdesc="Simple GTK+ Calculator"
arch=(x86_64)
url="https://github.com/vikdevelop/VCalculator"
license=(GPL)
depends=(qt5-base qt5-svg qt5-x11extras libx11 libxext hicolor-icon-theme kwindowsystem)
makedepends=(cmake qt5-tools)
source=('git+https://github.com/vikdevelop/VCalculator.git')
sha256sums=('SKIP')

build() {
  cd VCalculator
  python -m main.py
}

package() {
  make -C build DESTDIR="${pkgdir}" install
}

