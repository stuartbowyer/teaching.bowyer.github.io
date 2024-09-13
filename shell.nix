{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python311Packages.ipykernel
    pkgs.python311Packages.jupyter
    pkgs.python311Packages.nbconvert
    pkgs.python311Packages.playwright
    pkgs.python311Packages.pandas
    pkgs.python311Packages.numpy
    pkgs.python311Packages.matplotlib
    pkgs.python311Packages.faker
  ];
  shellHook = ''
    # Switch from bash to zsh shell
    export SHELL=$(which zsh)
    exec ${pkgs.zsh}/bin/zsh
  '';
}
