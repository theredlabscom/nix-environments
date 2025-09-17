{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Define the packages that should be available in the shell environment.
  # These are added to the PATH and other relevant environment variables.
  buildInputs = with pkgs; [
    dotnetCorePackages.sdk_9_0-bin
    gemini-cli
  ];

  # Define environment variables specific to this shell.
  # These can be used to configure tools or set up project-specific paths.
  shellHook = ''
    ENV_FILE=".env"

    # Check if the .env file exists
    if [ -f "$ENV_FILE" ]; then
      # Source the .env file to export variables
      source "$ENV_FILE"
      echo "Variables from $ENV_FILE have been exported."
    else
      echo "Error: .env file not found at $ENV_FILE"
    fi

    echo "Welcome to the Nix development shell!"
    echo "Using dotnet version: $(dotnet --version)"
  '';
}