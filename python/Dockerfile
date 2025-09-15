FROM codercom/code-server:latest

USER root
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y xz-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory for nix
RUN mkdir /nix
RUN curl -L https://nixos.org/nix/install | sh -s -- --daemon
RUN chown -R coder:coder /nix


USER coder
# Set the environment variable to use nix
ENV NIX_PROFILES="/nix/var/nix/profiles/default /root/.nix-profile"
ENV NIX_PATH="nixpkgs=/nix/var/nix/profiles/per-user/root/channels/nixpkgs"

SHELL ["/bin/bash", "-c"]
CMD ["/nix/var/nix/profiles/default/bin/nix-daemon"]
RUN exts=(\
      gitpod.gitpod-theme \
      ms-python.python \
      jnoortheen.nix-ide \
    )\
    && for ext in "${exts[@]}"; do code-server --install-extension "${ext}"; done
