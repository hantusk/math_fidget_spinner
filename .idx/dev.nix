# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"
  packages = [ pkgs.python3 pkgs.libGL pkgs.xorg.libX11 pkgs.gcc8 pkgs.bash ];
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [ "ms-python.python" "ms-toolsai.jupyter"];
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onCreate = {
        install =
          "python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
        # Open editors for the following files by default, if they exist:
        default.openFiles = [ "README.md" "math_fidget_spinner.ipynb" ];
      }; # To run something each time the workspace is (re)started, use the `onStart` hook
    };
  };
}

