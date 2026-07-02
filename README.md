Repo for the source code for farama.org

## Setup

Install [mise](https://mise.jdx.dev/), then from the repo root:

```
mise install
bundle install
```

This installs Ruby, `just`, and `bundler` (via the `mise postinstall` hook), then the Jekyll gems.

## Serving locally

Serve on the local network (accessible from phone):
```
just serve
```

Find your IP:
```
just find-local-ip
```
Then open `http://<your-ip>:4000` on the other device.

## Built with

* Jekyll
* Bootstrap 5
* Font Awesome
