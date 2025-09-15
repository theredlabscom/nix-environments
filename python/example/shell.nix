{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Define the packages that should be available in the shell environment.
  # These are added to the PATH and other relevant environment variables.
  buildInputs = with pkgs; [
    python313Packages.pip
    htop
    sqlite
  ];

  # Define environment variables specific to this shell.
  # These can be used to configure tools or set up project-specific paths.
  shellHook = ''
    echo "Welcome to the Nix development shell!"
    echo "Using Python version: $(python --version)"

    if [ ! -d .venv ]; then
      python -m venv .venv
      source .venv/bin/activate
      if [ -f requirements.txt ]; then
        pip install -r requirements.txt
      fi
    else
      source .venv/bin/activate
    fi
  '';
}