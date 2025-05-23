{ pkgs }: {
  deps = with pkgs; [
    python39Full
    python39Packages.pip
    nodejs
    cacert

    libnss3
    nspr
    dbus
    libatk
    atk
    atkbridge
    libcups
    libxcb
    libxkbcommon
    at-spi2-core
    libxcomposite
    libxdamage
    libxfixes
    libgbm
    pango
    cairo
    libasound
  ];
}
