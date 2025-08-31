{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python312.withPackages (ps: with ps; [
      pandas
      matplotlib
      numpy
      scipy
      seaborn
      jupyter
    ]))
    
    jupyter
    gcc

  ];
}
