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
    pkgs.python311Packages.scipy
    pkgs.python311Packages.scikit-learn
    pkgs.python311Packages.imbalanced-learn
    pkgs.python311Packages.faker
    pkgs.python311Packages.db-dtypes
    pkgs.python311Packages.pydata-google-auth
    pkgs.python311Packages.google-cloud-bigquery
    
    (pkgs.python3Packages.buildPythonPackage rec {
      pname = "pandas-gbq";
      version = "0.23.2";

      src = pkgs.fetchFromGitHub {
        owner = "googleapis";
        repo = "python-bigquery-pandas";
        rev = "v${version}";
        sha256 = "mAr2YA6UPvwqFrm4SaQQ0xr6d3nsjfBWiiHK2FO+oxc=";
      };

      doCheck = false; # check requires infrastructure
    })

    pkgs.jq

  ];
  shellHook = ''
    # Switch from bash to zsh shell
    export SHELL=$(which zsh)
    exec ${pkgs.zsh}/bin/zsh
  '';
}
